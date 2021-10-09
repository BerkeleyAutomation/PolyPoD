import pickle
import os
import plotly_test as pt
import time
import re

directory = "datasets/dataset5"
list = [x for x in range(1000)]
print(list)
for entry in os.scandir(directory):
    if (entry.path.endswith("data") and entry.is_file()):
        m = re.search("_[0-9]+_", entry.path)
        num = m.group(0)[1:-1]
        list.remove(int(num))
print(list)
