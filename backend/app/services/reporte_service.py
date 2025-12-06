from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


def generar_pdf_prioridad_ninos(resultados: list) -> BytesIO:
    """
    resultados = [
      {
        "nino": obj_nino,
        "criterios": {...},
        "score": 0.87,
      },
      ...
    ]
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Reporte de Prioridad de Niños (TOPSIS)")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 30

    for idx, r in enumerate(resultados, start=1):
        n = r["nino"]
        criterios = r["criterios"]
        score = r["score"]

        if y < 100:
            c.showPage()
            y = height - 50

        c.setFont("Helvetica-Bold", 11)
        nombre = f"{n.nombres} {n.apellido_paterno} {n.apellido_materno or ''}".strip()
        c.drawString(50, y, f"{idx}. {nombre}  (Score: {score:.4f})")
        y -= 14

        c.setFont("Helvetica", 9)
        for k, v in criterios.items():
            c.drawString(70, y, f"- {k}: {v}")
            y -= 12

        y -= 6

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
