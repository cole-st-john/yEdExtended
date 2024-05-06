import asyncio
import os
import platform
import xml.etree.ElementTree as xml
from time import sleep

import pytest

import yedextended as yed

# Set the trigger variable to True for testing
yed.testing = True


class Test_File:
    """Testing File class"""

    def test_file_object_basics(self):
        # Given: yed file object
        # When: given no basename or path
        # Then: returns default graphml basename and working dir path
        test_file_obj = yed.File()
        assert test_file_obj.basename == "temp.graphml"
        assert test_file_obj.window_search_name == "temp.graphml - yEd"
        assert test_file_obj.dir == os.getcwd()

        # Given: yed file object
        # When: given simple name w/o path
        # Then: returns same basename and working dir path
        test_file_obj = yed.File("abc.graphml")
        assert test_file_obj.basename == "abc.graphml"
        assert test_file_obj.window_search_name == "abc.graphml - yEd"
        assert test_file_obj.dir == os.getcwd()

        # Given: yed file object
        # When: given simple name w/ relative path (and cwd with that rel path)
        # Then: returns same basename and working dir path
        test_file_obj = yed.File("examples\\abc.graphml")
        assert test_file_obj.basename == "abc.graphml"
        assert test_file_obj.window_search_name == "abc.graphml - yEd"
        assert test_file_obj.fullpath.endswith("examples\\abc.graphml")
        assert os.path.exists(test_file_obj.dir) is True

        # Given: yed file object
        # When: given simple name and bad path
        # Then: returns same basename and diff path
        test_file_obj = yed.File(r"c:\fakepath11\abc.graphml")
        assert test_file_obj.basename == "abc.graphml"
        assert test_file_obj.dir == os.getcwd()

        # Given: yed file object
        # When: given simple name and valid path
        # Then: returns same basename and path
        test_file_obj = yed.File(os.path.join(os.getcwd(), "abc.graphml"))
        assert test_file_obj.basename == "abc.graphml"
        assert test_file_obj.dir == os.getcwd()

    # Given: yEd is installed
    # When: triggering open_with_yed
    # Then: file should be opened
    @pytest.mark.skipif(
        os.environ.get("CI") is not True or not platform.platform().startswith("Windows"),
        reason="Test not suitable for CI / Non-windows environments at this time",
    )
    def test_file_object_app(self):
        test_file_obj = yed.File("examples\\test.graphml")
        process = test_file_obj.open_with_yed()
        assert process is not None, "Expected a process object, but got None"

        yed.kill_yed()


def test_graph_added_node_has_default_fill():
    g = yed.Graph()
    g.add_node("N1")
    assert "#FFCC00" == g.nodes["N1"].shape_fill


def test_graph_added_node_keeps_custom_fill():
    g = yed.Graph()
    g.add_node("N1", shape_fill="#99CC00")
    assert "#99CC00" == g.nodes["N1"].shape_fill


def test_node_properties_after_nodes_and_edges_added():
    g = yed.Graph()

    g.add_node("foo", shape="ellipse")
    g.add_node("foo2", shape="roundrectangle", font_style="bolditalic")
    g.add_node("abc", shape="triangle", font_style="bold")
    g.add_edge("foo1", "foo2")

    assert g.nodes["foo"].shape == "ellipse"
    assert g.nodes["foo"].list_of_labels[0]._params["fontStyle"] == "plain"

    assert g.nodes["foo2"].shape == "roundrectangle"
    assert g.nodes["foo2"].list_of_labels[0]._params["fontStyle"] == "bolditalic"

    assert g.nodes["abc"].shape == "triangle"
    assert g.nodes["abc"].list_of_labels[0]._params["fontStyle"] == "bold"


def test_uml_node_properties_are_set():
    g = yed.Graph()

    expected_attributes = "int foo\nString bar"
    expected_methods = "foo()\nbar()"
    expected_stereotype = "abstract"

    g.add_node(
        "AbstractClass",
        node_type="UMLClassNode",
        UML={
            "stereotype": expected_stereotype,
            "attributes": expected_attributes,
            "methods": expected_methods,
        },
    )

    assert g.nodes["AbstractClass"].UML["stereotype"] == expected_stereotype
    assert g.nodes["AbstractClass"].UML["attributes"] == expected_attributes
    assert g.nodes["AbstractClass"].UML["methods"] == expected_methods

    graphml = g.stringify_graph()
    assertUmlNode(graphml, expected_stereotype, expected_attributes, expected_methods)


