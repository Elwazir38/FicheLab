.. _bidouilles:

======================================================
Bidouilles : Quelques outils pour développer Pyromaths
======================================================

Quelques outils permettent aux personnes développant Pyromaths de faciliter leur travail. Ces outils sont présents dans le dépôt mais ne sont pas distribués avec Pyromaths parce que :

- ils ne sont pas destinés au même public ;
- ils nécessitent d'avoir accès au dépôt (fichiers gérés par git) ;
- ils manipulent ces fichiers du dépôt.

Ces outils sont destinés à des développeurs ou développeuses : il se peut qu'ils ne fonctionnent que sous GNU/Linux, qu'ils soient cassés sans que personne ne s'en soit rendu compte, qu'ils soient obsolètes, ou autre. À utiliser à vos risques et périls.

Ils sont situés dans le dépôt, dans le dossier `utils <https://framagit.org/pyromaths/pyromaths/-/tree/develop/utils>`__.

.. contents:: Table des matières
   :local:
   :depth: 1

.. _pyrotests:

Tests de non régression
=======================

.. code-block:: bash

   utils/bidouilles test

Cet outil permet de mettre en œuvre des tests de non régression pour les
exercices.

Principe
--------

Les exercices de Pyromaths sont générés aléatoirement. Néanmoins, en fixant la
graine (:meth:`random.seed`) du générateur aléatoire, il est possible de
générer deux fois de suite exactement le même exercice.

Le principe de ces tests est le suivant : la personne concevant un
exercice peut en valider un énoncé particulier. Plus tard, il sera possible de
vérifier que l'exercice produit toujours exactement la même sortie.

Cet outil est conçu de telle manière à ce que l'appel au module :mod:`unittest`
de Python (par exemple avec ``python3 -m unittest discover``) effectue tous ces
tests.

Commandes
---------

Description rapide
^^^^^^^^^^^^^^^^^^

Les commandes détaillées sont décrites ci-après. En voici une version
simplifiée.

* Création (``python3 -m pyromaths.cli test create``), suppression des tests (``python3 -m pyromaths.cli test remove``)

* Mise à jour des tests (``python3 -m pyromaths.cli test update``) :
  Effectue les tests, et propose de mettre à jour les tests qui ont changé. Utile si le code LaTeX généré a changé, mais l'exercice reste valide pour autant.

* Exécution des tests (``python3 -m pyromaths.cli test check``) :
  Effectue les tests. Les tests sont aussi exécutés lorsqu'``unittest`` est appelé.


Description complète
^^^^^^^^^^^^^^^^^^^^

.. argparse::
    :module: pyromaths.cli.test.__main__
    :func: argument_parser

Manipulation des tags
=====================

.. code-block:: bash

   utils/bidouilles test

Cet outil permet de :

- renommer un tag dans tous les exercices (par exemple, je veux que dans tous les exercices concernés, le tag ``systeme`` devienne ``Système d'équations`` ;
- choisir les tags pour des exercices : pour chaque exercice donné en argument, cet outil affiche l'exercice, et la liste des tags, et permet de choisir des tags existants pour cet exercice, ou d'en ajouter de nouveaux.


Manipulation des exercices
==========================

.. code-block:: bash

   utils/bidouilles exo

Cet outil permet de :

- renommer un exercice. Attention : ce programme renomme des fichiers du dépôt git, et en modifie d'autres. Il est tout à fait possible qu'il ne fasse pas bien son travail. Il faut donc vérifier à la main, par la suite, que tout a été fait correctement.

Génération des vignettes
========================

.. code-block:: bash

   utils/creer-vignettes.py

Cet outil crée les vignettes des exercices (des images au format png de l'énoncé). Il ne prend pas d'arguments, mais ne crée que les vignettes des exercices qui ont changé.

Création d'une nouvelle version
===============================

.. code-block:: bash

   utils/make_packages.sh

Cet outil crée une nouvelle version : changement du numéro, création d'un tag git, édition du *changelog*, etc.
