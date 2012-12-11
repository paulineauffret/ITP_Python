#! /usr/bin/python
import sys
import os
import pygraph
import pydot
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------#
#	    Script de recherche du plus court chemin par l'algorithme de Dijkstra		#
#-----------------------------------------------------------------------------------------------#
#Warning : on considere que le poids de toutes les aretes vaut 1 

#Prerequis pour faire fonctionner ce script
# - le script directedGraph.py ;
# - le programme debruijn3.cpp.


#-----------------------------------------------------------------------------------------------#
#--------------------- Etape 1 : Conversion reads -> graphe de De Bruijn -----------------------#
#-----------------------------------------------------------------------------------------------#
#Le fichier donne en parametre 1 contient une serie de reads au format fasta (extension .fa)
fichier_reads=sys.argv[1]

#Le fichier donne en parametre 2 est le fichier resultat 
fichier_resultat=sys.argv[2]

#On ouvre le fichier fichier_reads en lecture
try:                     		
	fic_reads = open(fichier_reads,'r')
except IOError, e:      		
	print "Fichier inconnu: ", fichier_reads

#On ouvre le fichier fichier_resultat en ecriture
try:                     		
	fic_res = open(fichier_resultat,'w')
except IOError, e:      		
	print "Fichier inconnu: ", fichier_resultat

#On execute le programme debruijn3 qui transforme le fichier de reads en graphe de De Bruijn
os.system("./debruijn3 "+str(fichier_reads)+" -k 10 -o "+str(fichier_reads).replace(".fa","")+" -g 0")

#On met dans la variable fichier_graphe le nom du fichier contenant le graphe venant d'etre genere
fichier_graphe=str(fichier_reads).replace(".fa",".graph")
print fichier_graphe


#-----------------------------------------------------------------------------------------------#
#-- Etape 2 : Conversion graphe de De Bruijn -> graphe dirige sous forme de liste adjacente ----#
#-----------------------------------------------------------------------------------------------#
#On ouvre le fichier fichier_graphe en lecture
try:                     		
	fic_graphe = open(fichier_graphe,'r')
except IOError, e:      		
	print "Fichier inconnu: ", fichier_graphe

#on cree la variable listAdj qui contiendra le nom du fichier sortie du script directeGraph.py
listAdj="listeAdj.txt"

#On execute le script python directedGraph.py qui transforme le graphe de De Bruijn en graphe dirige (liste adjacente)
os.system("python directedGraph.py "+str(fichier_graphe)+" "+str(listAdj))

#On ouvre le fichier listAdj  en lecture
try:                     		
	fic_listAdj = open(listAdj,'r')
except IOError, e:      		
	print "Fichier inconnu: ", listAdj


#-----------------------------------------------------------------------------------------------#
#-------------------------------- Etape 3 : Lecture du graphe ----------------------------------#
#-----------------------------------------------------------------------------------------------#
#On initialise la liste nodes qui contiendra la liste des noeuds du graphe
nodes=list()

#On a cree un dictionnaire edges qui contiendra les aretes du graphe sous la forme {noeud pere} => {noeud fils}
edges = dict()

#On lit la premiere ligne du fichier et on la stocke dans la variable l
l=fic_listAdj.readline()

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
	l=fic_listAdj.readline()
print edges
print nodes
#On calcule le nombre total de noeuds dans le reseau
nb_nodes=len(nodes)


#-----------------------------------------------------------------------------------------------#
#---------------------------- Etape 4 : Dessin du graphe de depart -----------------------------#
#-----------------------------------------------------------------------------------------------#
#Cette partie permet de dessiner le graphe avant la ponderation des noeuds par la centralite

#Declaration d'un objet graph de type pydot.Dot
graph = pydot.Dot(graph_type='digraph')

#Declaration du dictionnaire graph_node, qui contiendra les noeuds du graphe a dessiner
graph_node=dict()

#Declaration du dictionnaire graph_edges, qui contiendra les aretes du graphe a dessiner
graph_edges=list()

#On parcourt la liste des noeuds du graphe, node, creee a l'etape precedente
for node in nodes :
	#On ajoute au dessin chacun des noeuds
	V = pydot.Node(str(node), style="filled")
	graph_node[node]=V
	graph.add_node(V)

