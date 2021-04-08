from PyQt5 import QtCore

class ApplicationThread(QtCore.QThread):
    def __init__(self, application, port=9090):
        super(ApplicationThread, self).__init__()
        self.application = application
        self.port = port

    def __del__(self):
        self.wait()

    def run(self):
        print("flask start to run")
        self.application.run(debug=False, host='0.0.0.0', port=self.port, threaded=True)

