"""
Tab: PDF Birleştir
Birden fazla PDF dosyasını tek dosya halinde birleştirir.
"""

import streamlit as st
from app.file_helpers import save_uploaded_files, download_button
from pdf_engine import merge_pdfs


def render():
    st.header("📎 PDF Birleştir")
    st.markdown("Birden fazla PDF dosyasını sırayla tek dosyada birleştirin.")

    uploaded = st.file_uploader(
        "PDF dosyalarını seçin (en az 2)",
        type=["pdf"],
        accept_multiple_files=True,
        key="merge_upload",
    )

    if not uploaded or len(uploaded) < 2:
        st.info("En az 2 PDF dosyası yükleyin.")
        return

    st.success(f"{len(uploaded)} dosya yüklendi.")

    # Sıralama göster
    st.markdown("**Birleştirme sırası:**")
    for i, f in enumerate(uploaded, 1):
        st.text(f"  {i}. {f.name}")

    if st.button("🔗 Birleştir", key="merge_btn", type="primary"):
        with st.spinner("Birleştiriliyor..."):
            paths = save_uploaded_files(uploaded)
            file_list = [{"path": str(p), "pages": None} for p in paths]
            try:
                result = merge_pdfs(file_list)
                st.success("Birleştirme tamamlandı!")
                download_button(result, "📥 Birleştirilmiş PDF'i İndir")
            except Exception as e:
                st.error(f"Hata: {e}")
