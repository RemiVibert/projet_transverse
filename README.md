# PROJET TRANSVERSE: DERIVE

## Un jeu d'aventure spatiale à la rescousse d'astronautes !

## PRESENTATION DU PROJET

### CONTRIBUTEURS
Myriam MOUTTALIB: Chef Développement, Direction Artistique, Notion Managment, Art, Test, Debug, Level Implementation, Journal de Bord, PowerPoint

Kévin-Seng TEK: Développement, Level Design, Level Implementation, Physique, Test, Bug Report, Debug, ReadM, Monday et Notion Managment

Rémi VIBERT: Développement, Level Design, Sound Design, Debug

Eliott LE GUEN: Power Point et Collaboration Ponctuelle

Valentin BOINAY: Collaboration Ponctuelle

### DESCRIPTION
Vous êtes le Capitaine Meko, traversant l'espace pour rejoindre la station spatiale. En cours de route, vous rencontrez des astronautes qui ont l'air d'avoir besoin d'aide...
Ce jeu simule un vaisseau traversant l'espace, secourant les astronautes sur le chemin et atteignant la base, tout en évitant de tomber à court de carburant en plein milieu du niveau.
### FONCTIONNALITES PRINCIPALES

Le joueur devra traverser les différents niveaux en atteignant la ligne d'arrivée avec un carburant limité, représenté par une barre qui se vide et dépendant de la puissance du lancer. Des astronautes à secourir servent de bonus à ramasser pour obtenir les étoiles.


### TECHNOLOGIES UTILISEES
Python: en utilisant PyCharm Community Edition 2024.3
Des bibilothèques JSON se trouvant dans le dossier data du projet
Discord pour la communication
Monday et Notion pour la gestion des réunions et tâches
Github pour pouvoir partager facilement le projet 
Procreate et Photoshop pour le design artistique
Canva pour le PowerPoint
Internet pour la documentation sur pygame

### INSTALLATION DU PROJET 
- Aller sur le Github du projet et appuyer sur le bouton Code (bouton vert, exemple ci-dessous)
- [Où est le bouton Code ?][https://github.com/RemiVibert/projet_transverse.git]
- Puis choisissez "Download ZIP"
- Une fois le fichier ZIP téléchargé, le projet sera bien copié, il suffira d'avoir alors un éditeur Python 3 pour pouvoir l'exploiter
- Il est aussi possible de cloner le projet en copiant l'URL qui se trouve après avoir appuyé sur le bouton Code

### UTILISATION DU PROJET
- Pour l'utiliser, une fois le fichier ZIP téléchargé, il faudra clic-droit dessus
- Extraire tout ou utiliser un extracteur de fichiers
- Ouvrir le dossier décompressé et lancer le main.py avec un éditeur Python 3
- Une fois main.py lancé, il ne suffit plus que d'appuyer sur lancer le programme. Profitez du jeu !

### ALGORITHME DU JEU
- 30 niveaux
- Une partie se déroulera ainsi dans le programme:
1. Menu principal, choix entre démarrer la partie, choisir le niveau ou lire les règles
2. Commencer la partie:
  - Lance le niveau 1
- Sélectionner un niveau:
  - Affiche des astéroïdes contenant les niveaux, cliquer sur un pour pouvoir le lancer !
- Règles:
  - Affiche les règles

3. Durant une partie:
- Le joueur apparait à un point donné et doit rejoindre l'arrivée.
- Il se déplace en tirant la souris dans le sens opposé comme un lance-pierre et la puissance est ajustable
- Des planètes rocheuses et gazeuses ainsi que des astéroïdes existent pour faire obstacle au joueur:
  - Planète rocheuse:  Attire le joueur vers elle. Le joueur meurt et échoue le niveau à l'impact
  - Planète gazeuse: Attire le joueur vers elle et le piège au centre, forçant le joueur à utiliser un grand tir pour s'échapper
  - Astéroide: n'attire pas le joueur et sert de mur. Le joueur meurt et échoue le niveau à l'impact
De plus, une jauge de carburant est présente et se vide en fonction de la puissance de tir du joueur. Le joueur échoue le niveau si la jauge de carburant atteint 0 (réprésentée par la jauge à gauche de l'éccran)
Du carburant peut-être collecté dans un niveau pour recharger la jauge. Existe sous différentes itérations qui donnent chacun une quantié différente.
Plusieurs Astronautes sont dispersés dans les niveaux et servent de bonus. Le joueur les sauve en passant de dessus et aura un score en fonction du pourcentage sauvés: respectivement 1/3, 2/3 et tous.
Lors de la mort, le joueur à la possibilité de retourner à l'écran titre ou de recommencer le niveau
Lors de la victoire, le joueur à l'écran titre, rejouer ou passer au niveau suivant.

### DETAIL DES FICHIERS
Voici une liste des implémentés et leur utilité au programme

#### MAIN
Le "squelette" qui gère le projet entier et qui fait appel à tous les autres fichiers

#### BASE
Gère la base (la ligne d'arrivée)

#### LEVELS (JSON)
Gère l'agencement des différents niveaux (position des obstacles, collectibles, départ/arrivée)

#### PLANET
Gère les planètes, leurs propriétés et la physique

#### BUTTONS
Gère l'interaction avec les différents boutons du jeu, leurs changements d'état etc.

#### CAMERA
Gère la caméra du jeu, le positionnement, le zoom et le dézoom

#### COLLECTIBLE
Gère les collectibles du jeu (les Astronautes)

#### FUEL
Gère le carburant, la jauge et les différentes itérations du collectible carburant

#### GAME
Gère le déroulement d'une partie et ce qui y est affiché

#### GRAPHISMES
Gère le background étoilé

#### PLAYER
Gère le contrôle du vaisseau joueur et ses intéractions avec les autres éléments

### GESTION DES ENTREES ET DES ERREURS
Beaucoup de déboggage a été fait: Commencençant par une physique qui ne marchait pas apparement: c'était un problème de planet.py
Les bugs ont été présents et nombreux et ont été une majeure partie du développement: nous pouvons citer la base qui ne s'affiche pas ou une inversion des états des boutons...

## JOURNAL DE BORD
Rendu sur Monday[https://efrei681330.monday.com/boards/1746704228/pulses/1798848489]

## CHRONOLOGIE DU PROJET
Sur Notion[https://www.notion.so/Projet-Transverse-Equipe-1-18fef785d30a8017bca9de6e4e69deba]

### REPARTITION DES TACHES
Les tâches se sont crées petit à petit au fur et à mesure du projet. 
- Myriam MOUTTALIB: A codé une partie majeure du projet, implémenté les différents designs artistiques, implenté les différents niveaux, géré le Notion et a testé et débuggé le projet.
- Kévin-Seng TEK: A codé le projet incluant les différents menus du projet, la physique, implémenté les différents niveaux, géré le Notion et rédigé le readME et testé et débuggé le projet.
- Rémi VIBERT: A codé le projet, et a crée les différents niveaux, ainsi que le sound design.
- Eliott LE GUEN: A fait une base de PowerPoint et a été présent aux réunions.
- Valentin BOINAY: A été présent aux réunions.

## TESTS ET VALIDATION
De nombreux tests ont été faits et ont mené petit à petit au succès du projet:


### STRATEGIES DE TEST
Avant l'introduction des niveaux, nous avons crée un niveau temporaire dans lequel nous avons pu interagir avec tous les éléments du jeu, permettant un fix rapide et efficace en cas de soucis.
Pour limiter les aller-retour inutiles dans le code, nous avons décidé de structurer la construction du projet, spécialement vers la fin: ne pas construire des niveaux tant que la base ne marche pas correctement.
