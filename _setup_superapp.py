#!/usr/bin/env python3
"""Emare SuperApp dosya yapısı kurulum scripti"""
import pathlib

BASE = pathlib.Path(__file__).parent

dirs = [
    "src/core",
    "src/modules/auth",
    "src/modules/wallet",
    "src/modules/marketplace",
    "src/modules/social",
    "src/modules/ai_assistant",
    "src/modules/notifications",
    "src/modules/analytics",
    "src/api/v1",
    "src/api/middleware",
    "src/services",
    "src/models",
    "src/utils",
    "src/config",
    "mobile/ios",
    "mobile/android",
    "mobile/shared",
    "web/public",
    "web/src/components",
    "web/src/pages",
    "web/src/styles",
    "web/src/hooks",
    "web/src/store",
    "web/src/utils",
    "desktop/src",
    "plugins",
    "templates",
    "static/css",
    "static/js",
    "static/img",
    "tests/unit",
    "tests/integration",
    "tests/e2e",
    "docs/api",
    "docs/architecture",
    "docs/guides",
    "scripts",
    "deploy",
    "data",
    "web_dizayn",
    "EMARE_ORTAK_CALISMA",
]

for d in dirs:
    (BASE / d).mkdir(parents=True, exist_ok=True)

print(f"Created {len(dirs)} directories under {BASE}")
