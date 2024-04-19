import yedextended as yed

graph1 = yed.Graph()

n0 = graph1.add_node("node0")
group1 = graph1.add_group("main1")
n11 = group1.add_node("node11")
group12 = group1.add_group("sub12")
n121 = group12.add_node("node121")
group122 = group12.add_group("sub122")

graph1.persist_graph("test.graphml")
