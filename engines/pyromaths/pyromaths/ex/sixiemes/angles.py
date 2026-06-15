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

import math
import textwrap
from random import randrange

from pyromaths.outils import Geometrie
from pyromaths import ex


def eq_droites(A, B):
    (xA, yA) = A
    (xB, yB) = B
    a = (yB - yA) / (xB - xA)
    b = (xB * yA - xA * yB) / (xB - xA)
    return (a, b)


def inter_droites(A, B, C, D):
    """
    Calcule les coordonnées du point d'intersection des droites (AB) et (CD)
    """

    (a1, b1) = eq_droites(A, B)
    (a2, b2) = eq_droites(C, D)
    if a1 == a2:  # droites parallèles
        xI = A[0]
        yI = A[1]
    else:
        xI = (b2 - b1) / (a1 - a2)
        yI = (a1 * b2 - a2 * b1) / (a1 - a2)
    return (xI, yI)


def dist_pt_droite(A, B, C):
    """
    calcule la distance du point C à la droite (AB)
    """

    (a, b) = eq_droites(A, B)
    (xC, yC) = C
    d = abs(a * xC - yC + b) / math.sqrt(a ** 2 + 1)
    return d


def dist_points(A, B):
    """ Calcul la distance entre deux points"""

    (xA, yA) = A
    (xB, yB) = B
    d = math.sqrt((xB - xA) ** 2 + (yB - yA) ** 2)
    return d


def coord_projete(A, B, C):
    """
    Calcule les coordonnées du projeté orthogonal de C sur la droite (AB)
    """

    (xA, yA) = A
    (xB, yB) = B
    (xC, yC) = C
    n = dist_points(A, B)
    p = (xB - xA) // n
    q = (yB - yA) // n
    s = p * (xC - xA) + q * (yC - yA)
    return (xA + s * p, yA + s * q)


def verifie_distance_mini(A, B, C, D):
    """
    Vérifie que la distance minimale entre [AB] et [AC] est supérieure à dmin
    """

    dmin = 1.2
    (xA, yA) = A
    (xB, yB) = B
    if xA > xB:
        (xA, yA, xB, yB) = (xB, yB, xA, yA)
    (xC, yC) = C
    (xD, yD) = D
    if xC > xD:
        (xC, yC, xD, yD) = (xD, yD, xC, yC)
    (xI, dummy) = inter_droites(A, B, C, D)
    if xA <= xI <= xB and xC <= xI <= xD or xA <= coord_projete(A, B, C)[0] <= \
        xB and dist_pt_droite(A, B, C) < dmin or xA <= coord_projete(A,
            B, D)[0] <= xB and dist_pt_droite(A, B, D) < dmin or xC <= \
        coord_projete(C, D, A)[0] <= xD and dist_pt_droite(C, D, A) < \
        dmin or xC <= coord_projete(C, D, B)[0] <= xD and dist_pt_droite(C,
            D, B) < dmin or dist_points(A, C) < dmin or dist_points(A, D) < \
        dmin or dist_points(B, C) < dmin or dist_points(B, D) < dmin:
        isValid = False
    else:
        isValid = True
    return isValid


def verifie_angle(lpoints, A, B, C):
    """
    Vérifie que l'angle BAC ne coupe pas les autres angles déjà tracés
    """

    if len(lpoints) == 0:  # Premier angle créé
        isValid = True
    else:
        for i in range(len(lpoints)):
            (A1, B1, C1) = (lpoints[i])[:3]
            isValid = verifie_distance_mini(A, B, A1, B1) and \
                verifie_distance_mini(A, B, A1, C1) and \
                verifie_distance_mini(A, C, A1, B1) and \
                verifie_distance_mini(A, C, A1, C1)
            if not isValid:
                break
    return isValid


def cree_angles(nb_angles, xmax, ymax):
    '''
    crée une série d\'angles "non séquents"
    '''

    (xmax, ymax) = (xmax - .5, ymax - .5)  # taille de l'image en cm
    lg_seg = 6  # longueur des côtés des angles
    lpoints = []
    cpt = 0  # evite une boucle infinie
    while len(lpoints) < nb_angles and cpt < 1000:
        (xA, yA) = (randrange(5, xmax * 10) / 10, randrange(5, ymax * 10) / 10)
        alpha = randrange(360)  # angle entre un côté et l'horizontal
        if len(lpoints) < nb_angles // 2:
            beta = randrange(90, 180)  # crée un angle droit ou obtus
        else:
            beta = randrange(0, 75) + 15  # crée un angle aigu (entre 15° et 89°)
        xB = xA + lg_seg * math.cos((alpha * math.pi) / 180)
        yB = yA + lg_seg * math.sin((alpha * math.pi) / 180)
        xC = xA + lg_seg * math.cos(((alpha + beta) * math.pi) / 180)
        yC = yA + lg_seg * math.sin(((alpha + beta) * math.pi) / 180)
        (A, B, C) = ((xA, yA), (xB, yB), (xC, yC))
        if xA != xB and xA != xC and .5 < xB < xmax and .5 < yB < ymax and \
            .5 < xC < xmax and .5 < yC < ymax and verifie_angle(lpoints,
                A, B, C):
            lpoints.append((A, B, C, alpha, beta))
        else:
            cpt = cpt + 1

    return lpoints


