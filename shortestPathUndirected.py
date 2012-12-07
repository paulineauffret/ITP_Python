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
#	  		  Conversion reads -> graphe de De Bruijn				#
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
os.system("./debruijn3 "+str(fichier_reads)+" -k 3 -o reads -g 0")

#On met dans la variable fichier_graphe le nom du fichier contenant le graphe venant d'etre genere
fichier_graphe=str(fichier_reads).replace(".fa",".graph")


#-----------------------------------------------------------------------------------------------#
#	  Conversion graphe de De Bruijn -> graphe dirige sous forme de liste adjacente		#
#-----------------------------------------------------------------------------------------------#
#On ouvre le fichier fichier_graphe en lecture
try:                     		
	fic_graphe = open(fichier_graphe,'r')
except IOError, e:      		
	print "Fichier inconnu: ", fichier_graphe

#on cree la variable listAdj qui contiendra le nom du fichier sortie du script directeGraph.py
listAdj="listeAdj.txt"

#On execute le script python directedGraph.py qui transforme le graph de De Bruijn en graphe dirige (liste adjacente)
os.system("python directedGraph.py "+str(fichier_graphe)+" "+str(listAdj))

#On ouvre le fichier listAdj  en lecture
try:                     		
	fic_listAdj = open(listAdj,'r')
except IOError, e:      		
	print "Fichier inconnu: ", listAdj


#-----------------------------------------------------------------------------------------------#
#				Bac a sable : dessins de graphes				#
#-----------------------------------------------------------------------------------------------#
#graph = pydot.Dot(graph_type='graph')

#for i in range(3):
#	edge = pydot.Edge("king", "lord%d" % i)
#	graph.add_edge(edge)
#vassal_num = 0
#for i in range(3):
    # we create new edges, now between our previous lords and the new vassals
    # let us create two vassals for each lord
#    for j in range(2):
#        edge = pydot.Edge("lord%d" % i, "vassal%d" % vassal_num)
#        graph.add_edge(edge)
#        vassal_num += 1

# ok, we are set, let's save our graph into a file
#graph.write_png('example1_graph.png')

#Exemple 2
#graph = pydot.Dot(graph_type='digraph')

# creating nodes is as simple as creating edges!
#node_a = pydot.Node("Node A", style="filled", fillcolor="#976806")
#node_b = pydot.Node("Node B", style="filled", fillcolor="#976826")
#node_c = pydot.Node("Node C", style="filled", fillcolor="#976846")
#node_d = pydot.Node("Node D", style="filled", fillcolor="#976866")

#ok, now we add the nodes to the graph
#graph.add_node(node_a)
#graph.add_node(node_b)
#graph.add_node(node_c)
#graph.add_node(node_d)

# and finally we create the edges
# to keep it short, I'll be adding the edge automatically to the graph instead
# of keeping a reference to it in a variable

#graph.add_edge(pydot.Edge(node_b, node_c))
#graph.add_edge(pydot.Edge(node_c, node_d))
# but, let's make this last edge special, yes?
#graph.add_edge(pydot.Edge(node_d, node_a, label="and back we go again", labelfontcolor="#009933", fontsize="10.0", color="blue"))

# and we are done
#graph.write_png('example2_graph.png')

# this is too good to be true!

#-----------------------------------------------------------------------------------------------#
#------------------------------ Partie 1 : Lecture du fichier ----------------------------------#
#-----------------------------------------------------------------------------------------------#
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
	print liste_fichier
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

#-----------------------------------------------------------------------------------------------#
#					 Dessin du graphe					#
#-----------------------------------------------------------------------------------------------#
graph = pydot.Dot(graph_type='graph')
graph_node=dict()
for node in nodes :
	V = pydot.Node(str(node), style="filled")
	graph_node[node]=V
	graph.add_node(V)
for key in edges.keys() :
	node1=graph_node[key]
	node2=graph_node[edges[key][0]]
	graph.add_edge(pydot.Edge(node1, node2))
graph.write_png('test.png')



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

somme_dist=0
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
		somme_dist+=dist[k]

print dico_final
print somme_dist
	
	
	
