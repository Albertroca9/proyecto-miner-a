import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const skillDir = "C:/Users/alber/.codex/plugins/cache/openai-primary-runtime/presentations/26.1026.10807/skills/presentations";
const runtimePython = "C:/Users/alber/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe";
process.env.RUNTIME_NODE_MODULES = "C:/Users/alber/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules";
const buildDir = path.join(root, "tmp", "presentation_build");
const outputDir = path.join(root, "output");
await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(outputDir, { recursive: true });

const summary = JSON.parse(await fs.readFile(path.join(root, "results", "summary.json"), "utf8"));
const metrics = JSON.parse(await fs.readFile(path.join(root, "results", "metrics.json"), "utf8"));
const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });
deck.theme.defaultFont = "Arial";
const ink = "slate-950";
const muted = "slate-600";
const blue = "blue-700";
const teal = "teal-700";
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
  addText(slide, title, 72, 48, 1136, 72, 38, ink, true);
  addText(slide, `El precio de la inteligencia   ${number}/5`, 72, 675, 600, 22, 13, muted);
  return slide;
}

// 1. Cover
{
  const slide = deck.slides.add();
  slide.background.fill = "slate-950";
  addText(slide, "El precio de la inteligencia", 72, 166, 1120, 132, 58, "white", true);
  addText(slide, "Avance de proyecto", 75, 319, 760, 60, 30, "teal-300");
  addText(slide, "Jos, Albert, Maria, Unai, Pau y Bernardo", 75, 574, 1000, 38, 22, "slate-200");
  slide.speakerNotes.text = "Seguimos con El precio de la inteligencia. En la propuesta prometimos preparar los datos, montar el entorno experimental y comenzar con modelos exploratorios. Hoy mostramos ese avance y qué falta para poder recomendar tarifas y estudiar su evolución con rigor.";
}

// 2. Data
{
  const slide = slideWithTitle("Datos preparados", 2);
  addText(slide, "4.403", 74, 160, 350, 90, 64, blue, true);
  addText(slide, "listados actuales", 74, 248, 350, 45, 23, muted);
  addText(slide, "167.787", 650, 160, 510, 90, 64, blue, true);
  addText(slide, "observaciones históricas", 650, 248, 510, 45, 23, muted);
  addText(slide, "Cohorte comparable", 74, 374, 450, 50, 29, ink, true);
  addText(slide, "3.082 listados chat con precios positivos de entrada y salida", 74, 433, 1090, 85, 28, ink);
  addText(slide, "157 semanas · precios de lista · país del desarrollador", 74, 562, 1100, 42, 20, muted);
  slide.speakerNotes.text = "Partimos de dos CSV de precios de lista. Para comparar tarifas por tokens seleccionamos modelos de chat con precios positivos de entrada y salida; resultan 3.082 listados actuales y 139.874 observaciones históricas. Dejamos los originales intactos y automatizamos el procesamiento. El archivo indica el país del desarrollador, no del proveedor. Tampoco incluye una puntuación de calidad, por lo que nuestra recomendación inicial se basa en requisitos y coste.";
}

// 3. Price history
{
  const slide = slideWithTitle("Precios y composición del catálogo", 3);
  slide.charts.add("bar", {
    position: { left: 72, top: 150, width: 800, height: 440 },
    categories: ["Sept. 2023", "Sept. 2026"],
    series: [
      { name: "Entrada", values: [summary.first_week_median_input_usd, summary.last_week_median_input_usd], fill: blue },
      { name: "Salida", values: [summary.first_week_median_output_usd, summary.last_week_median_output_usd], fill: teal },
    ],
    hasLegend: true,
    barOptions: { direction: "column", grouping: "clustered" },
    dataLabels: { showValue: true, position: "outEnd", textStyle: { fontSize: 18 } },
    yAxis: { title: "USD / millón de tokens", majorGridlines: { style: "solid", fill: "slate-200", width: 1 } },
  });
  addText(slide, "41 → 3.082", 900, 194, 320, 75, 39, blue, true);
  addText(slide, "listados entre la primera y la última semana", 900, 269, 320, 115, 21, muted);
  addText(slide, "573", 900, 416, 290, 70, 44, teal, true);
  addText(slide, "cambios de precio de entrada en 136.118 comparaciones del mismo listado", 900, 487, 310, 120, 20, muted);
  slide.speakerNotes.text = "La mediana del precio de entrada de los listados comparables baja de 1,875 a 0,60 dólares por millón de tokens entre la primera y la última semana. Al mismo tiempo, la oferta observada crece de 41 a 3.082 listados. Por eso no atribuimos toda la caída a rebajas: entre 136.118 comparaciones sucesivas de precio de entrada del mismo listado detectamos 573 cambios. La entrada de nuevos modelos podría explicar parte de la diferencia; lo estudiaremos en la entrega final. Son observaciones sucesivas disponibles de cada model_id, no necesariamente semanas de calendario adyacentes.";
}

