# import
import yedextended as yed

# Instantiate graph instance
graph1 = yed.Graph()

# Add arbitrary graph detail - nodes and edges
graph1.add_node("a")
graph1.add_node("b")
graph1.add_edge("a", "b")

# Add arbitrary graph detail - group and group objects
group1 = graph1.add_group("group 1", shape="rectangle")
group1.add_node("c")
group1.add_node("d")
group1.add_edge("c", "d")

graph1.persist_graph().open_with_yed()
