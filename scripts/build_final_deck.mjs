import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const skillDir = "C:/Users/alber/.codex/plugins/cache/openai-primary-runtime/presentations/26.1119.11507/skills/presentations";
const runtimePython = "C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1119-907-0_26.1119.907.0_x64__3k8sg7r9htsxt/dependencies/python/python.exe";
process.env.RUNTIME_NODE_MODULES = "C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1119-907-0_26.1119.907.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules";
const staging = path.join(root, ".codex-finalizer");
const output = path.join(root, "output");
await fs.mkdir(staging, { recursive: true });
await fs.mkdir(output, { recursive: true });

const clustering = JSON.parse(await fs.readFile(path.join(root, "results", "metrics.json"), "utf8"));
const result = JSON.parse(await fs.readFile(path.join(root, "results", "final", "evaluation.json"), "utf8"));
const script = await fs.readFile(path.join(root, "docs", "guion_final_5_min.md"), "utf8");
const notes = [...script.matchAll(/«([\s\S]*?)»/g)].map(match => match[1]);
if (notes.length !== 7) throw new Error("Expected seven narration blocks");

const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });
deck.theme.defaultFont = "Arial";
const ink = "slate-950";
const muted = "slate-600";
const blue = "blue-700";
const teal = "teal-700";
const orange = "orange-600";
const font = "Arial";

function addText(slide, value, x, y, width, height, size, color = ink, bold = false) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position: { left: x, top: y, width, height },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = value;
  shape.text.style = { typeface: font, fontSize: size, color, bold };
  return shape;
}

function slideWithTitle(title, number) {
  const slide = deck.slides.add();
  slide.background.fill = "white";
  addText(slide, title, 72, 48, 1136, 75, 38, ink, true);
  addText(slide, `El precio de la inteligencia   ${number}/7`, 72, 675, 700, 22, 13, muted);
  slide.speakerNotes.text = notes[number - 1];
  return slide;
}

// 1. Cover
{
  const slide = deck.slides.add();
  slide.background.fill = "slate-950";
  addText(slide, "El precio de la inteligencia", 72, 150, 1120, 142, 58, "white", true);
  addText(slide, "Proyecto final · Minería de Datos", 75, 323, 900, 60, 30, "teal-300");
  addText(slide, "Jos, Albert, Maria, Unai, Pau y Bernardo", 75, 575, 1000, 40, 22, "slate-200");
  slide.speakerNotes.text = notes[0];
}

// 2. Data and process
{
  const slide = slideWithTitle("Datos comparables", 2);
  addText(slide, "4.403", 74, 170, 320, 88, 59, blue, true);
  addText(slide, "listados actuales", 74, 255, 360, 40, 22, muted);
  addText(slide, "167.787", 495, 170, 410, 88, 59, blue, true);
  addText(slide, "observaciones históricas", 495, 255, 470, 40, 22, muted);
  addText(slide, "3.082", 995, 170, 240, 88, 59, teal, true);
  addText(slide, "chat elegibles", 995, 255, 245, 40, 22, muted);
  addText(slide, "CSV originales  →  cohorte comparable  →  experimentos  →  recomendación", 74, 383, 1135, 65, 26, ink, true);
  addText(slide, "Coste de ejemplo: 1 M de entrada + 0,25 M de salida", 74, 500, 1060, 52, 26, ink);
  addText(slide, "157 semanas · precios de lista · país del desarrollador", 74, 589, 1100, 38, 21, muted);
}

// 3. Catalogue dynamics
{
  const slide = slideWithTitle("El catálogo cambia más que las tarifas", 3);
  addText(slide, "519 cambios en 135.928 comparaciones de listados continuadores (0,382 %)", 74, 127, 1130, 40, 23, teal, true);
  const chartBytes = await fs.readFile(path.join(root, "results", "final", "dinamica_catalogo.png"));
  slide.images.add({
    blob: chartBytes.buffer.slice(chartBytes.byteOffset, chartBytes.byteOffset + chartBytes.byteLength),
    contentType: "image/png",
    alt: "Medianas de tarifa de entrada y eventos semanales de entrada y cambio de tarifa",
    fit: "contain",
    position: { left: 72, top: 173, width: 1136, height: 485 },
  });
}

