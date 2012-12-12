#! /usr/bin/python
import sys
import os
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------#
#	Script MAIN permettant d'executer les scripts selon le choix de l'utilisateur :		#	
#				Graphe dirige ou non dirige ?					#
#-----------------------------------------------------------------------------------------------#

#Le fichier donne en parametre 1 contient une serie de reads au format fasta (extension .fa)
fichier_reads=sys.argv[1]

#L'entier donne en parametre 2 est la taille des kmers
kmer=sys.argv[2]

#L'entier donne en parametre 3 indique si on veut un graphe dirige (1) ou non dirige (0)
dir=int(sys.argv[3])

#On initialise le nom d'un fichier resultat qui sera passe en parametre des scripts Python
fichier_resultat="fic_out"

#Si c'est le graphe non dirige qui est souhaite
if(dir==0) :
	#On execute le script shortestPathUndirected.py
	os.system("python shortestPathUndirected.py "+fichier_reads+" "+fichier_resultat+" "+kmer)
#Si c'est le graphe dirige qui est souhaite
elif(dir==1) :
	#On execute le script shortestPathDirected.py
	os.system("python shortestPathDirected.py "+fichier_reads+" "+fichier_resultat+" "+kmer)
#Si le choix a ete mal entre on demande a l'utilisateur de recommencer
else :
	print "argument 4 incorrect : taper 1 (graphe dirige) ou 0 (graphe non dirige)"


#2012 Auffret Pauline, Marino Anais & Parent Kevin
#Cours de Gustavo Sacomoto
