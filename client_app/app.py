from re import sub
from tkinter.tix import ComboBox
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from client_app.mlModel import *

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            cv_img = get_frame_from_tensor(cv_img)
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt app")
        self.disply_width = 640
        self.display_height = 480
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        self.image_label.move(150,0)
        self.textLabel = QLabel('Webcam')
        self.startButtom = QPushButton('Start')
        names = ['Red','Green', 'Blue', 'Purple', 'Yellow']
        positions = ['1','2','3','4','5']

        hbox = QHBoxLayout()
        sublayout = QVBoxLayout()
        sublayout.addStretch(0)
        
        layout = QVBoxLayout()

        hbox.addLayout(sublayout)
        hbox.addLayout(layout)

        for i in range(len(names)):
            text = QLabel(names[i])
            combo = QComboBox()
            combo.addItems(positions)
            grid = QGridLayout()
            grid.addWidget(text,0,0)
            grid.addWidget(combo,0,1)
            sublayout.addLayout(grid)

        sublayout.addStretch(1)
        sublayout.addWidget(self.startButtom,stretch=1)

        layout.addWidget(self.image_label)
        layout.addWidget(self.textLabel)
        self.setLayout(hbox)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
     
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())