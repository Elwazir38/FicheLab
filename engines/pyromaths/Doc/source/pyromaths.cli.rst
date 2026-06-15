.. _pyromaths-cli:

==============================
Interface en ligne de commande
==============================

Pyromaths dispose d'une interface en ligne de commande : `pyromaths`. Elle
peut-être utilisées dans des scripts, ou pour l'écriture de nouveaux exercices,
pour controler le rendu au fur et à mesure du développement.

.. contents::
   :local:
   :depth: 2

Exécution
=========

Il y a deux manières d'appeler ce programme, qui sont équivalentes.

* En laissant Python rechercher le module correspondant.  Ceci suppose que le module `pyromaths` est dans le `PYTHONPATH`.

  .. code-block:: sh

    python3 -m pyromaths

* En exécutant un fichier situé dans le répertoire `utils`. Le `PYTHONPATH` est automatiquement géré ; c'est utile si vous n'arrivez pas à le faire vous-même, ou si vous n'avez pas compris la phrase précédente.

  .. code-block:: sh

    utils/pyromaths

Commandes disponibles
=====================

* Compilation d'un exercice (``python3 -m pyromaths generate``) :
  Compile un exercice, et crée le PDF correspondant (énoncé et solution) dans le dossier courant. Cette commande est utile pour tester un exercice en cours de rédaction, plutôt que de passer par l'interface graphique.

  Il est également possible de fournir des commandes à exécuter sur les fichiers LaTeX avant leur compilation. Ceci est utile pour déceler des erreurs de code LaTeX. Par exemple, la commande ``python3 -m pyromaths generate -p more EXERCICE`` affiche le code LaTeX dans `more` avant compilation; la commande ``python3 -m pyromaths generate -p vim EXERCICE`` édite le fichier avec `vim` avant compilation. Ceci peut aussi être utilisé (en attendant une solution plus propre) pour garder une copie du fichier LaTeX en cas d'erreur de compilation, pour pouvoir l'analyser, ainsi que le log : ``python3 -m pyromaths generate -p 'cp {} exercices.tex' EXERCICE``.

* Liste des identifiants des exercices disponibles (``python3 -m pyromaths ls``) :
  Affiche la liste des identifiants des exercices, pour retrouver facilement l'exercice en cours de travail. Plus d'informations sont données dans la partie :ref:`id_exos`.

.. _id_exos:

Description des exercices
=========================

Les exercices sur lesquels s'appliquent les commandes de ``pyromaths`` sont
décrits comme ``exo_pythagore:4,6``, où :

* ``exo_pythagore`` est l'identifiant de l'exercice (le nom de la fonction ou
  de la classe qui le définit) ;
* ``4,6`` sont les graines du générateur
  aléatoire qui nous intéressent. Si les graines sont omises, suivant le cas,
  soit tous les tests enregistrés sont considérés, soit la graine 0 est
  utilisée.

La liste des exercices disponibles peut être obtenue avec la commande
``python3 -m pyromaths ls``.


