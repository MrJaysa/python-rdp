from PyQt5.QtWidgets          import QApplication, QMainWindow #QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel       import QWebChannel
from PyQt5.uic                import loadUi
from PyQt5.QtCore    import QObject, pyqtSlot, pyqtSignal, QUrl, Qt
from sys             import argv
from os.path         import abspath, join, dirname
from base64          import b64encode
from jinja2          import Template
import autopy


class CallHandler(QObject):
    uiSignal = pyqtSignal(str)
    getstream  = pyqtSignal()

    devs = []

    @pyqtSlot(list)
    def save_devices(self, data):
        self.devs = data
    
    @pyqtSlot()
    def load_devs(self):
        path     = abspath(join(dirname(__file__), "./Content/devs.htm"))
        with open(path) as html:
            template = Template(html.read()).render(devs=self.devs)
        
        self.uiSignal.emit(template)

    @pyqtSlot()
    def start_stream(self):
        self.getstream.emit()    

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        loadUi('UI/test1.ui', self)
        # self.setWindowOpacity(0.1)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.channel = QWebChannel()
        self.handler  = CallHandler()
        self.handler.getstream.connect(self.enlarge)
        # autopy.mouse.move(1, 1)
        # autopy.mouse.smooth_move(100, 600)
        # function must be triggered from js
        # self.hander.sendCustomSignal()
        self.channel.registerObject('handler', self.handler)
        self.View.page().setWebChannel(self.channel)

        self.View.load(QUrl.fromLocalFile(abspath(join(dirname(__file__), "./Content/index.htm"))))

    def enlarge(self):
        self.setWindowFlags( self.windowFlags() & Qt.FramelessWindowHint )
        self.showMaximized()
        

def main():
    app=QApplication(argv)
    window = Ui()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    try:
        main()
        print("closed")
    except Exception as why:
        print(why)

