"""
EditPDF — Git Hook Kurulum Scripti

Kullanım: python scripts/install_hooks.py
"""

import os
import stat
import sys
from pathlib import Path

REPO_ROOT  = Path(__file__).resolve().parent.parent
HOOKS_DIR  = REPO_ROOT / ".git" / "hooks"
HOOK_FILE  = HOOKS_DIR / "pre-commit"

HOOK_CONTENT = """\
#!/bin/bash
# EditPDF — pre-commit hook
# Her commit öncesi build numarasını ve BUILD_LOG.md'yi otomatik günceller.

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

# Venv Python'u bul
if [ -f "../.venv/Scripts/python.exe" ]; then
    PYTHON="../.venv/Scripts/python.exe"
elif [ -f ".venv/Scripts/python.exe" ]; then
    PYTHON=".venv/Scripts/python.exe"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    PYTHON="python3"
fi

PYTHONIOENCODING=utf-8 "$PYTHON" scripts/bump_build.py
STATUS=$?

if [ $STATUS -ne 0 ]; then
    echo "❌ bump_build.py başarısız — commit iptal edildi."
    exit 1
fi

exit 0
"""


def install():
    if not HOOKS_DIR.exists():
        print(f"HATA: .git/hooks dizini bulunamadı: {HOOKS_DIR}")
        sys.exit(1)

    HOOK_FILE.write_text(HOOK_CONTENT, encoding="utf-8", newline="\n")

    # Çalıştırılabilir yap (Unix/macOS/Git Bash)
    current = HOOK_FILE.stat().st_mode
    HOOK_FILE.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"OK pre-commit hook kuruldu: {HOOK_FILE}")
    print()
    print("Kullanım:")
    print("  git commit -m 'açıklama'          → build otomatik artar")
    print("  python scripts/bump_build.py --patch 'açıklama'  → PATCH bump")
    print("  python scripts/bump_build.py --minor 'açıklama'  → MINOR bump")
    print("  python scripts/bump_build.py --dry-run           → önizleme")


if __name__ == "__main__":
    install()
