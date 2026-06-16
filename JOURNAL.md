# JOURNAL — FicheLab

Notes datées des passes de travail. Une entrée par session significative,
focus sur ce qui a changé et **pourquoi**, pas sur "comment". Un changement
de code est dans `git` ; ici on capture le contexte décisionnel.

---

## 2026-06-16 — Excision MathALEA : on devient mono-moteur Pyromaths

**Pourquoi.** L'app avait deux moteurs : MathALEA (composeur d'URLs qui ouvre
`coopmaths.fr` pour compiler) et Pyromaths (local). En usage réel, le moteur
MathALEA cassait la promesse de l'app : il fallait *quitter* FicheLab pour finir
le PDF côté CoopMaths. Rachid n'utilisait que la moitié locale. Choix : couper
proprement la moitié MathALEA et repositionner le projet comme « moteur Pyromaths
local + UI propre ». Le diff parle de lui-même : -32 fichiers (module, données
brutes, scaffold de bibliothèque MathALEA, 17 fiches `.json` qui pointaient vers
des `id` MathALEA inexistants après suppression).

**Ce qui a été retiré.**
- `backend/mathalea.py` (composition d'URL, spec dérivée de createURL.ts).
- `backend/catalogue.py` (lisait `data/mathalea_raw/`).
- `backend/tests/test_mathalea.py` (couvrait le builder d'URL).
- `data/mathalea_raw/` (référentiels officiels + specs `.ts`).
- `scripts/build_library.py` et `scripts/__init__.py` (scaffold de la
  bibliothèque MathALEA, devenu sans objet).
- 17 fiches collège auto-générées + la démo `demo-4eme-fractions.json`.
- Côté UI : `src-tabs` MathALEA/Pyromaths, iframe d'aperçu live, onglets de vue
  (Élève/Diaporama/LaTeX), bouton « PDF MathALEA », réglages avancés `s/s2/s3`.

**Ce qui a été refondu.**
- `backend/app.py` : route `/api/catalogue` retourne maintenant directement le
  catalogue Pyromaths (`pyromaths_engine.list_exercices()`). Route
  `/api/fiche/preview` et `/api/catalogue/pyromaths` retirées.
- `backend/cli.py` : subcommandes `build` / `url` / `build-all` retirées ;
  reste `pyromaths-list` et `pyromaths-gen`.
- `backend/tests/test_bibliotheque.py` : ne valide plus les `id` MathALEA ;
  contrôle structure minimale + présence du `name` Pyromaths.
- `web/index.html` + `web/app.js` : moteur unique. La colonne 3 devient
  « Génération » (note explicative + gros bouton « Générer le PDF »).
- `web/onboarding.js` : étape ③ reformulée (plus de double bouton PDF).
- `README.md`, `CLAUDE.md`, `AGENTS.md`, `RUNBOOK.md` : refonte. La feuille de
  route pointe vers CM1/CM2 (BO 17 avril 2025) et la Seconde (à partir des
  générateurs Pyromaths `lycee/` réellement programme Seconde).

**Décision conservée.** Le champ `source` reste dans le format de fiche, même
s'il vaut systématiquement `"pyromaths"` aujourd'hui. Raison : un moteur LLM
local (contextes d'énoncés générés par Gemma / Qwen-Coder via LM Studio) est
prévu en phase 4, et garder le discriminant maintenant évite une migration de
format dans deux semaines.

**Frontière de licence — clarifiée.** Plus aucune ambiguïté AGPL : il ne reste
que Pyromaths (GPLv3, vendorisé) et le code maison sous GPLv3. La mention
« n'embarque aucun code MathALEA (AGPL) » disparaît du README parce qu'il n'y
a plus d'interaction du tout avec MathALEA — pas même par URL.

**Garde-fous.** Commit cohérent en un seul `git commit` (recommandation
d'advisor) pour que le diff reste lisible. Tests `backend/tests/` à relancer
après cette session — adapter le seuil de `test_dossier_fiches_non_vide`
(plus que 1 fiche livrée tant que la phase 3 CM1/CM2 n'est pas faite).

## 2026-06-15 — Couche de prise en main (onboarding) sur une UI déjà aboutie

**Pourquoi.** L'interface était déjà un design system fini (tokens `--brand-*`/`--amber-*`,
gradients, animations sobres, accessibilité clavier). Le manque n'était pas esthétique mais
**cognitif** : un nouvel utilisateur ouvre trois colonnes et ne sait pas par où commencer, ni
ce que fait « graine », ni la différence entre les deux boutons PDF (le point le plus déroutant :
MathALEA ouvre coopmaths.fr pour compiler, Pyromaths génère un PDF en local via LaTeX). On
**n'a pas refait l'UI** — on a ajouté une couche de guidage qui s'y fond, **100 % additive et
réversible**.

**Ce qui a été ajouté.**
- `web/onboarding.js` (nouveau, chargé après `app.js`) : panneau de bienvenue 1re visite réutilisant
  `.modal`/`.modal-back`, mémorisé via `localStorage` clé `fichelab:onboarded` ; bouton « ⓘ Guide »
  dans la topbar pour le rouvrir ; fermeture Échap + clic hors-modal (ces handlers n'existaient pas,
  on les a posés localement sans toucher la modale existante) ; gestion du focus ; échappatoire
  `?guide=skip` pour démos/captures.
- `web/index.html` : bouton « ⓘ Guide », état vide `#fiche-empty` enrichi (« Étape ② »), note
  explicative `#pdf-note` (« Étape ③ ») au-dessus de `.preview-foot`, `title=` sur vues + boutons PDF.
- `web/app.js` : `title=` sur graine (= reproductibilité), Réglages avancés s/s2/s3, dans les
  templates de `renderExoRow` (markup passif, survit aux re-renders, retrait propre).
- `web/style.css` : section commentée « COUCHE PRISE EN MAIN » en fin de fichier, **zéro couleur
  en dur**, uniquement des tokens existants ; placée avant le bloc `prefers-reduced-motion` qui
  reste la dernière règle et continue de neutraliser toute animation.

**Garde-fous.** `#preview-hint` est réécrit par `refreshPreview()` à chaque appel : on ne l'a donc
pas édité (on a ajouté `#pdf-note` en élément frère). Offline préservé (aucun CDN/police distante).
Vérifié en vrai sur `http://localhost:8010` (capture headless Chrome) : modale de bienvenue au 1er
lancement, bouton Guide, note PDF, états vides parlants, tooltips servis.

## 2026-06-15 — CI pytest + publication GitHub

**Levier.** Git venait d'être posé (entrée précédente) mais restait **local** :
ni filet de sécurité automatique (les tests ne tournaient qu'à la main), ni
sauvegarde hors-machine. Brancher une CI et publier le dépôt transforme « 32
tests verts chez moi » en « 32 tests verts vérifiés à chaque push, pour tout
le monde ». C'est la suite logique et le dernier maillon de l'armature.

**Ce qui a été ajouté.**
- `.github/workflows/ci.yml` — GitHub Actions : `pytest backend/tests` sur
  `push` et `pull_request`, matrice Python 3.11 / 3.12 / 3.13. **Aucune chaîne
  LaTeX installée** : choix permis par le fait que les tests Pyromaths sont
  « sans compilation » (catalogue, reproductibilité par graine, injection du
  template au niveau chaîne) — CI rapide (~15 s/job) et sans dépendance lourde.
- Dépôt **public** publié : https://github.com/Elwazir38/FicheLab (GPLv3,
  cohérent avec l'esprit libre du projet et Pyromaths vendorisé).

**Vérification.**
- Run CI `27571209872` : **✓ vert sur les 3 versions** (3.11/3.12/3.13).
- `git ls-remote origin` : `master` présent, 3 commits poussés.

**Frictions traversées (pour mémoire).**
- `gh` installé mais hors PATH du shell → appelé par chemin complet.
- Push initial **rejeté** : le token OAuth n'avait pas le scope `workflow`
  (GitHub interdit de pousser `.github/workflows/` sans lui — défense contre
  l'injection de CI). Résolu par `gh auth refresh -s workflow`.

**Reste à faire (non bloquant).** Annotation GitHub : `checkout@v4` /
`setup-python@v5` tournent sur Node 20 (déprécié, bascule Node 24 le
16/06/2026) — avertissement seulement, la CI ne casse pas ; à relever lors
d'une passe de maintenance. Toujours en suspens : dossier `fonts/` absent,
`pyproject.toml` si la config se densifie.

---

## 2026-06-15 — Mise sous contrôle de version + armature de projet

**Levier.** L'outil était fonctionnel (32 tests verts) mais vivait **hors
Git**, dans OneDrive — alors que toute la doctrine le présuppose : le JOURNAL
parle de « git (le futur) », le CLAUDE.md exige que « toute règle durable
s'écrive dans le dépôt », le README qualifie les fiches de « versionnables ».
Sans dépôt : aucune historisation, aucun rollback, et un risque réel de
corruption via la synchro OneDrive. C'était le manque n°1, en amont de tout
le reste. Choix : poser l'armature manquante d'un coup plutôt que du code
fonctionnel — la valeur ici est la traçabilité, pas une feature de plus.

**Ce qui a été ajouté / corrigé.**
- `git init` + commit initial (`95b836f`, 449 fichiers suivis).
- `LICENSE` — **GPLv3**, texte officiel verbatim (réutilisé depuis
  `engines/pyromaths/COPYING`). Choix dicté par la vendorisation de Pyromaths
  (GPLv3) dans `engines/` : distribuer l'ensemble sous GPLv3 est le seul choix
  juridiquement sûr. FicheLab déclarait scrupuleusement la licence *des autres*
  (MathALEA AGPL non embarqué) mais n'avait pas la sienne.
- `.gitignore` — `.venv`, caches Python, PDF temporaires, artefacts OneDrive.
- `.gitattributes` — normalisation LF dans le dépôt.
- **Pyromaths réellement vendorisé** : le `.git` imbriqué a été supprimé.
  Avant, `git add` le voyait comme un *gitlink* (`Am engines/pyromaths`) — un
  simple pointeur de sous-module, sans les fichiers. Après suppression :
  **390 fichiers source tracés**. C'est ce qui rend le choix GPLv3 cohérent
  (le code GPL est présent et tracé, pas juste référencé).
- Nettoyage des sauvegardes manuelles `web/*.AVANT-design-web.*` (rôle rendu
  obsolète par Git).
- Dépendance de test déclarée : `requirements-dev.txt` (`pytest>=9.0`,
  installé via `-r requirements.txt`) ; `requirements.txt` et la section
  « Tests » du README pointent désormais dessus, au lieu du `pip install
  pytest` en commentaire.

**Vérification.**
- `pytest backend\tests` : **32 passed** — inchangé avant/après la
  vendorisation (le moteur Pyromaths s'importe et tourne toujours).
- `git ls-files engines/pyromaths` : 390 fichiers (vendorisation réelle, pas
  un gitlink). `git status` : arbre propre.
- `pip install -r requirements-dev.txt --dry-run` : résolu sans conflit.

**Frontière de licence — respectée.** Aucun code MathALEA (AGPL) embarqué.
Pyromaths (GPLv3) est vendorisé *et* la distribution est désormais sous GPLv3,
ce qui lève l'ambiguïté précédente (code GPL présent sans licence déclarée).

**Reste à faire (non bloquant).** Dossier `fonts/` documenté mais absent
(doc ≠ réalité) ; pas de CI (possible maintenant que Git existe, utile si
push distant) ; envisager `pyproject.toml` si la config se densifie.

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
