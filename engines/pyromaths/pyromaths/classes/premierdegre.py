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

"""Quelques outils pour manipuler les équations et inéquations du premier degré."""

from fractions import Fraction
from ..outils.jinja2utils import facteur

# pylint: disable=invalid-name

INVERSESIGNE = {
    "<": ">",
    "=": "=",
    ">": "<",
    "≤": "≥",
    "≥": "≤",
}  #: Donne l'inverse des signes : `<` devient `>` (et inversement), `≤` devient `≥` (et inversement), `=` reste `=`.


def solution_equation(a, b, c, d):
    """Renvoit la solution de l'équation ax+b=cx+d.

    Les quatre nombres a, b, c, d sont des entiers, tels que d≠b et a≠c.

    La valeur retournée est un entier ou une :class:`fractions.Fraction`.
    """
    solution = Fraction(d - b, a - c)
    if solution == 0:
        return 0
    if solution.denominator == 1:
        return solution.numerator
    return solution


def resout_tex(a, b, signe, c, d):
    """Itère les étapes de résolution de l'équation ou inéquation ax+b<cx+d (ou >, ≤, ≥).

    * `a`, `b`, `c`, `d` sont des entiers
    * `signe` est un caractère parmi `=<>≤≥`.

    Les étapes itérées sont : ``(gauche, signe, droite, opération)``, avec :

    * `gauche` et `droite` : membres gauche et droite de l'(in)équation ;
    * `signe` : le symbole, parmi `=<>≤≥`.
    * `opération` : l'opération (par exemple `+2x`, `÷7`)
      qui sera la prochaine étape appliquée dans la résolution de l'(in)équation.
    """
    # De la forme ax+b=cx+d
    yield (
        f"""{facteur(a, "x*")}{facteur(b, "so")}""",
        signe,
        f"""{facteur(c, "x*")}{facteur(d, "so")}""",
        facteur(-c, "x*s"),
    )
    a = a - c

    # De la forme ax+b=d
    yield (
        f"""{facteur(a, "x*")}{facteur(b, "so")}""",
        signe,
        facteur(d, "o"),
        facteur(-b, "so"),
    )
    d = d - b

    # De la forme ax=d
    yield (
        facteur(a, "x*"),
        signe,
        facteur(d, "o"),
        fr"""\div {facteur(a, "p")}""",
    )
