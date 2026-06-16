# AGENTS.md — amorçage de « FicheLab »

> Lu automatiquement par **Codex** à l'ouverture de ce dossier. Amorce le pilotage.
> Ne pas supprimer. Jumeau de `CLAUDE.md` (Claude Code) — garder les deux synchronisés.
> Discipline commune : `../_Atelier-IA/CHARTE-AIDD.md`.

## Ce qu'est ce projet
**Composeur visuel de fiches d'exercices de maths** avec **génération PDF
100 % locale** via le moteur **Pyromaths** (vendorisé sous GPLv3 dans `engines/`).
Tu choisis des exercices dans le catalogue, tu règles la fiche, tu génères le PDF
hors-ligne avec ton style maison (couleur, établissement, police).
Profil : **B (appli Python)**. Rangement : `backend/`, `engines/`, `web/`, `fiches/`, `styles/`, `fonts/`.

## Comment travailler ici
Avant toute action, lis dans l'ordre :
1. `README.md` — rôle, architecture, format de fiche (source canonique).
2. `RUNBOOK.md` — démarrage, tests, dépannage.
3. `requirements.txt` / `.venv` — l'environnement.

Boucle : comprendre → modifier petit et traçable → **lancer/tester** → consigner.

## Frontières (profil B)
**Licence — GPLv3** (cohérent avec Pyromaths vendorisé). Toute règle durable
s'écrit dans le dépôt.
**Frontière technique** : la génération de fiches reste **locale** ; pas
d'appel sortant à un service tiers depuis l'app. Le pipeline LLM optionnel
(LM Studio en local) suit la même règle.

## Démarrage rapide
Installer : `pip install -r requirements.txt` puis `pip install -e engines\pyromaths`
(dans `.venv`). Lancer `uvicorn backend.app:app --reload` puis ouvrir `http://localhost:8000`.
