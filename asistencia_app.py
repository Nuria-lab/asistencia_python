import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests

st.title("Registro de Asistencia 📋 v1.1")
st.write("Por favor, completá los campos para registrar tu asistencia.")

# Campos para nombre y apellido
nombre = st.text_input("Nombre")
apellido = st.text_input("Apellido")

# Campo para el mail
email = st.text_input("Correo electrónico")

# Campo para la palabra clave
clave = st.text_input("Palabra clave", type="password")
st.caption("🔒 Si tu navegador sugiere guardar la contraseña, ignoralo: este campo no guarda datos de acceso.")

# Opciones de emoji/comentario
opciones_emoji = [
    "🐍 Python power",
    "💻 Full code mode",
    "🔧 Manos al código",
    "⚙️ Ingeniería aplicada",
    "📈 Subiendo nivel",
    "🤖 Pensando en ceros y unos",
    "🚀 ¡A toda velocidad!",
    "🧠 Exprimí el cerebro",
    "😵‍💫 Me quemó la cabeza",
    "🧘 Lo entendí zen",
    "☕ Necesito más café",
    "Otro..."
]
eleccion_emoji = st.selectbox("¿Cómo estuvo la clase?", opciones_emoji)

emoji_extra = ""
if eleccion_emoji == "Otro...":
    emoji_extra = st.text_input("Especificá tu emoji o comentario:")

comentario = emoji_extra if eleccion_emoji == "Otro..." else eleccion_emoji

# 👉 Configuración de Airtable
try:
    AIRTABLE_TOKEN = st.secrets["AIRTABLE_TOKEN"]
    BASE_ID = st.secrets["BASE_ID"]
    TABLE_NAME = st.secrets["TABLE_NAME"]
except:
    from airtable_config import AIRTABLE_TOKEN, BASE_ID, TABLE_NAME

# Botón de envío
if st.button("Registrar asistencia"):
    if nombre and apellido and email and "@" in email:
        now = datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        hora = now.strftime("%H:%M:%S")

        data = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "fecha": fecha,
            "hora": hora,
            "clave": clave,
            "comentario": comentario
        }

        url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
        headers = {
            "Authorization": f"Bearer {AIRTABLE_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "records": [
                {
                    "fields": data
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            st.success("✅ Asistencia registrada correctamente en Airtable")
        else:
            st.error(f"❌ Error al registrar asistencia: {response.status_code} - {response.text}")
    else:
        st.warning("Por favor, completá todos los campos correctamente (nombre, apellido y un correo válido).")
