"""Scaffold reproductible de la BIBLIOTHÈQUE de fiches FicheLab.

Idée : un seul endroit où sont décrites les fiches prêtes à l'emploi du
catalogue (6e -> 3e). Ce script les écrit dans `fiches/` sous forme de
manifestes `.json` *reproductibles* (uuid/alea figés) — exactement le
même format que les fiches sauvegardées via l'UI.

Pourquoi un script et pas écrire les JSON à la main ?
- une seule source de vérité pour 16 fiches : moins de copier-coller, et on
  vérifie au passage que les `id` MathALEA existent vraiment (sinon plantage
  net plutôt qu'URL silencieusement cassée).
- les fiches résultantes RESTENT la source de vérité : versionnées, ouvrables
  dans l'UI, régénérables par `python -m backend.cli build-all fiches/`.
- pour AJOUTER une fiche, soit on l'enregistre depuis l'UI, soit on ajoute
  une entrée à `LIBRARY` ci-dessous et on relance ce script.

Utilisation :
    python -m scripts.build_library            # écrit toute la bibliothèque
    python -m scripts.build_library --check    # vérifie sans rien écrire

Les `uuid` (5 hex) et `alea` (4 hex) sont des constantes mnémoniques —
n'importe quelle paire bien formée fonctionne ; on les fixe pour que les
URLs soient identiques d'une exécution à l'autre.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Permet `python scripts/build_library.py` ET `python -m scripts.build_library`.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.catalogue import index_titres  # noqa: E402
from backend.mathalea import build_url  # noqa: E402

FICHES_DIR = ROOT / "fiches"

# Mini-DSL : chaque exercice = (id, n, sup?). `n` = nombre de questions.
# `sup` est facultatif (réglages avancés MathALEA, dépendant de l'exercice ;
# on s'en tient ici aux variantes par défaut, plus sûres).
Exo = tuple  # (id: str, n: int, uuid: str, alea: str)


def _ex(id_: str, n: int, uuid: str, alea: str, **extra) -> dict:
    e = {"id": id_, "n": n, "uuid": uuid, "alea": alea}
    e.update(extra)
    return e


# --------------------------------------------------------------------------- #
# La bibliothèque. Une liste de manifestes prêts à l'emploi.
# Couvre les chapitres centraux du collège (6e -> 3e), 2-4 exercices par fiche,
# 3-4 questions par exo : un volume raisonnable pour une fiche imprimée recto.
# --------------------------------------------------------------------------- #
LIBRARY: list[dict] = [
    # ----------------------------- 6ème ----------------------------- #
    {
        "titre": "6ème — Nombres entiers, décimaux et repérage",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("6N10",   4, "6N101", "a601"),
            _ex("6N11",   3, "6N111", "a602"),  # lecture d'abscisse
            _ex("6N12",   4, "6N121", "a603"),
            _ex("6N31",   3, "6N311", "a604"),
        ],
    },
    {
        "titre": "6ème — Fractions et pourcentages",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("6N32",   3, "60321", "a611"),
            _ex("6N33",   4, "60331", "a612"),
            _ex("6N33-1", 4, "60332", "a613"),
        ],
    },
    {
        "titre": "6ème — Périmètres et aires",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("6M11-3", 3, "6M113", "a621"),  # périmètres (ordre du titre)
            _ex("6M11",   3, "6M111", "a622"),  # aires
            _ex("6M10",   2, "6M101", "a623"),  # problèmes mixtes
        ],
    },
    {
        "titre": "6ème — Angles : nommer et mesurer",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("6G22-1", 3, "60631", "a631"),  # vocabulaire
            _ex("6G22",   3, "60632", "a632"),  # nommer un angle
            _ex("6G23-4", 3, "60634", "a633"),  # mesurer avec rapporteur
        ],
    },

    # ----------------------------- 5ème ----------------------------- #
    {
        "titre": "5ème — Calcul littéral : écrire, réduire, calculer",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("5L10",   3, "50711", "a711"),
            _ex("5L12",   4, "50712", "a712"),
            _ex("5L14",   3, "50713", "a713"),
            _ex("5L15",   3, "50715", "a714"),
        ],
    },
    {
        "titre": "5ème — Fractions : comparer, simplifier, ratio",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("5N13",   3, "50721", "a721"),
            _ex("5N14",   3, "50722", "a722"),
            _ex("5N15",   3, "50723", "a723"),
        ],
    },
    {
        "titre": "5ème — Nombres relatifs : repérage et calculs",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("5R10",   4, "50731", "a731"),
            _ex("5R11",   3, "50732", "a732"),
            _ex("5R12",   3, "50733", "a733"),
        ],
    },
    {
        "titre": "5ème — Statistiques : lire et calculer",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("5S10",   2, "50741", "a741"),
            _ex("5S11",   3, "50742", "a742"),
            _ex("5S13",   3, "50743", "a743"),
            _ex("5S14",   3, "50744", "a744"),
        ],
    },

    # ----------------------------- 4ème ----------------------------- #
    {
        "titre": "4ème — Fractions : opérations",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("4C21",   4, "40811", "a811"),
            _ex("4C22",   4, "40812", "a812"),
            _ex("4C23",   3, "40813", "a813"),
        ],
    },
    {
        "titre": "4ème — Puissances et notation scientifique",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("4C30",   3, "40821", "a821"),
            _ex("4C32",   3, "40822", "a822"),
            _ex("4C33-3", 4, "40823", "a823"),
        ],
    },
    {
        "titre": "4ème — Théorème de Pythagore",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("4G20",   3, "40831", "a831"),  # calcul longueur
            _ex("4G21",   3, "40832", "a832"),  # nature triangle
            _ex("4G22",   2, "40833", "a833"),  # problèmes
        ],
    },
    {
        "titre": "4ème — Calcul littéral : distributivité et factorisation",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("4L10",   4, "40841", "a841"),
            _ex("4L11",   4, "40842", "a842"),
            _ex("4L14-1", 3, "40843", "a843"),  # tester une équation
        ],
    },

    # ----------------------------- 3ème ----------------------------- #
    {
        "titre": "3ème — Arithmétique : diviseurs et nombres premiers",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("3A10",   4, "30911", "a911"),
            _ex("3A10-3", 4, "30913", "a912"),  # décomposition
            _ex("3A11",   3, "30914", "a913"),  # irréductibilité
        ],
    },
    {
        "titre": "3ème — Calcul littéral : développer, factoriser, équations",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("3L11",   4, "30921", "a921"),
            _ex("3L11-7", 4, "30927", "a922"),  # (a+b)^2, (a-b)^2
            _ex("3L13",   3, "30923", "a923"),  # équation 1er degré
        ],
    },
    {
        "titre": "3ème — Trigonométrie : longueurs et angles",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("3G30-1", 3, "30931", "a931"),  # exprimer cos/sin/tan
            _ex("3G30",   3, "30932", "a932"),  # calcul longueur
            _ex("3G31",   3, "30933", "a933"),  # calcul angle
        ],
    },
    {
        "titre": "3ème — Fonctions affines et linéaires",
        "entete": {"classe": "", "date": ""},
        "mise_en_page": {"colonnes": 2, "corrige": True, "vue": "eleve"},
        "exercices": [
            _ex("3F10",   3, "30941", "a941"),  # tableau de valeurs
            _ex("3F12",   3, "30942", "a942"),  # calculs d'images
            _ex("3F21",   3, "30943", "a943"),  # déterminer fonction linéaire
        ],
    },
]

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _slug(titre: str) -> str:
    """Slugification minimale, identique à backend.fiches.slugify."""
    from backend.fiches import slugify
    return slugify(titre)


def _validate(fiche: dict, idx: dict[str, str]) -> list[str]:
    """Renvoie la liste des problèmes détectés (vide = OK)."""
    errs: list[str] = []
    seen_uuid: set[str] = set()
    for ex in fiche.get("exercices", []):
        if ex["id"] not in idx:
            errs.append(f"id inconnu : {ex['id']}")
        uid = ex.get("uuid")
        if uid:
            if uid in seen_uuid:
                errs.append(f"uuid dupliqué intra-fiche : {uid}")
            seen_uuid.add(uid)
    # build_url valide vue + structure
    try:
        url = build_url(fiche, vue=fiche["mise_en_page"].get("vue", "eleve"))
        if "?" not in url:
            errs.append("URL sans query string")
    except Exception as exc:  # noqa: BLE001
        errs.append(f"build_url a levé : {exc}")
    return errs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="Valide la bibliothèque sans écrire de fichier.")
    parser.add_argument("--dossier", type=Path, default=FICHES_DIR,
                        help="Où écrire (défaut : fiches/).")
    args = parser.parse_args(argv)

    idx = index_titres()
    total_err = 0
    for fiche in LIBRARY:
        errs = _validate(fiche, idx)
        slug = _slug(fiche["titre"])
        if errs:
            total_err += len(errs)
            print(f"  KO  {slug}")
            for e in errs:
                print(f"      - {e}")
            continue
        if args.check:
            print(f"  OK  {slug}  ({len(fiche['exercices'])} exos)")
            continue
        args.dossier.mkdir(parents=True, exist_ok=True)
        fiche_with_version = {"version": 1, **fiche}
        (args.dossier / f"{slug}.json").write_text(
            json.dumps(fiche_with_version, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  wrote {slug}.json  ({len(fiche['exercices'])} exos)")
    print(f"\n{len(LIBRARY)} fiches, {total_err} erreur(s).")
    return 1 if total_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
