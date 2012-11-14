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
		edges[liste_fichier[0]].append(liste_fichier[1])
	#Sinon
	else :
		#On cree une nouvelle arete 
		edges[liste_fichier[0]]=list()
		edges[liste_fichier[0]].append(liste_fichier[1])
		
	#On lit la ligne suivante du fichier
	l=fic_graphe.readline()
print edges
print nodes[0]
#------------------------------------------------------------------------------------------------------------------#
#-------------- Partie 2 : Fonctions de recherche du plus court chemin via l'algorithme de Dijkstra ---------------#
#------------------------------------------------------------------------------------------------------------------#
def ExtractMin(Q,dist) :
	mini=Q[0]
	for i in Q :
		if dist[i]<dist[mini] :
			mini=i
	return mini


def dijkstra(nodes,edges,s) :

	dist=dict()
	Q=list()
	for n in nodes :
		dist[n]=1000
	dist[s]=0
	Q=nodes
	while Q :
		u=ExtractMin(Q,dist)
		print dist[u]
		Q.remove(u)
		if edges.has_key(u) :
			for v in edges[u] :
				print dist[v]
				print dist[u]
				if dist[v]>=dist[u]+1 :
					dist[v]=dist[u]+1
	return dist

dist=list()
dist=dijkstra(nodes,edges,nodes[0])

print dist
	
	
	
