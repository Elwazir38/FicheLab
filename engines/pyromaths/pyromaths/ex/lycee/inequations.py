# Pyromaths
#
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
#
# Copyright (C) 2021-2022 -- Louis Paternault (spalax@gresille.org)
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

"""Résolution d'inéquations"""

# pylint: disable=invalid-name

import math
import random

from pyromaths.ex import Jinja2Exercise
from pyromaths.outils.jinja2utils import facteur
from pyromaths.classes import premierdegre, ensembles


def _contexte_inequation():
    a = b = c = d = 0
    while (
        a == c
        or abs(c - a) == 1
        or abs(a) == 1
        or abs(c) == 1
        or 0 in {a, b, c, d}
        or b == d
    ):
        a = random.randint(-9, 9)
        b = random.randint(-9, 9)
        c = random.randint(-9, 9)
        d = random.randint(-9, 9)
        symbole = random.choice("<>≤≥")

    solution = {}
    if a - c > 0:
        solution["symbole"] = symbole
    else:
        solution["symbole"] = premierdegre.INVERSESIGNE[symbole]
    solution["valeur"] = premierdegre.solution_equation(a, b, c, d)

    return {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "symbole": symbole,
        "solution": solution,
        "etapes": list(premierdegre.resout_tex(a, b, symbole, c, d)),
    }


class InequationPremierDegre(Jinja2Exercise):
    """Résoudre une inéquation du premier degré"""

    tags = [
        "Troisième",
        "inéquation",
    ]

    filters = {"facteur": facteur}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = _contexte_inequation()


class CoupleInequationsPremierDegre(Jinja2Exercise):
    """Résoudre un couple inéquations du premier degré"""

    tags = [
        "Seconde",
        "inéquation",
        "intervalles",
    ]

    filters = {"facteur": facteur}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        while True:
            eq1 = _contexte_inequation()
            eq2 = _contexte_inequation()

            if abs(eq1["solution"]["valeur"] - eq2["solution"]["valeur"]) <= 1:
                continue

            break

        self.context = {}
        for i, inequation in enumerate((eq1, eq2)):
            for key, value in inequation.items():
                self.context[f"{key}{i+1}"] = value

        self.context["etou"] = random.choice(("et", "ou"))
        self.context["min"] = (
            math.floor(
                min(
                    float(self.context["solution1"]["valeur"]),
                    float(self.context["solution2"]["valeur"]),
                )
                / 5
                - 0.1
            )
            * 5
        )
        self.context["max"] = (
            math.ceil(
                max(
                    float(self.context["solution1"]["valeur"]),
                    float(self.context["solution2"]["valeur"]),
                )
                / 5
                + 0.1
            )
            * 5
        )

        solutions = tuple(
            ensembles.Intervalle.from_inequation(
                self.context[f"solution{i}"]["symbole"],
                self.context[f"solution{i}"]["valeur"],
            )
            for i in range(1, 3)
        )
        if self.context["etou"] == "et":
            self.context["solution"] = solutions[0] * solutions[1]
        else:
            self.context["solution"] = solutions[0] + solutions[1]