def test_uml_stereotype_is_optional():
    g = yed.Graph()

    expected_attributes = "int foo\nString bar"
    expected_methods = "foo()\nbar()"

    g.add_node(
        "Class",
        node_type="UMLClassNode",
        UML={"attributes": expected_attributes, "methods": expected_methods},
    )

    assert g.nodes["Class"].UML["methods"] == expected_methods
    assert g.nodes["Class"].UML["attributes"] == expected_attributes

    graphml = g.stringify_graph()
    assertUmlNode(graphml, "", expected_attributes, expected_methods)


def assertUmlNode(graphml, expected_stereotype, expected_attributes, expected_methods):
    doc = xml.fromstring(graphml)
    nsmap = {
        "g": "http://graphml.graphdrawing.org/xmlns",
        "y": "http://www.yworks.com/xml/graphml",
    }
    umlnode = doc.find("g:graph/g:node/g:data/y:UMLClassNode/y:UML", namespaces=nsmap)
    attributes = umlnode.find("y:AttributeLabel", namespaces=nsmap)
    methods = umlnode.find("y:MethodLabel", namespaces=nsmap)

    assert umlnode.attrib["stereotype"] == expected_stereotype
    assert attributes.text == expected_attributes
    assert methods.text == expected_methods


def test_numeric_node_ids():
    g = yed.Graph()
    g.add_node(1, label="Node1")
    g.add_node(2, label="Node2")
    g.add_edge(1, 2)

    assert g.nodes[1].list_of_labels[0]._text == "Node1"
    assert g.nodes[2].list_of_labels[0]._text == "Node2"

    node1 = g.edges["1"].node1
    node2 = g.edges["1"].node2

    assert g.nodes[node1].list_of_labels[0]._text == "Node1"
    assert g.nodes[node2].list_of_labels[0]._text == "Node2"

    assert g.stringify_graph()


def test_multiple_edges():
    g = yed.Graph()
    g.add_node("a", font_family="Zapfino").add_label("a2")
    g.add_node("b", font_family="Zapfino").add_label("b2")
    g.add_node("c", font_family="Zapfino").add_label("c2")

    g.add_edge("a", "b")
    g.add_edge("a", "b")
    g.add_edge("a", "c")

    e1 = g.edges["1"]
    e2 = g.edges["2"]
    e3 = g.edges["3"]

    assert g.nodes[e1.node1].list_of_labels[0]._text == "a"
    assert g.nodes[e1.node2].list_of_labels[0]._text == "b"

    assert g.nodes[e2.node1].list_of_labels[0]._text == "a"
    assert g.nodes[e2.node2].list_of_labels[0]._text == "b"

    assert g.nodes[e3.node1].list_of_labels[0]._text == "a"
    assert g.nodes[e3.node2].list_of_labels[0]._text == "c"

    # Test-cases for the second label
    assert g.nodes[e1.node1].list_of_labels[1]._text == "a2"
    assert g.nodes[e1.node2].list_of_labels[1]._text == "b2"

    assert g.nodes[e2.node1].list_of_labels[1]._text == "a2"
    assert g.nodes[e2.node2].list_of_labels[1]._text == "b2"

    assert g.nodes[e3.node1].list_of_labels[1]._text == "a2"
    assert g.nodes[e3.node2].list_of_labels[1]._text == "c2"

    assert g.stringify_graph()


def test_node_already_there_check():
    g = yed.Graph()
    g.add_node("a")
    with pytest.raises(RuntimeWarning):
        g.add_node("a")
    with pytest.raises(RuntimeWarning):
        g.add_group("a")

    g = yed.Graph()
    g.add_group("a")
    with pytest.raises(RuntimeWarning):
        g.add_node("a")
    with pytest.raises(RuntimeWarning):
        g.add_group("a")

    g = yed.Graph()
    g.add_edge("a", "b")
    with pytest.raises(RuntimeWarning):
        g.add_node("a")
    with pytest.raises(RuntimeWarning):
        g.add_group("a")
    g1 = g.add_group("g1")
    with pytest.raises(RuntimeWarning):
        g1.add_node("a")
    with pytest.raises(RuntimeWarning):
        g1.add_group("a")

    g = yed.Graph()
    g1 = g.add_group("g1")
    g1.add_node("a")
    g2 = g.add_group("g2")
    with pytest.raises(RuntimeWarning):
        g.add_node("a")
    with pytest.raises(RuntimeWarning):
        g.add_group("a")
    with pytest.raises(RuntimeWarning):
        g1.add_node("a")
    with pytest.raises(RuntimeWarning):
        g1.add_group("a")
    with pytest.raises(RuntimeWarning):
        g2.add_node("a")
    with pytest.raises(RuntimeWarning):
        g2.add_group("a")


