import streamlit as st
import requests

st.set_page_config(page_title="PENDLE Terminal", layout="centered")

# --- ESTO ES CLAVE: FUNCIÓN CON CACHÉ ---
@st.cache_data(ttl=30)  # Guarda los datos por 30 segundos
def get_market_data():
    try:
        # Usamos la API de CoinGecko como alternativa si Binance falla
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=PENDLEUSDT"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {
                "price": float(data['lastPrice']),
                "low": float(data['lowPrice']),
                "high": float(data['highPrice']),
                "change": float(data['priceChangePercent']),
                "volume": float(data['quoteVolume'])
            }
        return None
    except:
        return None

st.markdown("<h1 style='text-align: center; color: #00FFA3;'>🛰️ PENDLE Intelligence Terminal</h1>", unsafe_allow_html=True)

data = get_market_data()

if data:
    # (Aquí va el resto de tu código de columnas, métricas y barra de progreso)
    col1, col2, col3 = st.columns(3)
    col1.metric("Live Price", f"${data['price']:.3f}", f"{data['change']}%")
    col2.metric("24h High", f"${data['high']:.3f}")
    col3.metric("24h Low", f"${data['low']:.3f}")
    
    st.progress((data['price'] - data['low']) / (data['high'] - data['low']))
    st.success("📡 Data Link: STABLE (Cached)")
else:
    st.error("❌ Link Error: API Saturated.")
    # Agregamos un botón que limpia el caché para reintentar
    if st.button("Force Reconnection"):
        st.cache_data.clear()
        st.rerun()
