#! /usr/bin/python
import sys
import os
import pygraph
import pydot
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------#
#	Script permettant de produire un graphe non dirige dessine sur lequel les noeuds ont 	#
#		une couleur proportionnelle a leur centralite dans le graphe, a partir		#
#			d'un fichier fasta contenant une liste de lectures			#
#-----------------------------------------------------------------------------------------------#
#Warning : on considere que le poids de toutes les aretes vaut 1 

#Prerequis pour faire fonctionner ce script
# - le script directedGraph.py ;
# - le programme debruijn3.cpp.

#-----------------------------------------------------------------------------------------------#
#------------------- Etape 0 : Lecture des arguments, ouverture des fichiers -------------------#
#-----------------------------------------------------------------------------------------------#
#Le fichier donne en parametre 1 contient une serie de reads au format fasta (extension .fa)
fichier_reads=sys.argv[1]

#Le fichier donne en parametre 2 est le fichier resultat 
fichier_resultat=sys.argv[2]

#L'entier donne en parametre 3 est la taille des kmers
kmer=sys.argv[3]

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


#-----------------------------------------------------------------------------------------------#
#--------------------- Etape 1 : Conversion reads -> graphe de De Bruijn -----------------------#
#-----------------------------------------------------------------------------------------------#
#On execute le programme debruijn3 qui transforme le fichier de reads en graphe de De Bruijn
os.system("./debruijn3 "+str(fichier_reads)+" -k "+kmer+" -o "+str(fichier_reads).replace(".fa","")+" -g 0")

#On met dans la variable fichier_graphe le nom du fichier contenant le graphe venant d'etre genere
fichier_graphe=str(fichier_reads).replace(".fa",".graph")


#-----------------------------------------------------------------------------------------------------#
#---- Etape 2 : Conversion graphe de De Bruijn -> graphe NON dirige sous forme de liste adjacente ----#
#-----------------------------------------------------------------------------------------------------#
#On ouvre le fichier fichier_graphe en lecture
try:                     		
	fic_graphe = open(fichier_graphe,'r')
except IOError, e:      		
	print "Fichier inconnu: ", fichier_graphe

#on cree la variable listAdj qui contiendra le nom du fichier sortie du script undirecteGraph.py
listAdj="listeAdj.txt"

#On execute le script python directedGraph.py qui transforme le graphe de De Bruijn en graphe non dirige (liste adjacente)
os.system("python undirectedGraph.py "+str(fichier_graphe)+" "+str(listAdj)+" "+kmer)

#On ouvre le fichier listAdj  en lecture
try:                     		
	fic_listAdj = open(listAdj,'r')
except IOError, e:      		
	print "Fichier inconnu: ", listAdj


#-----------------------------------------------------------------------------------------------#
#-------------------------------- Etape 3 : Lecture du graphe ----------------------------------#
#-----------------------------------------------------------------------------------------------#
#Cette partie permet de lire le graphe sous forme de liste adjacente, et d'en stocker les informations (noeuds et aretes)

#On initialise la liste nodes qui contiendra la liste des noeuds du graphe
nodes=list()

#On a cree un dictionnaire edges qui contiendra les aretes du graphe sous la forme {noeud pere} => {noeud fils}
edges = dict()

#On lit la premiere ligne du fichier et on la stocke dans la variable l
l=fic_listAdj.readline()

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
	l=fic_listAdj.readline()

#On calcule le nombre total de noeuds dans le reseau
nb_nodes=len(nodes)


#-----------------------------------------------------------------------------------------------#
#---------------------------- Etape 4 : Dessin du graphe de depart -----------------------------#
#-----------------------------------------------------------------------------------------------#
#Cette partie permet de dessiner le graphe non dirige avant la ponderation des noeuds par la centralite

#Declaration d'un objet graph de type pydot.Dot
graph = pydot.Dot(graph_type='graph')

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
graph.write_png('graphe_before_undirected.png')

