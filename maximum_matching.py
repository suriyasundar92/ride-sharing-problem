import networkx as nx
import pickle
result_file = open('result_graph.p', 'wb')
graph = nx.Graph()
graph.add_nodes_from([1, 2, 3, 4, 5])
graph.add_edge(1,2, weight=4)
graph.add_edge(2,4, weight=5)
graph.add_edge(1,4, weight=3)
graph.add_edge(3,5, weight=1)
graph.add_edge(1,3, weight=2)
pickle.dump(graph, result_file)
print(nx.algorithms.matching.max_weight_matching(graph))