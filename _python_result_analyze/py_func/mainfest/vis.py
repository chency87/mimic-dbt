import networkx as nx
from pyvis.network import Network
from typing import Any, Generator, List, Dict

_WIDTH = '100%'
_HEIGHT = '1050px'

class GraphVis:

    def __call__(self, graph: nx.DiGraph, manifest: Dict) -> Any:
        self.graph = graph
        self.manifest = manifest

        self.pos_y = {}
        self.scores = self._get_scores(self.graph)
        self._graph_vis()
        # return 

    def _grouped_topological_sort(self, 
        graph: nx.DiGraph,
    ) -> Generator[List[str], None, None]:
        """Topological sort of given graph that groups ties.
        Adapted from `nx.topological_sort`, this function returns a topo sort of a graph however
        instead of arbitrarily ordering ties in the sort order, ties are grouped together in
        lists.
        Args:
            graph: The graph to be sorted.
        Returns:
            A generator that yields lists of nodes, one list per graph depth level.
        """
        indegree_map = {v: d for v, d in graph.in_degree() if d > 0}
        zero_indegree = [v for v, d in graph.in_degree() if d == 0]

        while zero_indegree:
            yield zero_indegree
            new_zero_indegree = []
            for v in zero_indegree:
                for _, child in graph.edges(v):
                    indegree_map[child] -= 1
                    if not indegree_map[child]:
                        new_zero_indegree.append(child)
            zero_indegree = new_zero_indegree

    def _get_scores(self, graph: nx.DiGraph) -> Dict[str, int]:
        """Scoring nodes for processing order.
        Scores are calculated by the graph depth level. Lowest score (0) should be processed first.
        Args:
            graph: The graph to be scored.
        Returns:
            A dictionary consisting of `node name`:`score` pairs.
        """
        # split graph by connected subgraphs
        subgraphs = (graph.subgraph(x) for x in nx.connected_components(nx.Graph(graph)))

        # score all nodes in all subgraphs
        scores = {}
        
        for subgraph in subgraphs:
            grouped_nodes = self._grouped_topological_sort(subgraph)
            for level, group in enumerate(grouped_nodes):
                le_list = []
                for node in group:
                    le_list.append(node)
                    scores[node] = level
                self.pos_y[f'level_{level}'] = le_list if f'level_{level}' not in self.pos_y else self.pos_y[f'level_{level}'].merge(le_list)
                    # print(f'position for {node} is {x_pos.send(level)}')

                    # print(level)
        return scores
    def _yield_pos_x(self, idx):
        i = 0
        while True:
            x = yield i + idx * 100
            idx = idx if x is None else x
    def _yield_pos_y(self, idx):
        i = 0
        while True:
            y = yield i + idx * 50
            i = y
            idx = idx if y is None else y

    def _get_color(self, color = None):
        colors = {
            'cte' : 'red',
            'subquery' : 'green',
            'src' : 'blue'

        }
        return colors[color] if color in colors else 'Purple'

    def _graph_vis(self):

        net = Network(height= _HEIGHT, width= _WIDTH, notebook=False, directed =True)

        for node in self.graph:
            # ['size', 'value', 'title', 'x', 'y', 'label', 'color']
            x = self.scores[node] * 200
            y = 0
            le_list = self.pos_y[f'level_{self.scores[node]}']
            y =le_list.index(node) * 150
            color = self._get_color(self.manifest[node].q_type) if node in self.manifest else self._get_color()
            title = self.manifest[node].raw if node in self.manifest else None
            value=  self.manifest[node].where if node in self.manifest else None
            net.add_node(node, physics = False,x = x, y = y, color = color)

        net.barnes_hut()
        neighbor_map = net.get_adj_list()
        for node in net.nodes:
            idx = node['id']
            # print(node[id])
            rel_name =  self.manifest[idx].rel_name if idx in self.manifest else None
            node['title'] = f' References: \n' + '\n'.join([it for it in rel_name ] if rel_name is not None else [])
            node['title'] += '\n\n'
            node['title'] +=  self.manifest[idx].raw if idx in self.manifest else ''
            # node['title'] = f"{node['x']}, {node['y']}"
            # change size of nodes according to neighbor nums
            # node['value'] = len(neighbor_map[node['id']])

        net.add_edges(self.graph.edges)

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

    def _set_lengend(self):
        pass