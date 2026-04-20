"""
EditPDF — Build & Versiyon Yönetimi

Kullanım:
  python scripts/bump_build.py                       # sadece build numarası artır
  python scripts/bump_build.py "açıklama"            # açıklamayla build artır
  python scripts/bump_build.py --patch "açıklama"    # PATCH bump (1.0.x → 1.0.x+1)
  python scripts/bump_build.py --minor "açıklama"    # MINOR bump (1.x.0 → 1.x+1.0)
  python scripts/bump_build.py --major "açıklama"    # MAJOR bump (x.0.0 → x+1.0.0)
  python scripts/bump_build.py --dry-run             # değişiklik yapmadan göster

Git pre-commit hook tarafından otomatik çağrılır.
"""

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ── Yollar ────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).resolve().parent
REPO_ROOT    = SCRIPT_DIR.parent
CONFIG_PATH  = REPO_ROOT / "app" / "config.py"
LOG_PATH     = REPO_ROOT / "dokumanlar" / "BUILD_LOG.md"


# ── Git yardımcıları ───────────────────────────────────────────
def git(*args, check=False) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    if check and result.returncode != 0:
        print(f"git {' '.join(args)} başarısız: {result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()


def staged_files() -> list[str]:
    out = git("diff", "--cached", "--name-only")
    return [f for f in out.splitlines() if f.strip()]


def short_hash() -> str:
    h = git("rev-parse", "--short", "HEAD")
    return h or "—"


def staged_summary(files: list[str]) -> str:
    if not files:
        return "güncelleme"
    if len(files) <= 4:
        return ", ".join(Path(f).name for f in files)
    return f"{len(files)} dosya değişikliği"


# ── Config okuma/yazma ─────────────────────────────────────────
def read_config() -> str:
    return CONFIG_PATH.read_text(encoding="utf-8")


def write_config(text: str) -> None:
    CONFIG_PATH.write_text(text, encoding="utf-8")


def parse_version(config: str) -> tuple[int, int, int, int]:
    ver   = re.search(r'APP_VERSION\s*=\s*"(\d+)\.(\d+)\.(\d+)"', config)
    build = re.search(r'APP_BUILD\s*=\s*"(\d+)"', config)
    if not ver or not build:
        print("HATA: config.py'de APP_VERSION veya APP_BUILD bulunamadı.")
        sys.exit(1)
    return int(ver.group(1)), int(ver.group(2)), int(ver.group(3)), int(build.group(1))


def apply_version(config: str, major: int, minor: int, patch: int,
                  build: int, today: str) -> str:
    config = re.sub(
        r'APP_VERSION\s*=\s*"[^"]+"',
        f'APP_VERSION = "{major}.{minor}.{patch}"',
        config,
    )
    config = re.sub(
        r'APP_BUILD\s*=\s*"\d+"',
        f'APP_BUILD = "{build:04d}"',
        config,
    )
    config = re.sub(
        r'APP_VERSION_DATE\s*=\s*"[^"]*"',
        f'APP_VERSION_DATE = "{today}"',
        config,
    )
    return config


# ── Build log ──────────────────────────────────────────────────
def append_log(build: int, version: str, description: str, git_hash: str) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    line  = f"| {build:04d} | {today} | {version} | {description} | {git_hash} |\n"

    text = LOG_PATH.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    text += line
    LOG_PATH.write_text(text, encoding="utf-8")


# ── Ana işlev ─────────────────────────────────────────────────
def bump(bump_type: str = "build", description: str = "", dry_run: bool = False) -> None:
    config = read_config()
    maj, min_, pat, bld = parse_version(config)
    today  = datetime.now().strftime("%Y-%m-%d")

    old_ver   = f"{maj}.{min_}.{pat}"
    old_build = bld

    if bump_type == "major":
        maj += 1; min_ = 0; pat = 0; bld = 1
    elif bump_type == "minor":
        min_ += 1; pat = 0; bld = 1
    elif bump_type == "patch":
        pat += 1; bld = 1
    else:
        bld += 1

    new_ver   = f"{maj}.{min_}.{pat}"
    new_full  = f"{new_ver}.{bld:04d}"
    old_full  = f"{old_ver}.{old_build:04d}"

    if not description:
        files = staged_files()
        description = staged_summary(files)

    print(f"  Build  : {old_full} -> {new_full}")
    print(f"  Aciklama: {description}")

    if dry_run:
        print("  [dry-run] Degisiklik yapilmadi.")
        return

    # config.py güncelle
    new_config = apply_version(config, maj, min_, pat, bld, today)
    write_config(new_config)

    # BUILD_LOG.md güncelle
    append_log(bld, new_ver, description, short_hash())

    # Değişen dosyaları staging'e ekle
    git("add", str(CONFIG_PATH), str(LOG_PATH), check=True)

    print(f"  OK {new_full} -- staging'e eklendi.")


# ── CLI ────────────────────────────────────────────────────────
def main() -> None:
    args = sys.argv[1:]

    dry_run   = "--dry-run" in args
    args      = [a for a in args if a != "--dry-run"]

    bump_type = "build"
    if args and args[0] in ("--major", "--minor", "--patch"):
        bump_type = args[0].lstrip("-")
        args = args[1:]

    description = " ".join(args).strip()

    print(f"\n[EditPDF] bump -- {bump_type.upper()}")
    bump(bump_type=bump_type, description=description, dry_run=dry_run)


if __name__ == "__main__":
    main()
