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

precio, fuente = traer_precio()

if precio:
    st.metric("Precio actual de PENDLE", f"${precio} USD")
    st.caption(f"Fuente de datos: {fuente}")
    st.success("Conexión estable")
else:
    st.error("⚠️ Todas las fuentes de datos están saturadas. Por favor, refresca en 1 minuto.")
    if st.button('Reintentar ahora'):
        st.rerun()
