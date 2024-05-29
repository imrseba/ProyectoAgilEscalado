from firebase_utils import obtener_sprints_con_hitos
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
from reportlab.platypus import Image, Table, TableStyle
from reportlab.lib import colors

import pandas as pd
import matplotlib.pyplot as plt


def generar_pdf(grupo, fecha, hitos_cumplidos, avance, selected_sprint,grupo_id):
    # Definir la ruta de la imagen
    img_path = "404_Log.png"

    # Crear un buffer temporal para almacenar el PDF
    buffer = tempfile.TemporaryFile()

    # Crear un PDF
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Definir el tamaño deseado para el logo
    logo_width = 115  # Ancho de la imagen del logo en puntos
    logo_height = 47  # Alto de la imagen del logo en puntos

    # Calcular las coordenadas para colocar el logo en la esquina superior derecha
    logo_x = width - logo_width - 50  # Ajustar el margen derecho
    logo_y = height - logo_height - 50  # Ajustar el margen superior

    # Dibujar el logo
    img = Image(img_path, width=logo_width, height=logo_height)
    img.drawOn(c, logo_x, logo_y)

    # Calcular las coordenadas para los textos de grupo, fecha y sprint
    text_x = 100  # Ajustar horizontalmente
    text_y = height - 120  # Ajustar verticalmente

    # Escribir el título del grupo, la fecha y el sprint en negrilla
    c.setFont("Helvetica-Bold", 12)
    c.drawString(text_x, text_y, "Grupo:")
    c.drawString(text_x, text_y - 20, "Fecha:")
    c.drawString(text_x, text_y - 40, "Sprint:")

    # Escribir los valores del grupo, fecha y sprint
    c.setFont("Helvetica", 12)
    c.drawString(text_x + 60, text_y, grupo)
    c.drawString(text_x + 60, text_y - 20, fecha.strftime("%Y-%m-%d"))  # Formatear la fecha como "YYYY-MM-DD"
    c.drawString(text_x + 60, text_y - 40, selected_sprint)

    # Crear una lista de datos para la tabla de hitos
    table_data = [['#', 'Hito', 'Cumplimiento']]

    # Llenar la lista de datos con los hitos, su estado de cumplimiento y enumeración
    for i, (_, hito, cumplido) in enumerate(hitos_cumplidos, start=1):
        estado = "✓" if cumplido else "X"
        table_data.append([str(i), hito, estado])

    # Crear la tabla de hitos
    table = Table(table_data)

    # Estilo para la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Aplicar el estilo a la tabla
    table.setStyle(style)

    # Calcular la posición vertical de la tabla de hitos
    table_y = height - 320  # Ajustar verticalmente

    # Dibujar la tabla en el PDF centrada horizontalmente
    table.wrapOn(c, width, height)
    table.drawOn(c, (width - table._width) / 2, table_y)

    # Escribir la sección de retroalimentación
    c.drawString(text_x, table_y - 100, "Retroalimentación:")
    retro_y = table_y - 120  # Ajustar verticalmente
    y = retro_y - 20
    for line in avance.split('\n'):
        c.drawString(text_x + 20, y, line)
        y -= 20

    line_chart_filename = "line_chart.png"
    draw_line_chart(grupo_id,line_chart_filename)

    # Coordenadas de la posición de la imagen
    image_x = 100
    image_y = 500 # Ajusta esta posición verticalmente para mover la imagen más abajo

    # Obtener la altura de la imagen
    image_height = 300

    # Calcular la posición y donde termina el texto de retroalimentación
    retro_end_y = retro_y - len(avance.split('\n')) * 20

    # Si la imagen sobrepasa el límite de la página actual, cambia a una nueva página
    if image_y - image_height < retro_end_y:
        c.showPage()  # Cambiar a una nueva página
        c.drawImage(line_chart_filename, image_x, 400, width=400, height=300)  # Ajusta la coordenada y según sea necesario
    else:
        c.drawImage(line_chart_filename, image_x, image_y, width=400, height=300)
    
    # Guardar el PDF y volver al inicio del archivo
    c.save()
    buffer.seek(0)
    return buffer


def calcular_porcentaje_cumplimiento_sprint(sprint):
    total_hitos = len(sprint)
    cumplidos = sum(1 for hito, cumplido in sprint if cumplido)
    porcentaje_cumplimiento = (cumplidos / total_hitos) * 100 if total_hitos > 0 else 0
    return porcentaje_cumplimiento



def draw_line_chart(grupo_id, filename):
    # Obtener los datos de los sprints y hitos
    sprints_data = obtener_sprints_con_hitos(grupo_id)
    
    # Calcular el porcentaje de cumplimiento de cada sprint
    porcentajes_cumplimiento = [(sprint[0], calcular_porcentaje_cumplimiento_sprint(sprint[1])) for sprint in sprints_data]
    
    # Separar los nombres de los sprints y los porcentajes de cumplimiento
    nombres_sprints = [sprint[0] for sprint in porcentajes_cumplimiento]
    porcentajes = [porcentaje[1] for porcentaje in porcentajes_cumplimiento]
    
    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.bar(nombres_sprints, porcentajes, color='skyblue')
    plt.xlabel('Sprints')
    plt.ylabel('Porcentaje de Cumplimiento')
    plt.title('Porcentaje de Cumplimiento por Sprint')
    plt.xticks(rotation=45, ha='right')
    
    # Guardar el gráfico en un archivo
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()