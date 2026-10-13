#!/bin/sh
# Mix a voice track over a score: duck the music under the voice, then
# normalise the whole mix to -16 LUFS / -1.5 dBTP with two-pass loudnorm.
#
# usage: mix.sh <voice.wav> <music.wav> <out.wav> <total-seconds> [impulse.wav]
#
# MUSIC_GAIN (default 0.55) sets the music level before ducking. An optional
# impulse response adds a trace of the score's hall to the voice. Needs ffmpeg.
set -eu
[ $# -ge 4 ] || { echo "usage: mix.sh <voice.wav> <music.wav> <out.wav> <total-seconds> [impulse.wav]" >&2; exit 2; }
VOICE=$1 MUSIC=$2 OUT=$3 TOTAL=$4 IR=${5:-}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
FADE=$(awk "BEGIN { print $TOTAL - 1.2 }")

VOICE_CHAIN="highpass=f=85,equalizer=f=3200:t=q:w=1.2:g=2.5,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=2"
if [ -n "$IR" ]; then
  INPUTS="-i $VOICE -i $MUSIC -i $IR"
  VOICE_GRAPH="[0:a]$VOICE_CHAIN,asplit=3[v1][v2][vk];[v2][2:a]afir=dry=0:wet=1,volume=0.07[vr];[v1][vr]amix=inputs=2:normalize=0[voice]"
else
  INPUTS="-i $VOICE -i $MUSIC"
  VOICE_GRAPH="[0:a]$VOICE_CHAIN,asplit=2[voice][vk]"
fi

# shellcheck disable=SC2086
ffmpeg -v error -y $INPUTS -filter_complex "
$VOICE_GRAPH;
[1:a]apad,atrim=0:$TOTAL,volume=${MUSIC_GAIN:-0.55}[m];
[m][vk]sidechaincompress=threshold=0.02:ratio=8:attack=35:release=500[duck];
[voice][duck]amix=inputs=2:normalize=0,afade=t=out:st=$FADE:d=1.2,aformat=channel_layouts=stereo[out]" \
  -map "[out]" -c:a pcm_f32le "$TMP/premix.wav"

MEASURE=$(ffmpeg -i "$TMP/premix.wav" -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')
get() { echo "$MEASURE" | python3 -c "import json, sys; print(json.load(sys.stdin)[sys.argv[1]])" "$1"; }
ffmpeg -v error -y -i "$TMP/premix.wav" \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true" \
  -ar 48000 -c:a pcm_s16le "$OUT"
echo "wrote $OUT"
