# Pyromaths
#
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
#
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

"""Outils à facilitant l'écriture d'exercices avec Jinja2
"""

import fractions
import math
import numbers

import jinja2


class LatexEnvironment(jinja2.Environment):
    """Environnement (au sens jinja2) utilisé pour les templates des exercices.

    :meta private:
    """

    # pylint: disable=too-many-instance-attributes, too-few-public-methods

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.block_start_string = "(*"
        self.block_end_string = "*)"
        self.variable_start_string = "(("
        self.variable_end_string = "))"
        self.comment_start_string = "(% "
        self.comment_end_string = " %)"
        self.trim_blocks = True
        self.lstrip_blocks = True


def facteur(
    nombre,
    court="",
    parentheses=False,
    zero=False,
    arrondi=None,
    signe=False,  # pylint: disable=redefined-outer-name
    operation=False,
    produit=False,
    variable="",
):
    r"""Renvoit le code :math:`LaTeX` correspondant au nombre, dans un ``\\numprint{}``, en gérant de nombreux cas particuliers.

    Les cas d'utilisation de cette fonction sont détaillés dans le :ref:`tutoriel pour écrire un nouvel exercice <ecrire-facteur>`.

    En utilisant les arguments, cette fonction permet de prendre en compte les arrondis, et de nombreux cas particuliers (dans chaque cas, c'est le 3 qui est destiné à être rendu par cette fonction.

    - ajout de parenthèses uniquement si nécessaire (produit `2×3` et `2×(-3)` plutôt que `2×-3` ou `2×(3)`) ;
    - ajout du signe, même s'il est positif (produit `1+3x` et `1-3x` plutôt que `1 3x` ou `1+-3x`) ;
    - n'affiche pas le nombre 1, et seulement le signe de -1 (produit `x` et `-x` plutôt que `1x` et `-1x`) ;
    - n'affiche pas l'opérande nulle d'un produit (produit `2` plutôt que `2+0x`) ;
    - etc.

    Le séparateur décimal est le point, mais celui-ci sera converti en une virgule par ``\\numprint{}``.

    :param numbers.Real nombre: Nombre à formatter (il peut aussi être de type :class:`decimal.Decimal`).
    :param str court: Version courte des arguments (voir plus loin).
    :param boolean parentheses: Encadre le nombre avec des parenthèses, s'il est négatif (utile pour produire `2×(-3)` plutôt que `2×3`).
    :param int arrondi: Arrondi le nombre. L'argument est le nombre de chiffres après la virgule à utiliser. Mettre cet argument à ``None`` pour ne pas arrondir.
    :param boolean zero: Ajoute des zéros à la fin du nombre pour avoir autant de chiffres que défini par `arrondi` (par exemple, avec cette option et un arrondi au centième, `2` devient `2.00`).
    :param boolean signe: Produit le signe, même si le nombre est positif (produit alors un +).
    :param boolean operation: Indique que le signe plus ou moins est une opération (comme `2-3`) et non pas un opérateur unaire (comme `2×(-3)`). Cela a pour effet d'espacer un peu le signe du nombre.
    :param boolean produit: Le facteur est une opérande d'un produit : le nombre 1 ne doit pas être affiché ; du nombre -1, on ne conserve que le signe ; rien n'est affiché si le nombre est 0 (pour produire `x`, `-x` ou rien plutôt que `1x`, `-1x`, `0x`).
    :param str variable: Seconde opérande du produit. Doit être du code :math:`LaTeX` valide.
    :return: Le nombre, formatté comme du code :math:`LaTeX`.
    :rtype: str

    :Dépendances entre arguments:

    - Le comportement n'est pas défini si les arguments ``operation`` et ``parentheses`` sont utilisées en même temps.

    :Version courte des arguments:

    Pour que les arguments soient moins verbeux, il est possible d'utiliser la version courte des arguments. Par exemple, ``facteur(2, produit=True, parentheses=True, arrondi=3)`` peut s'écrire comme ``facteur(2, '*p3')``.

    Cet argument est une chaîne de caractères, chaque caractère « activant » une option longue. Par exemple ``*p3`` active les options ``produit``, ``parentheses`` et ``arrondi=3``. L'ordre des caractères n'a aucune importance. Plusieurs comportement sont non-définis :

    - présence de caractères ne correspondant à aucun argument ;
    - utilisation conjointe des arguments courts et longs ;
    - utilisation de plusieurs chiffres (pour l'argument ``arrondi``).

    Les arguments sont :

    - ``p``: ``parentheses`` ;
    - ``z``: ``zero`` ;
    - ``s``: ``signe`` ;
    - ``o``: ``operation`` ;
    - ``*``: ``produit`` ;
    - chiffres ``0`` à ``9``: ``arrondi`` à l'entier correspondant ;
    - ``x``, ``X``, ``y``, ``Y``, ``n``, ``N`` : Raccourcis pour (respectivement) ``variable="x"``, ``variable="x^2"``, ``variable="y"``, ``variable="y^2"``, ``variable="n"``, ``variable="n^2"``.

    :Exemples:

    Cas de base
        >>> from pyromaths.outils.jinja2utils import facteur
        >>> facteur(2)
        \numprint{2}
        >>> facteur(2.0)
        \numprint{2}
        >>> facteur(2.3)
        \numprint{2.3}
        >>> facteur(-122.0)
        \numprint{-122}

    Arrondi
        >>> facteur(12345.6789, arrondi=None)
        \numprint{12345.6789}
        >>> facteur(12345.6789, arrondi=0)
        \numprint{12346}
        >>> facteur(12345.6789, arrondi=2)
        \numprint{12345.68}
        >>> facteur(.6789, arrondi=0)
        \numprint{1}
        >>> facteur(.6789, arrondi=2)
        \numprint{0.68}

    Zéro
        >>> facteur(12345.6789, arrondi=None, zero=True)
        \numprint{12345.6789}
        >>> facteur(12345, arrondi=2, zero=True)
        \numprint{12345.00}
        >>> facteur(12345, arrondi=2, zero=False)
        \numprint{12345}
        >>> facteur(12345.7, arrondi=2, zero=True)
        \numprint{12345.70}
        >>> facteur(12345.7, arrondi=2, zero=False)
        \numprint{12345.7}

    Parenthèse
        >>> facteur(-2, parentheses=True)
        \left(\numprint{-2}\right)
        >>> facteur(2, parentheses=True)
        \numprint{2}

    Signe
        >>> facteur(-2, signe=True)
        \numprint{-2}
        >>> facteur(2, signe=True)
        \numprint{+2}
        >>> facteur(2, signe=False)
        \numprint{2}

    Opération
        >>> facteur(-2, operation=False)
        \numprint{-2}
        >>> facteur(2, signe=True, operation=False)
        \numprint{+2}
        >>> facteur(-2, operation=True)
        -\numprint{2}
        >>> facteur(2, signe=True, operation=True)
        +\numprint{2}

    Produit
        >>> facteur(1, produit=True, variable="x")
        x
        >>> facteur(-1, produit=True, variable="x")
        -x
        >>> facteur(0, produit=True, variable="x")
        <BLANKLINE>
        >>> facteur(1, produit=False, variable="x")
        \numprint{1}\,x

    Variable
        >>> facteur(2, variable="x")
        \numprint{2}\,x
        >>> facteur(-1, produit=True, variable="x")
        -x

    Version courte des arguments
        >>> facteur(-2, court="2zXo")
        -\numprint{2.00}\,x^2
        >>> facteur(-2, court="2zXp")
        \left(\numprint{-2.00}\,x^2\right)
        >>> facteur(-3, court="2zY")
        \numprint{-3.00}\,y^2
        >>> facteur(-1, court="y*")
        -y
        >>> facteur(1, court="p*x")
        x
        >>> facteur(-1, court="p*x")
        \left(-x\right)
        >>> facteur(-2, court="p*x")
        \left(\numprint{-2}\,x\right)
        >>> facteur(2, court="p*x")
        \numprint{2}\,x
        >>> facteur(1, court="s*x")
        +x

    Fractions
        >>> from fractions import Fraction
        >>> facteur(Fraction(-2, 5), court="p")
        \left(-\frac{\numprint{2}}{\numprint{5}}\right)
        >>> facteur(Fraction(7, 1))
        \numprint{7}
        >>> facteur(Fraction(3, 2))
        \frac{\numprint{3}}{\numprint{2}}

    """

    # pylint: disable=too-many-arguments, too-many-return-statements, too-many-branches, too-many-statements

    # Format court des arguments
    if "p" in court:
        parentheses = True
    if "z" in court:
        zero = True
    if "s" in court:
        signe = True
    if "o" in court:
        operation = True
    if "*" in court:
        produit = True
    if "x" in court:
        variable = "x"
    if "y" in court:
        variable = "y"
    if "n" in court:
        variable = "n"
    if "X" in court:
        variable = "x^2"
    if "Y" in court:
        variable = "y^2"
    if "N" in court:
        variable = "n^2"
    for entier in range(10):
        if str(entier) in court:
            arrondi = entier

    # Cas particuliers : produit
    if produit:
        if nombre == 1:
            if operation or signe:
                return "+{}".format(variable)
            return variable
        if nombre == -1:
            if operation:
                return "-{}".format(variable)
            if parentheses:
                return r"\left(-{}\right)".format(variable)
            return "-{}".format(variable)
        if nombre == 0:
            return ""

    # Division du nombre en signe et valeur absolue
    absolu = abs(nombre)
    if signe and nombre >= 0:
        plusoumoins = "+"
    elif nombre < 0:
        plusoumoins = "-"
    else:
        plusoumoins = ""

    # Conversion du nombre en prenant compte de l'arrondi et des zéros
    # Je n'ai pas réussi à faire ça uniquement à coup de
    # str.format(). Je serai ravi si quelqu'un me prouvait que
    # c'est possible !
    numprint = True
    if arrondi is None:
        if (
            isinstance(absolu, fractions.Fraction)
            and absolu.denominator != 1
            and absolu.numerator != 0
        ):
            numprint = False
            strabsolu = f"{plusoumoins}{tex(absolu)}"
        elif round(absolu) == absolu:
            strabsolu = str(int(absolu))
        else:
            strabsolu = str(absolu)
    elif arrondi == 0:
        strabsolu = f"{round(absolu):g}"
    else:
        entier = math.trunc(absolu)
        decimal = str(round(absolu - entier, arrondi))[2:]
        if zero:
            strabsolu = f"{entier}.{decimal:0<{arrondi}}"
        elif entier == absolu:
            strabsolu = f"{entier}"
        else:
            strabsolu = f"{entier}.{decimal}"

    # Ajout éventuel d'une espace devant la variable
    if variable:
        variable = r"\," + variable

    # Ajout éventuel des parenthèses
    # pylint: disable=no-else-return
    if parentheses and nombre < 0:
        if numprint:
            return fr"\left(\numprint{{{plusoumoins}{strabsolu}}}{variable}\right)"
        else:
            return fr"\left({strabsolu}{variable}\right)"
    elif numprint:
        if operation:
            return fr"{plusoumoins}\numprint{{{strabsolu}}}{variable}"
        else:
            return fr"\numprint{{{plusoumoins}{strabsolu}}}{variable}"
    else:
        return fr"{strabsolu}{variable}"


