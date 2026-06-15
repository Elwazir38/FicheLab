#!/usr/bin/env python3

# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
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
from itertools import count
'''
Created on 24 janv. 2015

@author: jerome
'''
from pyromaths import ex
from pyromaths.outils.Arithmetique import pgcd
from pyromaths.classes.Fractions import Fraction
from pyromaths.outils import tikz
from random import randrange, shuffle

def InitPoints(minimum=-6.1, maximum=6.1, nbval=3):
    dY = []
    directions = [(-1) ** i for i in range(nbval - 1)]
    directions.append(0)
    shuffle(directions)
    for i in range((nbval - 1) // 2):
        while True:
            a, b = randrange(1, 5), randrange(1, 5)
            if pgcd(a, b) == 1 and a % b != 0:
                dY.append(Fraction(a, b))
                break
    for i in range(nbval - 1 - len(dY)):
        dY.append(randrange(1, 5))
    shuffle(dY)
    for i in range(nbval):
        if directions[i] == 0:
            dY.insert(i, 0)
        else:
            dY[i] = dY[i] * directions[i]
    dY.insert(0, 0)
    dY.append(0)
    redo = True
    while redo:
        lX = [int(minimum) + 1 + int(1.*i * (maximum - minimum - 2) / nbval) + randrange(4) for i in range(nbval)]
        for i in range(len(lX) - 1):
            if lX[i + 1:].count(lX[i]):
                redo = True
                break
            else:
                redo = False
    lX.insert(0, minimum)
    lX.append(maximum)
    lX.sort()
    lY = [randrange(-4, 5)]
    for i in range(1, len(lX)):
        inf = lY[-1] - 4 * int(lX[i] - lX[i - 1])
        sup = lY[-1] + 4 * int(lX[i] - lX[i - 1])
        nY = randrange(int(max(-4, inf)), int(min(5, sup)))
        lY.append(nY)
        #=======================================================================
        # while True:
        #     lg = randrange(1, 4) * (-1) ** randrange(2) * int(lX[i] - lX[i - 1])
        #     nY = lY[-1] + lg
        #     if -4 <= nY <= 4 :
        #         lY.append(nY)
        #         break
        #=======================================================================
    return lX, lY, dY


class Fd1Tangentes(ex.TexExercise):
    """Nombre dérivé graphiquement"""

    tags = [
        "1re Spé math",
        "dérivation",
        "fonctions",
        "lecture graphique",
    ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lX1, self.lY1, self.dY1 = InitPoints(minimum=-6.1, maximum=6.1, nbval=3)
        self.lX2, self.lY2, self.dY2 = InitPoints(minimum=-6.1, maximum=6.1, nbval=4)

    def _graphique(self, X, Y, dY):
        axis = tikz.axis((-6, 6), (-5, 5), options={'enlargelimits': 'false'})
        txt = ""
        txt += axis.begin()
        txt += r"""\draw[ultra thick, Maroon] {};""".format(tikz.interpolation_avec_pente(zip(X, Y, dY), systeme="axis cs:"))
        for i in range(1, len(X)-1):
            txt += fr"\draw (axis cs:{X[i]}, {Y[i]}) node{{$\bullet$}};" + "\n"
            if isinstance(dY[i], Fraction):
                x = dY[i].d
                y = dY[i].n
            else:
                x = 1
                y = float(dY[i])
            txt += fr"\draw[thick, Stealth-Stealth] (axis cs:{X[i]-x}, {Y[i]-y}) -- (axis cs:{X[i]+x}, {Y[i]+y});" + "\n"
        txt += axis.end()
        return txt

    def tex_statement(self):
        dY1 = list(self.dY1)
        for i in range(len(dY1)):
            if isinstance(dY1[i], Fraction): dY1[i] = 1. * dY1[i].n / dY1[i].d
        exo = [r'\exercice']
        exo.append(r'\begin{minipage}[]{\linewidth-8cm}')
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Déterminer graphiquement les nombres dérivés de la fonction $f$ en $\qquad x=%s \qquad x=%s \qquad x=%s$.') % (self.lX1[1], self.lX1[2], self.lX1[3]))
        exo.append(_(u'\\item On considère le tableau de valeurs suivant :\\par'))
        exo.append(r'\renewcommand{\arraystretch}{2}')
        exo.append(r'\begin{tabularx}{\linewidth}[t]{|*5{>{\centering\arraybackslash}X|}}')
        exo.append(r'\hline')
        exo.append(r'$x$ & $%s$ \\ \hline' % ("$ & $".join([str(a) for a in self.lX2[1:-1]])))
        exo.append(r'$g\,(x)$ & $%s$ \\ \hline' % ("$ & $".join([str(a) for a in self.lY2[1:-1]])))
        exo.append('$g\'\\,(x)$ & $%s$ \\\\ \\hline' % ("$ & $".join([str(a) for a in self.dY2[1:-1]])))
        exo.append(r'\end{tabularx}')
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item Dans un nouveau repère, placer les points de la courbe $\\mathcal{C}_g$ ainsi connus.'))
        exo.append(_(u'\\item Tracer les tangentes à $\\mathcal{C}_g$ en ces points.'))
        exo.append(_(u'\\item Donner une allure possible de la courbe $\\mathcal{C}_g$.'))
        exo.append(r'\end{enumerate}')
        exo.append(r'\end{enumerate}')
        exo.append(r'\end{minipage}')
        exo.append(r'\hfill')
        exo.append(r'\begin{minipage}[]{7.5cm}')
        exo.append(self._graphique(self.lX1, self.lY1, self.dY1))
        exo.append(r'\end{minipage}')
        return "\n".join(exo)

    def tex_answer(self):
        dY2 = list(self.dY2)
        for i in range(len(dY2)):
            if isinstance(dY2[i], Fraction): dY2[i] = 1. * dY2[i].n / dY2[i].d
        exo = [r'\exercice*']
        exo.append(r'\begin{enumerate}')
        exo.append(_(u'\\item  On lit graphiquement le coefficient directeur de chacune des tangentes en ces points.\par'))
        exo.append(u'$f\'\\,(%s)=%s \\qquad f\'\\,(%s)=%s \\qquad f\'\\,(%s)=%s$.' % (self.lX1[1], self.dY1[1], self.lX1[2], self.dY1[2], self.lX1[3], self.dY1[3]))
        exo.append(u'\\item')
        exo.append(self._graphique(self.lX2, self.lY2, self.dY2))
        exo.append(r'\end{enumerate}')
        return "\n".join(exo)
