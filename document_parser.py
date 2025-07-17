from docx import Document
import fitz  # PyMuPDF
import pandas as pd
import pytesseract
import cv2
import os

def extraer_preguntas_word(ruta):
    doc = Document(ruta)
    preguntas = []
    buffer = ""
    for para in doc.paragraphs:
        texto = para.text.strip()
        if not texto: continue
        if texto.endswith("?"):
            if buffer:
                preguntas.append({"pregunta": buffer, "respuesta": texto})
                buffer = ""
            else:
                preguntas.append({"pregunta": texto, "respuesta": ""})
        else:
            buffer = texto
    return preguntas

def extraer_preguntas_pdf(ruta):
    doc = fitz.open(ruta)
    texto = "".join([page.get_text() for page in doc])
    return procesar_texto_plano(texto)

def extraer_preguntas_excel(ruta):
    df = pd.read_excel(ruta, header=None)
    preguntas = []
    for row in df.itertuples():
        if isinstance(row[1], str):
            texto = row[1].strip()
            if texto.endswith("?"):
                preguntas.append({"pregunta": texto, "respuesta": ""})
    return preguntas

def extraer_preguntas_imagen(ruta):
    imagen = cv2.imread(ruta)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(gris)
    return procesar_texto_plano(texto)

def procesar_texto_plano(texto):
    preguntas = []
    buffer = ""
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea: continue
        if linea.endswith("?"):
            if buffer:
                preguntas.append({"pregunta": buffer, "respuesta": linea})
                buffer = ""
            else:
                preguntas.append({"pregunta": linea, "respuesta": ""})
        else:
            buffer = linea
    return preguntas

def cargar_documento(ruta):
    ext = os.path.splitext(ruta)[1].lower()
    if ext == ".docx":
        return extraer_preguntas_word(ruta)
    elif ext == ".pdf":
        return extraer_preguntas_pdf(ruta)
    elif ext in [".xls", ".xlsx"]:
        return extraer_preguntas_excel(ruta)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extraer_preguntas_imagen(ruta)
    else:
        raise ValueError("Formato no soportado")
