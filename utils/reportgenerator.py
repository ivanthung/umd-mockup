""" This module contains the logic to generate a PDF report from the data visualizations and tables. """

import base64
from io import BytesIO

import plotly.io as pio
import streamlit as st
import xhtml2pdf.pisa as pisa
from jinja2 import Environment, FileSystemLoader

# This is necessary to render the Plotly figures as SVG images in color as streamlit defaults to B&W.
pio.templates.default = "plotly"


def render_html(text: str, figs_in_base64: dict) -> str:
    """Renders the HTML template with the text and figures provided."""

    figs = [
        f"<h3>{fig_name}</h3> <img src='data:image/svg;base64,{fig_data}' alt='{fig_name}'>"
        for fig_name, fig_data in figs_in_base64.items()
    ]
    figs_html = " ".join(figs)

    file_loader = FileSystemLoader(
        "resources/templates"
    )  # Specify the directory of your templates
    env = Environment(loader=file_loader)
    template = env.get_template("report.html")

    data = {
        "title": "Urban Mining Potential Assessment Report",
        "text": text,
        "figs_html": figs_html,
    }
    return template.render(data)


def transform_fig_to_base64(fig) -> str:
    """Transforms a Plotly figure to a base64 encoded SVG image."""
    img_bytes = BytesIO()
    fig.write_image(img_bytes, format="svg")
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
    return img_base64


def generate_report_pdf(text: str, figs: dict):
    """Generates a PDF report from the text and figures provided and returns the PDF as bytes."""

    figs_in_base64 = {
        fig_name: transform_fig_to_base64(fig_data)
        for fig_name, fig_data in figs.items()
    }
    html = render_html(text, figs_in_base64)
    pdf_output = BytesIO()  # Open a file-like object in memory
    pdf = pisa.CreatePDF(html, dest=pdf_output)

    if not pdf.err:
        pdf_bytes = pdf_output.getvalue()  # Get PDF data as bytes
        pdf_output.close()  # Close in-memory file
        return pdf_bytes
    else:
        st.error("Error generating PDF.")
        return None
