"""
EditPDF — Konfigürasyon Ayarları
Versiyon bilgileri, sabitler ve ayarlar burada tutulur.
"""

import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# ── Versiyon Bilgisi (SemVer: MAJOR.MINOR.PATCH.BUILD) ────────
# MAJOR: 1=Web MVP (temel PDF işlemleri)
# MINOR: Yeni özellik (geriye uyumlu)
# PATCH: Hata düzeltme
# BUILD: Her değişiklik için artan 4 basamaklı sayaç
APP_VERSION = "1.0.0"
APP_BUILD = "0006"  # bump_build.py tarafından otomatik yönetilir
APP_VERSION_FULL = f"{APP_VERSION}.{APP_BUILD}"
APP_VERSION_DATE = "2026-04-21"
APP_VERSION_NOTES = [
    "#0001 — Proje iskeleti, Streamlit web arayüzü başlangıç",
    "#0002 — 7 tab: Birleştir, Böl, Sıkıştır, Şifrele, Dönüştür, Filigran, Sayfa Yönetimi",
    "#0005 — EditPDF markalaması ve modern UI tasarımı",
]

# ── Uygulama Sabitleri ─────────────────────────────────────────
APP_NAME = "EditPDF"
APP_ICON = "📄"

# Desteklenen dosya uzantıları
SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".xlsx", ".xls",
    ".jpg", ".jpeg", ".png", ".bmp", ".tiff",
}

# Yükleme limiti (MB)
MAX_UPLOAD_SIZE_MB = 200

# ── Dizin Ayarları ─────────────────────────────────────────────
# .env varsa yükle (opsiyonel, lokal geliştirme için)
_BASE_DIR = Path(__file__).resolve().parent.parent
_env_path = _BASE_DIR / ".env"
if _env_path.exists():
    load_dotenv(dotenv_path=_env_path)

# Web'de geçici dizinler kullanılır (her oturum kendi alanı)
_temp_dir = tempfile.mkdtemp(prefix="editpdf_")
OUTPUT_DIR = Path(_temp_dir) / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Loglama seviyesi
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Tesseract (varsa; Cloud'da genelde yok)
TESSERACT_PATH = os.getenv("TESSERACT_PATH", "")
