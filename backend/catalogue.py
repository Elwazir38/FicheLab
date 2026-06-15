"""Chargement et normalisation du catalogue d'exercices.

Source faisant autorité : `data/mathalea_raw/allExercice.json`, le
référentiel officiel de MathALEA. C'est un arbre

    { categorie : { niveau : { codeThème : { ref : <feuille> } } } }

où chaque *feuille* est un exercice **réellement chargeable** :

    { "ref": "4C21", "uuid": "5f429", "url": "4e/4C21.js",
      "titre": "Additionner ou soustraire deux fractions", "tags": {...} }

Le `ref` est le `id` à passer dans l'URL MathALEA. (Attention : les
clés de `*AvecSousThemes.json` sont des *sous-thèmes du programme* et ne
sont PAS toutes chargeables — d'où l'usage d'allExercice.json ici.)

Les `*AvecSousThemes.json` servent uniquement à donner de jolis
**libellés de thème** (ex. code "4C2" -> "Fractions").

Format normalisé renvoyé par `load_catalogue()` :
    { "niveaux": [
        { "niveau": "4e", "label": "4ème", "themes": [
            { "code": "4C2", "titre": "Fractions", "exercices": [
                { "id": "4C21", "titre": "...", "uuid": "5f429",
                  "interactif": true }, ... ] }, ... ] }, ... ] }
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "mathalea_raw"
ALL_EXO = RAW_DIR / "allExercice.json"

#: Niveaux exposés (collège), dans l'ordre d'affichage.
LEVELS: list[tuple[str, str]] = [
    ("6e", "6ème"), ("5e", "5ème"), ("4e", "4ème"), ("3e", "3ème"),
]

#: Fichiers de libellés de thèmes (facultatifs ; fallback = code du thème).
THEME_LABEL_FILES: dict[str, str] = {
    "6e": "6emeAvecSousTheme.json",
    "5e": "5eAvecSousThemes.json",
    "4e": "4eAvecSousThemes.json",
    "3e": "3eAvecSousThemes.json",
}


def _is_leaf(o) -> bool:
    return isinstance(o, dict) and "ref" in o and "url" in o


def _walk_leaves(node):
    """Itère toutes les feuilles-exercices sous un nœud (profondeur libre)."""
    if _is_leaf(node):
        yield node
        return
    if isinstance(node, dict):
        for value in node.values():
            yield from _walk_leaves(value)


def _theme_labels(level: str) -> dict[str, str]:
    fname = THEME_LABEL_FILES.get(level)
    if not fname:
        return {}
    path = RAW_DIR / fname
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {code: node.get("titre", code) for code, node in raw.items()}


@lru_cache(maxsize=1)
def load_catalogue() -> dict:
    """Catalogue normalisé (mis en cache)."""
    allx = json.loads(ALL_EXO.read_text(encoding="utf-8"))
    niveaux = []
    for level, label in LEVELS:
        subtree = allx.get(level, {})
        labels = _theme_labels(level)
        themes = []
        for theme_code, theme_node in subtree.items():
            exercices = []
            seen = set()
            for leaf in _walk_leaves(theme_node):
                ref = leaf["ref"]
                if ref in seen:
                    continue
                seen.add(ref)
                exercices.append({
                    "id": ref,
                    "titre": leaf.get("titre", ref),
                    "uuid": leaf.get("uuid"),
                    "interactif": bool((leaf.get("tags") or {}).get("interactif")),
                })
            if not exercices:
                continue
            themes.append({
                "code": theme_code,
                "titre": labels.get(theme_code, theme_code),
                "exercices": exercices,
            })
        niveaux.append({"niveau": level, "label": label, "themes": themes})
    return {"niveaux": niveaux}


@lru_cache(maxsize=1)
def index_titres() -> dict[str, str]:
    """Index code d'exercice -> intitulé, pour enrichir les manifestes."""
    idx = {}
    for niveau in load_catalogue()["niveaux"]:
        for theme in niveau["themes"]:
            for ex in theme["exercices"]:
                idx[ex["id"]] = ex["titre"]
    return idx
