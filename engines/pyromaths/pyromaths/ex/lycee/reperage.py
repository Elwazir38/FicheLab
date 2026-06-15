# Pyromaths
#
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
#
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
#

"""Repérage en seconde"""

import random

from pyromaths.ex import Jinja2Exercise
from pyromaths.outils.jinja2utils import facteur
from pyromaths.classes.Vecteurs import Coordonnees2D, Vecteur

POINTS = ("ABCD", "EFGH", "KLMN", "PQRS", "STUV")


def _triangle_quelconque():
    return [
        Coordonnees2D(random.randint(-10, 10), random.randint(-10, 10))
        for _ in range(3)
    ]


def _triangle_isocele():
    B = Coordonnees2D(random.randint(-10, 10), random.randint(-10, 10))
    translation = Vecteur(random.randint(-10, 10), random.randint(-10, 10))
    A = B + translation
    if random.random() > 0.5:
        # Échange les coordonnées x et y
        translation.x, translation.y = translation.y, translation.x
    C = B + Vecteur(
        random.choice((1, -1)) * translation.x,
        random.choice((1, -1)) * translation.y,
    )
    return A, B, C


def _triangle_rectangle():
    B = Coordonnees2D(random.randint(-10, 10), random.randint(-10, 10))
    translation = Vecteur(random.randint(-10, 10), random.randint(-10, 10))
    A = B + translation
    C = B + random.choice((-2, 2)) * Vecteur(translation.y, -translation.x)
    return A, B, C


def _triangle_isocele_rectangle():
    B = Coordonnees2D(random.randint(-10, 10), random.randint(-10, 10))
    translation = Vecteur(random.randint(-10, 10), random.randint(-10, 10))
    A = B + translation
    C = B + random.choice((-1, 1)) * Vecteur(translation.y, -translation.x)
    return A, B, C


class BilanDistanceMilieu(Jinja2Exercise):
    """Calcul de distances et de coordonnées du milieu."""

    tags = [
        "Seconde",
        "coordonnées",
        "géométrie",
        "repérage",
    ]
    filters = {"facteur": facteur}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        points = random.choice(
            (
                _triangle_quelconque,
                _triangle_isocele,
                _triangle_rectangle,
                _triangle_isocele_rectangle,
            )
        )

        while True:
            A, B, C = points()
            if Vecteur.points(A, B).colineaire(Vecteur.points(A, C)):
                # Les trois points sont alignés
                # Cela inclut le cas où deux points sont confondus
                continue
            if (
                abs(Vecteur.points(A, B))[0] == 1
                or abs(Vecteur.points(A, C))[0] == 1
                or abs(Vecteur.points(B, C))[0] == 1
            ):
                # Les distances AB, BC, AC ne sont pas des carrés parfaits
                continue
            if (
                abs(Vecteur.points(A, B))[1] == 1
                or abs(Vecteur.points(A, C))[1] == 1
                or abs(Vecteur.points(B, C))[1] == 1
            ):
                # Les distances AB, BC, AC ne sont pas des nombres entiers
                continue
            break

        noms = random.choice(POINTS)

        AB = abs(Vecteur.points(A, B))
        AC = abs(Vecteur.points(A, C))
        BC = abs(Vecteur.points(B, C))

        self.context = {
            # Coordonnées des trois sommets
            "A": A,
            "B": B,
            "C": C,
            # Longueurs des trois segments, sous la forme (a, b), où la norme est égale à a*sqrt(b)
            "AB": AB,
            "AC": AC,
            "BC": BC,
            # Coordonnées du milieu, et du quatrième sommet
            "I": (A + C) / 2,
            "D": A + C - B,
            # Noms des quatre sommets
            "nA": noms[0],
            "nB": noms[1],
            "nC": noms[2],
            "nD": noms[3],
            # Noms du triangle et du parallélogramme
            "nABC": noms[0:3],
            "nABCD": noms,
            # Booléens disant si le triangle ABC est isocèle ou rectangle
            "isocele": AB == BC,
            "rectangle": AC[0] ** 2 * AC[1] == AB[0] ** 2 * AB[1] + BC[0] ** 2 * BC[1],
        }
