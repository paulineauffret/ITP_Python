#! /usr/bin/python

import sys

adj_list = []
visited = []
vertices=[]

def dfs(s, t):
    if s == t:
        return True

    visited[s] = True
    for v in adj_list[s]:
        if not visited[v]:
            if dfs(v, t):
                vertices.append(str(s) + " " + str(v))
                return True
    return False

def find_path(s, t):
    for i in range(len(adj_list)):
        visited.append(False)
    
    if (dfs(s, t)):
        print "There is a path from " + str(s) + " to " + str(t) + "."
    else:
        print "There is no path from " + str(s) + " to " + str(t) + "."
    j=len(vertices)
    while j!=0:
        print vertices[j-1]
        j=j-1

def read_graph_from_file(file_name):
    f = open(file_name, 'r')
    for line in f:
        elem_list = line.split()
        if (len(elem_list) == 1):
            for i in range(int(elem_list[0])):
                adj_list.append([])
        else:
            u, v = elem_list
            adj_list[int(u)].append(int(v))
    f.close()

#def afficher_chemin
	

def main():
    read_graph_from_file(sys.argv[1])
    s = int(sys.argv[2]) 
    t = int(sys.argv[3])
    find_path(s,t)
 
if __name__ == '__main__': 
    main() 