def PosAngle(alpha, beta):
    """retourne les angles pour placer les points sur la figure"""

    A = (alpha + beta / 2 + 180) % 360
    B = (alpha - 90) % 360
    C = (alpha + beta + 90) % 360
    return (A, B, C)


def PointName(l3noms, indice):
    liste = []
    for i in range(3):
        liste.append(l3noms[i])
    return tuple(liste)


def figure(exo, cor, lpoints, lnoms, xmax, ymax):
    dessin = []
    dessin.append(r"\begin{tikzpicture}[very thick]")
    dessin.append(r"\draw[Maroon] (0,0) rectangle (%s,%s);" % (xmax, ymax))
    for i in range(len(lnoms)):
        points_exo = ''
        points_cor = ''
        for j in range(3):
            dessin.append(textwrap.dedent(fr"""
            \coordinate ({"BAC"[j]}) at {lpoints[i][j]};
            """))
        dessin.append(textwrap.dedent(fr"""
            \draw pic [draw=Maroon,angle radius=20pt] {{angle = A--B--C}};
            \draw[|-, Maroon] (A) -- (B);
            \draw[|-, Maroon] (C) -- (B);
            \draw[Maroon] ($1.1*(A)-.1*(B)$) -- (A);
            \draw[Maroon] ($1.1*(C)-.1*(B)$) -- (C);
            \draw ($(A) + ({lpoints[i][3]-90}:.5)$) node{{${lnoms[i][1]}$}};
            \draw ($(B) + ({.5 * lpoints[i][4]+lpoints[i][3]+180}:.5)$) node{{${lnoms[i][0]}$}};
            \draw ($(C) + ({lpoints[i][4]+lpoints[i][3]+90}:.5)$) node{{${lnoms[i][2]}$}};
        """))
    dessin.append(r"\end{tikzpicture}\par")

    exo.extend(dessin)
    cor.extend(dessin)


def reponses(exo, cor, lpoints, lnoms):
    cor.append("\\begin{multicols}{4}")
    for i in range(len(lnoms)):
        cor.append("$\\widehat{%s%s%s}=\\ang{%s}$\\par" % (lnoms[i][1],
                 lnoms[i][0], lnoms[i][2], lpoints[i][4]))
        if lpoints[i][4] < 90:
            cor.append("angle aigu\\par")
        elif lpoints[i][4] > 90:
            cor.append("angle obtus\\par")
        else:
            cor.append("angle droit\\par")
    cor.append("\\end{multicols}")
    exo.append("\\begin{tabularx}{\\textwidth}{|*{4}{X|}}")
    exo.append("\\hline angle 1 : & angle 2 : & angle 3 : & angle 4 : \\\\")
    exo.append("\\hline &&& \\\\ &&& \\\\ &&& \\\\ \\hline")
    exo.append("\\end{tabularx}")


def _MesureAngles():
    nb_angles = 4
    (xmax, ymax) = (18, 8)  # taille de l'image en cm
    lnoms = []
    lpoints = []
    cpt = 0
    while len(lpoints) < nb_angles:
        if cpt > 1000:
            lpoints = []
            cpt = 0
        lpoints = cree_angles(nb_angles, xmax, ymax)
        cpt = cpt + 1
    tmpl = Geometrie.choix_points(3 * nb_angles)
    for i in range(nb_angles):
        lnoms.append(tuple(tmpl[3 * i:3 * i + 3]))
    exo = ["\\exercice", "Nommer, mesurer et donner la nature de chacun des angles suivants :\\par "]
    cor = ["\\exercice*", "Nommer, mesurer et donner la nature de chacun des angles suivants :\\par "]
    figure(exo, cor, lpoints, lnoms, xmax, ymax)
    reponses(exo, cor, lpoints, lnoms)
    return (exo, cor)

class MesureAngles(ex.LegacyExercise):
    """Mesurer des angles"""

    tags = [
        "angles",
        "géométrie",
        "Cycle 3",
    ]
    function = _MesureAngles

