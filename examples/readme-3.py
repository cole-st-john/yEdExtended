# import
import yedextended as yed

# Instantiate graph instance
graph1 = yed.Graph()

# Add graph nodes and edges with some examples of non-default formatting
foo = graph1.add_node(
    "foo",
    font_family="Zapfino",
)

foo2 = graph1.add_node(
    "foo2",
    shape="roundrectangle",
    font_style="bolditalic",
    underlined_text="true",
)

graph1.add_edge(
    "foo1",
    foo2,
)


graph1.add_node(
    "abc",
    font_size="72",
    height="100",
)

graph1.add_node("bar").add_label(
    "Multi\nline\ntext",
)
graph1.add_node(
    "foobar",
).add_label(
    """Multi
Line
Text!""",
)

graph1.add_edge(
    foo,
    foo2,
    name="EDGE!",
    width="3.0",
    color="#0000FF",
    arrowhead="white_diamond",
    arrowfoot="standard",
    line_type="dotted",
)

graph1.persist_graph().open_with_yed()
