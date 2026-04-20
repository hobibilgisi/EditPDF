"""
EditPDF — Streamlit Giriş Noktası
Kullanım: streamlit run app.py
"""

import time
import os
import base64
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
            top: 0; left: 0;
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
            <img src="data:image/webp;base64,{_gif_b64}" alt="EditPDF">
            <div class="splash-ver">v{APP_VERSION_FULL}</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

# ── Tab Modülleri ──────────────────────────────────────────────
from app.tabs import tab_merge, tab_split, tab_compress, tab_encrypt, tab_convert, tab_watermark, tab_pages

# ── Tema Yönetimi ──────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "light"

is_dark = st.session_state.theme == "dark"


def get_css(dark: bool) -> str:
    if dark:
        bg_app        = "#0f172a"
        bg_card       = "#1e293b"
        bg_input      = "#1e293b"
        bg_tab_list   = "#1e293b"
        bg_tab_hover  = "#0f172a"
        bg_radio      = "#1e293b"
        bg_expander   = "#1e293b"
        text_primary  = "#f1f5f9"
        text_secondary= "#94a3b8"
        text_label    = "#cbd5e1"
        border        = "#334155"
        border_accent = "#4f46e5"
        accent_a      = "#818cf8"
        accent_b      = "#60a5fa"
        tab_text      = "#94a3b8"
        sel_shadow    = "rgba(129,140,248,0.45)"
        btn_shadow    = "rgba(129,140,248,0.35)"
        dl_a          = "#34d399"
        dl_b          = "#10b981"
        dl_shadow     = "rgba(52,211,153,0.3)"
        divider       = "#334155"
        footer_border = "#1e293b"
        subtitle_col  = "#64748b"
        alert_bg      = "#162032"
    else:
        bg_app        = "#f1f5f9"
        bg_card       = "#ffffff"
        bg_input      = "#ffffff"
        bg_tab_list   = "#ffffff"
        bg_tab_hover  = "#f1f5f9"
        bg_radio      = "#ffffff"
        bg_expander   = "#ffffff"
        text_primary  = "#1e293b"
        text_secondary= "#64748b"
        text_label    = "#374151"
        border        = "#e2e8f0"
        border_accent = "#c7d2fe"
        accent_a      = "#6366f1"
        accent_b      = "#3b82f6"
        tab_text      = "#64748b"
        sel_shadow    = "rgba(99,102,241,0.35)"
        btn_shadow    = "rgba(99,102,241,0.3)"
        dl_a          = "#10b981"
        dl_b          = "#059669"
        dl_shadow     = "rgba(16,185,129,0.3)"
        divider       = "#e2e8f0"
        footer_border = "#e2e8f0"
        subtitle_col  = "#94a3b8"
        alert_bg      = "#f8fafc"

    return f"""
<style>
/* ─── Temel ──────────────────────────────────────────────────── */
html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
}}

/* ─── Arka plan ve konteyner ────────────────────────────────── */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.stApp {{
    background: {bg_app} !important;
}}
[data-testid="stHeader"] {{
    background: {bg_app} !important;
    border-bottom: 1px solid {border};
}}
.main .block-container {{
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1020px;
}}

/* ─── Genel metin rengi ──────────────────────────────────────── */
p, span, li, div, h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stText"] {{
    color: {text_primary} !important;
}}

/* ─── Başlık alanı ───────────────────────────────────────────── */
.app-header h1 {{
    background: linear-gradient(90deg, {accent_a}, {accent_b});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    font-size: 2rem;
    letter-spacing: -0.5px;
    margin: 0;
}}
.app-subtitle {{
    color: {subtitle_col} !important;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}}

/* ─── Tabs ───────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    background: {bg_tab_list};
    border-radius: 14px;
    padding: 5px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.1);
    gap: 3px;
    flex-wrap: wrap;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px;
    font-weight: 500;
    font-size: 0.88rem;
    color: {tab_text} !important;
    padding: 0.45rem 1rem;
    transition: background 0.15s, color 0.15s;
}}
.stTabs [data-baseweb="tab"]:hover {{
    background: {bg_tab_hover};
    color: {text_primary} !important;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {accent_a} 0%, {accent_b} 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 3px 10px {sel_shadow};
}}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {{
    display: none;
}}

/* ─── Birincil Buton ─────────────────────────────────────────── */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {{
    background: linear-gradient(135deg, {accent_a} 0%, {accent_b} 100%);
    border: none;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.55rem 1.6rem;
    transition: opacity 0.2s, transform 0.12s, box-shadow 0.2s;
    box-shadow: 0 4px 14px {btn_shadow};
    color: #ffffff !important;
}}
.stButton > button[kind="primary"]:hover {{
    opacity: 0.92;
    transform: translateY(-1px);
    box-shadow: 0 6px 18px {btn_shadow};
}}
.stButton > button[kind="primary"]:active {{
    transform: translateY(0);
}}

/* ─── İkincil Buton ─────────────────────────────────────────── */
.stButton > button[kind="secondary"] {{
    border-radius: 10px;
    font-weight: 500;
    border: 1.5px solid {border_accent};
    color: {accent_a} !important;
    background: transparent;
    transition: background 0.15s, border-color 0.15s;
}}
.stButton > button[kind="secondary"]:hover {{
    background: {bg_tab_hover};
    border-color: {accent_a};
}}

/* ─── İndirme Butonu ─────────────────────────────────────────── */
.stDownloadButton > button {{
    background: linear-gradient(135deg, {dl_a} 0%, {dl_b} 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.55rem 1.6rem;
    transition: opacity 0.2s, transform 0.12s;
    box-shadow: 0 4px 14px {dl_shadow};
}}
.stDownloadButton > button:hover {{
    opacity: 0.92;
    transform: translateY(-1px);
}}

/* ─── Tema Butonu ────────────────────────────────────────────── */
.theme-toggle-btn .stButton > button {{
    background: transparent !important;
    border: 1.5px solid {border} !important;
    border-radius: 10px;
    color: {text_secondary} !important;
    font-size: 1.1rem;
    padding: 0.35rem 0.75rem;
    box-shadow: none !important;
    transition: border-color 0.15s, background 0.15s;
    min-height: auto;
}}
.theme-toggle-btn .stButton > button:hover {{
    border-color: {accent_a} !important;
    background: {bg_tab_hover} !important;
    color: {accent_a} !important;
    transform: none;
}}

/* ─── Dosya Yükleyici ────────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {{
    background: {bg_card};
    border: 2px dashed {border_accent};
    border-radius: 14px;
    transition: border-color 0.2s, background 0.2s;
}}
[data-testid="stFileUploaderDropzone"]:hover {{
    border-color: {accent_a};
}}
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] label {{
    color: {text_secondary} !important;
}}

/* ─── Input, Select, Textarea ───────────────────────────────── */
input[type="text"], input[type="password"], textarea,
[data-testid="stTextInput"] input,
[data-testid="stPasswordInput"] input,
[data-baseweb="select"] div,
[data-baseweb="input"] input {{
    background: {bg_input} !important;
    color: {text_primary} !important;
    border-color: {border} !important;
    border-radius: 8px !important;
}}
[data-baseweb="select"] svg {{
    fill: {text_secondary} !important;
}}

/* ─── Bildirim Kutuları ──────────────────────────────────────── */
[data-testid="stAlert"] {{
    background: {alert_bg} !important;
    border-radius: 10px;
    border-left-width: 4px;
    color: {text_primary} !important;
}}
[data-testid="stAlert"] p {{
    color: {text_primary} !important;
}}

/* ─── Radio ──────────────────────────────────────────────────── */
.stRadio > div {{
    background: {bg_radio};
    border-radius: 10px;
    padding: 0.5rem 0.75rem;
}}
.stRadio label span {{
    color: {text_primary} !important;
}}

/* ─── Slider ─────────────────────────────────────────────────── */
[data-baseweb="slider"] [data-testid="stThumbValue"] {{
    color: {text_primary} !important;
}}
[data-baseweb="slider"] div[data-testid="stSliderTickBarMin"],
[data-baseweb="slider"] div[data-testid="stSliderTickBarMax"] {{
    color: {text_secondary} !important;
}}

/* ─── Etiket / Label ─────────────────────────────────────────── */
label[data-testid="stWidgetLabel"] p,
.stSelectSlider label p {{
    font-weight: 500;
    color: {text_label} !important;
}}

/* ─── Genişletilebilir Panel ─────────────────────────────────── */
[data-testid="stExpander"] details {{
    background: {bg_expander};
    border-radius: 12px;
    border: 1px solid {border} !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}}
[data-testid="stExpander"] summary {{
    color: {text_primary} !important;
}}

/* ─── Divider ───────────────────────────────────────────────── */
hr {{
    border-color: {divider};
    margin: 1.5rem 0;
}}

/* ─── Footer ve Toolbar gizle ───────────────────────────────── */
[data-testid="stToolbar"], #MainMenu, footer {{
    display: none !important;
}}

/* ─── Özel Footer ───────────────────────────────────────────── */
.editpdf-footer {{
    text-align: center;
    color: {subtitle_col};
    font-size: 12px;
    margin-top: 2.5rem;
    padding: 1rem 0 0.5rem;
    border-top: 1px solid {footer_border};
}}
.editpdf-footer strong {{
    color: {accent_a};
}}

/* ─── App başlık satırı ─────────────────────────────────────── */
.app-header {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.25rem;
}}
</style>
"""


