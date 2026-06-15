"""Chemin de quelques répertoires propres à Pyromaths."""

import os
import sys

# Portage Python 3.12+/3.14 : pkg_resources (setuptools) n'est plus disponible.
# Le dossier `data` est livré dans le paquet, à côté de ce fichier.
DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
EXODIR = os.path.join(DATADIR, "exercices")
LOCALEDIR = os.path.join(DATADIR, "locale")
HOME = os.path.expanduser("~")

if os.name == 'nt': # Windows
    CONFIGDIR = os.path.join(os.environ['APPDATA'], "pyromaths")
elif sys.platform == "darwin":  # Mac OS X
    CONFIGDIR = os.path.join(HOME, "Library", "Application Support", "Pyromaths")
else: # Linux (et autres ?)
    CONFIGDIR = os.path.join(HOME, ".config", "pyromaths")

