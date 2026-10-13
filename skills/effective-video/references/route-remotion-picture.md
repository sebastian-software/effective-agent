# Remotion Picture

Use for building or fixing the picture of a film in Remotion: scenes, camera,
transitions, brand look, and copied snapcn components.

## Structure

- One composition per film, at the master format and 30 fps. Scenes are
  `Sequence`s whose `from` and `durationInFrames` come from the bar grid of
  the [Film Plan](route-film-plan.md).
- Render picture only, muted. Voice and score are mixed outside Remotion and
  muxed with ffmpeg, so a render stays deterministic and audio changes do not
  require a re-render.
- Pass timing that depends on the voice as props, such as the frame where a
  line's key word lands, from the cue sheet, so swapping a take does not mean
  editing scene code.
- Load the brand's fonts as files with `@font-face` and delay rendering until
  `document.fonts.ready`. A render machine's fallback font silently changes
  the look.

## Motion That Reads as Intentional

- A camera over a large world canvas, with eased moves between keyed
  positions and zoom interpolated in log space, gives continuous action
  without slide-show cuts. Add a little blur only while the camera moves fast.
- Use springs for things that arrive, and eased ramps for things that travel.
  Stagger elements by a few frames, and land important arrivals on beats.
- Shake, jitter, and glitch effects tire quickly. Keep them short and small,
  for a beat or two before a cut, and never under speech that needs reading.
- Every on-screen word must be readable at the shot's scale for at least
  half a second. Text overlays must not cover what the voice is describing.

## Own Components vs snapcn

[snapcn](https://snapcn.dev) is a shadcn-style registry of Remotion
components. `npx shadcn@latest add @snapcn/<name>` copies the source into the
repository.

- **Setup:** It needs a `components.json` and the `@/` import alias in both
  `tsconfig.json` and the Remotion bundler config, because Remotion does not
  read tsconfig paths. Pin every dependency the CLI adds to an exact version
  matching the project's Remotion version.
- **Theming:** Wrap the composition in the snapcn theme provider with concrete
  brand values (hex colours, font family). CSS variables do not exist in a
  render.
- **What it's good at:** generic, well-crafted beats such as prompt typing,
  kinetic headlines, logo stings, captions, and device frames.
- **What it's not:** a substitute for product-specific scenes. A film built
  only from generic beats looks like it could advertise any product.
- **Defaults leak.** Components ship demo props: placeholder text, sample
  chips, stock images, default speeds. Set every content prop explicitly, then
  review frames for leftover demo content.
- **Keep the choreography.** Prefer the component's own timeline played with
  `speed` over re-timing its internal keyframes one by one; partial re-timing
  breaks the choreography.
- **Built-in shots.** Check them before placing a component, for example a
  close-up after a wide shot. Cut before an unwanted shot instead of fighting
  it.
- **Edit the copy freely**, for example to add a missing prop such as a font
  weight. Remove components the film no longer uses.

## Frame Checks

You cannot judge motion from code. After each render, extract contact sheets
with ffmpeg: one frame per scene for composition, and dense strips across
transitions, the hook, and the ending. Look for clipped text, empty
backgrounds, wrong fonts, demo content, mesh or gradient edges exposed by
rotation, and doubled cuts. Render a half-scale preview for iteration and the
full master only at checkpoints.
