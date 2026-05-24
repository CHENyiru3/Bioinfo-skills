#!/usr/bin/env python3
"""Repair a moved Seurat tutorial conda R runtime enough for local probes."""

from __future__ import annotations

import argparse
import shutil
import stat
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PREFIX = ROOT.parent / "seurat_tutorial" / "conda_env"
OLD_PREFIX = "/home/heybro/mnt/workspace/seurat_tutorial/conda_env"


def patch_text_file(path: Path, old: str, new: str) -> bool:
    if not path.exists():
        return False
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    if old not in text:
        return False
    path.write_text(text.replace(old, new), encoding="utf-8")
    return True


def patch_text_tree(path: Path, old: str, new: str) -> list[str]:
    patched: list[str] = []
    if not path.exists():
        return patched
    for child in sorted(path.rglob("*")):
        if not child.is_file() or child.stat().st_size > 10_000_000:
            continue
        if patch_text_file(child, old, new):
            patched.append(str(child.relative_to(path)))
    return patched


def ensure_r_shell_exports(path: Path, prefix: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    marker = "# bioinfo-skills relocated env exports"
    if marker in text:
        return False
    anchor = "R_DOC_DIR="
    anchor_pos = text.find(anchor)
    if anchor_pos == -1:
        return False
    export_pos = text.find("export R_DOC_DIR", anchor_pos)
    if export_pos == -1:
        return False
    line_end = text.find("\n", export_pos)
    if line_end == -1:
        return False
    insert = f"""
{marker}
PATH={prefix}/bin:${{PATH}}
export PATH
if test -f "{prefix}/ssl/cacert.pem"; then
  if test -z "${{SSL_CERT_FILE}}" || test "${{SSL_CERT_FILE}}" = "{OLD_PREFIX}/ssl/cacert.pem"; then
    SSL_CERT_FILE={prefix}/ssl/cacert.pem
    export SSL_CERT_FILE
  fi
  if test -z "${{CURL_CA_BUNDLE}}" || test "${{CURL_CA_BUNDLE}}" = "{OLD_PREFIX}/ssl/cacert.pem"; then
    CURL_CA_BUNDLE={prefix}/ssl/cacert.pem
    export CURL_CA_BUNDLE
  fi
  if test -z "${{REQUESTS_CA_BUNDLE}}" || test "${{REQUESTS_CA_BUNDLE}}" = "{OLD_PREFIX}/ssl/cacert.pem"; then
    REQUESTS_CA_BUNDLE={prefix}/ssl/cacert.pem
    export REQUESTS_CA_BUNDLE
  fi
fi
"""
    path.write_text(text[: line_end + 1] + insert + text[line_end + 1 :], encoding="utf-8")
    return True


def rscript_wrapper(depth_to_prefix: str) -> str:
    return f"""#!/bin/sh
set -eu
prefix=$(CDPATH= cd -- "$(dirname -- "$0")/{depth_to_prefix}" && pwd)
R_HOME="${{prefix}}/lib/R"
export R_HOME
export R_SHARE_DIR="${{R_HOME}}/share"
export R_INCLUDE_DIR="${{R_HOME}}/include"
export R_DOC_DIR="${{R_HOME}}/doc"
if [ -n "${{LD_LIBRARY_PATH:-}}" ]; then
  export LD_LIBRARY_PATH="${{prefix}}/lib:${{LD_LIBRARY_PATH}}"
else
  export LD_LIBRARY_PATH="${{prefix}}/lib"
fi
export PATH="${{prefix}}/bin:${{PATH}}"
if [ -f "${{prefix}}/ssl/cacert.pem" ]; then
  case "${{SSL_CERT_FILE:-}}" in
    ""|"{OLD_PREFIX}/ssl/cacert.pem") export SSL_CERT_FILE="${{prefix}}/ssl/cacert.pem" ;;
  esac
  case "${{CURL_CA_BUNDLE:-}}" in
    ""|"{OLD_PREFIX}/ssl/cacert.pem") export CURL_CA_BUNDLE="${{prefix}}/ssl/cacert.pem" ;;
  esac
  case "${{REQUESTS_CA_BUNDLE:-}}" in
    ""|"{OLD_PREFIX}/ssl/cacert.pem") export REQUESTS_CA_BUNDLE="${{prefix}}/ssl/cacert.pem" ;;
  esac
fi

case "${{1:-}}" in
  --version)
    exec "${{R_HOME}}/bin/exec/R" --version
    ;;
  --help|-h)
    exec "${{R_HOME}}/bin/exec/R" --help
    ;;
  -e)
    exec "${{R_HOME}}/bin/exec/R" --no-echo --no-restore "$@"
    ;;
  "")
    exec "${{R_HOME}}/bin/exec/R" --no-echo --no-restore
    ;;
  -*)
    exec "${{R_HOME}}/bin/exec/R" --no-echo --no-restore "$@"
    ;;
  *)
    script="$1"
    shift
    exec "${{R_HOME}}/bin/exec/R" --no-echo --no-restore --file="${{script}}" --args "$@"
    ;;
esac
"""


def replace_rscript(path: Path, depth_to_prefix: str) -> bool:
    if not path.exists():
        return False
    backup = path.with_name(path.name + ".conda-binary")
    if not backup.exists():
        shutil.copy2(path, backup)
    path.write_text(rscript_wrapper(depth_to_prefix), encoding="utf-8")
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", type=Path, default=DEFAULT_PREFIX)
    parser.add_argument("--old-prefix", default=OLD_PREFIX)
    args = parser.parse_args()

    prefix = args.prefix.resolve()
    if not (prefix / "lib/R/bin/exec/R").exists():
        raise SystemExit(f"R executable not found under {prefix}")

    patched = []
    for rel in (
        "bin/R",
        "lib/R/bin/R",
        "lib/R/bin/libtool",
        "lib/R/etc/ldpaths",
        "lib/R/etc/Renviron",
        "lib/R/etc/Makeconf",
    ):
        path = prefix / rel
        if patch_text_file(path, args.old_prefix, str(prefix)):
            patched.append(rel)
    for rel in patch_text_tree(prefix / "bin", args.old_prefix, str(prefix)):
        patched.append("bin/" + rel)
    for rel in patch_text_tree(prefix / "etc", args.old_prefix, str(prefix)):
        patched.append("etc/" + rel)
    for rel in ("bin/R", "lib/R/bin/R"):
        if ensure_r_shell_exports(prefix / rel, prefix):
            patched.append(rel + ":exports")

    replaced = []
    if replace_rscript(prefix / "bin/Rscript", ".."):
        replaced.append("bin/Rscript")
    if replace_rscript(prefix / "lib/R/bin/Rscript", "../../.."):
        replaced.append("lib/R/bin/Rscript")

    print(f"prefix={prefix}")
    print("patched_text=" + ",".join(patched))
    print("replaced_rscript=" + ",".join(replaced))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
