import numpy as np
import networkx as nx
import hiperwalk as hpw

N = 128
K_N = nx.complete_graph(N)
A = nx.adjacency_matrix(K_N)+np.eye(N)
graph = hpw.Graph(A)
qw = hpw.Coined(graph, shift='flipflop', coin='G', marked={'-G': [0]})
r = (round(4*np.pi*np.sqrt(N)/4) + 1)
states = qw.simulate(range=r,
                     state=qw.uniform_state())

print(states)
