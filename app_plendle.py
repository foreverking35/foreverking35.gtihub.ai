import streamlit as st
import pandas as pd
import requests

st.title("🛰️ Monitor de Pendle Online")

# Función para traer el precio de internet
def traer_precio():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=pendle&vs_currencies=usd"
        r = requests.get(url)
        return r.json()['pendle']['usd']
    except:
        return "Error al conectar"

precio = traer_precio()

if precio != "Error al conectar":
    st.metric("Precio actual de PENDLE", f"${precio} USD")
    st.success("¡Datos obtenidos directamente de internet!")
else:
    st.error("No se pudo obtener el precio.")
