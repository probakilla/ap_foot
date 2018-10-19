# Tasks

## 1 - Construire le graph

- [ ] **Fichier graph.py**

  - [ ] _Fonction de création de graph : buildGraph(file)_

    - Paramètre : file -> chemin vers fichier json
    - Retour : un graph opposants/défenseurs
    - Dépend des fonctions :
      - builAttackNode

  - [ ] _Fonction buildAttackNodes(atkPos, goal, theta)_

    - Paramètre : atkPos -> Position de l'attaquant
    - Paramètre : goal -> Classe Goal
    - Paramètre : theta -> Angle entre chaque tir
    - Construit les noeuds correspondants aux possibilitées de tir cadrés de
      l'attaquant. (Voir pseudo algo sur Trello)
    - Dépend des fonctions :
      - intersect

  - [ ] _Fonction buildDefendNodes(graph, posStep, radius, fieldLimits)_

  - [ ] _Fonction isSegmentIntersectLine(goalPt1, goalPt2, atkPt1, shiftedAtkPt)_

    - Paramètres : Les deux paires de points pour calculer l'intersection
    - Retour : Vrai si intersection sinon Faux

  - [ ] _Fonction isLineIntersectCircle(pt1, pt2, center, radius)_

    - Paramètres : Les points de la droite, le centre du cercle et son rayon
    - Retour : Vrai si intersection sinon Faux

  - [ ] _Fonction isCirclesIntersect (circleCenter1, circleCenter2, radius)_

    - Paramètres : Les centres de cercles et leurs rayons.
    - Retour : Vrai si intersection sinon Faux

  - [ ] _Fonction graphToJson(graph, fileName)_

    - Paramètre : graph -> un graph
    - Paramètre : fileName -> Le nom du fichier .json à créer, ex: "file"
    - Retour : Rien
    - Ecrit dans un fichier .json (l'extension du fichier n'est pas présente
      dans la variable fileName) la position contenue dans chaque sommet du
      graphe passé en paramètre.

- [x] **Fichier node.py contenant**

- [x] Classe DefNode

  - position (Point -> x/y)
  - color (boolean -> n/b)

- [x] Classe AtkNode

  - position (Point -> x/y)
  - color (boolean -> n/b)
  - angle (integer)

- [x] Class Point
  - abscisses (float)
  - ordonnées (float)

## 2 - Calculer l'ensemble dominant

- [ ] **Fichier dominating.py**
  - [ ] _Fonction searchDominating(graph, defNb)_
    - Paramètre : graph -> Un graph
    - Paramètre : defNb -> Le nombre de défenseurs (integer)
    - Retour : Un graph si un ensemble dominant de taille <= defNb est trouvé,
      null sinon.