# ── CSS Enjeksiyonu ────────────────────────────────────────────
st.markdown(get_css(is_dark), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ── Başlık Satırı ─────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════
col_title, col_toggle = st.columns([10, 1])

with col_title:
    st.markdown(f"""
    <div class="app-header">
        <span style="font-size:1.9rem">📄</span>
        <h1>{APP_NAME}</h1>
    </div>
    <p class="app-subtitle">PDF işlemleri için web uygulaması &nbsp;·&nbsp; v{APP_VERSION_FULL} &nbsp;·&nbsp; {APP_VERSION_DATE}</p>
    """, unsafe_allow_html=True)

with col_toggle:
    st.markdown('<div class="theme-toggle-btn">', unsafe_allow_html=True)
    toggle_icon = "☀️" if is_dark else "🌙"
    if st.button(toggle_icon, key="theme_toggle", help="Tema değiştir"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

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
with st.expander(f"📋 Güncelleme Notları — v{APP_VERSION_FULL}"):
    for note in APP_VERSION_NOTES:
        st.markdown(f"- {note}")

st.markdown(f"""
<div class="editpdf-footer">
    <strong>EditPDF</strong> · v{APP_VERSION_FULL} · {APP_VERSION_DATE}
</div>
""", unsafe_allow_html=True)
