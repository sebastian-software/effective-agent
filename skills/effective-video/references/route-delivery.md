# Delivery

Use for rendering masters, captions, and posters, for publishing a film to
streaming or video platforms, and for archiving originals.

## Keep Video Out of Git

Commit the sources: compositions, scripts, cue sheets, the line list, and the
score generator. Do not commit renders, audio, takes, weights, or soundfonts.
Keep them in an ignored work directory.

A binary pushed to a pull-request branch and removed by a force-push never
reaches the default branch or clones. It can stay reachable by SHA through the
PR's force-push history. Rewrite such a branch before merging; ask the hosting
provider's support to purge it only if the file is sensitive.

## Masters and Companions

- Mux the deterministic picture render with the final mix: H.264 at CRF about
  18, AAC at 192 kbps, `+faststart`. Keep the master's resolution and frame
  rate.
- Captions: SRT for YouTube and similar platforms, WebVTT for web players.
  Generate them from the cue sheet after the final take selection.
- Poster: pick a frame that tells the story on its own and leaves calm space
  where a play button or label will sit. Export a full-size PNG for platforms
  and a WebP of about 1280 px for the site.
- Build a fresh archive from the final render instead of patching an earlier
  one. It holds the master, the mix and its stems, captions, the poster, the
  chosen takes and their reference, the cue sheet and lines, a README with
  credits and platform metadata, and SHA-256 checksums.

## Publish

Uploading needs the requester's accounts and their explicit go-ahead for each
destination. The skill does not authorize it. A computer-use agent can do the
uploads from a written task. The task names the local files, the exact
settings, the checks, and what to report back (IDs and URLs).

- **Site playback:** use a streaming host that does not track viewers. Bunny
  Stream met this when checked in October 2026 (EU-hosted, adaptive, no ads, no
  player cookies); re-check its cookies and storage before relying on that.
  Restrict allowed domains to the site and `localhost`, and turn off
  heatmaps and resume-position storage.
- **Click to load:** show a self-hosted poster and request the player iframe
  only when the visitor clicks. Remove the iframe on close so playback stops.
  Without JavaScript, link to the player page. The player UI and embed code
  belong to `effective-web`.
- **Reach:** upload the same master to YouTube or similar as a separate
  channel for discovery and sharing, not as the site embed. A third-party
  embed requests the third party's servers on page load and needs consent
  handling.
- **Archive:** store the originals in private storage with no public pull
  zone. Verify size and checksum after upload.
- **Metadata:** reuse one title, description, tag set, and credit block across
  platforms. Attribution licences such as CC BY for a soundfont travel with
  every publication.

## Privacy Text

Do not restate privacy facts on the page ("no tracking, no cookies"). They
drift from the policy as the site changes. When a film adds a service such as
a streaming host, record its facts for the owner of the privacy policy:

- the provider and its location;
- what loads, and when it loads;
- cookies and local storage, as observed;
- data transfers.

Updating the policy itself is the policy owner's decision.
