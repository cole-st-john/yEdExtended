


# Extended Python Support for yEd 

[![Static Badge](https://img.shields.io/badge/PyPI%20-%20yEdExtended%20-%20GREEN?logoColor=0%2C0%2C255&color=0%2C1%2C1&link=https%3A%2F%2Fpypi.org%2Fproject%2Fyedextended%2F)](https://pypi.org/project/yedextended/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/yedextended?color=2334D058)
[![CI](https://github.com/cole-st-john/yEdExtended/actions/workflows/ci.yml/badge.svg)](https://github.com/cole-st-john/yEdExtended/actions/workflows/ci.yml)
![Test Coverage](https://raw.githubusercontent.com/cole-st-john/yedextended/master/test_coverage.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/cole-st-john/yedextended)
![PyPI - Downloads](https://img.shields.io/pypi/dm/yedextended)

This Python library extends the functionality of the readily available and free interactive graph editing program [yEd](http://www.yworks.com/en/products_yed_about.html), through providing a programmatic interface to graphs (of the [GraphML](http://graphml.graphdrawingraph1.org/) file format), including the following use case or functions:

- [x] creating graphs
- [x] formatting graphs
- [x] reading graphs
- [x] bulk data addition or management (MS excel-based)
- [x] management of the yEd application (starting, killing, etc.)
- [ ] enforcing rules on graphs
- [ ] additional layout methods
- [ ] graph comparison tools

![yEd Graph](https://raw.githubusercontent.com/cole-st-john/yedextended/master/images/graph.gif)


# Basic Usage

Below are some basic usages of yEdExtended in interfacing with yEd and GraphML files:


## Installing yEdExtended
From PyPI, using pip:
```console
$ pip install yedextended  
```
From GITHUB, using pip:
```console
$ python -m pip install git+https://github.com/cole-st-john/yEdExtended
```

From GITHUB, using git:
```console
$ git clone https://github.com/cole-st-john/yedextended
```



## Importing yEdExtended for usage

```python
import yedextended as yed
```


## Programmatically creating GraphML files

With yEdExtended you can easily create graphs, either through hardcoding, or more practically, through porting data from any data source (databases, csv, xml, etc) into a graph and graph objects (nodes, groups, edges, properties):

Hardcoding Example:
```python
# Instantiate graph instance
graph1 = yed.Graph()

# Adding arbitrary graph detail - nodes
a = graph1.add_node("a")
b = graph1.add_node("b")

# Adding edge (using node objects)
graph1.add_edge(a, b)

# Add arbitrary graph detail - group and group objects
group1 = graph1.add_group("group 1", shape="rectangle")

# Adding edge using node names, under owning group
group1.add_edge("c", "d")
```

Programmatic Example:
```python
# Adding graph objects based on csv input
with open("examples\\test.csv", encoding="utf-8-sig") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        graph1.add_node(row[0])
```

## Reading existing GraphML files

yEdExtended can read GraphML files into a Python class structure, allowing for simple programmatic analysis and modification:

```python
# Read graph file into python graph objects
graph1 = yed.Graph().from_existing_graph("examples/yed_created_edges.graphml")

```


## Using formatting

yEdExtended provides for the majority of formatting one expects in yEd graphs.

```python
# Add graph nodes and edges with some examples of non-default formatting
graph1.add_node("foo", font_family="Zapfino")

graph1.add_node(
    "foo2",
    shape="roundrectangle",
    font_style="bolditalic",
    underlined_text="true",
)

graph1.add_edge("foo1", "foo2")

graph1.add_node("abc", font_size="72", height="100")

graph1.add_node("Multi\nline\ntext")

graph1.add_node("foobar").add_label("""Multi
Line
Text!""")

graph1.add_edge(
    "foo",
    "foo1",
    name="EDGE!",
    width="3.0",
    color="#0000FF",
    arrowhead="white_diamond",
    arrowfoot="standard",
    line_type="dotted",
)
```


## Manipulating data in MS Excel 

Sometimes, it is practical to mass edit or enter data in an interactive way.  yEdExtended includes functionality to enter basic to complex data and relationships using an interface to MS Excel interface. Note: to use this functionality, MS Excel must be installed and on path:

```python
# Instantiate a graph
graph1 = Graph()

# Manage data in excel (add/remove/modify objects)
graph1.manage_graph_data_in_excel() # default is object and hierachy management

# Manage data in excel (add/remove/modify relations)
graph1.manage_graph_data_in_excel(type="relations")
```

### Excel - Adding Objects / Groups:

![Excel Object Entry](https://raw.githubusercontent.com/cole-st-john/yedextended/master/images/excel_obj_entry.gif)

### Result:

![Graph result of excel data entry](https://raw.githubusercontent.com/cole-st-john/yedextended/master/images/graph_from_excel_obj.gif)

### Excel - Adding Relationships:

![Excel Relation Entry](https://raw.githubusercontent.com/cole-st-john/yedextended/master/images/excel_rel_entry.gif)

### Result:

![Graph result of excel relation entry](https://raw.githubusercontent.com/cole-st-john/yedextended/master/images/graph_from_excel_rel.gif)


## Possible outputs of Graph

Eventually, one normally wants to visualize or transmit the graph in some format.  Here are a few options:

```python
# Demonstrate stringified GraphML version of structure
print(graph1.stringify_graph())
```

```python
# Several methods of writing graph to file ==============================

with open("test_graph.graphml", "w") as fp:  # using standard python functionality
    fp.write(graph1.stringify_graph())

graph_file = graph1.persist_graph("test.graphml")   # using tool specific method

graph_file = graph1.persist_graph("pretty_example.graphml", pretty_print=True)  #  tool specific with formatting

```


## Opening files in yEd Application *(assumes yEd installed and on PATH)*

To ease task switching between Python and yEd, functionality has been added to open graphs in yEd directly from Python.  Note: ensure you have installed yEd application from [here](https://www.yworks.com/products/yed/download#download) and that the app is on PATH (Win: "where yed.exe" in CMD should output a path).

```python
# Instantiating Graph
graph = Graph()

# Saving graph to file
graph_file = graph.persist_graph()

# Opening graph in yEd from file handle
graph_file.open_with_yed(force=True)

# Opening graph directly from file
yed.open_yed_file("examples/test.graphml")
```


## Visualizing in yEd Application (Layout)

Following programmatic creation or modification of a graph, consider using the following keystrokes in yEd to improve layout / positioning (yEdExtended does not currently include functionality for layout, which is readily available in yEd):

- ``Tools -> Fit Node to Label``  (_Win: Alt + T + N_)
- ``Layout -> Hierarchical``  (_Win: Alt + Shift + H_)


# Options

Provides comprehensive support for great variety of ``node_shapes``, ``line_types``, ``font_styles``, ``arrow_types``, custom parameters, UML, complex and deeply nested relationship structures and more.


# yEdExtended V1.0.12 vs V2.0.0

**yEdExtended v2.0.0** is a major rewrite focusing on a instantiation method - using names vs ids.  These changes can be summarized as following:

- **Backend ID Management:** The responsibility for managing IDs has been shifted primarily to the backend. This significant update enables the following enhancements:

- **Support for Duplicate Names:** Allows the use of duplicate names across different levels and areas within a graph.

- **Unique and Trackable IDs:** Despite allowing duplicate names, the system now provides and maintains unique and trackable IDs for all graph objects.

This change simplifies object handling, ensuring better consistency and flexibility, especially in larger graph management.


# Development


Interested in contributing or co-managing further development?  Just reach out!

Dev. Requirements:

Install yEd from [here](https://www.yworks.com/products/yed/download#download).

Ensure you have [MS Excel](https://www.microsoft.com/en/microsoft-365/excel?market=af) installed.

```console
$ pip install pytest
```

```console
$ setx CI "True"
```

To run the tests:
```console
$ PYTHONPATH=. pytest tests
```

References: 

+ [pyyed](https://github.com/jamesscottbrown/pyyed)
+ [GraphML Primer](http://graphml.graphdrawingraph1.org/primer/graphml-primer.html)
+ [NetworkX](https://github.com/networkx/networkx)
