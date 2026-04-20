"""
Tab: PDF Sıkıştır
PDF dosya boyutunu küçültür.
"""

import streamlit as st
from app.file_helpers import save_uploaded_file, download_button
from pdf_engine import compress_pdf


def render():
    st.header("🗜️ PDF Sıkıştır")
    st.markdown("PDF dosya boyutunu küçültün.")

    uploaded = st.file_uploader("PDF dosyası seçin", type=["pdf"], key="compress_upload")

    if not uploaded:
        st.info("Bir PDF dosyası yükleyin.")
        return

    original_size = len(uploaded.getvalue())
    st.info(f"📄 **{uploaded.name}** — {original_size / 1024 / 1024:.2f} MB")

    quality = st.select_slider(
        "Sıkıştırma kalitesi",
        options=["low", "medium", "high"],
        value="medium",
        format_func=lambda x: {"low": "🔴 Düşük (küçük boyut)", "medium": "🟡 Orta", "high": "🟢 Yüksek (büyük boyut)"}[x],
        key="compress_quality",
    )

    if st.button("🗜️ Sıkıştır", key="compress_btn", type="primary"):
        with st.spinner("Sıkıştırılıyor..."):
            path = save_uploaded_file(uploaded)
            try:
                result = compress_pdf(path, quality=quality)
                new_size = result.stat().st_size
                ratio = (1 - new_size / original_size) * 100
                if ratio > 0:
                    st.success(f"Boyut: {original_size/1024/1024:.2f} MB → {new_size/1024/1024:.2f} MB (**%{ratio:.1f} küçüldü**)")
                else:
                    st.warning("Dosya zaten optimize edilmiş, boyut azaltılamadı.")
                download_button(result, "📥 Sıkıştırılmış PDF'i İndir")
            except Exception as e:
                st.error(f"Hata: {e}")
