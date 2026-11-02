"""Create a teammate-facing PDF from the verified advance artifacts."""

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "avance_explicado_equipo.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
summary = json.loads((ROOT / "results" / "summary.json").read_text(encoding="utf-8"))
metrics = json.loads((ROOT / "results" / "metrics.json").read_text(encoding="utf-8"))

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")

NAVY = colors.HexColor("#0b1220")
BLUE = colors.HexColor("#1d4ed8")
TEAL = colors.HexColor("#0f766e")
INK = colors.HexColor("#1f2937")
MUTED = colors.HexColor("#526176")
LIGHT = colors.HexColor("#edf2f7")
PALE = colors.HexColor("#f7fafc")
WHITE = colors.white

styles = {
    "title": ParagraphStyle("title", fontName="Arial-Bold", fontSize=29, leading=34, textColor=NAVY, spaceAfter=10),
    "subtitle": ParagraphStyle("subtitle", fontName="Arial", fontSize=15, leading=21, textColor=TEAL, spaceAfter=24),
    "h1": ParagraphStyle("h1", fontName="Arial-Bold", fontSize=18, leading=23, textColor=NAVY, spaceAfter=12),
    "h2": ParagraphStyle("h2", fontName="Arial-Bold", fontSize=12.2, leading=17, textColor=TEAL, spaceBefore=13, spaceAfter=7),
    "body": ParagraphStyle("body", fontName="Arial", fontSize=9.8, leading=14.6, textColor=INK, spaceAfter=8),
    "small": ParagraphStyle("small", fontName="Arial", fontSize=8.2, leading=11.5, textColor=MUTED, spaceAfter=6),
    "cell": ParagraphStyle("cell", fontName="Arial", fontSize=8.8, leading=12.3, textColor=INK),
    "cell_bold": ParagraphStyle("cell_bold", fontName="Arial-Bold", fontSize=8.8, leading=12.3, textColor=NAVY),
    "metric": ParagraphStyle("metric", fontName="Arial-Bold", fontSize=21, leading=26, textColor=BLUE, alignment=TA_CENTER),
    "metric_label": ParagraphStyle("metric_label", fontName="Arial", fontSize=8.8, leading=12, textColor=MUTED, alignment=TA_CENTER),
}


def P(text, style="body"):
    return Paragraph(text, styles[style])


def bullet(text):
    return P("• " + text)


def table(headers, rows, widths, *, font_size=None):
    header_cells = [P(h, "cell_bold") for h in headers]
    data = [header_cells] + [[P(str(v), "cell") for v in row] for row in rows]
    result = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    result.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BLUE),
    ]))
    return result


def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page > 1:
        canvas.setFont("Arial-Bold", 8.5)
        canvas.setFillColor(TEAL)
        canvas.drawString(48, h - 31, "EL PRECIO DE LA INTELIGENCIA · AVANCE")
        canvas.setStrokeColor(LIGHT)
        canvas.line(48, h - 39, w - 48, h - 39)
    canvas.setStrokeColor(LIGHT)
    canvas.line(48, 42, w - 48, 42)
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(48, 29, "Informe para el equipo · 1 de noviembre de 2026")
    canvas.drawRightString(w - 48, 29, str(doc.page))
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4, leftMargin=48, rightMargin=48,
    topMargin=56, bottomMargin=58, title="El precio de la inteligencia — avance explicado",
    author="Equipo del proyecto", subject="Resumen técnico y operativo del avance de Minería de Datos",
)
W = A4[0] - 96
story = []

# 1. Executive summary
story += [
    Spacer(1, 76),
    P("El precio de la inteligencia", "title"),
    P("Qué hemos hecho en el avance y cómo continuar", "subtitle"),
    HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=20),
    P("Este documento permite a cualquier integrante explicar el trabajo, ejecutar la demo y distinguir resultados medidos de tareas pendientes. Se basa en los CSV y resultados guardados en el repositorio."),
    Spacer(1, 15),
]
metric_data = [[
    [P("4.403", "metric"), P("listados actuales", "metric_label")],
    [P("167.787", "metric"), P("filas históricas", "metric_label")],
    [P("3.082", "metric"), P("modelos chat comparables", "metric_label")],
]]
metric_table = Table(metric_data, colWidths=[W / 3] * 3)
metric_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PALE),
    ("TOPPADDING", (0, 0), (-1, -1), 13),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 13),
]))
story += [metric_table, Spacer(1, 23), P("Del compromiso inicial a lo entregado", "h1")]
story.append(table(["Prometimos", "Ya está preparado"], [
    ["Recolección, limpieza y entorno experimental", "Dos CSV originales, filtro reproducible, dependencias, pruebas y resultados regenerables."],
    ["Primeros modelos exploratorios", "Clustering de perfiles y clasificación de franjas tarifarias comparada con un baseline."],
    ["Recomendador y predicción de tarifas", "Prototipo interactivo de recomendación. La predicción temporal con validación queda para la entrega final."],
], [W * .40, W * .60]))
story += [Spacer(1, 16), P("Mensaje central", "h2"), P("Observamos una caída en la mediana de precios mientras el catálogo crece mucho. Como los precios de un mismo listado cambian pocas veces, el efecto de incorporar modelos nuevos merece un análisis separado. El recomendador actual encuentra opciones compatibles de menor coste, sin medir calidad."), PageBreak()]

