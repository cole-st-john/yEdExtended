import yedextended as yed

# Reading of graphml file into python objects
graph1 = yed.Graph().from_existing_graph("examples/yed_created_edges.graphml")
graph1.persist_graph("abc.graphml", overwrite=True).open_with_yed(force=True)
