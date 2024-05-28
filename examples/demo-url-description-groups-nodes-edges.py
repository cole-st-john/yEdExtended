"""
Demo script for utilising the yedextended "Adding URL & Description for Group, Node and Edge Elements" feature.
"""

# import
import yedextended as yed

# instantiate graph
graph1 = yed.Graph()

# Demonstration of urls / descriptions on various objects ======================

# Create GroupNode
italy = graph1.add_group(
    "Italy",
    description="Italy, country of south-central Europe, occupying a peninsula that juts deep into the Mediterranean Sea.",
    url="https://en.wikipedia.org/wiki/Italy",
)

# Create Nodes
italy.add_node(
    "Turin",
    description="Turin is the capital city of Piedmont in northern Italy, known for its refined architecture and cuisine.",
    url="http://www.comune.torino.it",
)
italy.add_node(
    "Brescia",
    description="Brescia is a city in the northern Italian region of Lombardy.",
    url="https://www.comune.brescia.it/Pagine/default.aspx",
)
italy.add_node(
    "Ivrea",
    description="Ivrea is a town and comune of the Metropolitan City of Turin in the Piedmont region of northwestern Italy.",
    url="https://www.comune.ivrea.to.it/",
)
italy.add_node(
    "Savona",
    description="Savona is a port city in Liguria, northwest Italy.",
    url="https://www.comune.savona.it/it/",
)

# Create Edges
italy.add_edge(
    "Turin",
    "Brescia",
    name="E64",
    arrowhead="none",
    description="Length	246 km (153 mi)",
    url="https://en.wikipedia.org/wiki/European_route_E64",
)
italy.add_edge(
    "Turin",
    "Ivrea",
    name="E612",
    arrowhead="none",
    description="Length	54 km (34 mi)",
    url="https://en.wikipedia.org/wiki/European_route_E612",
)
italy.add_edge(
    "Turin",
    "Savona",
    name="E717",
    arrowhead="none",
    description="Length	141 km (88 mi)",
    url="https://en.wikipedia.org/wiki/European_route_E717",
)

# Write Graph
graph1.persist_graph("demo-url-description-groups-nodes-edges.graphml", pretty_print=True).open_with_yed()

print(40 * "=")
print("""
DONE!

The yEd graph Editor allows to easily bind an URL and a description to groups, nodes and edges.
A description can be used to store additional text besides the label texts.
Typically, it is presented as tooltip when the mouse hovers above a graph element.

Open the file in yEd now.

Click on group, node or edge.  

Press F6 to view 'data' tab : objects URL and description

Press F8 to open the URL in default web browser.

More info available in the yEd Help pages.
""")
print(40 * "=")
print("")
