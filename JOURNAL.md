# JOURNAL — FicheLab

Notes datées des passes de travail. Une entrée par session significative,
focus sur ce qui a changé et **pourquoi**, pas sur "comment". Un changement
de code est dans `git` (le futur) ; ici on capture le contexte décisionnel.

---

## 2026-06-14 — Bibliothèque d'amorce 6e–3e (16 fiches)

**Levier.** Avant ce passage, FicheLab livrait 2 fiches d'exemple
(`demo-4eme-fractions.json`, `exemple-pyromaths-4e.json`) — l'outil était
techniquement complet mais "vide" d'usage. Choix : pousser le contenu, pas
la robustesse (la chaîne `mathalea.py` est déjà couverte et `latexmk` n'a
pas changé). 1 prof qui ouvre FicheLab après ce passage a 16 fiches prêtes
à imprimer ; c'est de la valeur immédiate.

**Ce qui a été ajouté.**
- `scripts/build_library.py` — scaffold qui décrit la bibliothèque
  ([id, n, uuid, alea] par fiche) et l'écrit dans `fiches/`. Une seule
  source de vérité, ids vérifiés contre `index_titres()` avant écriture,
  garde anti-doublon `uuid` intra-fiche.
- `fiches/` — 16 nouvelles fiches `.json` reproductibles : 4 par niveau
  (6e/5e/4e/3e), 2–4 exercices, 2 colonnes, corrigé activé, vue élève.
  Couvre les chapitres centraux du collège (nombres, calcul littéral,
  fractions, géo, Pythagore, trigo, fonctions, arithmétique, stats).
- `backend/tests/test_bibliotheque.py` — garde-fou qui parcourt
  `fiches/*.json` et vérifie pour chaque fiche : structure minimale, vue
  MathALEA valide, ids présents dans le catalogue, URL d'export se compose
  et contient un bloc `id=` par exercice **dans l'ordre** (`parse_qsl`,
  pas `count`, pour ne pas confondre `id` et `uuid`). Reste valide quand
  une fiche n'a que des exercices Pyromaths.

**Vérification.**
- `pytest backend\tests` : **32 passed in 0.20s** (13 avant, 19 nouveaux
  via paramétrisation sur les fiches livrées).
- `python -m backend.cli build-all fiches\ --no-open` : URL composée pour
  chacune des 18 fiches (16 nouvelles + 2 anciennes), pas d'erreur.

**Suivi de revue (code-reviewer, armoire globale).**
- Collisions `uuid` inter-fiches signalées (`60101`, `60111`) : renommées en
  `6N101`/`6M101`/`6N111`/`6M111` — plus mnémoniques (préfixe = code-thème),
  plus aucune collision.
- Ordre incohérent dans `6eme-perimetres-et-aires` (aires avant
  périmètres alors que le titre dit l'inverse) : inversé.
- Titre `6eme-nombres-entiers-et-decimaux` jugé trompeur (`6N11` est du
  repérage, pas du calcul décimal) : retitré "Nombres entiers, décimaux
  et repérage" (l'ancien fichier orphelin a été supprimé).
- Suggestion non-suivie : splitter la fiche stats 5e en deux niveaux. La
  variété d'un seul fichier (lecture + calcul) reste utile pour une fiche
  de révision ; à revoir si retour terrain négatif.

**Frontière de licence — respectée.** Le scaffold importe uniquement
`backend.catalogue` (lecture du référentiel local) et `backend.mathalea`
(composition d'URLs). Aucun code MathALEA (AGPL) n'a été embarqué.

**Comment ajouter une fiche.**
- Via l'UI : composer → "Enregistrer" → fichier écrit dans `fiches/`.
- À la main : copier un `.json` existant, éditer.
- Reproductible en lot : ajouter une entrée à `LIBRARY` dans
  `scripts/build_library.py` puis relancer `python -m scripts.build_library`.
