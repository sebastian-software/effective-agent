import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Self-contained SVGs in the Field Guide palette: opaque ivory substrates, system sans-serif lettering,
// and unchanged provider paths. No external fonts, images, scripts, or filters.
const assets = resolve(dirname(fileURLToPath(import.meta.url)), "../site/assets");
const models = [
  { file: "gpt-6", label: "GPT-6", provider: "openai-blossom", size: 68,
    icon: { x: 162, y: 103, width: 156, height: 156 } },
  { file: "opus-5-5", label: "Opus 5.5", provider: "claude-spark", size: 57,
    icon: { x: 189, y: 130, width: 102, height: 102 } },
];

const ticks = Array.from({ length: 60 }, (_, index) =>
  `    <path d="M240 82v${index % 5 === 0 ? 13 : 9}" transform="rotate(${index * 6} 240 240)"/>`
).join("\n");

for (const model of models) {
  const original = await readFile(resolve(assets, `providers/${model.provider}.svg`), "utf8");
  const attributes = Object.entries(model.icon).map(([key, value]) => `${key}="${value}"`).join(" ");
  const provider = original.replace(/<svg\b[^>]*>/, (tag) =>
    tag.replace(/\s(?:width|height)="[^"]*"/g, "").replace("<svg", `<svg ${attributes}`)
  );
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="480" height="480" viewBox="0 0 480 480" role="img" aria-labelledby="title desc">
  <title id="title">Tuned for ${model.label} — Sebastian Software</title>
  <desc id="desc">Sebastian Software's model-tuning label for its agent skills.</desc>
  <defs>
    <path id="top" d="M55 240a185 185 0 0 1 370 0"/>
    <path id="bottom" d="M41 240a199 199 0 0 0 398 0"/>
  </defs>
  <circle cx="240" cy="240" r="238" fill="#fffdf7"/>
  <circle cx="240" cy="240" r="229" fill="none" stroke="#18372b" stroke-width="2.5"/>
  <path d="M20 240a220 220 0 0 1 440 0h-56a164 164 0 0 0-328 0Z" fill="#18372b"/>
  <g fill="none" stroke="#8a9586" stroke-width="2">
${ticks}
  </g>
  <g font-family="Arial, Helvetica, sans-serif" font-weight="700" text-anchor="middle">
    <text fill="#fffdf7" font-size="31" letter-spacing="4"><textPath href="#top" startOffset="50%">TUNED FOR</textPath></text>
    <text x="240" y="321" fill="#18372b" font-size="${model.size}" letter-spacing="-2">${model.label}</text>
    <text fill="#18372b" font-size="25" letter-spacing="2.5"><textPath href="#bottom" startOffset="50%">SEBASTIAN SOFTWARE</textPath></text>
  </g>
  ${provider.trim()}
  <path d="m228 365 12 21 12-21Z" fill="#a54e2c"/>
</svg>
`;
  await writeFile(resolve(assets, `seals/${model.file}.svg`), svg);
}
console.log("Rendered GPT-6 and Opus 5.5 model seals.");
