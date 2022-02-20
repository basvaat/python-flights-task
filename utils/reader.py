import csv, json
class Reader:

    def __init__(self, inputPath):
        self.inputPath = inputPath


    def csv_as_list_of_dicts(self):
        data = {}
        try:
            with open(self.inputPath) as csvFile:
                csvReader = csv.DictReader(csvFile)
                id = 0
                for row in csvReader:
                    data[id] = dict(row)
                    id += 1
            return data
        except:
            raise FileNotFoundError('File not found. File name or path is incorrect.')
        
