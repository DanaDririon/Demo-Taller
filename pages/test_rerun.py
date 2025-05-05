import streamlit as st
import pandas as pd
from control_taller import utils as ct
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Datos de ejemplo
datos_ot_cotiz = {
    'tipo_documento': 'valor_tipo_documento',
    'responsable': 'Juan Pérez',
    'descripcion': 'Mantenimiento general de equipos',
    'tareas': [
        {'actividad': 'Revisión de motor', 'tiempo': '2 horas'},
        {'actividad': 'Cambio de aceite', 'tiempo': '30 minutos'}
    ]
}

# Cargar plantilla
env = Environment(loader=FileSystemLoader(['/templates/']))
template = env.get_template('template_cotizacion_ot.html')
html_rendered = template.render(**datos_ot_cotiz)
html_rendered = template.render()

# Generar PDF
HTML(string=html_rendered, base_url='.').write_pdf('C:\\Users\\EladioNB\\OneDrive\\Documents\\GitHub\\Demo-Taller\\template_cotizacion_2.pdf')
