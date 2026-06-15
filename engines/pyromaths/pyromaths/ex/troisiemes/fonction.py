# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006-2021 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
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

"""Exercices sur les fonctions"""

import math
import random

from pyromaths.classes.Vecteurs import Coordonnees2D
from pyromaths.ex import Jinja2Exercise
from pyromaths.outils.jinja2utils import facteur


class ExploiterEquationDeCourbe(Jinja2Exercise):
    """Exploiter une équation de courbe

    Cet exercice utilise l'appartenance d'un point à la courbe d'une fonction).
    """

    tags = [
        "Troisième",
        "Seconde",
        "1re technologique",
        "fonctions",
    ]
    filters = {"facteur": facteur, "pgcd": math.gcd}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sens = random.choice(("image-vers-antecedent", "antecedent-vers-image"))
        self.context = {
            "sens": sens,
            "f": random.choice("fghkpq"),
        }

        if sens == "image-vers-antecedent":
            a = random.choice([1, -1]) * random.randint(2, 9)
            b = random.choice([1, -1]) * random.randint(2, 9)

            def fonction(x):
                return a * x + b

            # Intersection avec l'axe des abscisses
            # On le calcule d'abord sans le signe, que l'on ajoute (éventuellement) à la fin
            if math.gcd(a, b) == 1:
                Cxfinal = fr"\frac{{ {abs(b)} }}{{ {abs(a)} }}"
            elif b % a == 0:
                Cxfinal = abs(b / a)
            else:
                Cxfinal = fr"\frac{{ {abs(b)//math.gcd(a, b)} }}{{ {abs(a)//math.gcd(a, b)} }}"

            if a * b > 0:
                self.context.update(
                    {
                        "Cxfinal": f"-{Cxfinal}",
                    }
                )
            else:
                self.context.update(
                    {
                        "Cxfinal": Cxfinal,
                    }
                )

            # Le point A est-il sur la courbe ?
            if random.choice([True, False]):
                x = random.randint(-10, 10)
                A = Coordonnees2D(x, fonction(x))
            else:
                A = Coordonnees2D(
                    random.randint(-10, 10),
                    random.randint(-10, 10),
                )

            # Trouver la valeur de x
            B = A.copy()
            while B.x == A.x:
                B.x = random.randint(-10, 10)
                B.y = fonction(B.x)

            self.context.update(
                {
                    "sens": sens,
                    "nature": "degre1",
                    "a": a,
                    "b": b,
                    "A": A,
                    "B": B,
                }
            )
        else:
            nature = random.choice(("degre1", "degre2"))
            self.context.update(
                {
                    "nature": nature,
                }
            )
            if nature == "degre1":
                a = random.choice([1, -1]) * random.randint(2, 9)
                b = random.choice([1, -1]) * random.randint(2, 9)

                def fonction(x):
                    return a * x + b

                self.context.update(
                    {
                        "a": a,
                        "b": b,
                        "C": Coordonnees2D(0, b),
                    }
                )
            elif nature == "degre2":
                a = random.choice([1, -1]) * random.randint(2, 9)
                b = random.choice([1, -1]) * random.randint(2, 9)
                c = random.choice([1, -1]) * random.randint(2, 9)

                def fonction(x):
                    return a * x ** 2 + b * x + c

                self.context.update(
                    {
                        "a": a,
                        "b": b,
                        "c": c,
                        "C": Coordonnees2D(0, c),
                    }
                )

            # Le point A est-il sur la courbe ?
            if random.choice([True, False]):
                x = random.randint(-10, 10)
                A = Coordonnees2D(x, fonction(x))
            else:
                A = Coordonnees2D(
                    random.randint(-10, 10),
                    random.randint(-100, 100),
                )

            # Trouver la valeur de y
            B = A.copy()
            while B.x == A.x:
                B.x = random.randint(-10, 10)
                B.y = fonction(B.x)

            self.context.update(
                {
                    "A": A,
                    "B": B,
                }
            )
