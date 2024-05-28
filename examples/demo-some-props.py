import yedextended as yed

graph1 = yed.Graph()
graph1.define_custom_property("node", "Population", "int", "0")
graph1.define_custom_property("edge", "Population", "int", "1")

group1 = graph1.add_group("group1", custom_properties={"Population": "2"})
node1 = graph1.add_node("a")
edge1 = graph1.add_edge("group1", "a")
node2 = group1.add_node("b")
node3 = group1.add_node("c", custom_properties={"Population": "3"})
print(node1.Population)
print(node2.Population)
print(node3.Population)
print(edge1.Population)
print(group1.Population)

graph1.persist_graph(overwrite=True).open_with_yed()

#
