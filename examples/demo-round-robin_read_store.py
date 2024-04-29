# import
import yedextended as yed

# "Round Robin" import-export ==============================

# Reading of graphml file into python objects
graph1 = yed.Graph().from_existing_graph("examples/yed_created_edges.graphml")

# Saving and opening the "read graph"
graph1.persist_graph("abc.graphml", overwrite=True).open_with_yed(force=True)
