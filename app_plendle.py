import streamlit as st
import requests

st.title("🛰️ Monitor de Pendle Online")

def traer_precio():
    # INTENTO 1: CoinGecko
    try:
        url_cg = "https://api.coingecko.com/api/v3/simple/price?ids=pendle&vs_currencies=usd"
        r = requests.get(url_cg, timeout=5)
        return r.json()['pendle']['usd'], "CoinGecko"
    except:
        # INTENTO 2: Binance (Si el primero falla)
        try:
            url_binance = "https://api.binance.com/api/v3/ticker/price?symbol=PENDLEUSDT"
            r = requests.get(url_binance, timeout=5)
            return float(r.json()['price']), "Binance"
        except:
            return None, None

# ... (aquí va tu código anterior de import y st.title)

def obtener_datos_avanzados():
    try:
        # 1. Pedimos el resumen de 24 horas a Binance
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=PENDLEUSDT"
        r = requests.get(url, timeout=5).json()
        
        datos = {
            "actual": float(r['lastPrice']),
            "minimo_24h": float(r['lowPrice']),  # Este es el "Piso" de hoy
            "cambio_porcentaje": float(r['priceChangePercent']),
            "volumen": float(r['quoteVolume'])
        }
        return datos
    except:
        return None

# Ejecutamos la función
d = obtener_datos_avanzados()

if d:
    # FILA DE MÉTRICAS
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Precio Actual", f"${d['actual']} USD", f"{d['cambio_porcentaje']}%")
    
    with col2:
        # Mostramos el piso (mínimo de 24h)
        st.metric("Piso (24h Low)", f"${d['minimo_24h']} USD")

    # LÓGICA DE INGENIERÍA: Detección de rebote
    # Si el precio actual está cerca (1%) del mínimo, es zona de rebote
    distancia_al_piso = ((d['actual'] - d['minimo_24h']) / d['minimo_24h']) * 100
    
    if distancia_al_piso < 1.0:
        st.warning(f"⚠️ ATENCIÓN: Precio muy cerca del piso técnico (${d['minimo_24h']}). Posible zona de rebote.")
    else:
        st.success(f"✅ El precio está un {distancia_al_piso:.2f}% por encima del piso de hoy.")

else:
    st.error("No se pudieron conectar los sensores de datos.")
