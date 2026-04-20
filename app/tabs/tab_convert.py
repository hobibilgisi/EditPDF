"""
Tab: Format Dönüştürme
PDF ↔ Word, PDF → Excel, PDF → JPG, Resim → PDF
"""

import streamlit as st
from app.file_helpers import save_uploaded_file, save_uploaded_files, download_button, download_button_zip
from pdf_engine import pdf_to_word, pdf_to_excel, pdf_to_jpg, word_to_pdf, jpg_to_pdf, images_to_pdf


def render():
    st.header("🔄 Format Dönüştürme")

    direction = st.radio(
        "Dönüşüm yönü",
        ["PDF → Diğer", "Diğer → PDF"],
        key="convert_direction",
        horizontal=True,
    )

    if direction == "PDF → Diğer":
        _render_from_pdf()
    else:
        _render_to_pdf()


def _render_from_pdf():
    target = st.selectbox(
        "Hedef format",
        ["Word (.docx)", "Excel (.xlsx)", "JPG (Resim)"],
        key="from_pdf_target",
    )

    uploaded = st.file_uploader("PDF dosyası seçin", type=["pdf"], key="from_pdf_upload")
    if not uploaded:
        st.info("Bir PDF dosyası yükleyin.")
        return

    btn_label = f"🔄 {target.split()[0]}'a Dönüştür"
    if st.button(btn_label, key="from_pdf_btn", type="primary"):
        path = save_uploaded_file(uploaded)

        with st.spinner("Dönüştürülüyor..."):
            try:
                if "Word" in target:
                    result = pdf_to_word(path)
                    st.success("Word'e dönüştürüldü!")
                    download_button(result, "📥 Word Dosyasını İndir",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

                elif "Excel" in target:
                    result = pdf_to_excel(path)
                    st.success("Excel'e dönüştürüldü!")
                    download_button(result, "📥 Excel Dosyasını İndir",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                elif "JPG" in target:
                    results = pdf_to_jpg(path)
                    st.success(f"{len(results)} sayfa JPG'ye dönüştürüldü!")
                    if len(results) == 1:
                        download_button(results[0], "📥 JPG İndir", mime="image/jpeg")
                    else:
                        download_button_zip(results, f"{path.stem}_resimler.zip")

            except Exception as e:
                st.error(f"Hata: {e}")


def _render_to_pdf():
    source = st.selectbox(
        "Kaynak format",
        ["Word (.docx)", "Resim (JPG/PNG)"],
        key="to_pdf_source",
    )

    if "Word" in source:
        uploaded = st.file_uploader("Word dosyası seçin", type=["docx"], key="to_pdf_word")
        if not uploaded:
            st.info("Bir Word dosyası yükleyin.")
            return

        if st.button("🔄 PDF'e Dönüştür", key="to_pdf_word_btn", type="primary"):
            path = save_uploaded_file(uploaded)
            with st.spinner("Dönüştürülüyor..."):
                try:
                    result = word_to_pdf(path)
                    st.success("PDF'e dönüştürüldü!")
                    download_button(result)
                except Exception as e:
                    st.error(f"Hata: {e}")

    elif "Resim" in source:
        uploaded = st.file_uploader(
            "Resim dosyaları seçin",
            type=["jpg", "jpeg", "png", "bmp", "tiff"],
            accept_multiple_files=True,
            key="to_pdf_img",
        )
        if not uploaded:
            st.info("En az bir resim dosyası yükleyin.")
            return

        if st.button("🔄 PDF'e Dönüştür", key="to_pdf_img_btn", type="primary"):
            paths = save_uploaded_files(uploaded)
            with st.spinner("Dönüştürülüyor..."):
                try:
                    if len(paths) == 1:
                        result = jpg_to_pdf(paths[0])
                    else:
                        result = images_to_pdf([str(p) for p in paths])
                    st.success("PDF'e dönüştürüldü!")
                    download_button(result)
                except Exception as e:
                    st.error(f"Hata: {e}")
