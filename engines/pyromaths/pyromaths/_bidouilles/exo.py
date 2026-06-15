#!/usr/bin/env python3

# Copyright (C) 2021 -- Louis Paternault (spalax@gresille.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

"""Manipulation des exercices"""

import argparse
import gettext
import logging
import os
import pathlib
import subprocess
import sys
import tempfile
import textwrap
import unittest

from pyromaths.cli import PyromathsException
from pyromaths.ex import ExerciseBag

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def root():
    """Renvoit la racine du dépôt."""
    repertoire = pathlib.Path(__file__).parent
    while not (repertoire / ".git" / "config").is_file():
        if repertoire == repertoire.parent:
            raise OSError("Impossible de trouver la racine du dépôt.")
        repertoire = repertoire.parent
    return repertoire


def argument_parser():
    """Return an argument parser"""
    parser = argparse.ArgumentParser(
        prog="bidouilles exo",
    )
    subparsers = parser.add_subparsers(title="Commands", dest="command")
    subparsers.required = True
    subparsers.dest = "command"

    # Rename
    rename = subparsers.add_parser(
        "rename",
        help="Renomme un exercice",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    rename.add_argument(
        "old",
        type=str,
        help="Ancien nom.",
    )
    rename.add_argument(
        "new",
        type=str,
        help="Nouveau nom.",
    )

    return parser


def do_rename(options):
    """Renomme un exercice"""
    os.chdir(root())
    old = options.old
    new = options.new

    # Vérifie que l'ancien et le nouveau nom sont corrects
    bag = ExerciseBag()
    if old not in bag:
        raise PyromathsException(f"Exercice '{old}' introuvable.")
    if new in bag:
        raise PyromathsException(f"L'exercice '{new}' existe déjà.")

    # Vérifie que le dépôt est propre
    completed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    if completed.stdout:
        logging.error(
            """Cette commande ne fonctionne que dans un dépôt git propre (sans fichiers modifiés). Veuillez "nettoyer" votre dépôt (avec `git commit`, `git stash`, `git checkout`, ou autre) et recommencer."""
        )
        raise PyromathsException("Abandon…")

    # Collecte de tous les fichiers gérés par git
    depot = [
        pathlib.Path(nom)
        for nom in subprocess.run(
            ["git", "ls-files", "--full-name", "-z"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.split("\x00")
        if nom
    ]

    # Renomme les fichiers
    for (
        nom
    ) in (
        depot.copy()
    ):  # On itère sur une copie car la liste va être modifiée dans la boucle
        if nom.name.startswith(old):
            nouveaunom = str(nom.parent / nom.name.replace(old, new))
            logging.info(f"""Renommage de "{nom}" en "{nouveaunom}"…""")
            subprocess.run(
                ["git", "mv", str(nom), nouveaunom],
                check=True,
            )
            depot.remove(nom)
            depot.append(nouveaunom)

    # Modifie les fichiers
    logging.info(f"""Modification des fichiers…""")
    subprocess.run(
        ["sed", "--in-place=~", f"s/{old}/{new}/g"] + depot,
        check=True,
        capture_output=True,
    )

    # Fini !
    logging.info(
        textwrap.dedent(
            f"""
    Terminé ! Cette opération est un peu risquée, et vous DEVEZ maintenant vérifier que tout s'est bien passé :

    - vérifiez que les tests passent toujours : `utils/bidouille test check` ;
    - vérifiez que l'exercice fonctionne toujours : `utils/pyromaths generate {new}` ;
    - re-générez les vignettes : `utils/creer-vignettes.py` ;
    - soyez prudent en validant les modifications : `git add -p`.

    Bon courage !
    """.strip()
        )
    )


COMMANDS = {
    "rename": do_rename,
}


def main(argv=None):
    """Main function"""
    if argv is None:
        argv = sys.argv[1:]
    options = argument_parser().parse_args(argv)

    try:
        COMMANDS[options.command](options)
    except PyromathsException as error:
        logging.error(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
