# CLAUDE.md — amorçage de « FicheLab »

> Lu automatiquement par **Claude Code** à l'ouverture de ce dossier. Amorce le pilotage.
> Ne pas supprimer. Jumeau de `AGENTS.md` (Codex) — garder les deux synchronisés.
> Discipline commune : `../_Atelier-IA/CHARTE-AIDD.md`.

## Ce qu'est ce projet
**Composeur visuel de fiches d'exercices de maths** : pilote le moteur public **MathALEA**
(CoopMaths) en composant des **URLs** — il **n'embarque aucun code MathALEA** (AGPL-3.0).
Profil : **B (appli Python)**. Rangement : `backend/`, `engines/`, `web/`, `fiches/`, `styles/`, `data/`.

## Comment travailler ici
Avant toute action, lis dans l'ordre :
1. `README.md` — rôle, principe/licence, architecture (source canonique).
2. `requirements.txt` / `.venv` — l'environnement.

Boucle : comprendre → modifier petit et traçable → **lancer/tester** → consigner.

## Frontières (profil B)
**Frontière de licence non négociable** : aucun code AGPL embarqué ; FicheLab compose des URLs
vers `coopmaths.fr/alea/`. Toute règle durable s'écrit dans le dépôt.
**À compléter** : un RUNBOOK court (démarrer le backend · servir `web/` · dépanner).

## Démarrage rapide
Installer : `pip install -r requirements.txt` (dans `.venv`). Lancer le backend puis ouvrir `web/`.
