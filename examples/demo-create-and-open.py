import yedextended as yed

# Instantiate graph
graph1 = yed.Graph()

# Add arbitrary graph detail
graph1.add_node("a")
graph1.add_node("b")
graph1.add_edge("a", "b")

# Add arbitrary graph group detail
group1 = graph1.add_group(
    "group 1",
    shape="rectangle",
)
group1.add_node("c")
group1.add_node("d")
group1.add_edge("c", "d")

# Storing a graph to file and opening it
graph_file = graph1.persist_graph("test.graphml").open_with_yed()
