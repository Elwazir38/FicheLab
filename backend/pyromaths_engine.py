"""Moteur Pyromaths local : catalogue + génération de fiches PDF stylées.

S'appuie sur Pyromaths vendorisé (engines/pyromaths) : on liste les exercices
via `ExerciseBag`, on instancie chaque exercice (graine figée = reproductible),
et on rend via `render.py` (notre template maison). 100 % local.
"""
from __future__ import annotations

import re
import secrets
import sys
import warnings
from pathlib import Path

_ENGINE = Path(__file__).resolve().parent.parent / "engines" / "pyromaths"
if str(_ENGINE) not in sys.path:
    sys.path.insert(0, str(_ENGINE))
# Le vieux code Pyromaths déclenche des SyntaxWarning (échappements non-raw) :
# bruit inoffensif, on le masque au chargement.
warnings.filterwarnings("ignore", category=SyntaxWarning)

from pyromaths.ex import ExerciseBag  # noqa: E402

from . import render  # noqa: E402

_BAG: ExerciseBag | None = None


def bag() -> ExerciseBag:
    global _BAG
    if _BAG is None:
        _BAG = ExerciseBag()
    return _BAG


def _safe_desc(cls) -> str:
    try:
        return cls.description()
    except Exception:
        return cls.name()


def list_exercices() -> list[dict]:
    """Catalogue Pyromaths, groupé par niveau (ordre pédagogique)."""
    out = []
    for niveau, exos in bag().sorted_levels():
        items = [{"name": e.name(), "description": _safe_desc(e)} for e in exos]
        if items:
            out.append({"niveau": niveau, "exercices": items})
    return out


def build_blocs(selection: list[dict]) -> list[dict]:
    """selection: [{name, seed?, nb?}] -> blocs {enonce_tex, corrige_tex, name}.

    `nb` copies d'un même type d'exercice ; avec une graine fournie, les copies
    sont décalées de façon déterministe (seed, seed+1, …) pour rester reproductibles.
    """
    b = bag()
    blocs = []
    for item in selection:
        cls = b.get(item["name"])
        if cls is None:
            continue
        nb = int(item.get("nb", 1) or 1)
        base_seed = item.get("seed")
        for k in range(nb):
            if base_seed is not None:
                seed = int(base_seed) + k
            else:
                seed = secrets.randbelow(10 ** 9)
            inst = cls(seed=seed)
            blocs.append({
                "name": item["name"],
                "seed": seed,
                "enonce_tex": inst.tex_statement(),
                "corrige_tex": inst.tex_answer(),
            })
    return blocs


def generate(selection: list[dict], outpath, *, enonce: bool = True,
             corrige: bool = True, titre: str = "", niveau: str | None = None,
             classe: str = "", date_fiche: str = "", style: dict | None = None,
             verbose: bool = False) -> str:
    """Génère le PDF d'une fiche Pyromaths. Renvoie le chemin du PDF."""
    blocs = build_blocs(selection)
    if not blocs:
        raise ValueError("Sélection vide ou exercices introuvables.")
    tex = render.render_tex(
        blocs, enonce=enonce, corrige=corrige, titre=titre, niveau=niveau,
        classe=classe, date_fiche=date_fiche, style=style,
    )
    return render.compile_pdf(tex, outpath, verbose=verbose)
