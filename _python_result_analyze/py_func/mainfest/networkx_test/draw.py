import networkx as nx
from pyvis.network import Network

graph = nx.read_multiline_adjlist('self.graph.adjlist', create_using=nx.DiGraph)
net = Network(height='750px', width='100%', notebook=True)
net.from_nx(graph)

net.barnes_hut()
neighbor_map = net.get_adj_list()

for node in net.nodes:
    node['title'] = ' Neighbors:\n' + '\n'.join(neighbor_map[node['id']])
    # change size of nodes according to neighbor nums
    # node['value'] = len(neighbor_map[node['id']])

net.set_options('''
    const options = {
      "physics": {
        "barnesHut": {
          "centralGravity": 1.8,
          "avoidOverlap": 0.20
        },
        "minVelocity": 0.75
      }
    }
''')

# use buttons to find options
# net.show_buttons(filter_=['physics'])

net.show("res.html")
