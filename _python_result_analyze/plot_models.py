# import networkx as nx
# import numpy as np
# import matplotlib.pyplot as plt
# import pylab

# G = nx.DiGraph()

# G.add_edges_from([('A', 'B'),('C','D'),('G','D')], weight=1)
# G.add_edges_from([('D','A'),('D','E'),('B','D'),('D','E')], weight=2)
# G.add_edges_from([('B','C'),('E','F')], weight=3)
# G.add_edges_from([('C','F')], weight=4)


# val_map = {'A': 1.0,
#                    'D': 0.5714285714285714,
#                               'H': 0.0}

# values = [val_map.get(node, 0.45) for node in G.nodes()]
# edge_labels=dict([((u,v,),d['weight'])
#                  for u,v,d in G.edges(data=True)])
# red_edges = [('C','D'),('D','A')]
# edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]

# pos=nx.spring_layout(G)
# nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
# nx.draw(G,pos, node_color = values, node_size=1500,edge_color=edge_colors,edge_cmap=plt.cm.Reds)
# pylab.show()

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edges_from(
    [('A', 'B'), ('A', 'C'), ('D', 'B'), ('E', 'C'), ('E', 'F'),
     ('B', 'H'), ('B', 'G'), ('B', 'F'), ('C', 'G')])

val_map = {'A': 1.0,
           'D': 0.5714285714285714,
           'H': 0.0}

values = [val_map.get(node, 0.25) for node in G.nodes()]

# Specify the edges you want here
red_edges = [('A', 'C'), ('E', 'C')]
edge_colours = ['black' if not edge in red_edges else 'red'
                for edge in G.edges()]
black_edges = [edge for edge in G.edges() if edge not in red_edges]

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
                       node_color = values, node_size = 500)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
plt.show()