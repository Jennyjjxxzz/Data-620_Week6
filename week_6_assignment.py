# -*- coding: utf-8 -*-
"""Week 6 Assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11fJpM-sOhrYUwit9gSoBrGy2RVKK3Anc

## Week 6 Assignment: Data Sets

Here is a dataset that shows a simple 2-node network:  the attendance of 18 Southern Women at 14 social events:

1. Brief Description. Small “musty” datasets like that from this 1941 study have proven very valuable in testing and comparing new network algorithms.
2. Dataset.
3. Python code to create dataset: https://networkx.github.io/documentation/stable/auto_examples/algorithms/plot_davis_club.html
**What can you infer about the relationships between (1) the women, and (2) the social events?  **
"""

import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.bipartite as bipartite

G = nx.davis_southern_women_graph()
women = G.graph['top']
clubs = G.graph['bottom']

"""List of women's name"""

print(women)

"""Clubs' name"""

print(clubs)

nx.draw(G)
plt.show()

print("Biadjacency matrix")
print(bipartite.biadjacency_matrix(G, women, clubs))

# project bipartite graph onto women nodes
W = bipartite.projected_graph(G, women)
print()
print("#Friends, Member")
for w in women:
    print(f"{W.degree(w)} {w}")

# project bipartite graph onto women nodes keeping number of co-occurrence
# the degree computed is weighted and counts the total number of shared contacts
W = bipartite.weighted_projected_graph(G, women)
print()
print("#Friend meetings, Member")
for w in women:
    print(f"{W.degree(w, weight='weight')} {w}")

# Compute centrality measures
degree_centrality = bipartite.degree_centrality(G, women)
eigenvector_centrality = nx.eigenvector_centrality(G)

# Convert to DataFrame
df = pd.DataFrame({
    'Node': list(degree_centrality.keys()),
    'Degree Centrality': list(degree_centrality.values()),
    'Eigenvector Centrality': [eigenvector_centrality[n] for n in degree_centrality.keys()],
    'Type': ['Woman' if n in women else 'Event' for n in degree_centrality.keys()]
})

print(df)

# Draw the graph
pos = nx.bipartite_layout(G, women)
plt.figure(figsize=(10, 8))
nx.draw(
    G, pos, with_labels=True, node_color=['lightblue' if n in women else 'lightcoral' for n in G.nodes()],
    edge_color='gray', node_size=800, font_size=10
)

plt.title("Southern Women Network", fontsize=14)
plt.show()

"""**Graphic 1**
1. Key Women Social Figures: Evelyn, Jefferson, Laura Mandeville, and Nora Fayette have higher degree centrality. Meaning, they attended more events and played a main role in different event groups.

2. Some of the events are popular such as E9, E8, and E7. Some events connect women who wouldn't typically interact.

3. The socialnetwork was not random, it was around certain key figures and events. The shared event participation makes them closely tied together.
"""

weights = [edata['weight'] for f,t,edata in W.edges(data=True)]
plt.figure(figsize = (15,10))
nx.draw_networkx(W, width=weights, edge_color=weights)

"""**Graphic 2**

**Key Observations:**

**Nodes**: Represent individual women

**Edges**: Represent attendance at events

**Edge Thickness**: Indicate the number of shared events.
Thicker edges = More shared events.

**Edge Color Variation**:
1. Lighter (yellow/green) edges likely indicate stronger relationships
2. Darker (blue/purple) edges represent weaker ties.

**Bridge figures**: Some women (such as Evelyn, Jefferson, Laura Mandeville, and Nora Fayette) connect across two or more communities, serving as bridges between the social circles.
"""