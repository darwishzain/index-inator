import json,os,re

def fullpath(relative_path):
    return(os.path.join(os.path.dirname(__file__), relative_path))

def openjson(filename):
    file = fullpath(filename)
    with open(file) as f:
        jsondata = json.load(f)
    return(jsondata)

config = openjson('data.json')

class indexinator:
    def __init__(self):
        self.filelist = []
        self.directory = []

    def list(self):
        for directory in config['directory']:
            if os.path.exists(directory):
                print(directory)
                for item in os.listdir(directory):
                    if item == 'watch' or item == 'copy':
                        continue
                    if os.path.isdir(os.path.join(directory,item)) :
                        self.info(item,"Folder")
                    else :
                        self.info(item,"Media")
    
    def info(self,item,type):
        info = []
        symbols = [ "#","$","(",")","[","]" ]
        #language = re.search(r"(){2}",item)
        season = re.search(r"(\d+)$", item)
        year = re.search(r"(\d{4})", item)
        count = re.search(r"(\d+)#", item)
        #language = re.search(r"[({2})]", item)
        #if language: info.append("Bahasa: " + language.group(1))
        
        item = re.sub(r"(\d+)$","", item)#S
        item = re.sub(r"(\d+)#","", item)#C
        item = re.sub(r"(\d{4})","", item)#Y
        #item = re.sub(r"[()]","", item)
        item = re.sub(r"\(","", item)
        item = re.sub(r"\)","", item)
        item = re.sub(r"\$","", item)
        item = re.sub(r"\#","", item)
        item = item.strip()

        info.append(type + ": "+ item)
        if season: info.append("Musim: " + season.group(1))
        if count: info.append("Kandungan:" + count.group(1))
        if year: info.append("Tahun: " + year.group(1))

        print("\n".join(info))

if __name__ == "__main__":
    indexer = indexinator()
    indexer.list()

