from PyQt5.QtWidgets            import QApplication, QMainWindow #QMessageBox
from PyQt5.QtWebEngineWidgets   import QWebEngineView
from PyQt5.QtWebChannel         import QWebChannel
from PyQt5.uic                  import loadUi
from PyQt5.QtGui                import QScreen
from PyQt5.QtCore               import QObject, pyqtSlot, QUrl, pyqtSignal, QByteArray, QBuffer, QIODevice, Qt
from sys                        import argv
from os.path                    import abspath, join, dirname
from time                       import sleep
from PyQt5.QtCore               import QThread
from base64                     import b64encode
from io                         import BytesIO
from jinja2                     import Template 

class StreamProcess(QThread):
    mysignal = pyqtSignal(str)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        
    def run(self):
        while True:
            screen = QScreen.grabWindow(QApplication.primaryScreen(), QApplication.desktop().winId())
            ba = QByteArray()
            buff = QBuffer(ba)
            buff.open(QIODevice.WriteOnly) 

            screen.save(buff, "PNG")
            pixmap_bytes = ba.data()
            data = f"data:img/png;base64,{b64encode(pixmap_bytes).decode('utf-8')}"
            self.mysignal.emit(data)
            sleep(1)

class CallHandler(QObject):
    customSignal = pyqtSignal(str)

    def sendCustomSignal(self):
        self.progress = StreamProcess(self)
        self.progress.mysignal.connect(self.transmit)
        self.progress.start()

    def terminate_thread(self):
        self.progress.terminate()

    @pyqtSlot(str)
    def transmit(self, val):
        self.customSignal.emit(val)

    @pyqtSlot()
    def terminate_stream(self):
        self.terminate_thread()

    @pyqtSlot()
    def init(self):
        self.sendCustomSignal()

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        loadUi('UI/test1.ui', self)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.channel = QWebChannel()
        self.hander  = CallHandler()
        # function must be triggered from js
        self.channel.registerObject('handler', self.hander)
        self.View.page().setWebChannel(self.channel)

        self.View.load(QUrl.fromLocalFile(abspath(join(dirname(__file__), "./Content/index.htm"))))
        

def main():
    app=QApplication(argv)
    window = Ui()
    window.showMaximized()
    # window.show()
    app.exec_()

main()

# if __name__ == '__main__':
#     try:
#         main()
#         print("closed")
#     except Exception as why:
#         print(why)