# 2. Data and preparation
story += [P("1. Datos y preparación", "h1"), P("Qué archivos entran", "h2")]
story.append(table(["Archivo", "Contenido", "Volumen"], [
    ["ai_models_2026.csv", "Catálogo actual: precios, contexto, capacidades, desarrollador y proveedor.", "4.403 filas · 31 variables"],
    ["ai_model_price_history.csv", "Observaciones semanales de modelo, proveedor, modo, contexto y tarifas.", "167.787 filas · 157 semanas"],
], [W * .29, W * .47, W * .24]))
story += [
    P("La cobertura histórica va del 18 de septiembre de 2023 al 28 de septiembre de 2026. El histórico ofrece menos atributos que el catálogo actual: no contiene las capacidades booleanas ni el país del desarrollador.", "small"),
    P("La cohorte comparable", "h2"),
    bullet("Seleccionamos <b>mode = chat</b> y precios de entrada y salida <b>positivos</b> por millón de tokens. Las tarifas de imágenes, audio y otros modos usan unidades distintas."),
    bullet("Quedan <b>3.082</b> listados del catálogo y <b>139.874</b> observaciones históricas. Los originales permanecen intactos y los derivados se escriben en <b>results/</b>."),
    bullet("En el catálogo original falta el precio de entrada en el <b>17,1 %</b> de las filas y el de salida en el <b>17,4 %</b>. Estos registros no entran en la comparación de tarifas chat."),
    P("Coste de referencia", "h2"),
    P("Para poder comparar alternativas fijamos una carga de trabajo de <b>1.000.000 tokens de entrada y 250.000 de salida</b>. Coste estimado = tarifa de entrada + 0,25 × tarifa de salida. El cálculo usa USD y precios de lista; no incorpora descuentos, impuestos ni disponibilidad."),
    P("Interpretación de variables", "h2"),
    bullet("<b>developer_country</b> identifica el país del desarrollador del modelo; el archivo no indica el país del proveedor que lo comercializa."),
    bullet("Las capacidades, como visión o razonamiento, son indicadores de disponibilidad declarada. No constituyen una puntuación de calidad."),
    bullet("<b>model_id</b> representa el listado consumible. Un mismo nombre de modelo puede aparecer en varios proveedores con tarifas diferentes."),
    Spacer(1, 12),
    P("Código responsable: avance/data.py y avance/history.py. Reglas resumidas en README.md; fuentes originales conservadas en la raíz del repositorio.", "small"),
    PageBreak(),
]

# 3. EDA
story += [P("2. Qué muestran los datos", "h1"), P("Evolución semanal de los listados chat comparables", "h2")]
chart = Image(str(ROOT / "results" / "evolucion_semanal.png"), width=W, height=W * 2 / 3)
story += [chart, Spacer(1, 8), P("La mediana de entrada pasa de <b>1,875 a 0,60 USD</b> y la de salida de <b>4,0 a 1,8 USD</b> por millón de tokens entre la primera y la última semana. En el mismo período, la muestra crece de <b>41 a 3.082 listados</b>.")]
changes = summary["input_price_changes"]
comparison_count = f"{changes['comparisons']:,}".replace(",", ".")
change_pct = f"{changes['changes'] / changes['comparisons'] * 100:.2f}".replace(".", ",")
story += [P(f"Entre <b>{comparison_count}</b> comparaciones sucesivas del precio de entrada de un mismo <b>model_id</b> hay <b>{changes['changes']}</b> cambios ({change_pct} %): {changes['decreases']} bajadas y {changes['increases']} subidas. Estas comparaciones son observaciones sucesivas disponibles, no necesariamente semanas de calendario adyacentes.", "small")]
story += [P("Comparación geográfica exploratoria", "h2")]
story.append(table(["Desarrollador", "Listados chat", "Mediana entrada", "Mediana salida"], [
    ["EE. UU.", "1.642", "1,00 USD", "3,75 USD"],
    ["China", "1.060", "0,40 USD", "1,265 USD"],
], [W * .23, W * .22, W * .27, W * .28]))
story += [P("Son medianas descriptivas. El mix de modelos, capacidades, tamaños de contexto y proveedores puede diferir entre países. El avance no estima un efecto causal del país sobre el precio.", "small"), PageBreak()]

