"""Construction d'URL MathALEA à partir d'un manifeste de fiche.

Spec dérivée fidèlement de `src/lib/createURL.ts` du dépôt officiel
coopmaths/mathalea (forge.apps.education.fr, projet 451).

Principe : on ne fait que *composer une URL* vers le site public
https://coopmaths.fr/alea/ . Aucun code de MathALEA (AGPL-3.0) n'est
embarqué — l'app pilote le moteur public, comme le ferait un signet.

Convention d'URL (un bloc de paramètres répété par exercice, dans cet
ordre ; createURL.ts) :

    uuid, id, n, d, s, s2, s3, s4, s5, qcm, i, cd, tip, cols, alea

puis un paramètre global de vue `v` (VueType.ts) :

    alacarte diaporama can eleve latex pdf raw confeleve amc anki
    moodle l l2 overview myriade indices indice tools check-test

Reproductibilité : `uuid` (clé d'instance) et `alea` (graine du hasard)
sont *gelés* dans le manifeste — régénérer une fiche redonne exactement
les mêmes énoncés et le même corrigé.
"""
from __future__ import annotations

import secrets
from urllib.parse import urlencode

#: URL du moteur public MathALEA (point d'entrée unique, modifiable ici).
MATHALEA_BASE_URL = "https://coopmaths.fr/alea/"

#: Vues valides, copiées de src/lib/VueType.ts.
VUES = {
    "alacarte", "diaporama", "can", "eleve", "latex", "pdf", "raw",
    "confeleve", "amc", "anki", "moodle", "l", "l2", "overview",
    "myriade", "indices", "indice", "tools", "check-test",
}

#: Vue par défaut pour l'aperçu interactif (côté élève).
VUE_APERCU = "eleve"
#: Vue par défaut pour l'export imprimable (page LaTeX -> PDF de MathALEA).
VUE_EXPORT = "latex"

#: Clés de réglages supplémentaires d'un exercice (sup), telles quelles dans l'URL.
SUP_KEYS = ("s", "s2", "s3", "s4", "s5")


def short_token(n_chars: int = 5) -> str:
    """Petit jeton aléatoire hexadécimal, à l'image des uuid/alea du site."""
    return secrets.token_hex((n_chars + 1) // 2)[:n_chars]


def freeze_runtime_ids(exercice: dict) -> dict:
    """Renvoie une copie de l'exercice avec `uuid` et `alea` garantis.

    Appelé au moment où un exercice est ajouté à une fiche : fige les
    identifiants pour rendre la fiche reproductible. Idempotent.
    """
    e = dict(exercice)
    if not e.get("uuid"):
        e["uuid"] = short_token(5)
    if not e.get("alea"):
        e["alea"] = short_token(4)
    return e


def _coerce(value) -> str:
    """Sérialise une valeur de paramètre comme l'attend MathALEA."""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def build_pairs(fiche: dict, vue: str | None = None) -> list[tuple[str, str]]:
    """Construit la liste ordonnée des couples (clé, valeur) de la query.

    Renvoie une *liste* (et non un dict) car plusieurs clés se répètent
    — un bloc `uuid,id,n,...` par exercice. Fonction pure.
    """
    mep = fiche.get("mise_en_page", {}) or {}
    cols = mep.get("colonnes")
    corrige = mep.get("corrige", True)

    pairs: list[tuple[str, str]] = []
    for ex in fiche.get("exercices", []):
        # Ignore les exercices non-MathALEA (ex. Pyromaths) dans une fiche mixte.
        if ex.get("source") not in (None, "mathalea") or not ex.get("id"):
            continue
        e = freeze_runtime_ids(ex)
        # Ordre identique à createURL.ts.
        pairs.append(("uuid", e["uuid"]))
        pairs.append(("id", _coerce(e["id"])))
        pairs.append(("n", _coerce(e.get("n", 1))))
        if e.get("d") is not None:
            pairs.append(("d", _coerce(e["d"])))
        sup = e.get("sup") or {}
        for key in SUP_KEYS:
            if sup.get(key) is not None:
                pairs.append((key, _coerce(sup[key])))
        if e.get("qcm") is not None:
            pairs.append(("qcm", _coerce(e["qcm"])))
        if e.get("interactif") in (True, "1", 1):
            pairs.append(("i", "1"))
        # Correction détaillée : réglage par exercice sinon réglage de la fiche.
        cd = e.get("cd")
        if cd is None:
            cd = "1" if corrige else "0"
        pairs.append(("cd", _coerce(cd)))
        if cols is not None:
            pairs.append(("cols", _coerce(cols)))
        pairs.append(("alea", e["alea"]))

    v = vue or mep.get("vue") or VUE_APERCU
    if v:
        if v not in VUES:
            raise ValueError(f"Vue MathALEA inconnue : {v!r} (cf. VUES)")
        pairs.append(("v", v))
    return pairs


def build_url(fiche: dict, vue: str | None = None) -> str:
    """Manifeste de fiche -> URL MathALEA complète et prête à ouvrir."""
    return MATHALEA_BASE_URL + "?" + urlencode(build_pairs(fiche, vue))
