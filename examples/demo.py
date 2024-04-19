import yedextended as yed

graph1 = yed.Graph()


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

print(graph1.get_graph())

print("\n\n\n")

g = yed.Graph()
graph1.add_node(
	"foo",
	font_family="Zapfino",
)

group1 = graph1.add_group(
	"MY_Group",
	shape="diamond",
)
group1.add_node(
	"foo2",
	shape="roundrectangle",
	font_style="bolditalic",
	underlined_text="true",
)
group1.add_node(
	"abc",
	font_size="72",
	height="100",
)

graph1.add_edge("foo2", "abc")
graph1.add_edge("foo", "MY_Group")

print(graph1.get_graph())
