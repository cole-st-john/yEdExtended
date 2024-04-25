import yedextended as yed

# Pull graph into memory from file
graph1 = yed.Graph().from_existing_graph("examples/yed_created_edges.graphml")

# Manage data in excel (add elements, delete elements, rename elements, change change ownership)
graph1.manage_graph_data_in_excel()

# Reopen modified in yEd
graph1.persist_graph("bulk_changed", overwrite=True).open_with_yed(force=True)