# 4. Models
story += [P("3. Modelos exploratorios", "h1"), P("Clustering: perfiles de precio y capacidad", "h2")]
story += [P("Transformamos con logaritmos los precios y tamaños de contexto, añadimos los indicadores de capacidades, imputamos faltantes y estandarizamos las variables. Probamos KMeans con 2 a 6 grupos. La mayor silhouette de esa búsqueda fue <b>0,266</b> con <b>3 grupos</b>.")]
story.append(table(["Grupo", "Listados", "Coste mediano del ejemplo", "Contexto mediano", "Perfil resumido"], [
    ["0", "1.202", "2,9275 USD", "922.000", "Visión 81 % · razonamiento 87 %"],
    ["1", "1.763", "0,60 USD", "128.000", "Menor coste; visión 15 %"],
    ["2", "117", "1,6875 USD", "1.048.576", "Visión 100 % · razonamiento 96 %"],
], [W * .09, W * .15, W * .25, W * .19, W * .32]))
story += [P("Los grupos describen perfiles presentes en el catálogo. La silhouette mide separación interna; no demuestra que un grupo sea mejor para todos los usuarios.", "small"), P("Clasificación: tramo del coste de referencia", "h2")]
story += [P("El objetivo son tres franjas de coste definidas por dos umbrales obtenidos <b>solo del entrenamiento</b>: 0,5125 y 2,20 USD. Las entradas del clasificador son tamaños de contexto y capacidades; no contienen precios ni identificadores. Separamos el conjunto por <b>model_name</b> (2.332 filas para entrenar y 750 para probar) para reducir la presencia de variantes del mismo nombre en ambos lados.")]
story.append(table(["Modelo", "Accuracy", "Macro-F1"], [
    ["Baseline: clase más frecuente", "0,365", "0,178"],
    ["Bosque aleatorio", "0,615", "0,606"],
], [W * .52, W * .24, W * .24]))
story += [P("El bosque aleatorio supera al baseline en esta partición. El tramo intermedio es el más difícil: 108 de sus 241 casos de prueba se clasifican correctamente. El resultado aún requiere repetición de particiones o validación adicional antes de la conclusión final.", "small"), P("Archivos de evidencia", "h2"), P("results/metrics.json conserva métricas y matriz de confusión; results/cluster_profiles.csv guarda los perfiles. El código está en avance/models.py.", "small"), PageBreak()]

# 5. Demo, reproducibility, final plan
story += [P("4. Recomendador, demo y próximos pasos", "h1"), P("Qué hace el prototipo", "h2")]
story += [P("La aplicación pide volumen total de tokens de entrada y salida, contexto mínimo y capacidades requeridas. Primero excluye los modelos que no cumplen los requisitos; después calcula el coste de esa carga de trabajo y ordena los listados de menor a mayor coste. La interfaz está en <b>streamlit_app.py</b> y las reglas en <b>avance/recommend.py</b>.")]
story.append(table(["Entrada inicial de la demo", "Valor"], [
    ["Tokens de entrada", "1.000.000"],
    ["Tokens de salida", "250.000"],
    ["Contexto mínimo", "32.000 tokens"],
    ["Capacidad", "Visión"],
], [W * .50, W * .50]))
story += [P("El ranking ofrece la opción de menor precio de lista que cumple los filtros. No mide calidad, latencia, fiabilidad ni disponibilidad. Por ello aún no debe llamarse ranking de «calidad-precio».", "small"), P("Cómo reproducirlo desde la raíz del repositorio", "h2")]
commands = [
    r"python -m venv .venv",
    r".\.venv\Scripts\python.exe -m pip install -r requirements.txt",
    r".\.venv\Scripts\python.exe -m unittest discover -s tests -v",
    r".\.venv\Scripts\python.exe -m scripts.run_avance",
    r".\.venv\Scripts\python.exe -m streamlit run streamlit_app.py",
]
code = Preformatted("\n".join(commands), ParagraphStyle("code", fontName="Courier", fontSize=8.8, leading=13, textColor=INK))
code_table = Table([[code]], colWidths=[W])
code_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE), ("BOX", (0, 0), (-1, -1), 0.5, LIGHT), ("LEFTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
story += [code_table, Spacer(1, 8), P("El pipeline genera tablas, gráficos y métricas en <b>results/</b>. En la comprobación del avance pasaron 10 pruebas. La presentación está en <b>output/avance_proyecto_2026-11-01.pptx</b> y el guion en <b>docs/avance_video_4_min.md</b>. Trabajo guardado en la rama local <b>codex/avance-precios-ia</b>, commit <b>23c7874</b>.", "small")]
story += [P("Para la entrega final", "h2"), bullet("Evaluar una predicción temporal fuera de tiempo frente al baseline de mantener la última tarifa observada."), bullet("Separar mejor las rebajas de listados existentes de la incorporación de modelos nuevos; profundizar en las diferencias geográficas controlando características."), bullet("Ampliar y demostrar el recomendador en vivo. Una afirmación sobre IA de frontera o calidad-precio exige definir y medir calidad con una fuente adicional compatible.")]
story += [P("Punto administrativo: el enunciado indica grupos de cinco personas y el primer guion menciona seis. Confirmar con el docente que la composición del equipo está autorizada.", "small")]

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(OUTPUT)
