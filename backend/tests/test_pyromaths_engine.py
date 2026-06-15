"""Tests du moteur Pyromaths (sans compilation LaTeX — rapides).

On vérifie le catalogue, la reproductibilité des blocs (graine), et que le
template maison s'applique (style injecté dans la source LaTeX).
"""
import pytest

pe = pytest.importorskip("backend.pyromaths_engine")
from backend import render  # noqa: E402


def test_catalogue_non_vide_et_groupe_par_niveau():
    cat = pe.list_exercices()
    niveaux = {g["niveau"] for g in cat}
    assert "Quatrième" in niveaux
    # chaque exercice a un nom et une description
    q4 = next(g for g in cat if g["niveau"] == "Quatrième")
    assert q4["exercices"]
    assert all(e["name"] and e["description"] for e in q4["exercices"])


def test_build_blocs_reproductible():
    sel = [{"name": "distributivite", "seed": 11, "nb": 1}]
    b1 = pe.build_blocs(sel)
    b2 = pe.build_blocs(sel)
    assert len(b1) == 1
    # même graine -> même énoncé/corrigé
    assert b1[0]["enonce_tex"] == b2[0]["enonce_tex"]
    assert b1[0]["corrige_tex"] == b2[0]["corrige_tex"]
    # un énoncé Pyromaths commence par la macro \exercice
    assert "\\exercice" in b1[0]["enonce_tex"]


def test_build_blocs_nb_multiple_graines_decalees():
    sel = [{"name": "distributivite", "seed": 100, "nb": 3}]
    blocs = pe.build_blocs(sel)
    assert len(blocs) == 3
    assert [b["seed"] for b in blocs] == [100, 101, 102]


def test_render_applique_le_style():
    blocs = pe.build_blocs([{"name": "distributivite", "seed": 1, "nb": 1}])
    tex = render.render_tex(
        blocs, titre="Ma Fiche", niveau="Quatrième", classe="4B",
        date_fiche="16/06/2026", style={"couleur_principale": "AABBCC",
                                         "etablissement": "Mon Collège"},
    )
    assert "\\documentclass" in tex and "\\begin{document}" in tex
    assert "AABBCC" in tex                 # couleur injectée
    assert "Mon Collège" in tex            # établissement injecté
    assert "Ma Fiche" in tex               # titre dans l'en-tête
    assert "4B" in tex                     # bandeau élève
