# import
import yedextended as yed

# Read graph file into python graph objects
graph1 = yed.Graph().from_existing_graph("examples/yed_created_edges.graphml")

# Manage data in excel (add elements, delete elements, rename elements, change change ownership)
graph1.manage_graph_data_in_excel()  # default is management of objects and their hierarchy

# Reopen modified in yEd
graph1.persist_graph("bulk_changed", overwrite=True).open_with_yed(force=True)
