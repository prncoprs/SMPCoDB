import networkx as nx

DG = nx.DiGraph()

DG.add_nodes_from(["lineitem", "partsupp", "orders", "part", "supplier", "customer", "nation", "region"])
DG.add_edges_from([("lineitem", "partsupp"), ("lineitem", "orders"), ("partsupp", "part"), ("partsupp", "supplier"),
                   ("orders", "customer"), ("supplier", "nation"), ("customer", "nation"), ("nation", "region")])

# DG.add_node("partsupp")
# DG.add_node("orders")
# DG.add_node("supplier")
# DG.add_node("customer")
# DG.add_node("nation")

# DG.add_edge("lineitem", "partsupp")
# DG.add_edge("lineitem", "orders")
# DG.add_edge("partsupp", "supplier")
# DG.add_edge("orders", "customer")
# DG.add_edge("supplier", "nation")
# DG.add_edge("customer", "nation")

b = nx.is_directed_acyclic_graph(DG)
print(b)

node_list = ["lineitem", "orders", "customer"]
SDG = DG.subgraph(node_list)
c = nx.is_directed_acyclic_graph(SDG)

print(DG)
print(SDG.nodes)
print(SDG.edges)
print(c)
