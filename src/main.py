import json,os

def fullpath(relative_path):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, relative_path)

def openjson(filename):
    file = fullpath(filename)
    with open(file) as f:
        jsondata = json.load(f)
    return(jsondata)

directory = openjson('data.json')

class indexinator:
    def __init__(self, directory):
        self.directory = directory

    def listfiles(self):
        try:
            return os.listdir(self.directory)
        except FileNotFoundError:
            return f"Directory {self.directory} not found."
        except PermissionError:
            return f"Permission denied for directory {self.directory}."

if __name__ == "__main__":
    indexer = indexinator(directory)
    files = indexer.listfiles()
    print(files)