#On parcourt la liste des aretes du graphe, node, creee a l'etape precedente
for key in edges.keys() :
	node1=graph_node[key]
	for elem in edges[key] :
		node2=graph_node[elem]
		#On veille a ne pas dupliquer les aretes
		edgeF=str(node1)+"to"+str(node2)
		edgeR=str(node2)+"to"+str(node1)
		#Si l'arete n'a pas deja ete dessine dans l'autre sens
		if not graph_edges.__contains__(edgeF) and not graph_edges.__contains__(edgeR) :
			#On dessine l'arete consideree sur le graphe
			graph_edges.append(edgeF)			
			edgeF=pydot.Edge(node1, node2)
			graph.add_edge(edgeF)

#On dessine le graphe dans le fichier graphe_before.png
graph.write_png('graphe_before.png')

#On ouvre le graphe
os.system("gnome-open graphe_before.png")


#------------------------------------------------------------------------------------------------------------------#
#--------------- Etape 5 : Fonctions de recherche du plus court chemin via l'algorithme de Dijkstra ---------------#
#------------------------------------------------------------------------------------------------------------------#
#Cette partie permet de calculer les plus courts chemin entre chaque couple de noeuds du graphe, par l'algo de Dijkstra

#Fonction permettran de retourner l'element minimim d'une liste Q selon son poids dans un dict dist
def ExtractMin(Q,dist) :
	mini=Q[0]
	for i in Q :
		if dist[i]<dist[mini] :
			mini=i
	return mini

#Fonction qui prend en parametre le dictionnaire des noeuds d'un graphe, le dictionnaire des aretes, et un sommet de depart
#et qui retourne dans un dictionnaire les plus courtes distances (ici, pas de ponderation des aretes) qui existent entre s et 
#chacun des autres noeuds du graphe, selon l'algorithme de Dijsktra
def dijkstra(nodes,edges,s) :
	dist=dict()
	Q=list()
	for n in nodes :
		dist[n]=sys.maxint
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

#Suite d'instructions permettant d'appliquer la fonction dijkstra a tous les noeuds du graphe
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

#------------------------------------------------------------------------------------------------------------------#
#-------------------------- Etape 6 : Calcul de la centralite de proximite de chaque noeud ------------------------#
#------------------------------------------------------------------------------------------------------------------#
#Cette partie permet de calculer la centralite associee a chacun des noeuds du graphe, selon la formule :
#C(i)=(n-1)/[somme(d(i,j))] avec n = nombre total de noeuds du graphe, et d(i,j) = plus courte distance de i a j
centrality=dict()
inf = nb_nodes
for vertex in dico_final :
	sum_dist=0
	nb_inf=0
	for dist in dico_final[vertex] :
		if dist != sys.maxint :
			sum_dist+=float(dist)
		else :
			nb_inf+=1
	if sum_dist != 0 :
		sum_dist+=inf*nb_inf
		centrality[vertex]=float((nb_nodes-1)/sum_dist)
	else :
		centrality[vertex]=0
print centrality

#-----------------------------------------------------------------------------------------------------------------#
#------------------------------------ Etape 7 : Dessin du graphe final -------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#
#Cette etape permet de dessiner le graphe avec une intensite de couleur proportionnelle aux centralites des noeuds
graph = pydot.Dot(graph_type='digraph')
graph_node=dict()
graph_edges=list()
for node in nodes :
	if centrality[node]==0 :
		color = "0.2 0.2 0.1"
	else :
		color="0.2 0.2 "+str(centrality[node])
	print color
	V = pydot.Node(str(node), style="filled",fillcolor=color)
	graph_node[node]=V
	graph.add_node(V)
for key in edges.keys() :
	node1=graph_node[key]
	for elem in edges[key] :
		node2=graph_node[elem]
		edgeF=str(node1)+"to"+str(node2)
		edgeR=str(node2)+"to"+str(node1)
		if not graph_edges.__contains__(edgeF) and not graph_edges.__contains__(edgeR) :
			graph_edges.append(edgeF)			
			edgeF=pydot.Edge(node1, node2)
			graph.add_edge(edgeF)
graph.write_png('graphe_after.png')

#On ouvre le graphe
os.system("gnome-open graphe_after.png")

	

#2012 Auffret Pauline, Marino Anais & Parent Kevin
#Cours de Gustavo Sacomoto
