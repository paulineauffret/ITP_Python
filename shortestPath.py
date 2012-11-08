#! /usr/bin/python
import sys
import re
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------#
#				Scrit de recherche du plus court chemin				#
#-----------------------------------------------------------------------------------------------#

#Considere que le poids des aretes vaut 1 
#Le fichier donne en parametre 1 contient la structure d'un graphe dirige sous forme de liste adjacente
fichier_graphe=sys.argv[1]

#Le fichier donne en parametre 2 est le fichier resultat sous forme de liste adjacente
fichier_resultat=sys.argv[2]

#On ouvre le fichier fichier_graphe en lecture
try:                     		
	fic_graphe = open(fichier_graphe,'r')
except IOError, e:      		
	print "Fichier inconnu: ", fichier_graphe

#On ouvre le fichier fichier_resultat en ecriture
try:                     		
	fic_res = open(fichier_resultat,'w')
except IOError, e:      		
	print "Fichier inconnu: ", fichier_resultat

#On lit la premiere ligne du fichier et on la stocke dans la variable l
l=fic_graphe.readline()

#On initialise la liste nodes qui contiendra la liste des noeuds du graphe
nodes=list()
#On a cre un dictionnaire vide qui contiendra les aretes du graphe
edges = dict()

#Tant que le fichier n'est pas vide
while l :
	#On split notre chaine de caractere en une liste de deux elements
	liste_fichier = l.split()
	#Tant que la liste nodes contient des elements	
	
	ok1 = 0
	ok2 = 0	
	for i in nodes :
		#Si i egale notre premier element de la liste_fichier
		if i == liste_fichier[0] : 
			ok1 = 1
		#Si i egale notre deuxieme element de la liste_fichier 
		if i == liste_fichier[1] : 
			ok2 = 1 
	#Si le premier element de la liste_fichier n'est pas dans la liste nodes ok1 egale 0
	if ok1== 0 : 	
		#On ajoute dans notre liste nodes notre premier element	
		nodes.append(liste_fichier[0])
	#Si le deuxieme element de la liste_fichier n'est pas dans la liste nodes ok2 egale 0
	if ok2==0 : 
		#On ajoute dans notre liste nodes notre deuxieme element
		nodes.append(liste_fichier[1])
	#Si la cle est deja presente dans edges 
	if edges.has_key(liste_fichier[0]) : 
		#Il ajoute les deux valeurs cote a cote
		edges[liste_fichier[0]]= edges[liste_fichier[0]] +","+liste_fichier[1]
	#Sinon
	else :
		#Il cre une nouvelle arete 
		edges[liste_fichier[0]] = liste_fichier[1]

	l=fic_graphe.readline()


def dijkstra(node1,node2,nodes,edges) :
	#On cre un dictionnaire contenant tous les poids des noeuds
	poids=dict()
	#On initialise le poids du noeud de depart a 0 
	poids[node1]=0
	#On cre un dictionnaire contenant tous les antecedents des noeuds 
	antecedents=dict()
	#On cre un dictionnaire indiquant si le noeud a ete visite ou pas 
	visites=dict()

	# On met les poids de tous les noeuds a -1, on met tous les antecedents a 0 et aucuns noeuds n'est visite 
	for n in nodes:
		poids[n]=-1
		antecedents[n]=0
		visites[n]="non" 
	#Le noeud de depart c'est le noeud avec le plus petit poids 	
	noeud_depart=node1 
	#Le noeud de depart est visite	
	visites[node1]="oui"

	#Tant que le noeud de depart n'est pas egale au noeud d'arrive 
	while node_depart != node2 :		
		
		#On trouve le ou les noeuds avec les poids minimums
		PlusFaiblePoids=PoidsMinimum(edges[noeud_depart],poids)
		
		for mini in PlusFaibePoids : 

		for fils in edges[noeud_depart] :
			#Si le noeud fils n'a pas ete visite et que le poids du noeud de depart + arete est inferieur au poids du noeud 			fils ou que le poids du noeud fils vaut -1
			if visites[fils]=="non" and poids[noeud_depart] + 1 < poids[fils] or poids[fils]==-1 : 
				# Le poids du noeud fils est la somme du poids du noeuds de depart + l'arete
				poids[fils]=poids[noeud_depart]+1
				#L'antecedents du fils devient le noeud de depart 
				antecedents[fils]=noeud_depart
	


		
