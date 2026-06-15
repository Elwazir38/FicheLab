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

"""Quelques outils pour manipuler les ensembles de nombres.

.. note::

    Ce module pourrait être très riche ; chacune de ses classes pourrait mettre en œuvre de nombreuses fonctionnalités.
    Nous nous sommes limités à ce qui était réellement utilisé dans les exercices.
    Ce sera complété au fur et à mesure des besoins.

Les ensembles considérés ici sont des ensembles de nombres réels, au sens de :class:`numbers.Real`.

>>> from pyromaths.classes.ensembles import *
"""

import decimal
import numbers
import re

from ..outils.jinja2utils import tex


class EnsembleReels:
    """Ensemble de nombres réels.

    Cette classe est (quasi-)abstraite, et n'implémente presque aucune fonctionnalité.
    Tous les ensembles en hérite.
    """

    # pylint: disable=too-few-public-methods

    def __contains__(self, item):
        """Renvoit `True` si `item` est dans l'ensemble.

        :meta public:
        """
        raise NotImplementedError()

    def tex(self):
        """Renvoit la représentation en LaTeX de l'ensemble."""
        raise NotImplementedError()


class EnsembleVide(EnsembleReels):
    """Ensemble vide."""

    def __contains__(self, item):
        """Renvoit `False`."""
        return False

    def __repr__(self):
        return "∅"

    @staticmethod
    def tex():
        return r"\emptyset{}"


class TousLesReels(EnsembleReels):
    r"""Ensemble de tous les réels :math:`\mathbb{R}`."""

    def tex(self):
        return r"\mathbb{R}"

    def __repr__(self):
        return "ℝ"

    def __contains__(self, item):
        return isinstance(item, numbers.Real)


class UnionDisjointe(EnsembleReels):
    """Union d'ensembles disjoints.

    Pour le moment, seules les unions d'intervalles sont considérés (voire l'union de deux intervalle).

    :param list ensembles: Liste des sous-ensembles.
    """

    def __init__(self, *ensembles):
        super().__init__()
        self.ensembles = ensembles

    def __contains__(self, item):
        return any(item in ensemble for ensemble in self.ensembles)

    def tex(self):
        return r" \cup ".join(tex(ensemble) for ensemble in self.ensembles)

    def __repr__(self):
        return " ∪ ".join(str(ensemble) for ensemble in self.ensembles)


RE_INTERVALLE = re.compile(
    r"^ *(?P<crochetg>[\[\]]) *(?P<gauche>[-.0-9]+) *; *(?P<droite>[-.0-9]+) *(?P<crochetd>[\[\]]) *$"
)


