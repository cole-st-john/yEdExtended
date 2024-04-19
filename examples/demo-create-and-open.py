import yedextended as yed

# Instantiate graph
graph1 = yed.Graph()

# Add arbitrary graph detail
group1 = graph1.add_group(
    "group 1",
    shape="rectangle",
)
group1.add_node("a")
group1.add_node("b")
group1.add_edge("a", "b")

# Storing a graph to file and opening it
graph_file = graph1.persist_graph("test.graphml")
graph_file.open_with_yed()

# Demo adding further node and reopening
input(
    "close current version in yEd and press key in terminal to open overwritten version"
)
group1.add_node("c")
graph1.persist_graph("test.graphml", overwrite=True).open_with_yed()
