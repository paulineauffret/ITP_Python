#! /usr/bin/python
import sys
import re
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------#
# Scrit de tranformation d'un graphe de De Bruijn en graphe dirige #
#-----------------------------------------------------------------------------------------------#

#Le fichier donne en parametre 1 contient la structure d'un graphe de De Bruijn
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

#On initialise le dictionnaire nodes qui contiendra la liste des noeuds du graphe
nodes=dict()

#On initialise le dictionnaire visite qui contiendra la liste des arretes deja visitees
visite=dict()

#On lit la premiere ligne du fichier et on la stocke dans la variable l
l=fic_graphe.readline()

#Tant que le fichier n'est pas vide
while l :
	#Si la ligne lue ne contient pas "digraph debuijn {"
	if(str(l)!="digraph debuijn {\n" and str(l)!="}\n") :
		#Si la ligne ne contient pas "->" ie si elle contient la definition d'un noeud
		if not re.search("->",l) :
			#On recupere le numero du noeud
			result1=re.search("[0-9]+",l)
			#On recupere la sequence des noeuds
			result2=re.search("[A-Z]{3} / [A-Z]{3}",l)
			#Si le noeud est bien trouve, on le stocke dans le dictionnaire nodes sous la forme {numero}=>{sequenceF,sequenceR}
			if result1 is not None and result2 is not None :
				nodes[int(result1.group(0))]=result2.group(0).replace(' / ','/')
		#Si la ligne contient "->" ie si elle contient la definition d'une arete
		else :
			#On recupere les noeuds impliques et si ce sont les F (forward) ou les R (reverse)
			result=re.search("[0-9]+ -> [0-9]+",l)
			#Si l'arete est bien trouvee
			if result is not None :
				#On recupere les informations necessaires a la reconstruction du graphe
				step1=result.group(0).split(" -> ")
				step2=int(step1[0])
				step3=int(step1[1])
				#On initialise le dictionnaire des visites avec les noeuds recuperes si ils ne sont pas deja presents.
				if visite.get(step2) is None :
					visite[step2]=[]
				if visite.get(step3) is None :
					visite[step3]=[]
				#On verifie que l'arrete ne soit pas deja presente dans le dictionnaire des visites
				if not visite[step2].__contains__(step3) and not visite[step3].__contains__(step2) :
					#Si tout est bon on ecrit l'arrete
					fic_res.write(nodes[step2])
					fic_res.write(" ")
					fic_res.write(nodes[step3])
					fic_res.write("\n")
					#On n'oublie pas d'ajouter l'arrete au dictionnaire des visites...
					visite[step2].append(step3)
					visite[step3].append(step2)
	#On lit la ligne suivante du fichier
	l=fic_graphe.readline()

#On ferme les fichiers
fic_graphe.close()
fic_res.close()