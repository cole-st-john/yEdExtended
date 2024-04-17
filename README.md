<!-- [![PyPI](https://img.shields.io/pypi/v/pyyed)](https://pypi.org/project/pyyed)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyyed)](https://pypi.org/project/pyyed) -->

# Extended Python Support for yEd 

A basic Python library to work with network / graph visualizations in [yEd](http://www.yworks.com/en/products_yed_about.html).

The [yEd Graph Editor](https://www.yworks.com/products/yed) supports the [GraphML](http://graphml.graphdrawing.org/) ([GraphML Primer](http://graphml.graphdrawing.org/primer/graphml-primer.html)) file format (among other file types). 
This is an open standard based on XML, and is supported by Python libraries such as [NetworkX](https://networkx.github.io/).
However, the details of formatting (rather than network topology) are handled by yEd specific extensions to the standard, which are not supported by other libraries.

The purpose of this library is to extend yEd functionality through programmatic interface to graphs, including...
- [x] creating graphs
- [x] formatting graphs
- [ ] reading graphs  
- [ ] enforcing rules on graphs
- [ ] addition of standard sorting methods
- [ ] bulk data management methods

## Usage
The basic interface is similar to that of NetworkX:

```python
import yedextended as yed

g = yed.Graph()

g.add_node('foo', font_family="Zapfino")
g.add_node('foo2', shape="roundrectangle", font_style="bolditalic", underlined_text="true")

g.add_edge('foo1', 'foo2')
g.add_node('abc', font_size="72", height="100", shape_fill="#FFFFFF")

g.add_node('bar', label="Multi\nline\ntext")
g.add_node('foobar', label="""Multi
    Line
    Text!""")

g.add_edge('foo', 'foo1', label="EDGE!", width="3.0", color="#0000FF", 
               arrowhead="white_diamond", arrowfoot="standard", line_type="dotted")

print(g.get_graph())

# To write to file:
with open('test_graph.graphml', 'w') as fp:
    fp.write(g.get_graph())

# Or:
g.write_graph('example.graphml')

# Or, to pretty-print with whitespace:
g.write_graph('pretty_example.graphml', pretty_print=True)

```

Saving this to a file with a ``.graphml`` extension, opening in yEd, applying  ``Tools -> Fit Node to Label`` and ``Layout -> One-click layout`` produces something like the following:

![](example.png)

### UML
The file [``examples/demo-uml.py``](./examples/demo-uml.py), includes an example UML diagram:

![](example-UML.png)

## Options

Provides comprehensive support for ``node_shapes``, ``line_types``, ``font_styles``, ``arrow_types``, custom parameters and more.

## Development

Interested in contributing or co-managing further development?  Just reach out!

Requirements:

    $ pip install pytest

Run the tests:
    $ PYTHONPATH=. pytest tests
