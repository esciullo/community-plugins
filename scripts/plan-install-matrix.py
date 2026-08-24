#!/usr/bin/env python3
"""Build the CI job matrix for installing every plugin in `tools/`.

Each plugin declares which operating systems it supports (via `[platform.<os>]`)
and, usually, which architectures (via `platform.<os>.archs`). This script pairs
that declaration against the available runners so we only schedule combinations
the plugin actually claims to support -- an arm64-only runner will not be asked
to install an x64-only tool.

Prints `matrix=<json>` and `count=<n>` on stdout, ready to be appended to
$GITHUB_OUTPUT. Run it with no arguments to inspect the plan locally.
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

# Runners to schedule against. Add entries here to widen platform coverage --
# the plugins' own `archs` lists decide which tools land on which runner:
#   {"runner": "ubuntu-24.04-arm", "os": "linux", "arch": "arm64"},
#   {"runner": "macos-15-intel", "os": "macos", "arch": "x64"},
#   {"runner": "windows-11-arm", "os": "windows", "arch": "arm64"},
RUNNERS = [
    {"runner": "ubuntu-latest", "os": "linux", "arch": "x64"},
    {"runner": "macos-latest", "os": "macos", "arch": "arm64"},
    {"runner": "windows-latest", "os": "windows", "arch": "x64"},
]

# `archs` accepts the serde aliases as well as the canonical names, so both
# spellings appear across the plugins. Normalize before comparing.
ARCH_ALIASES = {
    "x86_64": "x64",
    "aarch64": "arm64",
    "loongarch64": "longarm64",
}

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"


def normalize(arch: str) -> str:
    return ARCH_ALIASES.get(arch, arch)


def supports(platform: dict, arch: str) -> bool:
    # No `archs` means the plugin makes no claim, so let the install decide.
    archs = platform.get("archs")

    return True if not archs else arch in {normalize(a) for a in archs}


def main() -> int:
    include = []
    skipped = []

    for path in sorted(TOOLS_DIR.glob("*.toml")):
        tool = path.stem

        try:
            schema = tomllib.loads(path.read_text())
        except tomllib.TOMLDecodeError as error:
            print(f"{path}: invalid TOML: {error}", file=sys.stderr)
            return 1

        platforms = schema.get("platform", {})

        if not platforms:
            print(f"{path}: no [platform.*] sections", file=sys.stderr)
            return 1

        for target in RUNNERS:
            platform = platforms.get(target["os"])

            if platform is None or not supports(platform, target["arch"]):
                skipped.append(f"{tool} on {target['os']}/{target['arch']}")
                continue

            include.append({"tool": tool, **target})

    for entry in skipped:
        print(f"skipping {entry} (not supported by the plugin)", file=sys.stderr)

    print(f"\n{len(include)} jobs across {len(RUNNERS)} runners", file=sys.stderr)

    print(f"matrix={json.dumps(include, separators=(',', ':'))}")
    print(f"count={len(include)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
