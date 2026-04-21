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

/* ─── Arka plan ──────────────────────────────────────────────── */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.stApp {{
    background: {bg_app} !important;
}}
[data-testid="stHeader"] {{
    display: none !important;
}}
.main .block-container {{
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1020px;
    margin-left: auto;
    margin-right: auto;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    box-sizing: border-box;
    transition: padding-top 0.35s ease;
}}
body.ep-scrolled .main .block-container {{
    padding-top: 84px;
}}

/* ─── Hero (büyük başlık, içerik akışında) ───────────────────── */
.editpdf-hero {{
    text-align: center;
    padding: 2.5rem 0 1rem;
    max-height: 250px;
    overflow: hidden;
    transition: opacity 0.38s ease, transform 0.38s ease, max-height 0.45s ease, padding 0.38s ease;
}}
body.ep-scrolled .editpdf-hero {{
    opacity: 0;
    transform: translateY(-12px);
    pointer-events: none;
    max-height: 0;
    padding: 0;
}}

/* ─── Sabit Topbar (scroll'da belirir) ───────────────────────── */
.editpdf-topbar {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 64px;
    z-index: 9997;
    background: {bg_app};
    border-bottom: 1px solid {border};
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    transform: translateY(-100%);
    opacity: 0;
    transition: transform 0.38s cubic-bezier(.4,0,.2,1), opacity 0.3s ease;
}}
body.ep-scrolled .editpdf-topbar {{
    transform: translateY(0);
    opacity: 1;
}}
.topbar-title {{
    font-size: 1.7rem;
    font-weight: 900;
    letter-spacing: -0.5px;
    line-height: 1;
    margin: 0;
}}
.topbar-title .part-edit {{
    background: linear-gradient(90deg, {accent_a}, {accent_b});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.topbar-title .part-pdf {{
    color: #cc2222;
    -webkit-text-fill-color: #cc2222;
}}
.topbar-subtitle {{
    font-size: 0.72rem;
    color: {subtitle_col};
    margin: 0;
    font-weight: 400;
    letter-spacing: 0.3px;
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
    border-radius: 16px;
    padding: 6px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    gap: 4px;
    flex-wrap: wrap;
    border: 1px solid {border};
    justify-content: center;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 12px;
    font-weight: 600;
    font-size: 0.82rem;
    color: {tab_text} !important;
    padding: 0.5rem 1.1rem;
    transition: background 0.18s, color 0.18s, box-shadow 0.18s;
    letter-spacing: 0.1px;
    border: 1px solid transparent;
}}
.stTabs [data-baseweb="tab"]:hover {{
    background: {bg_tab_hover};
    color: {accent_a} !important;
    border-color: {border_accent};
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {accent_a} 0%, {accent_b} 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px {sel_shadow};
    border-color: transparent !important;
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

/* ─── Tema Butonu (JS ile tab satırına hizalanır) ───────────── */
.theme-toggle-btn {{
    position: fixed !important;
    right: 18px;
    z-index: 9998;
    transition: top 0.15s ease;
}}
.theme-toggle-btn > button {{
    background: {bg_card} !important;
    border: 1.5px solid {border} !important;
    border-radius: 10px;
    color: {text_secondary} !important;
    font-size: 1.1rem;
    padding: 0.35rem 0.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    transition: border-color 0.15s, background 0.15s;
    min-height: auto;
}}
.theme-toggle-btn > button:hover {{
    border-color: {accent_a} !important;
    background: {bg_tab_hover} !important;
    color: {accent_a} !important;
    transform: none;
}}

/* Tema butonunu içeren satırı sıfırla (buton JS ile fixed olacak) */
[data-testid="stHorizontalBlock"]:has(button[title="Tema değiştir"]) {{
    height: 0 !important;
    min-height: 0 !important;
    overflow: visible !important;
    margin: 0 !important;
    padding: 0 !important;
}}
[data-testid="stHorizontalBlock"]:has(button[title="Tema değiştir"]) > div {{
    height: 0 !important;
    min-height: 0 !important;
    overflow: visible !important;
    padding: 0 !important;
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

/* ─── Streamlit geniş layout mobil düzeltmesi ───────────────── */
section[data-testid="stMain"] > div {{
    padding-left: 0 !important;
    padding-right: 0 !important;
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

/* ─── Responsive ────────────────────────────────────────────── */

/* Hero başlık stilleri */
.hero-title {{
    font-size: 3.5rem;
    font-weight: 900;
    letter-spacing: -1.5px;
    line-height: 1;
    margin: 0 0 0.4rem;
}}
.hero-title .part-edit {{
    background: linear-gradient(90deg, {accent_a}, {accent_b});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.hero-title .part-pdf {{
    color: #cc2222;
    -webkit-text-fill-color: #cc2222;
}}
.hero-subtitle {{
    font-size: 0.9rem;
    color: {subtitle_col};
    margin: 0;
    font-weight: 400;
    letter-spacing: 0.2px;
}}

/* Tablet (≤900px) */
@media (max-width: 900px) {{
    .main .block-container {{
        padding-left: 1rem;
        padding-right: 1rem;
    }}
    .hero-title {{ font-size: 2.8rem; }}
    .topbar-title {{ font-size: 1.4rem; }}
    .stTabs [data-baseweb="tab"] {{
        padding: 0.45rem 0.85rem;
        font-size: 0.8rem;
    }}
}}

/* Mobil (≤640px) */
@media (max-width: 640px) {{
    .main .block-container {{
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }}
    body.ep-scrolled .main .block-container {{
        padding-top: 72px;
    }}
    .editpdf-topbar {{ height: 56px; }}
    .hero-title {{ font-size: 2.2rem; letter-spacing: -1px; }}
    .topbar-title {{ font-size: 1.2rem; }}
    .topbar-subtitle {{ font-size: 0.65rem; }}
    .stTabs [data-baseweb="tab-list"] {{
        border-radius: 12px;
        padding: 4px;
        gap: 3px;
    }}
    .stTabs [data-baseweb="tab"] {{
        padding: 0.4rem 0.65rem;
        font-size: 0.75rem;
        border-radius: 9px;
    }}
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {{
        width: 100%;
        justify-content: center;
    }}
    .stDownloadButton > button {{
        width: 100%;
    }}
    [data-testid="stFileUploaderDropzone"] {{
        border-radius: 10px;
    }}
    [data-testid="stExpander"] details {{
        border-radius: 10px;
    }}
    .editpdf-footer {{
        font-size: 11px;
    }}
    /* Kolon layout'u mobilde dikey stack */
    [data-testid="stHorizontalBlock"] {{
        flex-wrap: wrap;
    }}
    [data-testid="stHorizontalBlock"] > [data-testid="stVerticalBlock"] {{
        min-width: 100% !important;
        width: 100% !important;
        flex: 1 1 100% !important;
    }}
}}

/* Küçük mobil (≤400px) */
@media (max-width: 400px) {{
    .topbar-title {{
        font-size: 1.2rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        padding: 0.35rem 0.5rem;
        font-size: 0.7rem;
    }}
}}
</style>
"""


# ── CSS Enjeksiyonu ────────────────────────────────────────────
st.markdown(get_css(is_dark), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ── Başlık Satırı ─────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════
# ── Scroll JS: hero→topbar animasyonu + tema butonu tab satırına hizalama ──
st.markdown("""
<script>
(function() {
    var SCROLL_T = 80;

    function getScrollY() {
        // Streamlit'te window.scrollY her zaman 0'dır;
        // gerçek scroll stAppViewContainer üzerinde olur.
        var c = document.querySelector('[data-testid="stAppViewContainer"]');
        if (c) return c.scrollTop;
        var m = document.querySelector('.main');
        if (m) return m.scrollTop;
        return window.pageYOffset || 0;
    }

    function findThemeBtn() {
        // title attribute ile dene (bazı Streamlit sürümlerinde help=title olur)
        var b = document.querySelector('button[title="Tema değiştir"]');
        if (b) return b;
        // emoji içeriğiyle bul (daha evrensel yöntem)
        var all = document.querySelectorAll('button');
        for (var i = 0; i < all.length; i++) {
            var t = all[i].textContent.trim();
            if (t === '🌙' || t === '☀️') return all[i];
        }
        return null;
    }

    function alignThemeBtn() {
        var btn = findThemeBtn();
        if (!btn) return;
        // .stButton wrapper'ına class ekle (CSS styling için)
        var wrap = btn.closest('.stButton');
        if (wrap && !wrap.classList.contains('theme-toggle-btn')) {
            wrap.classList.add('theme-toggle-btn');
        }
        // Tab listesinin konumuna hizala
        var tabs = document.querySelector('[data-baseweb="tab-list"]');
        if (!tabs || !wrap) return;
        var r = tabs.getBoundingClientRect();
        var top = Math.max(8, r.top + Math.round((r.height - 36) / 2));
        wrap.style.top = top + 'px';
    }

    function tick() {
        document.body.classList.toggle('ep-scrolled', getScrollY() > SCROLL_T);
        alignThemeBtn();
    }

    function bindScroll() {
        var c = document.querySelector('[data-testid="stAppViewContainer"]');
        if (c && !c._epBound) {
            c.addEventListener('scroll', tick, {passive: true});
            c._epBound = true;
        }
    }

    // 200ms interval: scroll değişikliklerini ve Streamlit re-render'larını yakala
    setInterval(function() { bindScroll(); tick(); }, 200);
    bindScroll();
    tick();
})();
</script>
""", unsafe_allow_html=True)

# ── Sabit Topbar (scroll'da belirir) ──────────────────────────
st.markdown(f"""
<div class="editpdf-topbar">
    <div class="topbar-title">
        <span class="part-edit">Edit</span><span class="part-pdf">PDF</span>
    </div>
    <p class="topbar-subtitle">PDF araç kutusu</p>
</div>
""", unsafe_allow_html=True)

# ── Hero (büyük başlık, sayfa açılışında) ─────────────────────
st.markdown(f"""
<div class="editpdf-hero">
    <div class="hero-title">
        <span class="part-edit">Edit</span><span class="part-pdf">PDF</span>
    </div>
    <p class="hero-subtitle">PDF araç kutusu</p>
</div>
""", unsafe_allow_html=True)

# ── Tema butonu (JS .stButton wrapper'ını bularak fixed konuma alır) ──
_, _col_btn = st.columns([14, 1])
with _col_btn:
    toggle_icon = "☀️" if is_dark else "🌙"
    if st.button(toggle_icon, key="theme_toggle", help="Tema değiştir"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

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
