"""Garde-fou : toute fiche `.json` livrée dans `fiches/` doit rester valide.

Le test parcourt `fiches/`, charge chaque manifeste et vérifie sa structure
minimale (titre, exercices). Pour les exercices Pyromaths, on vérifie que
`name` est non vide ; `seed` reste optionnel (s'il est absent, le moteur
tirera une graine au hasard à la génération).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

FICHES_DIR = Path(__file__).resolve().parent.parent.parent / "fiches"


def _fiches() -> list[Path]:
    return sorted(FICHES_DIR.glob("*.json"))


def test_dossier_fiches_non_vide():
    """Sanity : au moins une fiche d'amorce livrée avec le dépôt."""
    assert len(_fiches()) >= 1, "La bibliothèque doit livrer au moins une fiche d'amorce."


@pytest.mark.parametrize("path", _fiches(), ids=lambda p: p.stem)
def test_fiche_valide(path: Path):
    fiche = json.loads(path.read_text(encoding="utf-8"))

    # Structure minimale
    assert fiche.get("titre"), f"{path.name} : titre manquant"
    assert isinstance(fiche.get("exercices"), list) and fiche["exercices"], (
        f"{path.name} : exercices manquants ou vides"
    )

    # Chaque exercice Pyromaths doit nommer un générateur
    for ex in fiche["exercices"]:
        if ex.get("source") in (None, "pyromaths"):
            assert ex.get("name"), (
                f"{path.name} : exercice Pyromaths sans `name` (clé du générateur)"
            )
