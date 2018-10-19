# Tasks

## 1 - Construire le graph

- [ ] **Fichier graph.py**

  - [ ] _Fonction de création de graph : buildGraph(file)_

    - Paramètre : file -> chemin vers fichier json
    - Retour : un graph opposants/défenseurs
    - Créer à partir de json : positions.json

  - [ ] _Fonction graphToJson(graph, fileName)_

    - Paramètre : graph -> un graph
    - Paramètre : fileName -> Le nom du fichier .json à créer, ex: "file"
    - Retour : Rien
    - Ecrit dans un fichier .json (l'extension du fichier n'est pas présente
      dans la variable fileName) la position contenue dans chaque sommet du
      graphe passé en paramètre.

- [x] **Fichier node.py contenant**

  - [x] Classe node :
    - position (Point -> x/y)
    - color (boolean -> n/b)
    - isAttack (boolean -> attanquant ou non)

## 2 - Calculer l'ensemble dominant

- [ ] **Fichier dominating.py**
  - [ ] _Fonction searchDominating(graph, defNb)_
    - Paramètre : graph -> Un graph
    - Paramètre : defNb -> Le nombre de défenseurs (integer)
    - Retour : Un graph si un ensemble dominant de taille <= defNb est trouvé,
      null sinon.
