		    _                  
                   | |                 
 _ __ ___  __ _  __| |  _ __ ___   ___ 
| '__/ _ \/ _` |/ _` | | '_ ` _ \ / _ \
| | |  __/ (_| | (_| | | | | | | |  __/
|_|  \___|\__,_|\__,_| |_| |_| |_|\___|
                                       

Programme Project_main.py

1/ A quoi ça sert ?
Le programme permet de transformer une liste de lectures dans un fichier fasta (exemple : reads.fa) en graphe de De Bruijn orienté ou non orienté et de le dessiner.

2/ De quoi j'ai besoin pour le faire marcher ?
Il faut absolument avoir les fichiers suivants, dans le même dossier que reads.fa :
debruijn3.cpp
fasta.c
fasta.h
kmers.c
kmers.h
Makefile
directedGraph.py
undirectedGraph.py
shortestPathDirected.py
shortestPathUndirected.py

3/ Comment je fais ?
Après s'être assuré d'avoir tous les fichier nécessaires dans le même fichier, il faut taper en console :
> python Project_main.py reads.fa k 0
avec reads.fa : le fichier contenant les lectures au format fasta, ATTENTION l'extension du fichier doit être ABSOLUMENT .fa (et non .fasta)
     k : taille des kmers
     0 ou 1 : 0 = graphe non orienté, 1 = graphe orienté.
