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

"""Des trucs pour bidouiller les tags de Pyromaths"""

import argparse
import ast
import base64
import inspect
import logging
import os
import subprocess
import sys
import tempfile
import textwrap

import pyromaths
from pyromaths.cli import PyromathsException
from pyromaths.ex import ExerciseBag
from pyromaths.ex import NIVEAUX

# Logging configuration
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()

EDITOR = "vim"

################################################################################
# Modification des tags d'un ou plusieurs exercices


def _cherche_affectation_tags(exercice):
    """Cherche la ligne et le fichier où est défini la liste des tags de l'argument."""
    fichier = inspect.getfile(exercice)
    with open(fichier, encoding="utf8") as source:
        arbre = ast.parse(source.read())

    for node in ast.iter_child_nodes(arbre):
        if isinstance(node, ast.ClassDef) and node.name == exercice.name():
            for subnode in ast.iter_child_nodes(node):
                if isinstance(subnode, ast.Assign):
                    if subnode.targets[0].id == "tags":
                        return (
                            fichier,
                            (subnode.lineno, subnode.end_lineno),
                            subnode.col_offset,
                        )

    raise ValueError(
        "Exercice non trouvé. Merci de signaler un bug : https://framagit.org/pyromaths/pyromaths/-/issues"  # pylint: disable=line-too-long
    )


def edit_tags(exercice, tous):
    """Ouvre un éditeur de texte pour modifier la liste des tags de l'exercice."""
    with tempfile.TemporaryDirectory() as tempdir:
        tempname = os.path.join(tempdir, f"{exercice.name()}.txt")

        with open(tempname, mode="w", encoding="utf8") as temp:
            # Préparation
            temp.write(
                textwrap.dedent(
                    f"""\
                    ################################################################################
                    # Exercice {exercice.name()} ({exercice.description()})
                    ################################################################################
                    #
                    # Modifiez les tags de l'exercice en les (dé)commentant,
                    # puis quittez en sauvegardant le fichier.
                    #
                    # Vous pouvez ajouter de nouveaux tags.
                    #
                    # Pour annuler les modifications, enregistrez un fichier vide.
                    ################################################################################
                    """
                )
            )
            for tag in sort_tags(tous):
                if tag in exercice.tags:
                    temp.write(f"{tag}\n")
                else:
                    temp.write(f"# {tag}\n")

        # Édition
        print(
            [
                os.environ.get("EDITOR", EDITOR),
                tempname,
            ]
        )
        subprocess.run(
            [
                os.environ.get("EDITOR", EDITOR),
                tempname,
            ],
            check=True,
        )

        # Relecture
        with open(tempname, mode="r", encoding="utf8") as temp:
            lecture = temp.read()
            if not lecture.strip():
                return None
            return [
                ligne.strip()
                for ligne in lecture.split("\n")
                if ligne.strip() and not ligne.strip().startswith("#")
            ]


def sort_tags(tags):
    """Renvoit une liste triée des tags.

    D'abord les niveaux (en conservant l'ordre de la variable NIVEAUX),
    puis les autres tags par ordre alphabétique (en ignorant la casse).
    """
    return list(tag for tag in NIVEAUX if tag in tags) + list(
        sorted(set(tags) - set(NIVEAUX), key=str.lower)
    )


def set_tags(exercice, tags):
    """Ré-écrit l'exercice donné en remplaçant les tags.

    :param pyromaths.ex.TexExercise exercice: Exercice
    :param list tags: Liste des tags (chaînes de caractères).
    """
    fichier, limites, indentation = _cherche_affectation_tags(exercice)

    with open(fichier, mode="r", encoding="utf8") as source:
        lignes = source.readlines()

    with open(fichier, mode="w", encoding="utf8") as source:
        for i, ligne in enumerate(lignes):
            if limites[0] == i + 1:
                source.write(f"""{" " * indentation}tags = [\n""")
                for tag in tags:
                    source.write(f"""{" " * indentation}    "{tag}",\n""")
                source.write(f"""{" " * indentation}]\n""")
            elif limites[0] <= i + 1 <= limites[1]:
                pass
            else:
                source.write(ligne)


