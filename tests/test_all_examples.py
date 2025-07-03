import glob
import os
import sys
import importlib.util

example_files = glob.glob("examples/*.py")
path = os.getcwd()
print("Current working directory: ", path)
os.mkdir("temp") if not os.path.exists("temp") else None
os.chdir("temp")

output_files = glob.glob("*")
for output_file in output_files:
    os.remove(output_file) if output_file else None

for example_file in example_files:
    print("Running example file: ", example_file)

    # Load the module
    spec = importlib.util.spec_from_file_location("example_module", os.path.join(path, example_file))

    example_module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(example_module)

    input("Press Enter to continue to the next example...")  #

    output_files = glob.glob("*")
    for output_file in output_files:
        os.remove(output_file) if output_file else None