class Intervalle(EnsembleReels):
    """Intervalle.

    :param str crochetg: Crochet gauche : `[` ou `]`.
    :param str crochetd: Crochet droit : `[` ou `]`.
    :param number.Real gauche: Borne inférieure.
    :param number.Real droite: Borne supérieure.

    >>> from fractions import Fraction
    >>> Intervalle("[", -3, Fraction(4, 5), "[")
    [ -3 ; Fraction(4, 5) [
    >>> -3 in Intervalle("[", -3, Fraction(4, 5), "[")
    True
    >>> Fraction(4, 5) in Intervalle("[", -3, Fraction(4, 5), "[")
    False

    Il est aussi possible de calculer des :meth:`unions <Intervalle.__add__>` et :meth:`intersections <Intervalle.__mul__>` d'intervalles.
    """

    def __init__(self, crochetg, gauche, droite, crochetd):
        super().__init__()
        if crochetg not in "[]" or crochetd not in "[]":
            raise ValueError("Brackets must be '[' or ']'.")
        if gauche > droite:
            raise ValueError(
                "La borne inférieure doit être inférieure à la borne supérieure."
            )

        self.crochetg = crochetg
        self.crochetd = crochetd
        self.gauche = gauche
        self.droite = droite

    @classmethod
    def from_str(cls, string):
        """Contsruit un intervalle à partir d'une chaîne de caractères.

        >>> Intervalle.from_str("[1;2]")
        [ 1 ; 2 ]

        >>> Intervalle.from_str("[-2.5;.2]")
        [ Decimal('-2.5') ; Decimal('0.2') ]

        :Exceptions:

        >>> Intervalle.from_str("[2;1]")
        Traceback (most recent call last):
        ...
        ValueError: La borne inférieure doit être inférieure à la borne supérieure.


        >>> Intervalle.from_str("[2;1")
        Traceback (most recent call last):
        ...
        ValueError: Cannot parse interval.

        >>> Intervalle.from_str("[2.2.1;1]")
        Traceback (most recent call last):
        ...
        ValueError: Cannot parse interval.
        """
        if match := RE_INTERVALLE.match(string):
            groups = match.groupdict()
            try:
                if "." in groups["gauche"]:
                    gauche = decimal.Decimal(groups["gauche"])
                else:
                    gauche = int(groups["gauche"])
                if "." in groups["gauche"]:
                    droite = decimal.Decimal(groups["droite"])
                else:
                    droite = int(groups["droite"])
            except ArithmeticError as error:
                raise ValueError("Cannot parse interval.") from error

            return cls(
                groups["crochetg"],
                gauche,
                droite,
                groups["crochetd"],
            )
        raise ValueError("Cannot parse interval.")

    @classmethod
    def from_inequation(cls, signe, nombre):
        """Construit un intervalle à partir d'une inéquation de type :math:`x<7`.

        L'inéquation peut être stricte ou large, dans un sens ou dans l'autre.

        >>> Intervalle.from_inequation("≤", 7)
        ] -∞ ; 7 ]
        >>> Intervalle.from_inequation(">", 1.5)
        ] 1.5 ; +∞ [
        >>> Intervalle.from_inequation("<", float("inf"))
        ℝ
        """
        if signe in "<≤" and nombre == float("inf"):
            return TousLesReels()
        if signe in ">≥" and nombre == float("-inf"):
            return TousLesReels()
        if signe == "<":
            return cls("]", float("-inf"), nombre, "[")
        if signe == ">":
            return cls("]", nombre, float("inf"), "[")
        if signe == "≤":
            return cls("]", float("-inf"), nombre, "]")
        if signe == "≥":
            return cls("[", nombre, float("inf"), "[")

        raise ValueError(
            """L'argument `signe` doit être une chaîne d'une lettre parmi "<>≤≥"."""
        )

    def __contains__(self, item):
        """Renvoit `True` si `item` est un élément de l'intervalle.

        >>> 0 in Intervalle.from_str("[1;3]")
        False
        >>> 1 in Intervalle.from_str("[1;3]")
        True
        >>> 2 in Intervalle.from_str("[1;3]")
        True
        >>> 3 in Intervalle.from_str("[1;3]")
        True
        >>> 4 in Intervalle.from_str("[1;3]")
        False
        >>> 1 in Intervalle.from_str("]1;3[")
        False
        >>> 3 in Intervalle.from_str("]1;3[")
        False

        """
        return (
            (item == self.gauche and self.crochetg == "[")
            or self.gauche < item < self.droite
            or (item == self.droite and self.crochetd == "]")
        )

    def __repr__(self):
        if self.gauche == float("-inf"):
            gauche = "-∞"
        else:
            gauche = repr(self.gauche)
        if self.droite == float("inf"):
            droite = "+∞"
        else:
            droite = repr(self.droite)
        return f"{self.crochetg} {gauche} ; {droite} {self.crochetd}"

    def tex(self):
        texte = ""
        texte += fr"""\left{self.crochetg}"""
        if self.gauche == float("-inf"):
            texte += r"-\infty "
        else:
            texte += tex(self.gauche)
        texte += " ; "
        if self.droite == float("inf"):
            texte += r"+\infty "
        else:
            texte += tex(self.droite)
        texte += fr"""\right{self.crochetd}"""
        return texte

    def __mul__(self, other):
        """Renvoit l'intersection de deux intervalles.

        >>> Intervalle.from_str("[0 ; 2]") * Intervalle.from_str("[1 ; 3]")
        [ 1 ; 2 ]
        >>> Intervalle.from_str("[0 ; 1]") * Intervalle.from_str("[2 ; 3]")
        ∅
        >>> Intervalle.from_str("[0 ; 1[") * Intervalle.from_str("[1 ; 3]")
        ∅
        >>> Intervalle.from_str("[0 ; 3[") * Intervalle.from_str("[1 ; 2]")
        [ 1 ; 2 ]
        """
        if not isinstance(other, self.__class__):
            raise TypeError(f"L'autre opérande doit être de type '{self.__class__}'.")

        if self.gauche < other.gauche:
            int1, int2 = self, other
        else:
            int1, int2 = other, self

        if int1.droite < int2.gauche:
            return EnsembleVide()
        if int1.droite == int2.gauche and (
            int1.crochetd == "[" or int2.crochetg == "]"
        ):
            return EnsembleVide()

        # Crochets ouverts ou fermés ?
        if int2.gauche in int1 and int2.gauche in int2:
            crochetg = "["
        else:
            crochetg = "]"

        if (
            min(int1.droite, int2.droite) in int1
            and min(int1.droite, int2.droite) in int2
        ):
            crochetd = "]"
        else:
            crochetd = "["

        return self.__class__(
            crochetg,
            max(int1.gauche, int2.gauche),
            min(int1.droite, int2.droite),
            crochetd,
        )

    def __add__(self, other):
        """Renvoit l'union de deux intervalles.

        >>> Intervalle.from_str("[0 ; 2]") + Intervalle.from_str("[1 ; 3]")
        [ 0 ; 3 ]
        >>> Intervalle.from_str("[0 ; 1]") + Intervalle.from_str("[2 ; 3]")
        [ 0 ; 1 ] ∪ [ 2 ; 3 ]
        >>> Intervalle.from_str("[0 ; 1[") + Intervalle.from_str("[1 ; 3]")
        [ 0 ; 3 ]
        >>> Intervalle.from_str("[0 ; 3[") + Intervalle.from_str("[1 ; 2]")
        [ 0 ; 3 ]
        >>> Intervalle.from_inequation("≤", 0) + Intervalle.from_inequation("≥", 0)
        ℝ
        """
        if not isinstance(other, self.__class__):
            raise TypeError(f"L'autre opérande doit être de type '{self.__class__}'.")

        if self.gauche < other.gauche:
            int1, int2 = self, other
        else:
            int1, int2 = other, self

        if int1.droite >= int2.gauche:
            # Les deux intervalles se chevauchent peut-être

            if float("-inf") in (int1.gauche, int2.gauche) and float("inf") in (
                int1.droite,
                int2.droite,
            ):
                return TousLesReels()

            # Les deux intervalles ont peut-être la même borne inférieure.
            # Le crochet est-il ouvert ou fermé ?
            # De même pour la borne supérieure
            crochetg = int1.crochetg
            if int1.gauche == int2.gauche and "[" in (int1.gauche, int2.gauche):
                crochetg = "["

            crochetd = int2.crochetd
            if int1.droite == int2.droite and "]" in (int1.droite, int2.droite):
                crochetd = "]"

            return self.__class__(
                crochetg,
                min(int1.gauche, int2.gauche),
                max(int1.droite, int2.droite),
                crochetd,
            )

        # Les deux intervalles sont disjoints
        return UnionDisjointe(int1, int2)
