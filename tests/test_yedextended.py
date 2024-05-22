import os
import platform
import xml.etree.ElementTree as xml
import io
import openpyxl as pyxl
import pytest

import yedextended as yed

# Triggers around testing completion
yed.testing = True
local_testing = os.environ.get("CI") == "True" and platform.platform().startswith("Windows")


class Test_File:
    """Testing File class"""

    def test_file_object_basics(self):
        # Given: yed file object
        # When: given no basename or path
        # Then: returns default graphml basename and working dir path
        test_file_obj = yed.File()
        assert test_file_obj.basename == "temp.graphml"
        assert test_file_obj.window_search_name == "temp.graphml - yEd"
        assert test_file_obj.dir.lower() == os.getcwd().lower()

        # Given: yed file object
        # When: given simple name w/o path
        # Then: returns same basename and working dir path
        test_file_obj = yed.File("abc.graphml")
        assert test_file_obj.basename == "abc.graphml"
        assert test_file_obj.window_search_name == "abc.graphml - yEd"
        assert test_file_obj.dir.lower() == os.getcwd().lower()

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
        assert test_file_obj.dir.lower() == os.getcwd().lower()

        # Given: yed file object
        # When: given simple name and valid path
        # Then: returns same basename and path
        test_file_obj = yed.File(os.path.join(os.getcwd(), "abc.graphml"))
        assert test_file_obj.basename == "abc.graphml"
        assert test_file_obj.dir.lower() == os.getcwd().lower()

    # Given: yEd is installed
    # When: triggering open_with_yed
    # Then: file should be opened
    @pytest.mark.skipif(
        local_testing is not True,
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
    local_testing is not True,
    reason="Test not suitable for CI / Non-windows environments at this time",
)
def test_start_yed():
    process = yed.start_yed()
    assert process is not None, "Expected a process object, but got None"
    yed.kill_yed()  # redundant


