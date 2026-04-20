"""
Tab: PDF Böl
PDF dosyasını sayfalara ayırır veya belirli sayfaları çıkarır.
"""

import streamlit as st
from app.file_helpers import save_uploaded_file, download_button, download_button_zip
from pdf_engine import split_all_pages, extract_pages, get_page_count, parse_page_input


def render():
    st.header("✂️ PDF Böl / Sayfa Çıkar")

    uploaded = st.file_uploader("PDF dosyası seçin", type=["pdf"], key="split_upload")

    if not uploaded:
        st.info("Bir PDF dosyası yükleyin.")
        return

    path = save_uploaded_file(uploaded)
    total = get_page_count(path)
    st.info(f"📄 **{uploaded.name}** — {total} sayfa")

    mode = st.radio(
        "İşlem seçin",
        ["Her sayfayı ayrı PDF yap", "Belirli sayfaları çıkar"],
        key="split_mode",
    )

    if mode == "Her sayfayı ayrı PDF yap":
        if st.button("✂️ Tüm Sayfaları Ayır", key="split_all_btn", type="primary"):
            with st.spinner("Sayfalar ayrılıyor..."):
                try:
                    results = split_all_pages(path)
                    st.success(f"{len(results)} sayfa ayrıldı!")
                    download_button_zip(results, f"{path.stem}_sayfalar.zip")
                except Exception as e:
                    st.error(f"Hata: {e}")
    else:
        page_input = st.text_input(
            "Sayfa numaraları",
            placeholder="Örn: 1-3,5,8  veya  tümü",
            help=f"Toplam {total} sayfa. Virgül ve tire kullanabilirsiniz.",
            key="split_pages_input",
        )
        if page_input and st.button("📄 Sayfaları Çıkar", key="extract_btn", type="primary"):
            with st.spinner("Sayfalar çıkarılıyor..."):
                try:
                    pages = parse_page_input(page_input, total)
                    result = extract_pages(path, pages)
                    st.success(f"{len(pages)} sayfa çıkarıldı!")
                    download_button(result, "📥 Çıkarılan Sayfaları İndir")
                except Exception as e:
                    st.error(f"Hata: {e}")