def iter_facteurs(liste, short):
    """Applique :func:`facteur` à une liste de nombres.

    - Les éléments peuvent être des nombres, ou pas (auquel cas la fonction :func:`str` est appliquée).
    - L'argument ``short`` est transmis à :func:`facteur`.
    """
    for element in liste:
        if isinstance(element, numbers.Number):
            yield facteur(element, short)
        else:
            yield str(element)


def matrice(listes, short=""):
    r"""Renvoit le code LaTeX d'une matrice.

    - La matrice est sous la forme d'une liste de lignes (où chaque ligne est une liste de coefficients).
    - L'argument ``short`` est transmis à :func:`facteur`.

    >>> from pyromaths.outils.jinja2utils import matrice
    >>> matrice([[1, 2], [3, 4]])
    \begin{pmatrix}\numprint{1} & \numprint{2}\\\numprint{3} & \numprint{4}\\\end{pmatrix}
    """
    text = ""
    text += r"\begin{pmatrix}"
    for ligne in listes:
        text += " & ".join(iter_facteurs(ligne, short))
        text += r"\\"
    text += r"\end{pmatrix}"

    return text


def signe(nombre):
    """Renvoit le signe du nombre (c'est-à-dire + ou -)."""
    if nombre >= 0:
        return "+"
    return "-"


def tex(objet):
    """Convertit un objet mathématique en code LaTeX.

    * Soit l'objet a une méthode :meth:`tex`, auquel cas `objet.tex()` est renvoyé ;
    * sinon, si l'objet est de type :class:`numbers.Real`, une représentation adaptée est renvoyée (même si, pour plus de finesse, il pourra être utile d'utiliser :func:`facteur`) ;
    * sinon, si l'objet est une chaîne de caractères, elle est renvoyée ;
    * sinon, une exception est levée.
    """
    # pylint: disable=no-else-return
    if hasattr(objet, "tex") and callable(getattr(objet, "tex")):
        return getattr(objet, "tex")()
    if isinstance(objet, str):
        return objet
    if isinstance(objet, fractions.Fraction):
        if objet < 0:
            return fr"-\frac{{\numprint{{{-int(objet.numerator)}}}}}{{\numprint{{{objet.denominator}}}}}"
        else:
            return fr"\frac{{\numprint{{{objet.numerator}}}}}{{\numprint{{{objet.denominator}}}}}"
    if isinstance(objet, numbers.Real):
        return fr"\numprint{{{objet}}}"

    raise TypeError(f"L'objet {objet} n'a pas de méthode 'tex()'.")