@pytest.mark.skipif(
    local_testing is not True,
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


def test_round_trip():
    FILE = "roundtrip.graphml"
    if os.path.exists(FILE):
        os.remove(FILE)

    graph = yed.Graph()

    graph.add_node("a")
    graph.add_node("b")
    graph.add_edge("a", "b")  # .add_label("a_b")  #TODO: NEEDS LABEL TESTING

    graph_file = graph.persist_graph(FILE)
    graph_after = yed.Graph().from_existing_graph(graph_file)
    assert graph.stringify_graph() == graph_after.stringify_graph()

    graph.add_node("c")
    assert graph.stringify_graph() != graph_after.stringify_graph()

    if os.path.exists(FILE):
        os.remove(FILE)


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

    assert graph1.stringify_graph().find("Population") != -1, "Property not found in graphml"


def test_persist_graph():
    file1 = "abcd.graphml"
    file2 = "abcde.graphml"

    # Ensure cleaned up
    if os.path.exists(file1):
        os.remove(file1)
    if os.path.exists(file2):
        os.remove(file2)

    graph1 = yed.Graph()
    graph1.add_node("a")
    graph1.add_node("b")

    # Test that a file is created/stored
    graph1.persist_graph(file1)
    assert os.path.exists(file1) is True

    # Test redundant file error - if same filename used
    with pytest.raises(FileExistsError):
        yed.Graph().persist_graph(file1)

    # Test no error if overwrite is True
    yed.Graph().persist_graph(file1, overwrite=True)

    # Test pretty print not same contents as non-pretty print
    graph1.persist_graph(file2, pretty_print=True)
    file1_handle = open(file1, "r")
    file2_handle = open(file2, "r")
    file1_contents = file1_handle.read()
    file2_contents = file2_handle.read()
    file1_handle.close()
    file2_handle.close()
    assert file1_contents != file2_contents
    assert file2_contents.count("\n") > file1_contents.count("\n")

    # Ensure cleaned up
    if os.path.exists(file1):
        os.remove(file1)
    if os.path.exists(file2):
        os.remove(file2)


def test_from_existing_graph():
    assert isinstance(yed.Graph().from_existing_graph("examples\\yed_created_edges.graphml"), yed.Graph)

    with pytest.raises(FileNotFoundError):
        yed.Graph().from_existing_graph("not_existing_file")

    test_graph = yed.Graph().from_existing_graph("examples\\yed_created_edges.graphml")
    test_graph_stats = test_graph.gather_graph_stats()
    assert test_graph_stats.all_nodes["n0"].url is not None


def test_create_graph_with_url_description():
    FILE1 = "test.graphml"

    graph1 = yed.Graph()
    graph1.add_node(
        "a",
        url="http://www.google.com",
        description="This is a node with a URL and description",
    )
    graph1.add_node("b")
    graph1.add_edge(
        "a",
        "b",
        url="http://www.google.com",
        description="This is an edge with a URL and description",
    )
    group1 = graph1.add_group(
        "group1",
        url="http://www.google.com",
        description="This is a group with a URL and description",
    )
    group1.add_edge("c", "d")
    group1.add_group("group1_1")

    # Ensure cleaned up
    if os.path.exists(FILE1):
        os.remove(FILE1)

    graph1.persist_graph(FILE1)
    # graph1_reimport = yed.Graph().from_existing_graph(FILE1)

    if os.path.exists(FILE1):
        os.remove(FILE1)


def test_create_edge_w_o_nodes():
    graph1 = yed.Graph()
    graph1.add_edge("a", "b")
    assert graph1.nodes["a"] is not None
    assert graph1.nodes["b"] is not None


def test_removes():
    graph1 = yed.Graph()

    # first level nodes
    graph1.add_node("a")
    graph1.add_node("b")
    graph1.add_node("c")

    # first level edges
    graph1.add_edge("a", "b", edge_id="e0")
    graph1.add_edge("a", "c", edge_id="e1")

    # first level group
    group1 = graph1.add_group("group1")

    # second level items
    group1.add_node("d")
    group1.add_group("group1_1")
    group1.add_edge("e", "f")

    stats1 = graph1.gather_graph_stats()
    assert stats1.all_nodes == {
        "a": graph1.nodes["a"],
        "b": graph1.nodes["b"],
        "c": graph1.nodes["c"],
        "d": group1.nodes["d"],
        "e": group1.nodes["e"],
        "f": group1.nodes["f"],
    }
    assert stats1.all_groups == {"group1": group1, "group1_1": group1.groups["group1_1"]}
    assert stats1.all_edges == {"1": graph1.edges["1"], "2": graph1.edges["2"], "3": group1.edges["3"]}

    graph1.remove_node("b")
    graph1.remove_group("group1")
    stats2 = graph1.gather_graph_stats()
    assert stats2.all_nodes == {"a": graph1.nodes["a"], "c": graph1.nodes["c"]}
    assert stats2.all_groups == {}
    assert stats2.all_edges == {"1": graph1.edges["1"], "2": graph1.edges["2"]}

    graph1.run_graph_rules()

    stats3 = graph1.gather_graph_stats()
    assert stats3.all_nodes == {"a": graph1.nodes["a"], "c": graph1.nodes["c"]}
    assert stats3.all_groups == {}
    assert stats3.all_edges == {
        "2": graph1.edges["2"],
    }

    with pytest.raises(RuntimeWarning):
        graph1.remove_node("na")

    with pytest.raises(RuntimeWarning):
        graph1.remove_edge("na")

    with pytest.raises(RuntimeWarning):
        graph1.remove_group("group_na")


@pytest.mark.skipif(
    local_testing is not True,
    reason="Test not suitable for CI / Non-windows environments at this time",
)
def test_yed_kill():
    # Given: yEd is installed
    # When: yEd started and triggering yed kill
    # Then: yEd closed / no longer running

    # kill any yEd
    yed.kill_yed()

    # check for yed running
    assert yed.is_yed_open() is False

    # start yEd
    yed.start_yed()
    assert yed.is_yed_open() is True

    yed.kill_yed()
    assert yed.is_yed_open() is False

    process = yed.start_yed()
    assert process is not None

    process = yed.start_yed()  # duplicate start
    assert process is None


@pytest.mark.skipif(
    local_testing is not True,
    reason="Test not suitable for CI / Non-windows environments at this time",
)
def test_yed_start_extended():
    yed.kill_yed()
    process = yed.start_yed(wait=True)
    assert process is None


@pytest.mark.skipif(
    local_testing is not True,
    reason="Test not suitable for CI / Non-windows environments at this time",
)
def test_open_yed_file():
    graph_file = yed.File("examples\\yed_created_edges.graphml")

    process = yed.open_yed_file(graph_file)
    assert process is not None, "Expected a process object, but got None"
    yed.kill_yed()

    process = yed.open_yed_file(graph_file, force=True)
    assert process is not None, "Expected a process object, but got None"
    yed.kill_yed()

    graph_file = yed.File("not_real_file.graphml")
    process = yed.open_yed_file(graph_file)
    assert process is None, "Should not have successfully spawned a process"


def test_init():
    excel = yed.ExcelManager()
    graph = yed.Graph()
    excel.graph_to_excel_conversion(graph=graph)
    assert excel is not None
    assert os.path.isfile(excel.TEMP_EXCEL_SHEET) is True, "Expected template created"


def test_graph_to_excel_conversion_obj():
    def get_filtered_sheet_values(sheet):
        data = []
        for row in sheet.iter_rows(values_only=True):
            # Filter out empty columns
            filtered_row = [cell for cell in row if cell is not None]
            if filtered_row:  # Only add non-empty rows
                data.append(filtered_row)
        return data

    graph1 = yed.Graph().from_existing_graph("examples\\yed_created_edges.graphml")
    # test conversion to excel
    excel1 = yed.ExcelManager()
    excel1.graph_to_excel_conversion(graph=graph1)

    in_mem_file1 = None
    in_mem_file2 = None
    with open(excel1.TEMP_EXCEL_SHEET, "rb") as f:
        in_mem_file1 = io.BytesIO(f.read())

    with open("examples\\yed_test_to_excel1.xlsx", "rb") as f:
        in_mem_file2 = io.BytesIO(f.read())

    current = pyxl.load_workbook(in_mem_file1).active
    reference = pyxl.load_workbook(in_mem_file2).active
    current_data = get_filtered_sheet_values(current)
    reference_data = get_filtered_sheet_values(reference)
    assert current_data == reference_data

    if os.path.exists(excel1.TEMP_EXCEL_SHEET):
        os.remove(excel1.TEMP_EXCEL_SHEET)


def test_graph_to_excel_conversion_rel():
    def get_filtered_sheet_values(sheet):
        data = []
        for row in sheet.iter_rows(values_only=True):
            # Filter out empty columns
            filtered_row = [cell for cell in row if cell is not None]
            if filtered_row:  # Only add non-empty rows
                data.append(filtered_row)
        return data

    graph1 = yed.Graph().from_existing_graph("examples\\yed_created_edges.graphml")
    # test conversion to excel
    excel1 = yed.ExcelManager()
    excel1.graph_to_excel_conversion(graph=graph1, type="relations")

    in_mem_file1 = None
    in_mem_file2 = None
    with open(excel1.TEMP_EXCEL_SHEET, "rb") as f:
        in_mem_file1 = io.BytesIO(f.read())

    with open("examples\\yed_test_to_excel2.xlsx", "rb") as f:
        in_mem_file2 = io.BytesIO(f.read())

    current = pyxl.load_workbook(in_mem_file1)["Relations"]
    reference = pyxl.load_workbook(in_mem_file2)["Relations"]
    current_data = get_filtered_sheet_values(current)
    reference_data = get_filtered_sheet_values(reference)
    assert current_data == reference_data

    if os.path.exists(excel1.TEMP_EXCEL_SHEET):
        os.remove(excel1.TEMP_EXCEL_SHEET)


def test_bulk_data_management():
    graph1 = yed.Graph()

    # first level nodes
    graph1.add_node("a")
    graph1.add_node("b")
    graph1.add_node("c")

    # first level group
    group1 = graph1.add_group("group1")

    # second level items
    group1.add_node("d")
    group1_1 = group1.add_group("group1_1")
    group1_1.add_node("e")

    # shallow copy the stringified graph
    before_string = graph1.stringify_graph()[:]

    # doing nothing in excel should lead to the same graph being built back up (when talking about simple obj model)
    excel_obj = graph1.manage_graph_data_in_excel()

    after_string = graph1.stringify_graph()

    assert before_string is not None
    assert after_string is not None
    assert before_string == after_string

    if os.path.exists(excel_obj.TEMP_EXCEL_SHEET):
        os.remove(excel_obj.TEMP_EXCEL_SHEET)


@pytest.mark.skip(reason="Requires refactor of name vs id handling.")
def test_excel_to_graph():  # FIXME:
    graph1 = yed.Graph().from_existing_graph("examples\\yed_created_edges.graphml")
    # test conversion to excel
    excel1 = yed.ExcelManager()
    data = "examples\\yed_test_to_excel2.xlsx"
    excel1.excel_to_graph_conversion(type="obj_and_hierarchy", excel_data=data)
    excel1.excel_to_graph_conversion(type="relations", excel_data=data)
    assert graph1.stringify_graph() == excel1.graph.stringify_graph()