class ConstruireZigZag(ex.TexExercise):
    """Construire des angles"""

    tags = [
        "angles",
        "géométrie",
        "tracé",
        "Cycle 3",
    ]

    def __init__(self, *args, **kwargs):
        """ Crée une liste de nbp points situés à la distance lg les uns des
        autres"""
        super().__init__(*args, **kwargs)

        from pyromaths.outils.Conversions import radians
        from math import sin, cos
        self.lg, nbp = 4, 6
        while True:
            ar = randrange(80, 91)
            angles_relatifs = [ar]
            angles_absolus = [ar]
            ar = radians(ar)
            self.points = [(.2, .2), (.2 + self.lg * cos(ar), .2 + self.lg * sin(ar))]
            for i in range(nbp - 1):
                point = (-1, -1)
                cpt = 0  # évite les boucles infinies
                while (not point[0] < 16.2 or not 0.2 < point[1] < self.lg + 1) and cpt < 100:
                    if i % 2:
                        aa = randrange(angles_absolus[-1], 80)
                    else:
                        aa = randrange(-80, angles_absolus[-1])
                    ar = 180 - abs(aa - angles_absolus[-1])
                    aar = radians(aa)
                    point = (self.points[-1][0] + self.lg * cos(aar), self.points[-1][1] + self.lg * sin(aar))
                    cpt += 1
                if cpt == 100:
                    break
                else:
                    self.points.append(point)
                    angles_absolus.append(aa)
                    angles_relatifs.append(ar)

            if cpt >= 100:
                continue

            # Vérification que la cible n'est pas excentrée
            cible = self.cible
            excentree = False
            for i in (0, 1):
                if not min(pt[i] for pt in self.points) < cible[i] < max(pt[i] for pt in self.points):
                    excentree = True
            if excentree:
                continue

            # Tout va bien !
            break

        self.angles_relatifs, self.angles_absolus = angles_relatifs, angles_absolus

    @property
    def cible(self):
        x, y = inter_droites(self.points[0], self.points[-1], self.points[1], self.points[-2])
        if not (0 < x < 18 and 0 < y < self.lg + 2):
            x, y = inter_droites(self.points[0], self.points[-2], self.points[1], self.points[-1])
        return x, y

    @property
    def segments(self):
        x, y = inter_droites(self.points[0], self.points[-1], self.points[1], self.points[-2])
        if 0 < x < 18 and 0 < y < self.lg + 2:
            return "BF", "AG"
        else:
            return "BG", "AF"

    def tikz_zigzag(self, points, *, angles=False, cible=False, segments=False, solution=False, scale=.5):
        kwargs = points
        kwargs.update({
            "scale": scale,
            })
        kwargs.update({
            f"angle{i}": self.angles_relatifs[i]
            for i in range(1, 6)
            })

        code = textwrap.dedent("""\
                \\begin{{tikzpicture}}[ultra thick, scale={scale}]
                \\coordinate (A) at {A};
                \\coordinate (B) at {B};
                \\coordinate (C) at {C};
                \\coordinate (D) at {D};
                \\coordinate (E) at {E};
                \\coordinate (F) at {F};
                \\coordinate (G) at {G};
                \\draw (A) node[below]{{$A$}};
                \\draw (B) node[above]{{$B$}};
                \\draw[Maroon] (A) -- (B);
                \\draw[Maroon,draw,decoration={{markings, mark=at position .5  with {{\\node[transform shape] {{$\\parallel$}};}}}}] (A) edge[decorate] (B);"""
                )
        if cible:
            for i in range(1, 5):
                code += f"\\draw[Gray] {self.cible} circle ({i/10});\n"

        if segments:
            S1, S2 = self.segments
            code += f"\\draw[dotted, Maroon] ({S1[0]}) -- ({S1[1]});\n"
            code += f"\\draw[dotted, Maroon] ({S2[0]}) -- ({S2[1]});\n"

        if solution:
            code += textwrap.dedent("""\
                    \\draw (C) node[below]{{$C$}};
                    \\draw (D) node[above]{{$D$}};
                    \\draw (E) node[below]{{$E$}};
                    \\draw (F) node[above]{{$F$}};
                    \\draw (G) node[below]{{$G$}};
                    \\draw[Maroon] (B) -- (C) -- (D) -- (E) -- (F) -- (G);
                    \\draw[Maroon,draw,decoration={{markings, mark=at position .5  with {{\\node[transform shape] {{$\\parallel$}};}}}}]
                        (B) edge[decorate] (C)
                        (C) edge[decorate] (D)
                        (D) edge[decorate] (E)
                        (E) edge[decorate] (F)
                        (F) edge[decorate] (G);"""
                        )
            if angles:
                code += textwrap.dedent("""\
                    \\draw pic [draw=Maroon,angle radius=20pt, angle eccentricity=2, "\\ang{{ {angle1} }}"] {{angle = A--B--C}};
                    \\draw pic [draw=Maroon,angle radius=20pt, angle eccentricity=2, "\\ang{{ {angle2} }}"] {{angle = D--C--B}};
                    \\draw pic [draw=Maroon,angle radius=20pt, angle eccentricity=2, "\\ang{{ {angle3} }}"] {{angle = C--D--E}};
                    \\draw pic [draw=Maroon,angle radius=20pt, angle eccentricity=2, "\\ang{{ {angle4} }}"] {{angle = F--E--D}};
                    \\draw pic [draw=Maroon,angle radius=20pt, angle eccentricity=2, "\\ang{{ {angle5} }}"] {{angle = E--F--G}};"""
                    )
            else:
                code += textwrap.dedent("""\
                    \\draw pic [draw,Maroon,angle radius=20pt] {{angle = A--B--C}};
                    \\draw pic [draw,Maroon,angle radius=20pt] {{angle = D--C--B}};
                    \\draw pic [draw,Maroon,angle radius=20pt] {{angle = C--D--E}};
                    \\draw pic [draw,Maroon,angle radius=20pt] {{angle = F--E--D}};
                    \\draw pic [draw,Maroon,angle radius=20pt] {{angle = E--F--G}};"""
                    )
        else:
            code += textwrap.dedent("""\
                    \\draw (C) node[opacity=0, below]{{$C$}};
                    \\draw (D) node[opacity=0, above]{{$D$}};
                    \\draw (E) node[opacity=0, below]{{$E$}};
                    \\draw (F) node[opacity=0, above]{{$F$}};
                    \\draw (G) node[opacity=0, below]{{$G$}};"""
                    )
        code += "\\end{{tikzpicture}}"

        return code.format(**kwargs)

    def tex_commun(self):
        exo = [u'Construire sur la figure ci-dessous les points $C$, $D$, $E$, $F$ et $G$ pour obtenir un zigzag tel que :\\par']
        exo_t = '$'
        for i in range(len(self.angles_relatifs) - 1):
            exo_t += r"\widehat{%s%s%s}=\ang{%s} \qquad " % (chr(i + 65), chr(i + 66), chr(i + 67), self.angles_relatifs[i + 1])
        exo_t += r'$\par'
        exo.append(exo_t)
        exo.append(u"Quand le travail est fait avec une bonne précision, les ")
        x1, y1 = inter_droites(self.points[0], self.points[-1], self.points[1], self.points[-2])
        if 0 < x1 < 18 and 0 < y1 < self.lg + 2:
            exo.append(u"droites $(AG)$ et $(BF)$ se coupent au c\\oe ur de la cible.\\par")
        else:
            exo.append(u"droites $(AF)$ et $(BG)$ se coupent au c\\oe ur de la cible.")
        return exo


    def tex_statement(self):
        exo = [r'\exercice']
        exo.append(u'Voici deux exemples de zigzags :\par')
        exo.append(r'\begin{center}')
        exo.append(self.tikz_zigzag(
            scale=.4,
            points={
                "A": (0.20, 0.20),
                "B": (0.83, 6.17),
                "C": (2.48, 0.40),
                "D": (3.63, 6.29),
                "E": (9.23, 4.14),
                "F": (14.83, 6.29),
                "G": (15.87, 0.38),
                },
            solution=True,
            ))
        exo.append(r'\hspace{2cm}')
        exo.append(self.tikz_zigzag(
            scale=.4,
            points={
                "A": (0.20, 0.20),
                "B": (0.30, 6.20),
                "C": (1.76, 0.38),
                "D": (5.28, 5.23),
                "E": (10.37, 2.05),
                "F": (14.46, 6.44),
                "G": (15.61, 0.55),
                },
            solution=True,
            ))
        exo.append(r'\end{center}')
        exo.extend(self.tex_commun())
        exo.append(r"\begin{center}\fbox{")
        exo.append(self.tikz_zigzag(
            scale=1.1,
            points={
                "ABCDEFG"[i]: self.points[i]
                for i in range(7)
                },
            cible=True,
            ))
        exo.append(r"}\end{center}")
        return "\n".join(exo)

    def tex_answer(self):
        exo = [r'\exercice*']
        exo.extend(self.tex_commun())
        exo.append(r"\begin{center}\fbox{")
        exo.append(self.tikz_zigzag(
            scale=1.1,
            points={
                "ABCDEFG"[i]: self.points[i]
                for i in range(7)
                },
            cible=True,
            segments=True,
            solution=True,
            angles=True,
            ))
        exo.append(r"}\end{center}")
        return "\n".join(exo)

