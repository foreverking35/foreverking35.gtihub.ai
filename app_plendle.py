import streamlit as st
import pandas as pd
import sqlite3

st.title("🛰️ Monitor de Pendle Online")

try:
    # Intentamos leer la base de datos
    conn = sqlite3.connect('pendle_data.db')
    df = pd.read_sql_query("SELECT * FROM precios", conn)
    st.write("Datos capturados:")
    st.line_chart(df['precio'])
    st.dataframe(df)
except:
    st.warning("Esperando datos del capturador... Ejecuta el capturador en tu PC para enviar datos.")
