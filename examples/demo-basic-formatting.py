# Import
import yedextended as yed
import os

# Instantiate graph instance
graph1 = yed.Graph()

# Adding several nodes, edges and groups, using a few basic methods
graph1.add_node("foo", fontFamily="Zapfino")

graph1.add_node(
    "foo2",
    shape="roundrectangle",
    fontStyle="bolditalic",
    underlinedText="true",
)

graph1.add_edge("foo1", "foo2")

graph1.add_node("abc", fontSize="72", height="100", shapeFill="#FFFFFF")

graph1.add_node("bar").add_label("Multi\nline\ntext")

graph1.add_node(
    """Multi
    Line
    Text!""",
)

graph1.add_edge(
    "foo",
    "foo1",
    width="3.0",
    color="#0000FF",
    arrowhead="white_diamond",
    arrowfoot="standard",
    lineType="dotted",
).add_label("EDGE!")

# Demonstrate stringified graphml version of structure
print(graph1.stringify_graph())

# Several methods of writing graph to file ==============================
with open("test_graph.graphml", "w") as fp:  # using standard python functionality
    fp.write(graph1.stringify_graph())

saved_graph1 = graph1.persist_graph("example.graphml")  # using tool specific method

saved_graph2 = graph1.persist_graph("pretty_example.graphml", pretty_print=True)  # using tool specific method  with pretty print


# clean up after viewing
# os.remove(saved_graph1.fullpath)
# os.remove(saved_graph2.fullpath)
