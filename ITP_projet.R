# Script de R : trouver la moyenne des chemins les plus courts 

library(igraph)
graphes<-read.table("/home/anais/Documents/ITP_Python/graphes.txt", header = T)
g<-graph.data.frame(graphes,directed = FALSE)
# Calcule la matrice d'adjacence 
get.adjacency(g)
# Permet de trouver le chemin le plus court 
shortest.paths(g)
# Calcule la moyenne de tous les chemins (les chemins les plus courts et les autres)
average.path.length(g)
#Calcule la moyenne du chemin le plus court 
mean(shortest.paths(g))


