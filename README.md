# Blob Runner

<p align="justify">
Dans ce mini jeu, le joueur est situé en bas à gauche de l’écran. Des obstacles au sol ou aériens
viennent vers lui et il doit sauter pour les éviter. Un sol ainsi que des nuages en fond défilent, à
des vitesses différentes pour donner l’illusion de mouvement et de profondeur. Cet effet
s’appelle Parallaxe. Le score est affiché en haut à droite et s’incrémente tant que le joueur n’a
pas rencontré d’obstacle. S’il entre en collision avec un obstacle, il s’arrête et le texte « Game
Over » apparaît.
</p>

Version réalisée en C++ avec la librarie graphique SFML.

sudo apt-get install libsfml-dev

Exécution :

    Sur un linux
    Il faut vérifier la présence de g++ : g++ --version.
    
    Sur raspberry
    Utiliser le paquet : g++-arm-linux-gnueabi (4:10.2.1-1) à la place g++.

<p>&copy; 2021 Scaredom @Mathieu SEMIN</p>
