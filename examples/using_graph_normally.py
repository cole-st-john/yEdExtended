import yedextended as yed

print("Ensure graph saved if already open!")

path = input("Enter path for xgml file (leave empty for default, \" don't matter):")
path = path or r"C:\Users\Cole\OneDrive\LOGIC_MODELS\IT_CONCEPTS.graphml"
path = path.replace('"', "")
print(f"Path: {path}")

# Loading as python objects
graph = yed.Graph().from_existing_graph(path)
stats = graph.gather_graph_stats()
stats.print_stats()
input("Press enter to continue.")

# Modify with excel
graph.manage_graph_data_in_excel()

# Check changes
graph.gather_graph_stats().print_stats()

# Overwrite
input("Ok to overwrite previous graph? Commit if necessary.")
file1 = graph.persist_graph(path, overwrite=True, vcs_version=True)

# open in yEd

file1.open_with_yed()

# makes easier to see feedback in cmd
input("Press enter to continue.")
