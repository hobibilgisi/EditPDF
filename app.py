"""
PDFToolKit Web — Streamlit Giriş Noktası

Bu dosya uygulamayı başlatır.
Kullanım: streamlit run app.py
"""

import time
import streamlit as st

from app.config import (
    APP_NAME, APP_ICON, APP_VERSION_FULL, APP_VERSION_DATE, APP_VERSION_NOTES,
)

# ── Sayfa Ayarları ─────────────────────────────────────────────
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Açılış Animasyonu (Splash Screen) ─────────────────────────
# ALTINS1'deki kanıtlanmış splash yapısıyla aynı.
import os, base64
from streamlit_autorefresh import st_autorefresh

if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False
    st.session_state.splash_start = time.time()

if not st.session_state.splash_shown:
    _elapsed = time.time() - st.session_state.splash_start
    if _elapsed >= 5.0:
        st.session_state.splash_shown = True
        st.rerun()
    else:
        st_autorefresh(interval=500, key="splash_autorefresh")
        _splash_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "splash_logo_transparent.webp")
        with open(_splash_path, "rb") as _f:
            _gif_b64 = base64.b64encode(_f.read()).decode()
        st.markdown(f"""
        <style>
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: #1a1a2e !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        [data-testid="stHeader"],
        [data-testid="stSidebar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="stToolbar"],
        #MainMenu, footer {{
            display: none !important;
        }}
        .stMainBlockContainer, .block-container {{
            padding: 0 !important;
            max-width: 100vw !important;
        }}
        .splash-wrapper {{
            display: flex;
            flex-direction: column;
            width: 100vw;
            height: 100vh;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            position: fixed;
            top: 0;
            left: 0;
            z-index: 9999;
        }}
        .splash-wrapper img {{
            max-width: 60vw;
            max-height: 60vh;
            object-fit: contain;
        }}
        .splash-ver {{
            margin-top: 20px;
            color: rgba(255,255,255,.3);
            font-size: 13px;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }}
        </style>
        <div class="splash-wrapper">
            <img src="data:image/webp;base64,{_gif_b64}" alt="PDFToolKit">
            <div class="splash-ver">v{APP_VERSION_FULL}</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

# ── Tab Modülleri ──────────────────────────────────────────────
from app.tabs import tab_merge, tab_split, tab_compress, tab_encrypt, tab_convert, tab_watermark, tab_pages

# ══════════════════════════════════════════════════════════════
# ── Ana Uygulama ──────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════

st.title(f"{APP_ICON} {APP_NAME}")
st.caption(f"v{APP_VERSION_FULL}")

# ── Tab Arayüzü ───────────────────────────────────────────────
tabs = st.tabs([
    "📎 Birleştir",
    "✂️ Böl",
    "🗜️ Sıkıştır",
    "🔒 Şifrele",
    "🔄 Dönüştür",
    "💧 Filigran",
    "📑 Sayfa Yönetimi",
])

with tabs[0]:
    tab_merge.render()
with tabs[1]:
    tab_split.render()
with tabs[2]:
    tab_compress.render()
with tabs[3]:
    tab_encrypt.render()
with tabs[4]:
    tab_convert.render()
with tabs[5]:
    tab_watermark.render()
with tabs[6]:
    tab_pages.render()

# ── Footer ─────────────────────────────────────────────────────
st.markdown("---")
with st.expander(f"📋 Güncelleme Notları — v{APP_VERSION_FULL}"):
    for note in APP_VERSION_NOTES:
        st.markdown(f"- {note}")