def do_edit(options):
    """Modifie les tags

    :param options: Objet renvoyé par `argparse.ArgumentParser.parse_args`.
    """
    bag = ExerciseBag()
    if options.exercice == ["ALL"]:
        options.exercice = list(sorted(bag.keys()))
    if not set(options.exercice) <= set(bag):
        raise PyromathsException(
            "Les identifiants suivants ne sont pas des exercices : {}.".format(
                ", ".join(sorted(set(options.exercice) - set(bag), key=str.lower))
            )
        )

    with tempfile.TemporaryDirectory() as tempdir:
        pdf = os.path.join(tempdir, "exercice.pdf")
        with open(pdf, mode="wb") as pdffile:
            # Plus petit PDF valide selon
            # https://stackoverflow.com/questions/17279712/what-is-the-smallest-possible-valid-pdf#comment59467299_17280876
            pdffile.write(
                base64.b64decode(
                    "JVBERi0xLjAKMSAwIG9iajw8L1BhZ2VzIDIgMCBSPj5lbmRvYmogMiAwIG9iajw8L0tpZHNbMyAw\nIFJdL0NvdW50IDE+PmVuZG9iaiAzIDAgb2JqPDwvTWVkaWFCb3hbMCAwIDMgM10+PmVuZG9iagp0\ncmFpbGVyPDwvUm9vdCAxIDAgUj4+Cg=="  # pylint: disable=line-too-long
                )
            )
        subprocess.run(["gio", "open", pdf], check=True)

        touslestags = set(bag.tags())
        for exo in options.exercice:
            logging.info(f"Traitement le l'exercice {exo}…")
            os.rename(bag[exo]().generate(dir=tempdir), pdf)
            tags = edit_tags(bag[exo], touslestags)
            if tags is None:
                logging.warning(f"{exo}: Aucun tag. Abandon.")
                continue
            logging.info(f"Modification des tags de l'exercice {exo}.")
            set_tags(bag[exo], tags)
            touslestags.update(tags)


################################################################################
# Renommage d'un tag


def do_rename(options):
    """Renomme un tag.

    :param options: Objet renvoyé par `argparse.ArgumentParser.parse_args`.
    """
    source = options.source
    dest = options.dest

    bag = ExerciseBag()
    tags = set(bag.tags())

    if source in NIVEAUX:
        raise PyromathsException(
            f"""Ce logiciel ne permet pas de renommer un niveau. Commencez par le renommer « à la main » en modifiant la variable "NIVEAUX" dans le fichier "{inspect.getfile(pyromaths.ex)}", puis relancez cette commande."""  # pylint: disable=line-too-long
        )

    for exo in bag.values():
        tags = exo.tags
        if source not in tags:
            continue
        logging.info(f"Modification des tags de l'exercice {exo.name()}.")
        tags.remove(source)
        tags.append(dest)
        set_tags(exo, tags)


################################################################################
# Ligne de commande


def argument_parser():
    """Return an argument parser"""
    parser = argparse.ArgumentParser(
        prog="pyromaths._bidouilles.tag",
        description=textwrap.dedent(
            """\
                Des outils pour bidouiller les tags de Pyromaths.
                """
        ),
    )
    subparsers = parser.add_subparsers(title="Commandes", dest="commande")
    subparsers.required = True
    subparsers.dest = "commande"

    # Change les tags d'un ou plusieurs exercices
    edit = subparsers.add_parser(
        "edit",
        help="Modifie les tags d'un ou plusieurs exercices.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    edit.add_argument(
        "exercice",
        nargs="+",
        type=str,
        default=None,
        help="Nom des exercices dont il faut éditer les tags.",
    )

    # Renomme un tag
    rename = subparsers.add_parser(
        "rename",
        help="Renomme un tag.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    rename.add_argument(
        "source",
        type=str,
        help="Ancien nom.",
    )
    rename.add_argument(
        "dest",
        type=str,
        help="Nouveau nom.",
    )

    return parser


COMMANDES = {
    "edit": do_edit,
    "rename": do_rename,
}


def main():
    """Main function"""
    options = argument_parser().parse_args(sys.argv[1:])

    try:
        COMMANDES[options.commande](options)
    except PyromathsException as error:
        logging.error(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
