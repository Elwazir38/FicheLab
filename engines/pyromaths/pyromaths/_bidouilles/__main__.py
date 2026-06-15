#!/usr/bin/env python3

# Copyright (C) 2016-2021 -- Louis Paternault (spalax@gresille.org)
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

"""Des trucs pour bidouiller Pyromaths"""

import argparse
import logging
import runpy
import sys

from pyromaths.cli import PyromathsException

VERSION = "0.1.0"

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

COMMANDES = {
    "tag": "Manipule les tags",
    "test": "Effectue des tests",
    "exo": "Manipulation des exercices",
}


def argument_parser():
    """Return an argument parser"""
    parser = argparse.ArgumentParser(
        prog="bidouilles",
        description=(  # pylint: disable=line-too-long
            "Des outils pour bidouiller Pyromaths. Ce programme est destiné aux développeur·euse·s de Pyromaths, et ne doit être utilisé QUE depuis les sources (le dépôt git) de Pyromaths."
        ),
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s {version}'.format(version=VERSION),
        )
    subparsers = parser.add_subparsers(title="Commandes", dest="commande")
    subparsers.required = True
    subparsers.dest = "commande"

    # Définition des sous-commandes
    for commande, description in COMMANDES.items():
        subparsers.add_parser(commande, help=description)

    return parser


def main():
    """Main function"""
    try:
        if len(sys.argv) >= 2 and sys.argv[1] in COMMANDES:
            # On court-circuite argparse pour laisser le sous-module faire
            # l'analyse de la liste des arguments.
            commande = sys.argv[1]
            sys.argv[0] = ".".join(sys.argv[0:2])
            del sys.argv[1]
            runpy.run_module(f"{__package__}.{commande}", run_name="__main__")
        else:
            argument_parser().parse_args(sys.argv[1:])
    except PyromathsException as error:
        logging.error(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
