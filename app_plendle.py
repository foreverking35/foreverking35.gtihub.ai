import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor Pendle Pro", page_icon="📈")

st.title("🛰️ Monitor de Pendle Online (Tiempo Real)")

# Función para obtener datos de internet
def obtener_datos():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=pendle&vs_currencies=usd&include_24hr_change=true"
    try:
        response = requests.get(url)
        data = response.json()
        precio = data['pendle']['usd']
        cambio = data['pendle']['usd_24h_change']
        return precio, cambio
    except:
        return None, None

precio, cambio = obtener_datos()

if precio:
    # Mostrar métricas principales
    col1, col2 = st.columns(2)
    col1.metric("Precio PENDLE", f"${precio} USD")
    col2.metric("Cambio 24h", f"{cambio:.2f}%")

    # Crear un historial simulado (o puedes conectar una DB luego)
    st.info(f"Última actualización: {datetime.now().strftime('%H:%M:%S')}")
    
    # Botón para refrescar
    if st.button('Actualizar Precio Ahora'):
        st.rerun()
else:
    st.error("No se pudo conectar con la fuente de datos. Reintentando...")

st.write("---")
st.caption("Esta app se actualiza sola consultando la API de CoinGecko.")
