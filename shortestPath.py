#! /usr/bin/python
import sys
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------#
#	    Scrit de recherche du plus court chemin par l'algorithme de Dijkstra		#
#-----------------------------------------------------------------------------------------------#

#Warning : on considere que le poids de toutes les aretes vaut 1 

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

#-----------------------------------------------------------------------------------------------#
#------------------------------ Partie 1 : Lecture du fichier ----------------------------------#
#-----------------------------------------------------------------------------------------------#
#On initialise la liste nodes qui contiendra la liste des noeuds du graphe
nodes=list()

#On a cree un dictionnaire edges qui contiendra les aretes du graphe sous la forme {noeud pere} => {noeud fils}
edges = dict()

#On lit la premiere ligne du fichier et on la stocke dans la variable l
l=fic_graphe.readline()

#Tant que le fichier n'est pas vide
while l :
	#On split notre chaine de caractere en une liste liste_fichier de deux elements ie deux noeuds (un noeud pere et un noeud fils) 
	liste_fichier = l.split()
	#On initialise deux variables booleennes ok1 et ok2 qui seront des indicateurs de la presence du noeud pere et du noeud fils dans la liste nodes
	ok1 = 0
	ok2 = 0	
	#On parcourt tout le dictionnaire nodes pour chercher si le noeud en cours de traitement est deja present
	for i in nodes :
		#Si i egale le premier element de la liste_fichier = le noeud pere
		if i == liste_fichier[0] :
			#On passe le booleen ok1 a 1 
			ok1 = 1
		#Si i egale le deuxieme element de la liste_fichier = le noeud fils
		if i == liste_fichier[1] : 
			#On passe le booleen ok2 a 1 
			ok2 = 1 
	#Si le premier element de la liste_fichier n'est pas dans la liste nodes ie si ok1 egale 0
	if ok1== 0 : 	
		#On ajoute dans la liste nodes ce premier element	
		nodes.append(liste_fichier[0])
	#Si le deuxieme element de la liste_fichier n'est pas dans la liste nodes ie si ok2 egale 0
	if ok2==0 : 
		#On ajoute dans la liste nodes ce deuxieme element
		nodes.append(liste_fichier[1])

	#Si le noeud pere est deja present dans le dictionnaire edges 
	if edges.has_key(liste_fichier[0]) : 
		#On met a jour sa liste de noeuds fils ie on y ajoute le deuxieme element de liste_fichier
		edges[liste_fichier[0]]= edges[liste_fichier[0]] +","+liste_fichier[1]
	#Sinon
	else :
		#On cree une nouvelle arete 
		edges[liste_fichier[0]] = liste_fichier[1]
		
	#On lit la ligne suivante du fichier
	l=fic_graphe.readline()

#------------------------------------------------------------------------------------------------------------------#
#-------------- Partie 2 : Fonctions de recherche du plus court chemin via l'algorithme de Dijkstra ---------------#
#------------------------------------------------------------------------------------------------------------------#

def PoidsMinimum(node,poids)

#Fonction qui recherche le plus court chemin entre deux noeuds selon l'algorithme de Dijkstra
#Preconditions : node1 est le noeud de depart ; node 2 est le noeud d'arrivee ; nodes est une liste contenant tous les noeuds du graphe considere ; edges est un dictionnaire contenant les aretes du graphe considere sous la forme {noeud pere} => {noeud fils}
#Postconditions : shortestPath est une liste contenant le plus court chemin de node1 a node2
def dijkstra(node1,node2,nodes,edges) :

	#On cree un dictionnaire contenant tous les poids des noeuds
	poids=dict()
	#On initialise le poids du noeud de depart a 0 
	poids[node1]=0
	#On cree un dictionnaire contenant tous les antecedents des noeuds 
	antecedents=dict()
	#On cree un dictionnaire indiquant si le noeud a ete visite ou pas 
	visites=dict()
	# On met les poids de tous les noeuds a -1, on met tous les antecedents a 0 et aucun noeud n'est visite 
	for n in nodes:
		poids[n]=-1
		antecedents[n]=0
		visites[n]="non" 
	#Le noeud de depart est le noeud avec le plus petit poids, ie node1
	noeud_depart=node1 
	#Le noeud de depart est visite	
	visites[node1]="oui"

	#Tant que le noeud de depart ie le noeud ayant le poids le plus faible n'est pas egal au noeud d'arrive 
	while noeud_depart != node2 :		
		
		#On trouve le ou les noeuds avec les poids minimums
		PlusFaiblePoids=PoidsMinimum(edges[noeud_depart],poids)
		
		for mini in PlusFaiblePoids : 

		for fils in edges[noeud_depart] :
			#Si le noeud fils n'a pas ete visite et que le poids du noeud de depart + le poids de l'arete (1) est inferieur au poids du noeud fils OU que le poids du noeud fils vaut -1
			if ((visites[fils]=="non" and poids[noeud_depart] + 1 < poids[fils]) or poids[fils]==-1) : 
				#Le poids du noeud fils est la somme du poids du noeud de depart + celui de l'arete
				poids[fils]=poids[noeud_depart]+1
				#L'antecedent du fils devient le noeud de depart 
				antecedents[fils]=noeud_depart
	


		
