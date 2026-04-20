"""
EditPDF Web — PDF İşleme Motoru

Streamlit tab modüllerinin kullandığı üst düzey PDF fonksiyonları.
Tüm çekirdek mantık yerel core/, converters/, utils/ klasörlerindedir;
masaüstü PDFToolKit'e bağımlılık yoktur.
"""

# ── Core modüller ──────────────────────────────────────────────
from core.pdf_merger import merge_pdfs, insert_pdf
from core.pdf_splitter import split_all_pages, extract_pages
from core.pdf_compressor import compress_pdf
from core.pdf_encryptor import encrypt_pdf, decrypt_pdf
from core.pdf_watermark import add_watermark
from core.pdf_page_manager import delete_pages, rotate_pages, get_page_count
from core.pdf_metadata import get_metadata

# ── Dönüştürücüler ────────────────────────────────────────────
from converters.from_pdf import pdf_to_word, pdf_to_excel, pdf_to_jpg
from converters.to_pdf import word_to_pdf, jpg_to_pdf, images_to_pdf

# ── Yardımcılar ───────────────────────────────────────────────
from utils.page_parser import parse_page_input
