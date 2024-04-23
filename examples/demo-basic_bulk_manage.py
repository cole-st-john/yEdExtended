import yedextended as yed

# EXAMPLE GRAPH IN MEMORY ======================================
# Instantiate graph
graph1 = yed.Graph()

# Add arbitrary graph detail
graph1.add_node("a")
graph1.add_node("b")
graph1.add_edge("a", "b")

# Add arbitrary graph group detail
group1 = graph1.add_group("group 1", shape="rectangle")
group1.add_node("c")
group1.add_node("d")
group1.add_edge("c", "d")

# subnested group
group1_1 = group1.add_group("group1_1")

# sub group elements
group1_1.add_node("e")
group1_1.add_node("f")
group1_1.add_edge("e", "f")

# Complex connections ==============
# standalone node to 2-time nested node
graph1.add_edge("a", "e")
# node to subnested group
graph1.add_edge("b", "group1_1")


# Examining the data in excel
graph1.manage_graph_data_in_excel()
