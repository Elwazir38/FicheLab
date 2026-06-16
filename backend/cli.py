"""CLI de régénération : rejoue un manifeste de fiche sans ouvrir l'UI.

Exemples :
    python -m backend.cli pyromaths-list --niveau Quatrième
    python -m backend.cli pyromaths-list --search fraction
    python -m backend.cli pyromaths-gen fiches/ma-fiche.json -o ma-fiche.pdf

Grâce aux graines gelées (`seed` dans chaque exercice), une régénération
redonne exactement la même fiche / le même PDF.
"""
from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from pathlib import Path


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _pyromaths_list(niveau: str | None, search: str | None) -> int:
    from . import pyromaths_engine as pe
    s = (search or "").lower()
    for groupe in pe.list_exercices():
        if niveau and niveau.lower() not in groupe["niveau"].lower():
            continue
        exos = [e for e in groupe["exercices"]
                if not s or s in e["name"].lower() or s in e["description"].lower()]
        if not exos:
            continue
        print(f"\n## {groupe['niveau']} ({len(exos)})")
        for e in exos:
            print(f"  {e['name']:28} {e['description']}")
    return 0


def _pyromaths_selection(fiche: dict) -> list[dict]:
    """Extrait du manifeste les exercices Pyromaths."""
    sel = []
    for ex in fiche.get("exercices", []):
        if ex.get("source") == "pyromaths" or ex.get("name"):
            sel.append({"name": ex.get("name") or ex.get("id"),
                        "seed": ex.get("seed"), "nb": ex.get("nb", 1)})
    return sel


def _pyromaths_gen(manifest: Path, output: Path | None, open_pdf: bool, verbose: bool) -> int:
    from . import pyromaths_engine as pe
    if not manifest.exists():
        print(f"Introuvable : {manifest}", file=sys.stderr)
        return 1
    fiche = _load(manifest)
    selection = _pyromaths_selection(fiche)
    if not selection:
        print("Aucun exercice Pyromaths dans ce manifeste.", file=sys.stderr)
        return 1
    out = output or manifest.with_suffix(".pdf")
    mep = fiche.get("mise_en_page", {})
    entete = fiche.get("entete", {})
    pdf = pe.generate(
        selection, out,
        enonce=True, corrige=mep.get("corrige", True),
        titre=fiche.get("titre", ""), niveau=fiche.get("niveau"),
        classe=entete.get("classe", ""), date_fiche=entete.get("date", ""),
        verbose=verbose,
    )
    print(f"PDF généré : {pdf}")
    if open_pdf:
        webbrowser.open(Path(pdf).as_uri())
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="fichelab", description="Régénère des fiches Pyromaths.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    plist = sub.add_parser("pyromaths-list", help="Liste les exercices Pyromaths")
    plist.add_argument("--niveau", default=None, help="Filtrer par niveau")
    plist.add_argument("--search", default=None, help="Filtrer par mot-clé")

    pgen = sub.add_parser("pyromaths-gen", help="Génère le PDF (local) d'une fiche Pyromaths")
    pgen.add_argument("manifest", type=Path)
    pgen.add_argument("-o", "--output", type=Path, default=None)
    pgen.add_argument("--open", action="store_true", help="Ouvre le PDF généré")
    pgen.add_argument("--verbose", action="store_true")

    args = parser.parse_args(argv)

    if args.cmd == "pyromaths-list":
        return _pyromaths_list(args.niveau, args.search)

    if args.cmd == "pyromaths-gen":
        return _pyromaths_gen(args.manifest, args.output, args.open, args.verbose)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
