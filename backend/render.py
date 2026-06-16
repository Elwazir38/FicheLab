"""Renderer : blocs d'exercices Pyromaths -> LaTeX (template maison) -> PDF lualatex.

Chaque bloc fournit `enonce_tex` (= `exo.tex_statement()`) et `corrige_tex`
(= `exo.tex_answer()`). On réutilise l'environnement Jinja de Pyromaths
(délimiteurs (* *)/(( ))) et on compile via latexmk + lualatex (mêmes réglages
que Pyromaths/System.py), mais avec NOTRE template `styles/fiche.tex.j2` et
l'environnement complet (sinon MiKTeX refuse de compiler).
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import jinja2

from .style import STYLES_DIR, style_context

# Pyromaths fournit l'environnement Jinja LaTeX et le filtre `tex`.
_ENGINE = Path(__file__).resolve().parent.parent / "engines" / "pyromaths"
if str(_ENGINE) not in sys.path:
    sys.path.insert(0, str(_ENGINE))
from pyromaths.outils.jinja2utils import LatexEnvironment, tex  # noqa: E402

TEMPLATE = "fiche.tex.j2"


def _environment() -> LatexEnvironment:
    env = LatexEnvironment(loader=jinja2.FileSystemLoader(str(STYLES_DIR)))
    env.filters["tex"] = tex
    return env


def render_tex(
    blocs: list[dict],
    *,
    enonce: bool = True,
    corrige: bool = True,
    titre: str = "",
    niveau: str | None = None,
    classe: str = "",
    date_fiche: str = "",
    style: dict | None = None,
) -> str:
    """Construit la source LaTeX complète de la fiche."""
    ctx = style_context(style)
    ctx.update({
        "blocs": blocs,
        "enonce": enonce,
        "corrige": corrige,
        "titre": titre or ctx.get("titre_defaut", ""),
        "niveau": niveau,
        "classe": classe,
        "date_fiche": date_fiche,
    })
    return _environment().get_template(TEMPLATE).render(ctx)


def _latexmkrc(verbose: bool) -> str:
    silent = 0 if verbose else 1
    # -no-shell-escape : le .tex est en partie alimenté par des données client
    # (titre/classe/date, contenu d'exercices). Interdire \write18 ferme la
    # porte à l'exécution de commandes arbitraires. Le template (tikz/pgfplots,
    # sans \tikzexternalize ni minted) n'a pas besoin du shell-escape.
    return (
        "$pdf_mode = 4;\n"
        '$lualatex = "lualatex -no-shell-escape -interaction=nonstopmode %O %S";\n'
        "$auto_rc_use = 0;\n"
        f"$silent = {silent};\n"
        "$cleanup_mode = 2;\n"
    )


def compile_pdf(tex_source: str, outpath: str | Path, *, verbose: bool = False,
                keep: bool = False) -> str:
    """Compile la source LaTeX en PDF (lualatex via latexmk). Renvoie le chemin."""
    workdir = tempfile.mkdtemp(prefix="fichelab-")
    base = "fiche"
    Path(workdir, f"{base}.tex").write_text(tex_source, encoding="utf-8")
    Path(workdir, "latexmkrc").write_text(_latexmkrc(verbose), encoding="utf-8")

    env = os.environ.copy()  # environnement complet : MiKTeX en a besoin.
    try:
        subprocess.run(
            ["latexmk", "-norc", "-r", "latexmkrc", base],
            cwd=workdir, env=env, timeout=180,
        )
    except subprocess.TimeoutExpired as exc:
        # Évite un worker bloqué indéfiniment (paquet manquant, boucle…).
        raise RuntimeError(
            f"Compilation LaTeX interrompue (timeout 180s). Dossier conservé : {workdir}"
        ) from exc

    pdf = Path(workdir, f"{base}.pdf")
    if not pdf.exists():
        raise RuntimeError(
            f"Compilation LaTeX échouée. Dossier conservé pour diagnostic : {workdir}"
        )

    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(pdf, outpath)
    if not keep:
        shutil.rmtree(workdir, ignore_errors=True)
    return str(outpath)
