# Here is a Python code that implements the ant colony algorithm for graph coloring:

# import the necessary libraries 
import networkx as nx 
from random import randint 

def is_valid_coloring(G):
    for e in G.edges :
        n1,n2=e
        if G.nodes[n1]['color']==G.nodes[n2]['color'] :
            return False  
    return True

def nb_colors(G) :
    return len(set([G.nodes[n]['color'] for n in G.nodes()])) 
    
def graphe1() : 
    # create a graph 
    G = nx.Graph() 
    #add nodes to the graph 
    G.add_nodes_from([0,1,2,3]) 
    # add edges to the graph 
    G.add_edges_from([(0,1), (1,2), (2,3)])
    return G
    # Graphe G1 (3 couleurs suffisent : )
    #Final :  [(0, {'color': 2}), (1, {'color': 1}), (2, {'color': 2}), (3, {'color': 0})]
    #===> utilise  3 couleurs 
 
def graphe2() : 
    # create a graph 
    G = nx.Graph() 
    G.add_nodes_from([1,2,3,4,5]) 
    G.add_edges_from([(1,5), (5,3), (5,4), (2,3), (2,4)])
    return G
     
    #G= [(1, 5), (2, 3), (2, 4), (3, 5), (4, 5)]
    #Final :  [(1, {'color': 3}), (2, {'color': 0}), (3, {'color': 3}), (4, {'color': 3}),
    # (5, {'color': 0})] => utilise  2 couleurs
   
if __name__ == "__main__" :
    G=graphe2()
    
    # set the number of iterations 
    iter_count = 50

    # assign random colors to the nodes 
    for n in G.nodes(): 
        G.nodes[n]['color'] = randint(0, len(G.nodes())-1) 

    # set the number of ants 
    num_ants = 100
    
    nb_nodes=len(G.nodes())
    min_n=min(G.nodes())
    max_n=max(G.nodes())
    best_nb_colors = nb_nodes
    best_G=(G.copy(), nb_nodes)
    
    # Ant colony optimization 
    for i in range(iter_count): 
        # for each ant 
        for j in range(num_ants): 
            # randomly select a node 
            #current_node = randint(0, 3) 
            current_node = randint(min_n, max_n) 
            # choose a color 
            color = randint(0, len(G.nodes())-1) 
            # if the color is different 
            if G.nodes[current_node]['color'] != color: 
                # assign the new color 
                G.nodes[current_node]['color'] = color 
                # check if the new coloring is valid 
                #if nx.algorithms.coloring.is_valid_coloring(G): 
                if is_valid_coloring(G): 
                    print('Coloring found!') 
                    print(G.nodes(data=True)) 
                    print("===> utilise ", nb_colors(G), "couleurs ")
                    if  nb_colors(G) < best_G[1] :
                        best_G=(G.copy(), nb_colors(G))
                        
                    break 
                    

    # print the final graph 
    print("G=", G.edges)
    #print("Final : " , G.nodes(data=True))
    print("Final : " , best_G[0].nodes(data=True), end=' ')
    print("=> utilise ", best_G[1], "couleurs ")
