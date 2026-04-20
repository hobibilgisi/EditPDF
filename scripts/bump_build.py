"""
PDFToolKit Web — Build Numarası Otomatik Artırma

Git pre-commit hook tarafından çağrılır.
Sadece PDFToolKit_web/ altında değişiklik varsa çalışır.

- app/config.py içindeki APP_BUILD'i +1 artırır
- APP_VERSION_DATE'i günceller
- dokumanlar/BUILD_LOG.md'ye yeni satır ekler
- Değişen dosyaları staging'e ekler
"""

import os
import re
import subprocess
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)  # PDFToolKit_web/
MONO_ROOT = os.path.dirname(REPO_ROOT)   # Projects/
CONFIG_PATH = os.path.join(REPO_ROOT, "app", "config.py")
BUILD_LOG_PATH = os.path.join(REPO_ROOT, "dokumanlar", "BUILD_LOG.md")


def has_pdftoolkit_changes() -> bool:
    """Staged dosyalar arasında PDFToolKit_web/ değişikliği var mı?"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, cwd=MONO_ROOT,
        )
        files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        return any(f.startswith("PDFToolKit_web/") for f in files)
    except Exception:
        return False


def get_commit_message() -> str:
    """Staged commit mesajını al."""
    msg_file = sys.argv[1] if len(sys.argv) > 1 else None
    if msg_file and os.path.exists(msg_file):
        with open(msg_file, "r", encoding="utf-8") as f:
            return f.read().strip().split("\n")[0]
    # Fallback: staged diff özeti
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, cwd=MONO_ROOT,
        )
        files = [f.strip() for f in result.stdout.strip().split("\n")
                 if f.strip() and f.startswith("PDFToolKit_web/")]
        return f"{len(files)} dosya değişikliği"
    except Exception:
        return "güncelleme"


def get_short_hash() -> str:
    """Son commit'in kısa hash'ini al."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, cwd=MONO_ROOT,
        )
        return result.stdout.strip() or "—"
    except Exception:
        return "—"


def bump_build():
    # Sadece PDFToolKit_web değişikliği varsa çalış
    if not has_pdftoolkit_changes():
        return

    # config.py oku
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config_text = f.read()

    # Mevcut build numarasını bul
    match = re.search(r'APP_BUILD\s*=\s*"(\d+)"', config_text)
    if not match:
        print("HATA: APP_BUILD bulunamadı!")
        sys.exit(1)

    old_build = int(match.group(1))
    new_build = old_build + 1
    new_build_str = f"{new_build:04d}"

    # Mevcut versiyonu bul
    ver_match = re.search(r'APP_VERSION\s*=\s*"([^"]+)"', config_text)
    version = ver_match.group(1) if ver_match else "?.?.?"

    # config.py güncelle — BUILD ve tarih
    today = datetime.now().strftime("%Y-%m-%d")
    config_text = re.sub(
        r'APP_BUILD\s*=\s*"\d+"',
        f'APP_BUILD = "{new_build_str}"',
        config_text,
    )
    config_text = re.sub(
        r'APP_VERSION_DATE\s*=\s*"[^"]*"',
        f'APP_VERSION_DATE = "{today}"',
        config_text,
    )

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(config_text)

    # BUILD_LOG.md'ye yeni satır ekle
    commit_msg = get_commit_message()
    short_hash = get_short_hash()
    log_line = f"| {new_build_str} | {today} | {version} | {commit_msg} | {short_hash} |\n"

    with open(BUILD_LOG_PATH, "r", encoding="utf-8") as f:
        log_text = f.read()

    if not log_text.endswith("\n"):
        log_text += "\n"
    log_text += log_line

    with open(BUILD_LOG_PATH, "w", encoding="utf-8") as f:
        f.write(log_text)

    # Değişen dosyaları staging'e ekle
    subprocess.run(["git", "add", CONFIG_PATH, BUILD_LOG_PATH], cwd=MONO_ROOT)

    print(f"✅ PDFToolKit Web Build {old_build:04d} → {new_build_str} ({commit_msg})")


if __name__ == "__main__":
    bump_build()
