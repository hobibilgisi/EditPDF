"""
Tab: Filigran (Watermark)
PDF'e şeffaf metin filigranı ekler.
"""

import streamlit as st
from app.file_helpers import save_uploaded_file, download_button
from pdf_engine import add_watermark


def render():
    st.header("💧 Filigran Ekle")
    st.markdown("PDF sayfalarına şeffaf metin filigranı ekleyin.")

    uploaded = st.file_uploader("PDF dosyası seçin", type=["pdf"], key="watermark_upload")

    if not uploaded:
        st.info("Bir PDF dosyası yükleyin.")
        return

    col1, col2 = st.columns(2)
    with col1:
        text = st.text_input("Filigran metni", value="TASLAK", key="wm_text")
        font_size = st.slider("Yazı boyutu", 20, 120, 60, key="wm_fontsize")
    with col2:
        opacity = st.slider("Şeffaflık", 0.05, 0.8, 0.3, step=0.05, key="wm_opacity")
        angle = st.slider("Açı (derece)", 0, 90, 45, key="wm_angle")

    if text and st.button("💧 Filigran Ekle", key="watermark_btn", type="primary"):
        path = save_uploaded_file(uploaded)
        with st.spinner("Filigran ekleniyor..."):
            try:
                result = add_watermark(
                    path, text,
                    font_size=font_size,
                    opacity=opacity,
                    angle=angle,
                )
                st.success("Filigran eklendi!")
                download_button(result, "📥 Filigranlı PDF'i İndir")
            except Exception as e:
                st.error(f"Hata: {e}")
