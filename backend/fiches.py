"""Persistance des fiches : des manifestes `.json` lisibles, dans `fiches/`.

Une fiche EST un fichier. C'est le cœur « DX » du système : versionnable
(OneDrive / git), duplicable à la main, régénérable par la CLI, et qui
reproduit toujours le même PDF (grâce aux graines gelées dans chaque exercice).
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

FICHES_DIR = Path(__file__).resolve().parent.parent / "fiches"

MANIFEST_VERSION = 1


def slugify(texte: str) -> str:
    """Transforme un titre en nom de fichier sûr (sans accents ni espaces)."""
    texte = unicodedata.normalize("NFKD", texte)
    texte = texte.encode("ascii", "ignore").decode("ascii")
    texte = re.sub(r"[^\w\s-]", "", texte).strip().lower()
    texte = re.sub(r"[\s_]+", "-", texte)
    return texte or "fiche"


def _path(slug: str) -> Path:
    # Empêche toute évasion de répertoire.
    safe = slugify(slug)
    return FICHES_DIR / f"{safe}.json"


def list_fiches() -> list[dict]:
    """Métadonnées de toutes les fiches enregistrées (titre, slug, nb exos)."""
    FICHES_DIR.mkdir(parents=True, exist_ok=True)
    out = []
    for p in sorted(FICHES_DIR.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        out.append({
            "slug": p.stem,
            "titre": data.get("titre", p.stem),
            "nb_exercices": len(data.get("exercices", [])),
            "date": (data.get("entete") or {}).get("date", ""),
        })
    return out


def get_fiche(slug: str) -> dict | None:
    p = _path(slug)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def save_fiche(fiche: dict) -> str:
    """Écrit le manifeste sur disque. Renvoie le slug utilisé."""
    FICHES_DIR.mkdir(parents=True, exist_ok=True)
    fiche.setdefault("version", MANIFEST_VERSION)
    titre = fiche.get("titre") or "fiche"
    slug = slugify(titre)
    p = FICHES_DIR / f"{slug}.json"
    p.write_text(json.dumps(fiche, ensure_ascii=False, indent=2), encoding="utf-8")
    return slug


def delete_fiche(slug: str) -> bool:
    p = _path(slug)
    if p.exists():
        p.unlink()
        return True
    return False
