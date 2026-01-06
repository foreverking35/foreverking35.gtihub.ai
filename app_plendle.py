import streamlit as st
import requests

st.set_page_config(page_title="Pendle Data Engine", page_icon="🛰️")

st.title("🛰️ Pendle Market Intelligence")
st.markdown("---")

def obtener_datos():
    # Intentamos con la API de Binance (más robusta para ingenieros)
    try:
        # Añadimos un 'header' para que la API no nos bloquee pensando que somos un robot
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=PENDLEUSDT"
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # Verificamos si la respuesta es exitosa (código 200)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        # Esto nos permite ver el error exacto en la consola si algo falla
        print(f"Error de conexión: {e}")
        return None

# Procesamiento de Datos (Data Processing Layer)
datos = obtener_datos()

if datos:
    # Transformamos los textos en números (Ingeniería de Datos)
    actual = float(datos['lastPrice'])
    piso = float(datos['lowPrice'])
    cambio = float(datos['priceChangePercent'])
    
    # Visualización
    col1, col2 = st.columns(2)
    col1.metric("PRECIO ACTUAL", f"${actual:.3f} USD", f"{cambio}%")
    col2.metric("PISO DE HOY (24h Low)", f"${piso:.3f} USD")
    
    # Lógica de soporte (Piso)
    distancia = ((actual - piso) / piso) * 100
    
    if distancia < 1.0:
        st.warning(f"🚨 ALERTA: Estamos a solo {distancia:.2f}% del piso (${piso}). ¡Zona de rebote probable!")
    else:
        st.info(f"ℹ️ El precio está {distancia:.2f}% por encima del piso más cercano.")
        
    st.success("📡 Sensores conectados y recibiendo datos de Binance.")
else:
    # Si falla, mostramos este botón para forzar el reintento
    st.error("❌ Error de enlace: La API está saturada o no responde.")
    if st.button('🔄 Re-conectar Sensores'):
        st.rerun()

st.markdown("---")
st.caption("Arquitectura de Datos: Python + Streamlit Cloud + Binance API")




  
