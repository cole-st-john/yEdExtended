# import
import yedextended as yed

# Instantiate new and empty graph
graph1 = yed.Graph()

# Manage data in excel (add elements)
graph1.manage_graph_data_in_excel()

# Manage data in excel (add relationships)
graph1.manage_graph_data_in_excel(type="relations")

# Reopen modified in yEd
graph1.persist_graph("bulk_changed", overwrite=True).open_with_yed(force=True)
