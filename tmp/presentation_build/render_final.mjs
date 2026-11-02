import fs from "node:fs/promises";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const deck = await PresentationFile.importPptx(await FileBlob.load("output/avance_proyecto_2026-11-01.pptx"));
for (const [index, slide] of deck.slides.items.entries()) {
  const png = await deck.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(`tmp/presentation_build/final-slide-${index + 1}.png`, new Uint8Array(await png.arrayBuffer()));
}
console.log(`Rendered ${deck.slides.items.length} final slides`);