// 4. Temporal evaluation
{
  const slide = slideWithTitle("La persistencia supera a la regresión", 4);
  addText(slide, "26 semanas fuera de tiempo · abril a septiembre de 2026", 74, 129, 1090, 42, 23, muted);
  slide.charts.add("bar", {
    position: { left: 72, top: 205, width: 745, height: 380 },
    categories: ["Persistencia", "Regresión"],
    series: [{ name: "MAE (USD)", values: [Number(result.temporal.persistence.mae_usd.toFixed(4)), Number(result.temporal.regression.mae_usd.toFixed(4))], fill: blue }],
    hasLegend: false,
    barOptions: { direction: "bar", grouping: "clustered" },
    dataLabels: { showValue: true, position: "outEnd", textStyle: { fontSize: 19 } },
    xAxis: { minimumScale: 0, maximumScale: 0.05, title: "MAE (USD)" },
  });
  addText(slide, "0,0145", 888, 222, 300, 78, 54, teal, true);
  addText(slide, "USD de error medio con el baseline", 888, 307, 300, 98, 23, ink);
  addText(slide, "Repetir la última mediana predice mejor en este periodo", 888, 466, 300, 132, 22, muted);
}

// 5. Classification and clustering
{
  const slide = slideWithTitle("La clasificación supera su baseline", 5);
  addText(slide, "Macro-F1 medio · cinco particiones separadas por nombre de modelo", 74, 132, 1110, 42, 23, muted);
  slide.charts.add("bar", {
    position: { left: 72, top: 208, width: 725, height: 355 },
    categories: ["Clase mayoritaria", "Bosque aleatorio"],
    series: [{ name: "Macro-F1", values: [Number(result.classification_repeated.baseline_macro_f1.mean.toFixed(3)), Number(result.classification_repeated.model_macro_f1.mean.toFixed(3))], fill: blue }],
    hasLegend: false,
    barOptions: { direction: "bar", grouping: "clustered" },
    dataLabels: { showValue: true, position: "outEnd", textStyle: { fontSize: 19 } },
    xAxis: { minimumScale: 0, maximumScale: 0.7 },
  });
  addText(slide, "0,594", 864, 222, 335, 82, 53, teal, true);
  addText(slide, "macro-F1 medio del bosque", 864, 303, 335, 84, 23, ink);
  addText(slide, `Clustering: ${clustering.clustering.chosen_k} grupos · silhouette ${clustering.clustering.silhouette_by_k[3].toFixed(3).replace(".", ",")}`, 864, 453, 328, 120, 22, muted);
  addText(slide, "Predictores: contexto y capacidades; sin precio", 74, 587, 1100, 40, 21, muted);
}

// 6. Recommender
{
  const slide = slideWithTitle("Recomendador por requisitos y coste", 6);
  addText(slide, "Entrada del usuario", 74, 174, 470, 46, 28, ink, true);
  addText(slide, "Tokens de entrada y salida\nContexto mínimo\nCapacidades requeridas", 74, 235, 490, 190, 26, muted);
  addText(slide, "Salida de la demo", 660, 174, 505, 46, 28, ink, true);
  addText(slide, "Listados compatibles ordenados por coste de lista estimado", 660, 235, 520, 130, 26, blue, true);
  addText(slide, "El ranking cambia cuando cambian los requisitos", 74, 475, 1100, 60, 27, teal, true);
  addText(slide, "No mide calidad, latencia ni disponibilidad", 74, 555, 1100, 42, 22, muted);
}

// 7. Conclusion
{
  const slide = slideWithTitle("Conclusiones y límites", 7);
  addText(slide, "La mediana baja; pocos listados continuadores cambian su tarifa semanal", 74, 157, 1110, 110, 30, ink, true);
  addText(slide, "Clasificación: supera la clase mayoritaria", 74, 304, 1110, 52, 26, teal);
  addText(slide, "Predicción semanal: la persistencia gana", 74, 385, 1110, 52, 26, orange);
  addText(slide, "Sin benchmark de calidad ni definición de IA de frontera, no estimamos cuándo llegará a 0,10 USD", 74, 495, 1110, 106, 24, muted);
}

for (const [index, slide] of deck.slides.items.entries()) {
  const png = await deck.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(path.join(staging, `final-slide-${index + 1}.png`), new Uint8Array(await png.arrayBuffer()));
}

const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, "container_tools", "artifact_tool_utils.mjs")).href);
const candidatePath = path.join(staging, "candidate-final.pptx");
await (await PresentationFile.exportPptx(deck)).save(candidatePath);
const finalPath = path.join(output, "entrega_final_2026-11-23.pptx");
const validation = await finalizePresentation({
  workspaceDir: root,
  candidatePath,
  finalPath,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-heading-fit"],
  explicitTotalSlideCount: 7,
  requiredNativeChartOwnerSlides: [4, 5],
  materializeLiteralChartWorkbooks: true,
  fontPolicy: { basis: "design", families: [font] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(staging, "entrega_final.validation.json"),
});
console.log(JSON.stringify({ finalPath, validation }, null, 2));
