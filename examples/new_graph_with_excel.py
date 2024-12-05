import os

import yedextended as yed

print("Ensure graphs saved if open!")
path = input("Enter path for xgml file (leave empty for new, \" don't matter):")
path = path or os.path.join(os.getcwd(), "newgraph.graphml")
path = path.replace('"', "")
print(f"Path Used: {path}")
graph = yed.Graph()

# input("Press enter to continue.")

# Modify with spreadsheet
graph.manage_graph_data_in_spreadsheet()

# Check changes
graph.gather_graph_stats().print_stats()

# Overwrite
# input("Ok to overwrite previous graph? Commit if necessary.")
file1 = graph.persist_graph(path, overwrite=True)

# open in yEd
file1.open_with_yed()

# makes easier to see feedback in cmd
user_input = input("Type 'Y' to delete graph or enter simply to end program.")
if user_input in ("Y", "y"):
    os.remove(path)
