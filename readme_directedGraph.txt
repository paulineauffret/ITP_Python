					_                  
                   | |                 
 _ __ ___  __ _  __| |  _ __ ___   ___ 
| '__/ _ \/ _` |/ _` | | '_ ` _ \ / _ \
| | |  __/ (_| | (_| | | | | | | |  __/
|_|  \___|\__,_|\__,_| |_| |_| |_|\___|
                                       
                                      
Programme Python directedGraph.py

1/ A quoi ça sert ?
Le script permet de transformet un graphe de De Bruijn en graphe dirigé.

2/ Quels sont les fichiers à passer en arguments ?
-> Argument 1 : Un graphe de De Bruijn dans un fichier du type :

digraph debuijn {
0 [label="ACA / TGT"];
4 [label="CGA / TCG"];
6 [label="GAC / GTC"];
7 [label="ATC / GAT"];
9 [label="CAG / CTG"];
11 [label="ACT / AGT"];
11 -> 6 [label="RR" weight=1];
6 -> 11 [label="FF" weight=1];
0 -> 9 [label="FF" weight=1];
9 -> 0 [label="RR" weight=1];
7 -> 4 [label="FR" weight=1];
4 -> 7 [label="FR" weight=1];
11 -> 9 [label="FR" weight=1];
9 -> 11 [label="FR" weight=1];
4 -> 4 [label="RF" weight=1];
4 -> 6 [label="FF" weight=1];
6 -> 4 [label="RR" weight=1];
}

-> Argument 2 : Un fichier texte où sera écrit le graphe dirigé sous forme de liste adjacente.

3/ En bref
-> Taper "python directedGraph.py DeBruijn.graph fichier_resultat.txt" en ligne de commande.
