# imports
import csv

import yedextended as yed

# Instantiate graph instance
graph1 = yed.Graph()

# Adding graph objects based on csv input
with open("test.csv", encoding="utf-8-sig") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        graph1.add_node(row)