// 4. Experiments
{
  const slide = slideWithTitle("Primeros modelos", 4);
  slide.charts.add("bar", {
    position: { left: 72, top: 176, width: 610, height: 365 },
    categories: ["Clase mayoritaria", "Bosque aleatorio"],
    series: [{ name: "Macro-F1", values: [Number(metrics.classification.baseline.macro_f1.toFixed(3)), Number(metrics.classification.model.macro_f1.toFixed(3))], fill: blue }],
    hasLegend: false,
    barOptions: { direction: "bar", grouping: "clustered" },
    dataLabels: { showValue: true, position: "outEnd", textStyle: { fontSize: 19 } },
    xAxis: { minimumScale: 0, maximumScale: 1 },
  });
  addText(slide, "Clasificación de tramos", 72, 562, 600, 42, 23, ink, true);
  addText(slide, "Prueba separada por nombre de modelo", 72, 608, 610, 34, 18, muted);
  addText(slide, "3 grupos", 740, 195, 420, 72, 44, teal, true);
  addText(slide, "Silhouette 0,266", 740, 276, 430, 42, 24, ink);
  addText(slide, "1.763 listados: menor coste y contexto mediano de 128.000 tokens", 740, 366, 420, 115, 21, muted);
  addText(slide, "Otros grupos: más contexto y mayor proporción de capacidades", 740, 511, 420, 95, 21, muted);
  slide.speakerNotes.text = "Probamos clustering con precios, contexto y capacidades; tres grupos dan la mayor silhouette entre dos y seis grupos, 0,266. Encontramos un grupo numeroso de menor coste y contexto mediano de 128.000 tokens, y otros con mayor contexto y más capacidades. También entrenamos una clasificación exploratoria de tres rangos de coste usando solo especificaciones, nunca el precio que queremos predecir. Separando por nombre de modelo, el macro-F1 es 0,606 frente a 0,178 del baseline que elige la clase mayoritaria. Es un resultado inicial de una partición, que ampliaremos para el final.";
}

// 5. Recommendation and next step
{
  const slide = slideWithTitle("Recomendación y entrega final", 5);
  addText(slide, "El usuario indica", 72, 168, 490, 54, 29, ink, true);
  addText(slide, "Tokens de entrada y salida\nContexto mínimo\nCapacidades requeridas", 72, 239, 500, 180, 26, muted);
  addText(slide, "El prototipo devuelve", 658, 168, 520, 54, 29, ink, true);
  addText(slide, "Modelos compatibles ordenados por coste estimado", 658, 239, 520, 120, 26, muted);
  addText(slide, "Para la entrega final", 72, 474, 590, 54, 29, teal, true);
  addText(slide, "Predicción temporal frente a baseline, análisis de rebajas y entrada de modelos, demo en vivo", 72, 543, 1115, 100, 24, ink);
  slide.speakerNotes.text = "El prototipo permite indicar volumen de entrada y salida, contexto mínimo y capacidades como visión. Filtra los modelos que cumplen los requisitos y los ordena por coste estimado. En la entrega final conectaremos esta herramienta con una evaluación temporal frente a un baseline, estudiaremos cuánto del cambio de precios proviene de rebajas y cuánto de nuevos modelos, y haremos una demo en vivo. Para hablar de calidad-precio o de IA de frontera necesitamos primero una medida externa de calidad. Gracias.";
}

for (const [index, slide] of deck.slides.items.entries()) {
  const png = await deck.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(path.join(buildDir, `slide-${index + 1}.png`), new Uint8Array(await png.arrayBuffer()));
}

const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, "container_tools", "artifact_tool_utils.mjs")).href);
const staging = path.join(root, ".codex-finalizer");
await fs.mkdir(staging, { recursive: true });
const candidatePath = path.join(staging, "candidate.pptx");
await (await PresentationFile.exportPptx(deck)).save(candidatePath);
const finalPath = path.join(outputDir, "avance_proyecto_2026-11-01.pptx");
const validation = await finalizePresentation({
  workspaceDir: root,
  candidatePath,
  finalPath,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-heading-fit"],
  explicitTotalSlideCount: 5,
  requiredNativeChartOwnerSlides: [3, 4],
  materializeLiteralChartWorkbooks: true,
  fontPolicy: { basis: "design", families: [font] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(staging, "avance_proyecto.validation.json"),
});
console.log(JSON.stringify({ finalPath, validation }, null, 2));
