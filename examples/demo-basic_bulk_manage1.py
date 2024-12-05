# import
import os

import yedextended as yed

# Read graph file into python graph objects
graph1 = yed.Graph().from_existing_graph("examples/yed_created_edges.graphml")

# Manage data in spreadsheet (add elements, delete elements, rename elements, change change ownership)
graph1.manage_graph_data_in_spreadsheet()  # default is management of objects and their hierarchy

# Reopen modified in yEd
modified_graph = graph1.persist_graph("bulk_changed", overwrite=True)
modified_graph.open_with_yed(force=True)

# Clean-up following viewing in yEd
user_input = input("Type 'Y' to delete graph or ENTER to simply end program.")
if user_input in ("Y", "y"):
    os.remove(modified_graph.fullpath)
