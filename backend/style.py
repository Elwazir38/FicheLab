"""Chargement du style maison (styles/style.json) -> contexte du template.

Le style est volontairement minimal et lisible : Rachid édite `style.json`
(couleur, établissement, police) et dépose sa police dans `fonts/`.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLES_DIR = ROOT / "styles"
FONTS_DIR = ROOT / "fonts"

DEFAULTS = {
    "police": None,            # nom fontspec, ou None -> Latin Modern par défaut
    "police_path": None,       # dossier de la police si fichier local
    "couleur_principale": "1F4E79",
    "etablissement": "",
    "afficher_entete_eleve": True,
    "titre_defaut": "Fiche d'exercices",
}


def load_style() -> dict:
    data = dict(DEFAULTS)
    path = STYLES_DIR / "style.json"
    if path.exists():
        data.update(json.loads(path.read_text(encoding="utf-8")))
    # Si une police locale est nommée sans chemin, on pointe vers fonts/.
    if data.get("police") and not data.get("police_path"):
        if FONTS_DIR.exists() and any(FONTS_DIR.iterdir()):
            data["police_path"] = str(FONTS_DIR).replace("\\", "/")
    return data


def style_context(style: dict | None = None) -> dict:
    """Contexte de style final (style.json + surcharges éventuelles)."""
    ctx = load_style()
    if style:
        ctx.update({k: v for k, v in style.items() if v is not None})
    return ctx
