# import
import os

import yedextended as yed

# Instantiate new and empty graph
graph1 = yed.Graph()

# Manage data in spreadsheet (add elements)
graph1.manage_graph_data_in_spreadsheet()

# Manage data in spreadsheet (add relationships)
graph1.manage_graph_data_in_spreadsheet(type="relations")

# Reopen modified in yEd
modified_graph = graph1.persist_graph("bulk_changed", overwrite=True)
modified_graph.open_with_yed(force=True)

# makes easier to see feedback in cmd
user_input = input("Type 'Y' to delete graph or ENTER to simply end program.")
if user_input in ("Y", "y"):
    os.remove(modified_graph.fullpath)
