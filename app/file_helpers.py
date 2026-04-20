"""
PDFToolKit Web — Streamlit Dosya Yardımcıları

Upload edilen dosyaları geçici dizine kaydetme ve
işlenmiş dosyaları indirme butonu olarak sunma.
"""

import tempfile
import zipfile
import io
from pathlib import Path

import streamlit as st


def save_uploaded_file(uploaded_file) -> Path:
    """Streamlit UploadedFile → geçici dizinde gerçek dosya. Path döner."""
    tmp = Path(tempfile.mkdtemp(prefix="pdftk_"))
    dest = tmp / uploaded_file.name
    dest.write_bytes(uploaded_file.getbuffer())
    return dest


def save_uploaded_files(uploaded_files: list) -> list[Path]:
    """Birden fazla dosyayı geçici dizine kaydet."""
    return [save_uploaded_file(f) for f in uploaded_files]


def download_button(file_path: Path, label: str = "📥 İndir", mime: str = "application/pdf"):
    """Tek dosya için indirme butonu."""
    data = file_path.read_bytes()
    st.download_button(
        label=label,
        data=data,
        file_name=file_path.name,
        mime=mime,
    )


def download_button_zip(file_paths: list[Path], zip_name: str = "sonuc.zip", label: str = "📥 Tümünü İndir (ZIP)"):
    """Birden fazla dosyayı ZIP olarak indirme butonu."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in file_paths:
            zf.write(fp, fp.name)
    buf.seek(0)
    st.download_button(
        label=label,
        data=buf,
        file_name=zip_name,
        mime="application/zip",
    )
