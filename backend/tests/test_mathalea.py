"""Tests du constructeur d'URL — la pièce qui doit rester fiable.

On fige uuid/alea dans les manifestes pour des URLs déterministes.
"""
from urllib.parse import parse_qsl, urlsplit

import pytest

from backend.mathalea import (
    MATHALEA_BASE_URL,
    build_pairs,
    build_url,
    freeze_runtime_ids,
)


def _fiche(exercices, **mep):
    base_mep = {"colonnes": 2, "corrige": True, "vue": "eleve"}
    base_mep.update(mep)
    return {"titre": "Test", "mise_en_page": base_mep, "exercices": exercices}


def test_un_exercice_minimal():
    fiche = _fiche([{"id": "4C21", "uuid": "abc12", "alea": "VAQ7", "n": 4}])
    pairs = build_pairs(fiche, vue="latex")
    assert pairs == [
        ("uuid", "abc12"),
        ("id", "4C21"),
        ("n", "4"),
        ("cd", "1"),       # corrige=True -> cd=1
        ("cols", "2"),
        ("alea", "VAQ7"),
        ("v", "latex"),
    ]


def test_ordre_et_chainage_multi_exercices():
    fiche = _fiche([
        {"id": "4C21", "uuid": "u1", "alea": "a1", "n": 4},
        {"id": "4L10", "uuid": "u2", "alea": "a2", "n": 3},
    ])
    pairs = build_pairs(fiche, vue="latex")
    # uuid apparaît une fois par exercice, dans l'ordre.
    uuids = [v for k, v in pairs if k == "uuid"]
    ids = [v for k, v in pairs if k == "id"]
    assert uuids == ["u1", "u2"]
    assert ids == ["4C21", "4L10"]
    assert pairs[-1] == ("v", "latex")


def test_sup_et_booleens():
    fiche = _fiche([
        {"id": "4C30", "uuid": "u1", "alea": "a1", "n": 2,
         "sup": {"s": "1-2", "s2": True, "s3": 4}},
    ])
    d = dict(build_pairs(fiche))
    assert d["s"] == "1-2"
    assert d["s2"] == "true"   # bool -> "true"
    assert d["s3"] == "4"


def test_corrige_false_donne_cd_0():
    fiche = _fiche([{"id": "4C21", "uuid": "u1", "alea": "a1"}], corrige=False)
    assert ("cd", "0") in build_pairs(fiche)


def test_cd_par_exercice_prioritaire():
    fiche = _fiche([{"id": "4C21", "uuid": "u1", "alea": "a1", "cd": "0"}], corrige=True)
    assert ("cd", "0") in build_pairs(fiche)
    assert ("cd", "1") not in build_pairs(fiche)


def test_interactif():
    fiche = _fiche([{"id": "4C21", "uuid": "u1", "alea": "a1", "interactif": True}])
    assert ("i", "1") in build_pairs(fiche)


def test_build_url_complete_et_reproductible():
    fiche = _fiche([{"id": "4C21", "uuid": "u1", "alea": "a1", "n": 2}])
    url = build_url(fiche, vue="latex")
    assert url.startswith(MATHALEA_BASE_URL + "?")
    # même manifeste -> même URL
    assert url == build_url(fiche, vue="latex")
    # paramètres bien présents
    q = dict(parse_qsl(urlsplit(url).query))
    assert q["id"] == "4C21" and q["v"] == "latex"


def test_vue_invalide_leve_erreur():
    fiche = _fiche([{"id": "4C21", "uuid": "u1", "alea": "a1"}])
    with pytest.raises(ValueError):
        build_url(fiche, vue="nimporte-quoi")


def test_freeze_runtime_ids_idempotent():
    ex = {"id": "4C21"}
    e1 = freeze_runtime_ids(ex)
    assert e1["uuid"] and e1["alea"]
    # déjà gelé -> inchangé
    e2 = freeze_runtime_ids(e1)
    assert e2["uuid"] == e1["uuid"] and e2["alea"] == e1["alea"]
    # n'altère pas l'original
    assert "uuid" not in ex
