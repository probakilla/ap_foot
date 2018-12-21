# Projet d'algorithmique appliquée

## Instalation des modules python

```bash
pip install -r resources/requirements.txt
```

## Lancement du programme

Commande de lancement minimale du programme :

```bash
python src/main.py -f config/basic_problem_1.json -g dict
```

Le programme a besoin de ses deux paramètres pour se lancer. Voici la liste
complète des options du programme :
Note : Les paramètres des options ne sont pas sensibles à la casse.

- -a, -algo=[ALGORITHM] : Option facultative, Sélectionne l'algorithme à
  utiliser pour le calcul de l'ensemble dominant. Par défaut le programme lance
  l'algorithme glouton même si aucune option n'est précisée. Les valeurs
  possibles sont :
  - GREEDY : Algorithme glouton
  - BRUTE : Algorithme brute force

- -d, --display=[DISPLAY_TYPE] : Option facultative, permet de choisir si
  le visualiser affiche l'angle de tir des attaquants ou les arrêtes du graphe.
  Il n'est pas possible d'afficher les deux en même temps et si l'option n'est
  pas précisée au lancement, le visualiseur n'est alors pas utilisé. Les valeurs
  possibles sont :
  - GRAPH : Affiche les arrêtes entre les sommets
  - FIELD : Affiche les angles de tir des attaquants

- -f, --file=[CONFIG_FILE] : Option requise, indique au programme où chercher
  le fichier de configuration. Ce fichier doit être au format JSON.

- -g, --graph=[GRAPH_TYPE] : Option requise, indique au programme quelle
  structure de donnée utiliser. Les options sont, un graph à base de
  dictionnaire et un autre graph à base de liste et de matrice d'adjacence.
  La structure à base de matrice d'adjacence n'étant pas très optimisée, il est
  préférable de lancer avec le dictionnaire. Valeurs possibles :
  - ADJ : Graph avec liste et matrice d'adjacence
  - DICT : Graph avec dictionnaire

- -k INT, : Option facultative, indique le maximum de défenseur pour l'ensemble
  dominant. Par défaut cette valeur est initialisée à 3.

- -h, --help : Option facultative, affiche l'aide du programme.

- -o, --outfile=[FILE_PATH] : Option facultative, indique au programme de
  sauvegarder le résultat du calcul de l'ensemble dominant dans un fichier au
  format JSON. Le fichier indiqué ne doit pas exister et doit être préfixé par
  .json.

- -p, --profile : Option facultative, lance le profilage de la fonction
  buildGraph et affiche le résultat dans la console.