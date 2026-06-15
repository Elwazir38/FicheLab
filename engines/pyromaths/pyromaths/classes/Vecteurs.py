#!/usr/bin/env python3
#
# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006-2021 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
# Copyright (C) 2018-2021 -- Louis Paternault (spalax@gresille.org)
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

"""Coordonnées et vecteurs."""


import math
import numbers
import random

from .Racine import simplifie_racine


class Coordonnees2D:
    """Coordonnées en deux dimensions : abscisse, ordonnée, et plein de méthodes pour les manipuler."""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, coord):
        """Teste l'égalité entre deux coordonnées"""
        return (self.x == coord.x) and (self.y == coord.y)

    def __add__(self, coord):
        """Addition"""
        return self.__class__(self.x + coord.x, self.y + coord.y)

    def __sub__(self, coord):
        """Soustraction"""
        return self.__class__(self.x - coord.x, self.y - coord.y)

    def __mul__(self, c):
        """Multiplication par un nombre"""
        if isinstance(c, numbers.Real):
            return self.__class__(c * self.x, c * self.y)

    def __rmul__(self, c):
        """Multiplication Reverse"""
        if isinstance(c, float) or isinstance(c, int):
            return self * c

    def __neg__(self):
        """Négatif d'une coordonnées"""
        return -1 * self

    def __truediv__(self, c):
        if isinstance(c, numbers.Real):
            return self.__class__(self.x / c, self.y / c)

    def __abs__(self):
        r"""Retourne la distance à l'origine sous la forme `(entier, radicande)`,  avec : `abs(self)=entier * sqrt(radicande)`."""
        return simplifie_racine(self.x ** 2 + self.y ** 2)

    def __str__(self):
        """Affichage sous forme de coordonnées"""
        return "(" + str(self.x) + "," + str(self.y) + ")"

    @classmethod
    def points(cls, A, B):
        """Renvoit le vecteur AB."""
        return cls(B.x - A.x, B.y - A.y)

    def colineaire(self, other):
        """Teste si les deux vecteurs (self et other) sont colinéaires."""
        return self.x * other.y - self.y * other.x == 0

    def normeTex(self):
        """Affichage TeX de la racine simplifiée de la racine, sans les dollars."""
        norme = abs(self)
        if norme[0] == 1:
            return "\sqrt{" + str(norme[1]) + "}"
        elif norme[1] == 1:
            return str(norme[0])
        else:
            return str(norme[0]) + "\sqrt{" + str(norme[1]) + "}"

    def copy(self):
        """Renvoit une copie de cet objet."""
        return self.__class__(self.x, self.y)


class Vecteur(Coordonnees2D):
    """Vecteur en deux dimensions

    Cette classe n'apporte (au moment où j'écris ces lignes) rien de plus que
    la classe Coordonnees2D. Mais elle a été écrite plus tôt, et quand j'ai eu
    besoin d'une classe pour représenter les coordonnées d'un point, je n'ai
    pas voulu utiliser la classe Vecteur de peur que des modifications
    ultérieures à la classe Vecteur ne vienne casser mes points.
    """

    pass


def randvect(a, b):
    """Retourne un vecteur aléatoire et s'occupe de placer l'abscisse au-dessus de a et l'ordonnée dans [0,b]. Il faut que b>=10."""
    x = random.randint(-5, 5)
    y = random.randint(-5, 5)
    posx = a + max(1 - x, 1)  # # 1 colonne minimum d'écart
    if y >= 0:
        posy = (
            random.randint(0, math.fabs(y - 2)) + 1
        )  # # Ajouter 1 pour éviter de coller au bas de la grille
    else:
        posy = random.randint(
            math.fabs(y), b
        )  # # Comme y < 0, cela ne colle pas au bas de la grille
    return [Vecteur(x, y), posx, posy]
