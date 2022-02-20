import csv, json
class Reader:

    def __init__(self, inputPath):
        self.inputPath = inputPath

    def csv(self):
        with open(self.inputPath, newline='') as f:
            csvReader = csv.reader(f)
            w = []
            for row in csvReader:
                w.extend(row)
        return w

    def csv_as_list_of_dicts(self):
        data = {}
        
        with open(self.inputPath) as csvFile:
            csvReader = csv.DictReader(csvFile)
            id = 0
            for row in csvReader:
                data[id] = dict(row)
                id += 1
        return data
