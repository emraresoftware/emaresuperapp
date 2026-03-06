#!/usr/bin/env python3
"""Emare SuperApp Derviş kaydı scripti"""
import pathlib, json

root = pathlib.Path('/Users/emre/Desktop/Emare')
base = root / 'emareapi'
dervis = base / 'Dervisler'
dergah = base / 'Dergah'
superapp_path = root / 'emaresuperapp'

# Dervis klasoru
d = dervis / 'emaresuperapp Dervishi'
d.mkdir(parents=True, exist_ok=True)

# DERVISH_PROFIL.md
profil = """# emaresuperapp Dervishi

- Sorumlu Klasor Sahibi: emaresuperapp
- Proje Yolu: /Users/emre/Desktop/Emare/emaresuperapp

## Gorev
- Tum Emare hizmetlerini birlestiren SuperApp platformundan birincil sorumludur.
- Auth, Wallet, Marketplace, Social, AI, Notifications, Analytics modullerini yonetir.
- Dergah uzerinden diger Dervislere koordinasyon ve API entegrasyonu saglar.

## Moduller
- auth: Kimlik dogrulama + SSO
- wallet: Dijital cuzdan + odeme
- marketplace: Emare urun/servis pazaryeri
- social: Feed, mesajlasma
- ai_assistant: Gemini/OpenAI entegrasyonu
- notifications: Push/email/SMS
- analytics: Kullanim metrikleri

## Teknoloji
- FastAPI + SQLAlchemy + Redis
- React + Next.js (Web)
- React Native (Mobile)
- Docker + Nginx
"""
(d / 'DERVISH_PROFIL.md').write_text(profil, encoding='utf-8')

# PROJE_KISAYOLU symlink
link = d / 'PROJE_KISAYOLU'
if link.exists() or link.is_symlink():
    link.unlink()
link.symlink_to(superapp_path)

# Dergah symlink
dlink = dergah / 'emaresuperapp Dervishi'
if dlink.exists() or dlink.is_symlink():
    dlink.unlink()
dlink.symlink_to(pathlib.Path('..') / 'Dervisler' / 'emaresuperapp Dervishi')

# emareapi Dervishi.md guncelle
master_md = base / 'emareapi Dervishi.md'
content = master_md.read_text(encoding='utf-8')
if 'emaresuperapp' not in content:
    content = content.rstrip() + '\n- emaresuperapp Dervishi -> /Users/emre/Desktop/Emare/emaresuperapp\n'
    master_md.write_text(content, encoding='utf-8')

# projects.json guncelle
pj = root / 'projects.json'
projects = json.loads(pj.read_text(encoding='utf-8'))
ids = {p['id'] for p in projects}
if 'emaresuperapp' not in ids:
    projects.append({
        "id": "emaresuperapp",
        "name": "Emare SuperApp",
        "icon": "\U0001f680",
        "color": "#8b5cf6",
        "description": "Tum Emare hizmetlerini tek cati altinda birlestiren super uygulama platformu",
        "status": "development",
        "tech": ["FastAPI", "Python", "React", "Next.js", "React Native", "PostgreSQL", "Redis", "Docker"],
        "path": "/Users/emre/Desktop/Emare/emaresuperapp",
        "memory_file": "/Users/emre/Desktop/Emare/emaresuperapp/SUPERAPP_HAFIZA.md",
        "server": None,
        "local_start_cmd": "python3 main.py",
        "local_port": 8080,
        "category": "Platform",
        "url": None,
        "notes": []
    })
    pj.write_text(json.dumps(projects, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'projects.json guncellendi: {len(projects)} proje')

print('Dervish created and registered')
print('Profil:', (d / 'DERVISH_PROFIL.md').exists())
print('Shortcut:', link.is_symlink(), '->', link.resolve())
print('Dergah:', dlink.is_symlink())
