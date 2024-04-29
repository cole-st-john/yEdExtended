# import
import yedextended as yed

# Instantiate graph instance
graph1 = yed.Graph()

# Add graph nodes and edges with some examples of non-default formatting
graph1.add_node(
    "foo",
    font_family="Zapfino",
)

graph1.add_node(
    "foo2",
    shape="roundrectangle",
    font_style="bolditalic",
    underlined_text="true",
)

graph1.add_edge(
    "foo1",
    "foo2",
)
graph1.add_node(
    "abc",
    font_size="72",
    height="100",
)

graph1.add_node(
    "bar",
    label="Multi\nline\ntext",
)
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
