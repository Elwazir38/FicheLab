# engines/ — moteurs vendorisés

## pyromaths/

Clone de **Pyromaths** (générateur d'exercices de maths avec corrigés détaillés).

- Origine : https://framagit.org/pyromaths/pyromaths (GPLv3, Framasoft).
- État amont : gelé (dernière activité ~2023).
- Installé en editable dans le venv du projet : `pip install -e engines/pyromaths`.

### Patchs de portage Python 3.14 (appliqués localement)

Le code amont vise Python 3.7–3.9 et ne tourne pas tel quel sur 3.14. Trois
modifications minimales, sans toucher aux exercices :

1. `pyromaths/__init__.py` — suppression de
   `__import__('pkg_resources').declare_namespace(...)` (mécanisme de namespace
   legacy ; `pkg_resources` n'existe plus par défaut sur 3.14).
2. `pyromaths/directories.py` — `DATADIR` résolu via `os.path.dirname(__file__)`
   au lieu de `pkg_resources.resource_filename`.
3. `pyromaths/outils/System.py` — `write_pdf()` passe désormais
   l'environnement **complet** (`os.environ.copy()`) à `latexmk` ; avec un env
   restreint, MiKTeX ne voit pas son état (`LOCALAPPDATA`) et refuse de compiler.

Les `SyntaxWarning` (séquences d'échappement non-raw du vieux code) sont
inoffensifs et masqués au chargement (`backend/pyromaths_engine.py`).

### Licence

Pyromaths est sous **GPLv3**. Tant que l'usage reste local, la vendorisation et
ces patchs sont sans contrainte ; une distribution publique du tout déclencherait
les obligations de la GPL.
