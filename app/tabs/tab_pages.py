"""
Tab: Sayfa Yönetimi
Sayfa silme, döndürme ve meta bilgi görüntüleme.
"""

import streamlit as st
from app.file_helpers import save_uploaded_file, download_button
from pdf_engine import (
    delete_pages, rotate_pages, get_page_count,
    get_metadata, parse_page_input,
)


def render():
    st.header("📑 Sayfa Yönetimi & Bilgi")

    uploaded = st.file_uploader("PDF dosyası seçin", type=["pdf"], key="pages_upload")

    if not uploaded:
        st.info("Bir PDF dosyası yükleyin.")
        return

    path = save_uploaded_file(uploaded)
    total = get_page_count(path)

    # ── Meta bilgi ─────────────────────────────────────────────
    with st.expander("ℹ️ PDF Bilgileri", expanded=False):
        meta = get_metadata(path)
        for k, v in meta.items():
            st.text(f"{k}: {v}")

    st.divider()

    # ── İşlem seçimi ───────────────────────────────────────────
    operation = st.radio(
        "İşlem",
        ["Sayfa Sil", "Sayfa Döndür"],
        key="page_op",
        horizontal=True,
    )

    page_input = st.text_input(
        "Sayfa numaraları",
        placeholder=f"Örn: 1-3,5  (toplam {total} sayfa)",
        key="page_input",
    )

    if not page_input:
        return

    if operation == "Sayfa Sil":
        if st.button("🗑️ Sayfaları Sil", key="delete_btn", type="primary"):
            with st.spinner("Sayfalar siliniyor..."):
                try:
                    pages = parse_page_input(page_input, total)
                    result = delete_pages(path, pages)
                    st.success(f"{len(pages)} sayfa silindi! Kalan: {total - len(pages)} sayfa")
                    download_button(result, "📥 Düzenlenmiş PDF'i İndir")
                except Exception as e:
                    st.error(f"Hata: {e}")

    elif operation == "Sayfa Döndür":
        angle = st.selectbox("Döndürme açısı", [90, 180, 270], key="rotate_angle")
        if st.button("🔄 Sayfaları Döndür", key="rotate_btn", type="primary"):
            with st.spinner("Sayfalar döndürülüyor..."):
                try:
                    pages = parse_page_input(page_input, total)
                    result = rotate_pages(path, pages, angle)
                    st.success(f"{len(pages)} sayfa {angle}° döndürüldü!")
                    download_button(result, "📥 Döndürülmüş PDF'i İndir")
                except Exception as e:
                    st.error(f"Hata: {e}")
