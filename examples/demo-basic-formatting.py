# Import
import yedextended as yed

# Instantiate graph instance
graph1 = yed.Graph()

# Adding several nodes, edges and groups, using a few basic methods
graph1.add_node("foo", font_family="Zapfino")

graph1.add_node(
    "foo2",
    shape="roundrectangle",
    font_style="bolditalic",
    underlined_text="true",
)

graph1.add_edge("foo1", "foo2")

graph1.add_node("abc", font_size="72", height="100", shape_fill="#FFFFFF")

graph1.add_node("bar", label="Multi\nline\ntext")

graph1.add_node(
    "foobar",
    label="""Multi
    Line
    Text!""",
)

graph1.add_edge(
    "foo",
    "foo1",
    label="EDGE!",
    width="3.0",
    color="#0000FF",
    arrowhead="white_diamond",
    arrowfoot="standard",
    line_type="dotted",
)

# Demonstrate stringified graphml version of structure
print(graph1.stringify_graph())

# Several methods of writing graph to file ==============================
with open("test_graph.graphml", "w") as fp:  # using standard python functionality
    fp.write(graph1.stringify_graph())

graph1.persist_graph("example.graphml")  # using tool specific method

graph1.persist_graph("pretty_example.graphml", pretty_print=True)  # using tool specific method  with pretty print
