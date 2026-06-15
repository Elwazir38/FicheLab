"""Garde-fou : toute fiche `.json` livrée dans `fiches/` doit rester valide.

Le test parcourt `fiches/`, charge chaque manifeste et vérifie :
- structure minimale (titre, exercices) ;
- chaque exercice MathALEA pointe sur un `id` existant dans le catalogue ;
- l'URL d'export se compose sans lever (vues `eleve` et `latex`) et
  contient bien un bloc par exercice (`id=`).

Pour les fiches Pyromaths (un exemple est livré), on s'assure simplement
que `build_url` les *ignore* proprement (elles ne contribuent pas à l'URL
MathALEA, ce qui est le comportement attendu d'une fiche mixte).
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

import pytest

from backend.catalogue import index_titres
from backend.mathalea import VUES, build_url

FICHES_DIR = Path(__file__).resolve().parent.parent.parent / "fiches"


def _fiches() -> list[Path]:
    return sorted(FICHES_DIR.glob("*.json"))


def test_dossier_fiches_non_vide():
    """Sanity : la bibliothèque livre au moins quelques fiches d'amorce."""
    assert len(_fiches()) >= 5, "La bibliothèque doit livrer ≥5 fiches d'amorce."


@pytest.mark.parametrize("path", _fiches(), ids=lambda p: p.stem)
def test_fiche_valide(path: Path):
    fiche = json.loads(path.read_text(encoding="utf-8"))

    # Structure minimale
    assert fiche.get("titre"), f"{path.name} : titre manquant"
    assert isinstance(fiche.get("exercices"), list) and fiche["exercices"], (
        f"{path.name} : exercices manquants ou vides"
    )

    # Vue de mise en page valide (si présente)
    vue = (fiche.get("mise_en_page") or {}).get("vue")
    if vue is not None:
        assert vue in VUES, f"{path.name} : vue inconnue {vue!r}"

    # Ids MathALEA présents dans le catalogue
    idx = index_titres()
    ma_exos = [e for e in fiche["exercices"]
               if e.get("source") in (None, "mathalea") and e.get("id")]
    for ex in ma_exos:
        assert ex["id"] in idx, (
            f"{path.name} : id MathALEA inconnu {ex['id']!r} "
            f"(absent de data/mathalea_raw/allExercice.json)"
        )

    # URL d'export (latex) bien composée si la fiche contient du MathALEA
    if ma_exos:
        url = build_url(fiche, vue="latex")
        assert url.startswith("https://coopmaths.fr/alea/?"), (
            f"{path.name} : URL inattendue {url!r}"
        )
        # un bloc id=... par exercice MathALEA (parse_qsl pour ne pas confondre
        # `id` avec `uuid` ; `parse_qsl` autorise les clés répétées).
        params = parse_qsl(urlsplit(url).query)
        ids = [v for k, v in params if k == "id"]
        assert ids == [e["id"] for e in ma_exos], (
            f"{path.name} : ids dans l'URL = {ids}, attendus = "
            f"{[e['id'] for e in ma_exos]}"
        )
        # vue d'aperçu également (les deux sont utilisées par l'UI)
        assert build_url(fiche, vue="eleve").endswith("v=eleve")
