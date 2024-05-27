import yedextended as yed

# Instantiate graph
graph1 = yed.Graph()

# Add arbitrary graph detail - nodes and edges
a = graph1.add_node("a")
b = graph1.add_node("b")
graph1.add_edge(a, b)

# Add arbitrary graph detail - group and group objects
group1 = graph1.add_group("group 1", shape="rectangle")
c = group1.add_node("c")
d = group1.add_node("d")
group1.add_edge(c, d)

# subnested group
group1_1 = group1.add_group("group1_1")

# sub group elements
e = group1_1.add_node("e")
f = group1_1.add_node("f")
group1_1.add_edge(e, f)

# Complex connections ==============
# Standalone node to 2-layer-nested node
graph1.add_edge(a, e)
# Standalone node to subnested group
graph1.add_edge(b, group1_1)

# Storing a graph to file and opening it
graph1.persist_graph("test.graphml", overwrite=True).open_with_yed()
