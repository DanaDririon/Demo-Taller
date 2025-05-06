import streamlit as st
from control_taller import utils as ct
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def generador_pdf(template: None | str, datos: None | dict) -> bytes:
    """
    Genera un PDF a partir de una plantilla HTML y datos proporcionados.

    Args:
        template (str): Nombre de la plantilla HTML.
        datos (dict): Datos para renderizar la plantilla.

    Returns:
        None
    """
    # Cargar plantilla
    env = Environment(loader=FileSystemLoader(['./templates']))
    template = env.get_template(template)
    # Renderizar HTML
    html_rendered = template.render(**datos)
    
    # Generar PDF
    pdf = HTML(string=html_rendered, base_url='.').write_pdf()
    return pdf

