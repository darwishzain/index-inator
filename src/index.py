import json,os,sys,subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow,QListWidget,QListWidgetItem,QHeaderView, QTreeWidgetItem, QTreeWidget, QHBoxLayout,QVBoxLayout, QPushButton,QWidget, QLabel, QLineEdit

def openjson(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        jsondata = json.load(f)
    return(jsondata)

def opendefault(path):
    if sys.platform.startswith("win"):        # Windows
        os.startfile(path)
    elif sys.platform == "darwin":            # macOS
        subprocess.run(["open", path])
    else:                                     # Linux / Unix
        subprocess.run(["xdg-open", path])

class Index(QMainWindow):
    def upload(self,category,path):
        datafile = os.path.join(os.path.dirname(__file__), 'output/data.json')
        if os.path.exists(datafile):
            with open(datafile, 'r') as f:
                try:
                    uploading = json.load(f)
                except json.JSONDecodeError:
                    uploading = {}
        else:
            uploading = {}
        uploading[category][path] = os.listdir(path)
        print(path)
        with open(datafile, 'w') as f:
            json.dump(uploading, f, indent=4)

    def view(self,path,category):
        while self.content.count():
            item = self.content.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                child_layout = item.layout()
                if child_layout:
                    while child_layout.count():
                        sub_item = child_layout.takeAt(0)
                        sub_widget = sub_item.widget()
                        if sub_widget:
                            sub_widget.setParent(None)
        contentui = QHBoxLayout()
        contentui.addWidget(QLabel(">"))
        pathui = QLineEdit()
        pathui.setText(path)
        pathui.setStyleSheet("background-color:#0C0C0C")
        pathui.setReadOnly(True)
        contentui.addWidget(pathui)
        addbtn = QPushButton("+")
        addbtn.clicked.connect(lambda: self.upload(category, path))
        contentui.addWidget(addbtn)
        self.content.addLayout(contentui)

        listwidget = QListWidget()
        for item in sorted(os.listdir(path)):
            listitem = QListWidgetItem(item)
            listwidget.addItem(listitem)
            if os.path.isdir(os.path.join(path,item)):
                listitem.setForeground(Qt.GlobalColor.blue)
            else:
                listitem.setForeground(Qt.GlobalColor.darkGreen)
        listwidget.itemDoubleClicked.connect(lambda item: opendefault(os.path.join(path, item.text())))
        listwidget.setStyleSheet("background-color:#DDDDDD")
        self.content.addWidget(listwidget)
        self.setWindowTitle("Index Inator [" + path + "] ")


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Index Inator")
        self.showMaximized()
        self.config = openjson('config.json')

        # layout and container
        self.mainlayout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.mainlayout)
        self.setCentralWidget(container)

        self.reading = []
        self.watching = []
        self.listening = []
        self.category = ['read','watch','listen']
        self.library = QHBoxLayout()
        self.mainlayout.addLayout(self.library)

        for category in self.category:
            for d in self.config[category]:
                if os.path.exists(d):
                    button = QPushButton(d)
                    button.clicked.connect(lambda _, path=d, category=category: self.view(path,category))
                    self.library.addWidget(button)
        self.content = QVBoxLayout()
        self.content.addWidget(QLabel("Select a directory to view its content"))
        self.mainlayout.addLayout(self.content)



if __name__ == "__main__":
    app = QApplication([])
    window = Index()
    window.show()
    app.exec()
