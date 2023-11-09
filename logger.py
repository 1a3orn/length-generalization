import pandas as pd

# Simple logger that takes a dict 
# of values for various steps and
# writes them to a file.
class Logger:

    def __init__(self):
        self.data = []

    def add(self, dict):
        self.data.append(dict)

    def write(self, path):
        df = pd.DataFrame(self.data)
        df.to_csv(path, index=False)

    def average(self, key, last_num):
        numer = sum([d[key] for d in self.data[-last_num:]])
        denom = min(last_num, len(self.data))
        return numer / denom