def test_nested_graph_edges():
    g = yed.Graph()
    g.add_edge("a", "b")
    g1 = g.add_group("g1")
    g1n1 = g1.add_node("g1n1")
    g1n1 = g1.add_node("g1n2")
    g2 = g1.add_group("g2")
    g2n1 = g2.add_node("g2n1")
    g2n2 = g2.add_node("g2n2")
    g3 = g1.add_group("g3")
    g3n1 = g3.add_node("g3n1")
    g3n2 = g3.add_node("g3n2")

    assert g.num_edges == 1
    g1.add_edge("g1n1", "g1n2")
    assert g.num_edges == 2
    g2.add_edge("g2n2", "g2n2")  # No, that's not a typo
    assert g.num_edges == 3
    g3.add_edge("c", "d")
    g3.add_edge("c", "d")
    assert g.num_edges == 5

    g.add_edge("g2n1", "g2n2")
    g1.add_edge("g2n1", "g2n2")
    g2.add_edge("g2n1", "g2n2")
    with pytest.raises(RuntimeWarning):
        g3.add_edge("g2n1", "g2n2")
    assert g.num_edges == 8

    with pytest.raises(RuntimeWarning):
        g2.add_edge("a", "b")

    g.add_edge("g1n1", "g2n2")
    g1.add_edge("g1n1", "g2n2")
    with pytest.raises(RuntimeWarning):
        g2.add_edge("g1n1", "g2n2")
    with pytest.raises(RuntimeWarning):
        g3.add_edge("g1n1", "g2n2")
    assert g.num_edges == 10


@pytest.mark.skipif(
    os.environ.get("CI") is not True or not platform.platform().startswith("Windows"),
    reason="Test not suitable for CI / Non-windows environments at this time",
)
def test_start_yed():
    process = yed.start_yed()
    assert process is not None, "Expected a process object, but got None"
    yed.kill_yed()  # redundant


@pytest.mark.skipif(
    os.environ.get("CI") is not True or not platform.platform().startswith("Windows"),
    reason="Test not suitable for CI / Non-windows environments at this time",
)
def test_is_yed_open():
    # Initialize the test YED file
    test_graph = yed.File("examples\\yed_created_edges.graphml")

    # Open the YED file asynchronously and await its completion
    process = test_graph.open_with_yed()

    # Assert that the result is not None
    assert process is not None, "Expected a process object, but got None"

    # Assert that YED is findable
    assert yed.is_yed_findable() is True

    # Kill the YED process
    yed.kill_yed()


def test_xml_to_simple_string():
    # Given: yEd utility

    # When: valid file with items needing simplification
    # Then: returns simplified string
    test_string = yed.xml_to_simple_string("examples\\yed_created_edges.graphml")
    assert test_string.find("\n") == -1

    # When: invalid file
    # Then: returns Exception

    with pytest.raises(FileNotFoundError):
        yed.xml_to_simple_string("not_existing_file")


class Test_GraphStats:
    def test_graph_stats_basic(self):
        # Given: existing graph of known stats
        test_graph = yed.Graph().from_existing_graph("examples\\yed_created_edges.graphml")

        # When: taking the stats
        results_stats = test_graph.gather_graph_stats()

        # Then: we can assume the following stats
        assert len(results_stats.all_edges) == 3
        assert len(results_stats.all_groups) == 1
        assert len(results_stats.all_nodes) == 4

        # Given: existing graph of known stats - empty
        test_graph = yed.Graph().from_existing_graph("examples\\yed_created_empty_graph.graphml")

        # When: taking the stats
        results_stats = test_graph.gather_graph_stats()

        # Then: we can assume the following stats
        assert len(results_stats.all_edges) == 0
        assert len(results_stats.all_groups) == 0
        assert len(results_stats.all_nodes) == 0


def test_custom_property_assignment():
    graph1 = yed.Graph()

    graph1.define_custom_property("node", "Population", "int", "0")
    graph1.define_custom_property("edge", "Population", "int", "1")
    group1 = graph1.add_group("group1", custom_properties={"Population": "2"})
    node1 = graph1.add_node("a")
    edge1 = graph1.add_edge("group1", "a")
    node2 = group1.add_node("b")
    node3 = group1.add_node("c", custom_properties={"Population": "3"})

    assert node1.Population == "0", "Property not as expected"
    assert node2.Population == "0", "Property not as expected"
    assert node3.Population == "3", "Property not as expected"
    assert edge1.Population == "1", "Property not as expected"
    assert group1.Population == "2", "Property not as expected"