#On ouvre le graphe
os.system("gnome-open graphe_before_undirected.png")


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
graph = pydot.Dot(graph_type='graph')
graph_node=dict()
graph_edges=list()
for node in nodes :
	#centrality[node]=centrality[node]*10
	if centrality[node]==0 :
		color = "#FFFFFF"
	elif 0<centrality[node] and centrality[node]<=0.01 :
		color= "#FAFBFC"
	elif 0.01<centrality[node] and centrality[node]<=0.02 :
		color= "#F5F7F9"
	elif 0.02<centrality[node] and centrality[node]<=0.03 :
		color= "#F0F3F6"
	elif 0.03<centrality[node] and centrality[node]<=0.04 :
		color= "#EBEFF3"
	elif 0.04<centrality[node] and centrality[node]<=0.05 :
		color= "#E6EBF0"
	elif 0.05<centrality[node] and centrality[node]<=0.06 :
		color= "#E1E7ED"
	elif 0.06<centrality[node] and centrality[node]<=0.07 :
		color= "#DCE3EA"
	elif 0.07<centrality[node] and centrality[node]<=0.08 :
		color= "#D7DFE7"
	elif 0.08<centrality[node] and centrality[node]<=0.09 :
		color= "#D2DBE4"
	elif 0.09<centrality[node] and centrality[node]<=0.1 :
		color= "#CCD7E1"
	elif 0.1<centrality[node] and centrality[node]<=0.11 :
		color= "#C7D3DE"
	elif 0.11<centrality[node] and centrality[node]<=0.12 :
		color= "#C2CFDB"
	elif 0.12<centrality[node] and centrality[node]<=0.13 :
		color= "#BDCAD8"
	elif 0.13<centrality[node] and centrality[node]<=0.14 :
		color= "#B8C6D5"
	elif 0.14<centrality[node] and centrality[node]<=0.15 :
		color= "#B3C2D2"
	elif 0.15<centrality[node] and centrality[node]<=0.16 :
		color= "#AEBECF"
	elif 0.16<centrality[node] and centrality[node]<=0.17 :
		color= "#A9BACB"
	elif 0.17<centrality[node] and centrality[node]<=0.18 :
		color= "#A4B6C8"
	elif 0.18<centrality[node] and centrality[node]<=0.19 :
		color= "#9FB2C5"
	elif 0.19<centrality[node] and centrality[node]<=0.2 :
		color= "#A9BACB"
	elif 0.2<centrality[node] and centrality[node]<=0.21 :
		color= "#99AEC2"
	elif 0.21<centrality[node] and centrality[node]<=0.22 :
		color= "#94AABF"
	elif 0.22<centrality[node] and centrality[node]<=0.23 :
		color= "#8FA6BC"
	elif 0.23<centrality[node] and centrality[node]<=0.24 :
		color= "#8AA2B9"
	elif 0.24<centrality[node] and centrality[node]<=0.25 :
		color= "#859EB6"
	elif 0.25<centrality[node] and centrality[node]<=0.26 :
		color= "#8099B3"
	elif 0.26<centrality[node] and centrality[node]<=0.27 :
		color= "#7B95B0"
	elif 0.27<centrality[node] and centrality[node]<=0.28 :
		color= "#7691AD"
	elif 0.28<centrality[node] and centrality[node]<=0.29 :
		color= "#718DAA"
	elif 0.29<centrality[node] and centrality[node]<=0.3 :
		color= "#6C89A7"
	elif 0.3<centrality[node] and centrality[node]<=0.35 :
		color= "#6685A4"
	elif 0.35<centrality[node] and centrality[node]<=0.4 :
		color= "#6181A1"
	elif 0.4<centrality[node] and centrality[node]<=0.45 :
		color= "#5C7D9E"
	elif 0.45<centrality[node] and centrality[node]<=0.5 :
		color= "#57799B"
	elif 0.5<centrality[node] and centrality[node]<=0.6 :
		color= "#527597"
	elif 0.6<centrality[node] and centrality[node]<=0.7 :
		color= "#4D7194"
	elif 0.7<centrality[node] and centrality[node]<=0.9 :
		color= "#486D91"
	else :
		color="#013366"
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
graph.write_png('graphe_after_undirected.png')

#On ouvre le graphe
os.system("gnome-open graphe_after_undirected.png")

	

#2012 Auffret Pauline, Marino Anais & Parent Kevin
#Cours de Gustavo Sacomoto
