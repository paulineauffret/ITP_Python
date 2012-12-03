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
while l:
	#On split notre chaine de caractere en une liste liste_fichier de deux elements ie deux noeuds (un noeud pere et un noeud fils) 
	liste_fichier = l.split()
	if not nodes.__contains__(liste_fichier[0]):
		nodes.append(liste_fichier[0])
	if not nodes.__contains__(liste_fichier[1]) :
		nodes.append(liste_fichier[1])
	if edges.get(liste_fichier[0]) is None :
		edges[liste_fichier[0]]=[]
	if edges.get(liste_fichier[1]) is None :
		edges[liste_fichier[1]]=[]
	if not edges[liste_fichier[0]].__contains__(liste_fichier[1]) :
		edges[liste_fichier[0]].append(liste_fichier[1])
	if not edges[liste_fichier[1]].__contains__(liste_fichier[0]) :
		edges[liste_fichier[1]].append(liste_fichier[0])
	#On lit la ligne suivante du fichier
	l=fic_graphe.readline()
#print edges
#print nodes
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
		Q.remove(u)
		if edges.has_key(u) :
			for v in edges[u] :
				if dist[v]>=dist[u]+1 :
					dist[v]=dist[u]+1
	return dist

dico_final=dict()
nodes1=list()
for j in nodes:
		nodes1.append(j)
for i in nodes:
	dico_final[i]=[]

for i in nodes:
	dist=dijkstra(nodes1,edges,i)
	for j in nodes:
		nodes1.append(j)
	for k in nodes:
		dico_final[k].append(dist[k])

print dico_final
	
	
	
