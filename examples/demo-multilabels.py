import yedextended as yed

graph1 = yed.Graph()

# Label class is indeed abstract:
# label = yed.Label("test")


graph1.add_node(
    "foo",
    width="200",
    height="200",
    shapeFill="#FFFFFF",
    borderType="dotted",
).add_label("Center", fontFamily="Zapfino").add_label(
    "Top",
    modelPosition="t",
    fontFamily="Courier New",
    fontStyle="bold",
).add_label(
    "Left",
    modelName="internal",
    modelPosition="l",
    fontFamily="Arial",
    fontStyle="italic",
    textColor="#FF0000",
).add_label(
    "Right",
    modelName="internal",
    modelPosition="r",
    fontFamily="Tahoma",
    fontStyle="bold",
    textColor="#00FF00",
).add_label(
    "Bottom",
    modelName="internal",
    modelPosition="b",
    textColor="#0000FF",
)


graph1.add_node("foo2", width="100", height="100").add_label(
    "foo2",
).add_label(
    "North-West",
    modelName="corners",
    modelPosition="nw",
    fontFamily="Courier New",
    fontStyle="bold",
).add_label(
    "North-East",
    modelName="corners",
    modelPosition="ne",
    fontFamily="Arial",
    fontStyle="italic",
    textColor="#FF0000",
).add_label(
    "South",
    modelName="sides",
    modelPosition="s",
    fontFamily="Tahoma",
    fontStyle="bold",
    textColor="#00FF00",
).list_of_labels.pop(0)


graph1.add_edge(
    "foo",
    "foo2",
    width="3.0",
    color="#0000FF",
).add_label(
    "Head",
    modelName="two_pos",
    modelPosition="head",
    fontFamily="Courier New",
    fontStyle="bold",
    textColor="#FF00FF",
    backgroundColor="#FFFFFF",
).add_label(
    "Tail",
    modelName="two_pos",
    modelPosition="tail",
    fontFamily="Courier New",
    fontStyle="bold",
    backgroundColor="#FFFFFF",
).add_label(
    "Center",
    modelName="three_center",
    modelPosition="center",
    fontFamily="Courier New",
    fontStyle="bold",
    backgroundColor="#FFFFFF",
)

graph1.add_edge(
    "foo",
    "foo2",
    width="3.0",
    color="#0000FF",
).add_label(
    "Head",
    modelName="two_pos",
    modelPosition="head",
    fontFamily="Courier New",
    fontStyle="bold",
    textColor="#FF00FF",
    backgroundColor="#FFFFFF",
).add_label(
    "Tail2",
    modelName="two_pos",
    modelPosition="tail",
    fontFamily="Courier New",
    fontStyle="bold",
    backgroundColor="#FFFFFF",
).add_label(
    "Center2",
    modelName="three_center",
    modelPosition="center",
    fontFamily="Courier New",
    fontStyle="bold",
    backgroundColor="#FFFFFF",
)

graph1.persist_graph("demo_multilabel.graphml").open_with_yed()
