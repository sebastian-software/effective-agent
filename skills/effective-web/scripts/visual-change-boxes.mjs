#!/usr/bin/env node
// Finds what changed between two full-page screenshots of the same page and
// prints review annotations as JSON. Dependency-free: Node's zlib decodes PNG.
//
//   node visual-change-boxes.mjs before.png after.png [--scale 2]
//
// Rows are aligned like lines in a text diff, so content that only moved is not
// reported again. Moved content tolerates sub-pixel anti-aliasing differences;
// content that kept its position is compared exactly.

import { readFileSync, realpathSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { inflateSync } from "node:zlib";

const PNG_SIGNATURE = "89504e470d0a1a0a";
const CHANNELS = { 0: 1, 2: 3, 3: 1, 4: 2, 6: 4 };
/** Hunks closer than this many device pixels are framed together. */
const MERGE_GAP = 24;
/** Rows a moved line may have snapped up or down. */
const SNAP_ROWS = 2;
/** Text snaps to whole pixels while icons and images keep fractional offsets. */
const BLOCK_WIDTH = 32;
const FRACTIONS = [0, 0.25, 0.5, 0.75];
const SMOOTH_RADIUS = 2;
/** Blurred luminance of moved content this close counts as equal. */
const MOVED_TOLERANCE = 32;
const FRAME_PADDING = 6;
const LABEL_HEIGHT = 18;
const LABEL_GAP = 4;
const LABEL_PADDING = 6;
const LABEL_CHARACTER_WIDTH = 8;

export const STYLES = {
  added: { color: "#15803d", label: "NEW" },
  changed: { color: "#7c3aed", label: "CHANGED" },
  removed: { color: "#e11d48", label: "REMOVED" },
};

// ---------------------------------------------------------------- PNG decoding

function paeth(left, up, upperLeft) {
  const estimate = left + up - upperLeft;
  const distanceLeft = Math.abs(estimate - left);
  const distanceUp = Math.abs(estimate - up);
  const distanceUpperLeft = Math.abs(estimate - upperLeft);
  if (distanceLeft <= distanceUp && distanceLeft <= distanceUpperLeft) return left;
  return distanceUp <= distanceUpperLeft ? up : upperLeft;
}

function unfilter(data, width, height, bytesPerPixel) {
  const stride = width * bytesPerPixel;
  const pixels = new Uint8Array(stride * height);
  for (let row = 0; row < height; row++) {
    const filter = data[row * (stride + 1)];
    const source = row * (stride + 1) + 1;
    const target = row * stride;
    for (let index = 0; index < stride; index++) {
      const left = index >= bytesPerPixel ? pixels[target + index - bytesPerPixel] : 0;
      const up = row > 0 ? pixels[target - stride + index] : 0;
      const upperLeft = row > 0 && index >= bytesPerPixel ? pixels[target - stride + index - bytesPerPixel] : 0;
      const predictors = [0, left, up, (left + up) >> 1, paeth(left, up, upperLeft)];
      if (predictors[filter] === undefined) throw new Error(`Unknown PNG filter ${filter}`);
      pixels[target + index] = (data[source + index] + predictors[filter]) & 0xff;
    }
  }
  return pixels;
}

/**
 * Decodes an 8-bit, non-interlaced PNG, the format browser screenshots use.
 * @param {Uint8Array} bytes
 * @returns {{ width: number, height: number, data: Uint8Array }} RGBA pixels
 */
export function decodePng(bytes) {
  if (Buffer.from(bytes.subarray(0, 8)).toString("hex") !== PNG_SIGNATURE) {
    throw new Error("Not a PNG file");
  }
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const idat = [];
  let header;
  let palette;
  let transparency;
  for (let offset = 8; offset < bytes.length; ) {
    const length = view.getUint32(offset);
    const type = Buffer.from(bytes.subarray(offset + 4, offset + 8)).toString("latin1");
    const body = bytes.subarray(offset + 8, offset + 8 + length);
    if (type === "IHDR") {
      header = {
        width: view.getUint32(offset + 8),
        height: view.getUint32(offset + 12),
        bitDepth: body[8],
        colorType: body[9],
        interlace: body[12],
      };
    } else if (type === "PLTE") palette = body;
    else if (type === "tRNS") transparency = body;
    else if (type === "IDAT") idat.push(body);
    else if (type === "IEND") break;
    offset += length + 12;
  }
  const channels = header && CHANNELS[header.colorType];
  if (!header || channels === undefined || header.bitDepth !== 8 || header.interlace !== 0) {
    throw new Error("Only 8-bit, non-interlaced PNG files are supported");
  }
  const { width, height, colorType } = header;
  const raw = unfilter(inflateSync(Buffer.concat(idat)), width, height, channels);
  const data = new Uint8Array(width * height * 4);
  for (let pixel = 0; pixel < width * height; pixel++) {
    const source = pixel * channels;
    const target = pixel * 4;
    if (colorType === 3) {
      const entry = raw[source];
      data.set(palette.subarray(entry * 3, entry * 3 + 3), target);
      data[target + 3] = transparency && entry < transparency.length ? transparency[entry] : 255;
    } else if (colorType === 0 || colorType === 4) {
      data.fill(raw[source], target, target + 3);
      data[target + 3] = colorType === 4 ? raw[source + 1] : 255;
    } else {
      data.set(raw.subarray(source, source + 3), target);
      data[target + 3] = colorType === 6 ? raw[source + 3] : 255;
    }
  }
  return { width, height, data };
}

// -------------------------------------------------------------- row alignment

function pixelsOf(image) {
  const bytes = image.data.byteOffset % 4 === 0 ? image.data : Uint8Array.from(image.data);
  return {
    width: image.width,
    height: image.height,
    values: new Uint32Array(bytes.buffer, bytes.byteOffset, image.width * image.height),
  };
}

// Two independent 32-bit hashes per row keep accidental matches out of reach.
function rowKeys(pixels) {
  const keys = [];
  for (let row = 0; row < pixels.height; row++) {
    let first = 0x811c9dc5;
    let second = 0;
    for (const value of pixels.values.subarray(row * pixels.width, (row + 1) * pixels.width)) {
      first = Math.imul(first ^ value, 0x01000193);
      second = (Math.imul(second, 31) + value) | 0;
    }
    keys.push(`${pixels.width}:${first >>> 0}:${second >>> 0}`);
  }
  return keys;
}

function uniqueRows(keys, start, end) {
  const positions = new Map();
  const repeated = new Set();
  for (let row = start; row < end; row++) {
    if (positions.has(keys[row])) repeated.add(keys[row]);
    positions.set(keys[row], row);
  }
  for (const key of repeated) positions.delete(key);
  return positions;
}

// The longest chain of anchors increasing on both sides, by patience sorting.
function increasingAnchors(anchors) {
  const tailRows = [];
  const tailIndices = [];
  const previous = [];
  anchors.forEach(([, afterRow], index) => {
    let low = 0;
    let high = tailRows.length;
    while (low < high) {
      const middle = (low + high) >> 1;
      if (tailRows[middle] < afterRow) low = middle + 1;
      else high = middle;
    }
    previous[index] = low > 0 ? tailIndices[low - 1] : -1;
    tailRows[low] = afterRow;
    tailIndices[low] = index;
  });
  const chain = [];
  for (let index = tailIndices.at(-1) ?? -1; index >= 0; index = previous[index]) {
    chain.push(anchors[index]);
  }
  return chain.reverse();
}

/**
 * Aligns screenshot rows like a patience diff aligns lines.
 * @param {string[]} before
 * @param {string[]} after
 * @returns {{ beforeStart: number, beforeEnd: number, afterStart: number, afterEnd: number }[]}
 */
export function alignRows(before, after) {
  const hunks = [];
  const visit = (b0, b1, a0, a1) => {
    while (b0 < b1 && a0 < a1 && before[b0] === after[a0]) {
      b0++;
      a0++;
    }
    while (b0 < b1 && a0 < a1 && before[b1 - 1] === after[a1 - 1]) {
      b1--;
      a1--;
    }
    if (b0 === b1 && a0 === a1) return;
    const afterUnique = uniqueRows(after, a0, a1);
    const anchors = [];
    for (const [key, beforeRow] of uniqueRows(before, b0, b1)) {
      const afterRow = afterUnique.get(key);
      if (afterRow !== undefined) anchors.push([beforeRow, afterRow]);
    }
    const chain = increasingAnchors(anchors.sort(([left], [right]) => left - right));
    if (chain.length === 0) {
      hunks.push({ beforeStart: b0, beforeEnd: b1, afterStart: a0, afterEnd: a1 });
      return;
    }
    let nextBefore = b0;
    let nextAfter = a0;
    for (const [beforeRow, afterRow] of chain) {
      visit(nextBefore, beforeRow, nextAfter, afterRow);
      nextBefore = beforeRow + 1;
      nextAfter = afterRow + 1;
    }
    visit(nextBefore, b1, nextAfter, a1);
  };
  visit(0, before.length, 0, after.length);
  return hunks;
}

// ------------------------------------------------- noise in moved content

function smoothLuminance(image) {
  const { width, height, data } = image;
  let values = new Float32Array(width * height);
  for (let pixel = 0; pixel < values.length; pixel++) {
    const byte = pixel * 4;
    values[pixel] = 0.299 * data[byte] + 0.587 * data[byte + 1] + 0.114 * data[byte + 2];
  }
  for (const stride of [1, width]) {
    const blurred = new Float32Array(values.length);
    const length = stride === 1 ? width : height;
    for (let index = 0; index < values.length; index++) {
      const position = stride === 1 ? index % width : Math.floor(index / width);
      let sum = 0;
      for (let offset = -SMOOTH_RADIUS; offset <= SMOOTH_RADIUS; offset++) {
        const clamped = Math.min(length - 1, Math.max(0, position + offset));
        sum += values[index + (clamped - position) * stride];
      }
      blurred[index] = sum / (SMOOTH_RADIUS * 2 + 1);
    }
    values = blurred;
  }
  return { width, height, values };
}

function blockClose(plane, row, other, otherRow, start, fraction) {
  const { width } = plane;
  const next = Math.min(otherRow + 1, other.height - 1);
  for (let x = start; x < Math.min(width, start + BLOCK_WIDTH); x++) {
    const sampled =
      (1 - fraction) * other.values[otherRow * width + x] + fraction * other.values[next * width + x];
    if (Math.abs(plane.values[row * width + x] - sampled) > MOVED_TOLERANCE) return false;
  }
  return true;
}

// Every block of a row must match the other side a few rows around `near`,
// each block at its own sub-pixel offset.
function hasCloseRow(plane, row, other, near) {
  if (plane.width !== other.width) return false;
  for (let start = 0; start < plane.width; start += BLOCK_WIDTH) {
    let matched = false;
    for (let candidate = near - SNAP_ROWS; candidate <= near + SNAP_ROWS && !matched; candidate++) {
      if (candidate < 0 || candidate >= other.height) continue;
      matched = FRACTIONS.some((fraction) => blockClose(plane, row, other, candidate, start, fraction));
    }
    if (!matched) return false;
  }
  return true;
}

function isMovedContentNoise(planes, hunk) {
  const afterLength = hunk.afterEnd - hunk.afterStart;
  const beforeLength = hunk.beforeEnd - hunk.beforeStart;
  if (hunk.afterStart === hunk.beforeStart || Math.abs(afterLength - beforeLength) > SNAP_ROWS) {
    return false;
  }
  const shift = hunk.afterStart - hunk.beforeStart;
  for (let row = hunk.afterStart; row < hunk.afterEnd; row++) {
    if (!hasCloseRow(planes.after, row, planes.before, row - shift)) return false;
  }
  for (let row = hunk.beforeStart; row < hunk.beforeEnd; row++) {
    if (!hasCloseRow(planes.before, row, planes.after, row + shift)) return false;
  }
  return true;
}

// ------------------------------------------------------------ change boxes

// Columns of `span` that differ from `other`, rows compared top-aligned; rows
// without a counterpart are compared with their own first pixel.
function changedColumns(span, other) {
  let left = Infinity;
  let right = -Infinity;
  const { values, width } = span.pixels;
  for (let offset = 0; offset < span.length; offset++) {
    const row = (span.start + offset) * width;
    const otherRow = (other.start + offset) * other.pixels.width;
    for (let x = 0; x < width; x++) {
      let reference = values[row];
      if (offset < other.length) {
        reference = x < other.pixels.width ? other.pixels.values[otherRow + x] : undefined;
      }
      if (values[row + x] !== reference) {
        left = Math.min(left, x);
        right = Math.max(right, x);
      }
    }
  }
  return left <= right ? { left, right } : undefined;
}

function isUniformRow(pixels, row) {
  const start = row * pixels.width;
  const background = pixels.values[start];
  return pixels.values.subarray(start, start + pixels.width).every((value) => value === background);
}

// Added rows lose leading and trailing background, so frames hug new content.
function withoutBackgroundRows(span) {
  let { start, length } = span;
  while (length > 1 && isUniformRow(span.pixels, start)) {
    start++;
    length--;
  }
  while (length > 1 && isUniformRow(span.pixels, start + length - 1)) length--;
  return { ...span, start, length };
}

function hunkBox(before, after, hunk) {
  const beforeSpan = { pixels: before, start: hunk.beforeStart, length: hunk.beforeEnd - hunk.beforeStart };
  const afterSpan = { pixels: after, start: hunk.afterStart, length: hunk.afterEnd - hunk.afterStart };
  if (afterSpan.length === 0) {
    const removed = changedColumns(beforeSpan, { ...beforeSpan, length: 0 });
    const left = Math.min(removed?.left ?? 0, after.width - 1);
    const right = Math.min(removed?.right ?? after.width - 1, after.width - 1);
    return { kind: "removed", x: left, y: hunk.afterStart, width: right - left + 1, height: 0 };
  }
  const added = beforeSpan.length === 0;
  const content = added ? withoutBackgroundRows(afterSpan) : afterSpan;
  const columns = changedColumns(content, beforeSpan) ?? { left: 0, right: after.width - 1 };
  return {
    kind: added ? "added" : "changed",
    x: columns.left,
    y: content.start,
    width: columns.right - columns.left + 1,
    height: content.length,
  };
}

function mergeBoxes(boxes) {
  const merged = [];
  for (const box of boxes) {
    const last = merged.at(-1);
    if (!last || box.y - (last.y + last.height) > MERGE_GAP) {
      merged.push(box);
      continue;
    }
    const x = Math.min(last.x, box.x);
    const y = Math.min(last.y, box.y);
    const right = Math.max(last.x + last.width, box.x + box.width);
    const bottom = Math.max(last.y + last.height, box.y + box.height);
    // Neighboring edits of different kinds read as one replacement.
    const kind = last.kind === box.kind ? last.kind : "changed";
    merged[merged.length - 1] = { kind, x, y, width: right - x, height: bottom - y };
  }
  return merged;
}

/**
 * Finds the changed areas of the newer screenshot, in its device pixels.
 * @param {{ width: number, height: number, data: Uint8Array }} before
 * @param {{ width: number, height: number, data: Uint8Array }} after
 * @returns {{ kind: "added" | "changed" | "removed", x: number, y: number, width: number, height: number }[]}
 */
export function findChanges(before, after) {
  const beforePixels = pixelsOf(before);
  const afterPixels = pixelsOf(after);
  let hunks = alignRows(rowKeys(beforePixels), rowKeys(afterPixels));
  if (hunks.some((hunk) => hunk.afterStart !== hunk.beforeStart)) {
    const planes = { before: smoothLuminance(before), after: smoothLuminance(after) };
    hunks = hunks.filter((hunk) => !isMovedContentNoise(planes, hunk));
  }
  return mergeBoxes(hunks.map((hunk) => hunkBox(beforePixels, afterPixels, hunk)));
}

// ------------------------------------------------------------- annotations

/**
 * Numbers the changes in reading order and converts them to CSS pixels.
 * @param {ReturnType<typeof findChanges>} changes
 * @param {number} scale The device scale factor of the screenshots.
 */
export function annotate(changes, scale) {
  return changes.map((change, index) => {
    const x = Math.floor(change.x / scale);
    const y = Math.floor(change.y / scale);
    return {
      kind: change.kind,
      label: `${STYLES[change.kind].label} ${index + 1}`,
      color: STYLES[change.kind].color,
      x,
      y,
      width: Math.ceil((change.x + change.width) / scale) - x,
      height: Math.ceil((change.y + change.height) / scale) - y,
    };
  });
}

/**
 * A self-contained browser expression that draws the annotations as a
 * non-interactive overlay: dashed frames with a white halo, labels outside the
 * marked content, everything clipped to the page so its size does not change.
 * @param {ReturnType<typeof annotate>} annotations
 */
export function overlayScript(annotations) {
  const settings = { annotations, FRAME_PADDING, LABEL_HEIGHT, LABEL_GAP, LABEL_PADDING, LABEL_CHARACTER_WIDTH };
  return `(${paintOverlay.toString()})(${JSON.stringify(settings)})`;
}

function paintOverlay(settings) {
  const { annotations, FRAME_PADDING: pad, LABEL_HEIGHT: labelHeight, LABEL_GAP: gap } = settings;
  const root = document.documentElement;
  const pageWidth = root.scrollWidth;
  const overlay = document.createElement("div");
  overlay.dataset.visualChangeOverlay = "";
  overlay.style.cssText = `position:absolute;left:0;top:0;width:${pageWidth}px;height:${root.scrollHeight}px;overflow:hidden;z-index:2147483647;pointer-events:none`;
  for (const note of annotations) {
    const removed = note.kind === "removed";
    const left = Math.max(0, note.x - pad);
    const width = Math.min(pageWidth, note.x + note.width + pad) - left;
    const top = removed ? note.y : Math.max(0, note.y - pad);
    const frame = document.createElement("div");
    frame.style.cssText = `position:absolute;box-sizing:border-box;border-radius:4px;left:${left}px;top:${top}px;width:${width}px;height:${removed ? 0 : note.height + pad * 2}px;${removed ? "border-top" : "border"}:2px dashed ${note.color};box-shadow:0 0 0 1px #fff,inset 0 0 0 1px #fff`;
    const labelWidth = note.label.length * settings.LABEL_CHARACTER_WIDTH + settings.LABEL_PADDING * 2;
    const above = top - labelHeight - gap;
    const labelTop = removed ? note.y + gap : above >= 0 ? above : top + gap;
    const label = document.createElement("div");
    label.textContent = note.label;
    label.style.cssText = `position:absolute;left:${Math.max(0, Math.min(left, pageWidth - labelWidth))}px;top:${labelTop}px;height:${labelHeight}px;padding:0 ${settings.LABEL_PADDING}px;border-radius:3px;background:${note.color};color:#fff;font:700 11px/${labelHeight}px system-ui,sans-serif;letter-spacing:0.02em;white-space:nowrap;box-shadow:0 0 0 1px #fff`;
    overlay.append(frame, label);
  }
  root.append(overlay);
}

// --------------------------------------------------------------------- CLI

function main(argv) {
  const files = argv.filter((argument, index) => !argument.startsWith("--") && argv[index - 1] !== "--scale");
  const scaleIndex = argv.indexOf("--scale");
  const scale = scaleIndex === -1 ? 1 : Number(argv[scaleIndex + 1]);
  if (files.length !== 2 || !(scale > 0)) {
    process.stderr.write("Usage: node visual-change-boxes.mjs <before.png> <after.png> [--scale <device pixel ratio>]\n");
    return 2;
  }
  const [before, after] = files.map((file) => decodePng(readFileSync(file)));
  const changes = findChanges(before, after);
  const annotations = annotate(changes, scale);
  const result = {
    before: { width: before.width, height: before.height },
    after: { width: after.width, height: after.height },
    scale,
    changes: changes.map((change, index) => ({ ...change, label: annotations[index].label })),
    annotations,
    legend: annotations.map((annotation) => annotation.label).join(", "),
    overlayScript: overlayScript(annotations),
  };
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  return 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(realpathSync(process.argv[1])).href) {
  try {
    process.exitCode = main(process.argv.slice(2));
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}
