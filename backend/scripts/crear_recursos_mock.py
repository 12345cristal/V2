from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# Crear directorio
recursos_dir = Path("uploads/tareas")
recursos_dir.mkdir(parents=True, exist_ok=True)

def crear_pdf(nombre, titulo, contenido):
    """Crea un PDF de ejemplo."""
    ruta = recursos_dir / nombre
    doc = SimpleDocTemplate(str(ruta), pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = []
    story.append(Paragraph(titulo, styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(contenido, styles['Normal']))
    
    doc.build(story)
    print(f"✅ Creado: {ruta}")

# Crear PDFs de ejemplo
crear_pdf(
    "guia-soplo.pdf",
    "Guía de Ejercicios de Soplo",
    """
    <b>Ejercicio 1:</b> Soplar con pajita en un vaso de agua<br/>
    <b>Ejercicio 2:</b> Soplar plumas o papel picado<br/>
    <b>Ejercicio 3:</b> Inflar globos<br/>
    <br/>
    Realizar cada ejercicio durante 2 minutos.
    """
)

crear_pdf(
    "palabras-r.pdf",
    "Palabras con R",
    """
    Practicar estas palabras:<br/>
    1. Perro<br/>
    2. Carro<br/>
    3. Ratón<br/>
    4. Tierra<br/>
    5. Torre<br/>
    """
)

crear_pdf(
    "figuras-geometricas.pdf",
    "Plantillas de Figuras Geométricas",
    """
    Recortar y pegar estas figuras:<br/>
    - Círculo<br/>
    - Cuadrado<br/>
    - Triángulo<br/>
    - Rectángulo<br/>
    """
)

crear_pdf(
    "tarjetas-emociones.pdf",
    "Tarjetas de Emociones",
    """
    Emociones incluidas:<br/>
    😊 Feliz<br/>
    😢 Triste<br/>
    😠 Enojado<br/>
    😨 Asustado<br/>
    🤔 Confundido<br/>
    """
)

print("\n✅ Recursos mock creados exitosamente")