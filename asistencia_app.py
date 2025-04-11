import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.title("Registro de Asistencia 📋")

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
    "🐍 Python power",               # clásico
    "💻 Full code mode",            # programando a full
    "🔧 Manos al código",           # hands-on
    "⚙️ Ingeniería aplicada",       # el clásico engranaje
    "📈 Subiendo nivel",            # progreso, entendimiento
    "🤖 Pensando en ceros y unos",  # modo robot activado
    "🚀 ¡A toda velocidad!",        # todo claro y rápido
    "🧠 Exprimí el cerebro",        # difícil pero bien
    "😵‍💫 Me quemó la cabeza",     # colapso técnico
    "🧘 Lo entendí zen",            # paz mental con el código
    "☕ Necesito más café",         # siempre necesario
    "Otro..."                       # para personalizar
]
eleccion_emoji = st.selectbox("¿Cómo estuvo la clase?", opciones_emoji)

emoji_extra = ""
if eleccion_emoji == "Otro...":
    emoji_extra = st.text_input("Especificá tu emoji o comentario:")

# Determinar comentario final
comentario = emoji_extra if eleccion_emoji == "Otro..." else eleccion_emoji


import streamlit as st

# Intentar importar desde secrets (Streamlit Cloud)
try:
    AIRTABLE_TOKEN = st.secrets["AIRTABLE_TOKEN"]
    BASE_ID = st.secrets["BASE_ID"]
    TABLE_NAME = st.secrets["TABLE_NAME"]
except:
    # Si no está en secrets, usa archivo local (para testing)
    from airtable_config import AIRTABLE_TOKEN, BASE_ID, TABLE_NAME


# Botón de envío
if st.button("Registrar asistencia"):
    if nombre and apellido and email and "@" in email:
        now = datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        hora = now.strftime("%H:%M:%S")

        # 👉 Aquí se arman los datos a guardar
        data = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "fecha": fecha,
            "hora": hora,
            "clave": clave,
            "comentario": comentario
        }

        # 👉 Y acá se envía a Airtable
        import requests

        url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
        headers = {
            "Authorization": f"Bearer {AIRTABLE_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json={"fields": data})

        if response.status_code == 200 or response.status_code == 201:
            st.success("✅ Asistencia registrada correctamente")
        else:
            st.error(f"❌ Error al registrar asistencia: {response.status_code} - {response.text}")


        st.success("✅ Asistencia registrada correctamente")
    else:
        st.warning("Por favor, completá todos los campos correctamente (nombre, apellido y un correo válido).")
