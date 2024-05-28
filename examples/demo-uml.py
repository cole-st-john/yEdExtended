# import
import yedextended as yed

# instantiate graph
graph1 = yed.Graph()

# Demonstration of some UML objects =========================================
car = graph1.add_node(
    "Car",
    shape_fill="#EEEEEE",
    node_type="UMLClassNode",
    UML={
        "attributes": "Model\nManufacturer\nPrice",
        "methods": "getModel()\ngetManufacturer()\ngetPrice()\nsetPrice()",
    },
)

icar = graph1.add_node(
    "ICar",
    shape_fill="#EEEEEE",
    node_type="UMLClassNode",
    UML={
        "stereotype": "interface",
        "attributes": "",
        "methods": "getModel()\ngetManufacturer()\ngetPrice()\nsetPrice()",
    },
)

vehicle = graph1.add_node("Vehicle", shape_fill="#EEEEEE", node_type="UMLClassNode")
graph1.add_edge(car, vehicle, arrowhead="white_delta")
graph1.add_edge(car, icar, arrowhead="white_delta", line_type="dashed")

graph1.add_node("This is a note", shape_fill="#EEEEEE", node_type="UMLNoteNode")

# Store Graph
graph1.persist_graph("demo-uml.graphml").open_with_yed()
