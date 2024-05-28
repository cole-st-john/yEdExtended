"""
Demo script for utilising the yedextended "Adding Custom Properties for Node and Edge objects" feature.
"""

import yedextended as yed

graph1 = yed.Graph()

# Define Node Custom Properties
"""
scope: node
name: name of the custom property
property_type: [string|boolean|int|double]
                boolean: Java keywords [true|false]
default_value: any above datatype represented as a string
"""
graph1.define_custom_property("node", "Population", "int", "0")
graph1.define_custom_property("node", "Unemployment", "double", "0.0")
graph1.define_custom_property("node", "Environmental Engagements", "boolean", "false")
graph1.define_custom_property("node", "Mayor", "string", "")
graph1.define_custom_property("node", "Country", "string", "")

# Define Edge Custom Properties
"""
scope: edge
name: name of the custom property
property_type: [string|boolean|int|double]
                boolean: Java keywords [true|false]
default_value: any above datatype represented as a string
"""
graph1.define_custom_property("edge", "Distance", "int", "0")
graph1.define_custom_property("edge", "Availability", "double", "100.0")
graph1.define_custom_property("edge", "Toll Free", "boolean", "true")
graph1.define_custom_property("edge", "Year of build", "string", "")

# Create Groups
group1 = graph1.add_group("group1", custom_properties={"Country": "Kitchen"})


# Create Nodes
pasta_city = graph1.add_node(
    "Pasta City",
    custom_properties={
        "Population": "13000",
        "Unemployment": "13.7",
        "Environmental Engagements": "true",
        "Mayor": "Genarro",
    },
)


wurst_stadt = graph1.add_node(
    "Wurst Stadt",
    custom_properties={"Population": "25100", "Unemployment": "6.2", "Mayor": "Orlowsky"},
)
gruyereville = graph1.add_node(
    "Gruyereville",
    custom_properties={
        "Population": "29650",
        "Unemployment": "11.8",
        "Environmental Engagements": "true",
        "Mayor": "Delage",
    },
)

# Create Edges
graph1.add_edge(
    pasta_city,
    wurst_stadt,
    name="N666",
    arrowhead="none",
    custom_properties={
        "Year of build": "1974",
        "Distance": "356",
        "Toll Free": "false",
        "Availability": "85.7",
    },
)
graph1.add_edge(
    pasta_city,
    gruyereville,
    name="E55",
    arrowhead="none",
    custom_properties={
        "Year of build": "1986",
        "Distance": "1444",
        "Availability": "96.7",
    },
)
graph1.add_edge(
    gruyereville,
    wurst_stadt,
    name="E23",
    arrowhead="none",
    custom_properties={"Year of build": "2011", "Distance": "740", "Toll Free": "false"},
)

# Write Graph
graph1.persist_graph("demo-custom-properties-nodes-edges.graphml", pretty_print=True).open_with_yed()

print(40 * "=")
print("""
DONE!

Open the file in yEd now.
Click on the nodes and the edges, press F6 and select the 'data' tab to view the custom properties.

Node Custom Properties will show up into the yEd 'Structure View Window'.

All Custom Properties definitions should be populated into the 'Manage Custom Properties Menu'

To select Nodes & Edges based on Custom Properties open yEd 'Tools Menu' -> 'Select Elements' and define criteria in
the 'Nodes' and 'Edges' tabs
""")
print(40 * "=")
print("")
