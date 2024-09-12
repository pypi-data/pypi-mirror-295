
from firebase_admin import credentials, firestore
import firebase_admin

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QLabel, QGridLayout, QScrollArea, QSizePolicy, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent, QObject

import sys
import torch
import os
import requests
import json
import glob
import cv2
import itertools

from subprocess import Popen
from ultralytics import YOLO

from weapondetector.login_auth import login_auth
from weapondetector.text_input import Ui_Form

global main_path, api_url, dir_path, model_name

main_path = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(main_path, "assets", "logo.png")
icon_path = os.path.join(main_path, "assets", "main-icon.ico")
api_url = 'http://localhost:8000/uploadvideo'
# print(main_path)

# firebase
cred = credentials.Certificate(os.path.join(main_path, "assets", "secret-key.json"))
app = firebase_admin.initialize_app(cred)
store = firestore.client()

dir_path = main_path + '/results/'
model_name = main_path + '/model/best.pt'
os.makedirs(dir_path, exist_ok=True)

num = itertools.count(1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def convert_and_clamp(val, min_val=0.5, max_val=0.9, default_val=0.75):
    """Converts the input value to a float and clamps it to the specified range.

    Args:
        val: The input value to be converted and clamped.
        min_val: The minimum allowed value (inclusive). Defaults to 0.5.
        max_val: The maximum allowed value (inclusive). Defaults to 0.9.
        default_val: The default value to return if the conversion fails or the value is out of range. Defaults to 0.75.

    Returns:
        The converted and clamped value, or the default value if conversion fails.
    """

    try:
        converted_val = float(val)
        if min_val <= converted_val <= max_val:
            return converted_val
        else:
            return default_val
    except ValueError:
        return default_val


class CaptureIpCameraFramesWorker(QThread):
    ImageUpdated = pyqtSignal(QImage)

    def __init__(self, url, conf) -> None:
        super(CaptureIpCameraFramesWorker, self).__init__()

        self.camera_url = url.split(' ', 1)[0]
        try:
            self.camera_name = url.split(' ', 1)[1].strip()
        except:
            self.camera_name = f'Camera_{next(num)}'

        self.__thread_active = True

        self.model = YOLO(model_name)
        self.max_length = 0
        self.fps = 0
        self.detected = False
        self.counter = 0
        self.count_frames = 0
        self.out = None
        self.cap = None
        self.acc = 0.0
        self.conf = conf

        self.fourcc = None
        self.video_output_path = None
        self.img_output_path = None

    def handle_detection(self, height, width, result_frame, results):

        if self.out is None:
            files = [file for file in glob.glob(dir_path+'*.jpg')]
            output_path = f"{dir_path}{self.camera_name}_{str(len(files)+1)}"
            self.video_output_path = output_path + '.mp4'
            self.img_output_path = output_path + '.jpg'

            self.fourcc = cv2.VideoWriter_fourcc(*'avc1')
            self.out = cv2.VideoWriter(
                self.video_output_path, self.fourcc, self.fps, (width, height))

        if self.counter == 0:
            cv2.imwrite(self.img_output_path, result_frame)

        acc = results[0].boxes.data[0][4].tolist()
        self.acc = acc if acc > self.acc else self.acc
        # print('accuracy: ', self.acc)

        self.out.write(result_frame)
        self.detected = True
        self.counter += 1

    def release_video_and_send_data(self):
        self.out.release()
        self.out = None
        self.detected = False
        self.counter = 0
        self.acc = 0.0
        self.fourcc = None

        json_data = {"video_file_path": str(self.video_output_path),
                     "img_file_path": str(self.img_output_path),
                     "camera_name": str(self.camera_name),
                     "acc": float(self.acc)}

        jsonResponse = requests.post(api_url, json=json.dumps(json_data))
        # print(jsonResponse)

    def reconnect_camera(self):
        if self.cap.isOpened():
            self.cap.release()
        self.cap = cv2.VideoCapture(self.camera_url)

    def run(self) -> None:

        self.cap = cv2.VideoCapture(self.camera_url)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.max_length = int(self.fps) * 5

        if self.cap.isOpened():
            while self.__thread_active:
                retreive, frame = self.cap.read()

                if not retreive:
                    self.reconnect_camera()
                    continue

                else:
                    self.count_frames += 1

                    height, width, channels = frame.shape

                    if self.count_frames % 8 == 0:

                        results = self.model.predict(frame,
                                                     conf=self.conf,
                                                     verbose=False,
                                                     half=False,
                                                     stream=False)

                        frame = results[0].plot()
                        if len(results[0].boxes.data) > 0:

                            self.handle_detection(height, width, frame, results)

                            if self.counter >= self.max_length:
                                self.release_video_and_send_data()

                        elif (len(results[0].boxes.data) == 0) and (self.detected):
                            self.release_video_and_send_data()

                        self.count_frames = 0

                    qt_rgb_image = QImage(frame, width, height, QImage.Format_RGB888).rgbSwapped()
                    self.ImageUpdated.emit(qt_rgb_image)

        cv2.destroyAllWindows()
        self.cap.release()
        self.stop()

    def stop(self) -> None:
        self.__thread_active = False

    def unpause(self) -> None:
        self.__thread_pause = False


class MainWindow(QMainWindow):

    def __init__(self, inputs) -> None:
        super(MainWindow, self).__init__()

        # rtsp://<Username>:<Password>@<IP Address>:<Port>/cam/realmonitor?channel=1&subtype=0
        try:
            self.url_1 = inputs[0]
        except:
            self.url_1 = ""

        try:
            self.url_2 = inputs[1]
        except:
            self.url_2 = ""

        try:
            self.url_3 = inputs[2]
        except:
            self.url_3 = ""

        try:
            self.url_4 = inputs[3]
        except:
            self.url_4 = ""

        try:
            self.url_5 = inputs[4]
        except:
            self.url_5 = ""

        try:
            self.url_6 = inputs[5]
        except:
            self.url_6 = ""

        try:
            self.url_7 = inputs[6]
        except:
            self.url_7 = ""

        try:
            self.url_8 = inputs[7]
        except:
            self.url_8 = ""

        try:
            self.url_9 = inputs[8]
        except:
            self.url_9 = ""

        try:
            self.url_10 = inputs[9]
        except:
            self.url_10 = ""

        try:
            self.url_11 = inputs[10]
        except:
            self.url_11 = ""

        try:
            self.url_12 = inputs[11]
        except:
            self.url_12 = ""

        conf = convert_and_clamp(inputs[-1])
        # print("Conf: ", conf)
        # Dictionary to keep the state of a camera. The camera state will be: Normal or Maximized.
        self.list_of_cameras_state = {}

        self.camera_1 = QLabel()
        self.camera_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_1.setScaledContents(True)
        self.camera_1.installEventFilter(self)
        self.camera_1.setObjectName("Camera_1")
        self.list_of_cameras_state["Camera_1"] = "Normal"

        self.QScrollArea_1 = QScrollArea()
        self.QScrollArea_1.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_1.setWidgetResizable(True)
        self.QScrollArea_1.setWidget(self.camera_1)

        self.camera_2 = QLabel()
        self.camera_2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_2.setScaledContents(True)
        self.camera_2.installEventFilter(self)
        self.camera_2.setObjectName("Camera_2")
        self.list_of_cameras_state["Camera_2"] = "Normal"

        self.QScrollArea_2 = QScrollArea()
        self.QScrollArea_2.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_2.setWidgetResizable(True)
        self.QScrollArea_2.setWidget(self.camera_2)

        self.camera_3 = QLabel()
        self.camera_3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_3.setScaledContents(True)
        self.camera_3.installEventFilter(self)
        self.camera_3.setObjectName("Camera_3")
        self.list_of_cameras_state["Camera_3"] = "Normal"

        self.QScrollArea_3 = QScrollArea()
        self.QScrollArea_3.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_3.setWidgetResizable(True)
        self.QScrollArea_3.setWidget(self.camera_3)

        self.camera_4 = QLabel()
        self.camera_4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_4.setScaledContents(True)
        self.camera_4.installEventFilter(self)
        self.camera_4.setObjectName("Camera_4")
        self.list_of_cameras_state["Camera_4"] = "Normal"

        self.QScrollArea_4 = QScrollArea()
        self.QScrollArea_4.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_4.setWidgetResizable(True)
        self.QScrollArea_4.setWidget(self.camera_4)

        self.camera_5 = QLabel()
        self.camera_5.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_5.setScaledContents(True)
        self.camera_5.installEventFilter(self)
        self.camera_5.setObjectName("Camera_5")
        self.list_of_cameras_state["Camera_5"] = "Normal"

        self.QScrollArea_5 = QScrollArea()
        self.QScrollArea_5.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_5.setWidgetResizable(True)
        self.QScrollArea_5.setWidget(self.camera_5)

        self.camera_6 = QLabel()
        self.camera_6.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_6.setScaledContents(True)
        self.camera_6.installEventFilter(self)
        self.camera_6.setObjectName("Camera_6")
        self.list_of_cameras_state["Camera_6"] = "Normal"

        self.QScrollArea_6 = QScrollArea()
        self.QScrollArea_6.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_6.setWidgetResizable(True)
        self.QScrollArea_6.setWidget(self.camera_6)

        self.camera_7 = QLabel()
        self.camera_7.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_7.setScaledContents(True)
        self.camera_7.installEventFilter(self)
        self.camera_7.setObjectName("Camera_7")
        self.list_of_cameras_state["Camera_7"] = "Normal"

        self.QScrollArea_7 = QScrollArea()
        self.QScrollArea_7.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_7.setWidgetResizable(True)
        self.QScrollArea_7.setWidget(self.camera_7)

        self.camera_8 = QLabel()
        self.camera_8.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_8.setScaledContents(True)
        self.camera_8.installEventFilter(self)
        self.camera_8.setObjectName("Camera_8")
        self.list_of_cameras_state["Camera_8"] = "Normal"

        self.QScrollArea_8 = QScrollArea()
        self.QScrollArea_8.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_8.setWidgetResizable(True)
        self.QScrollArea_8.setWidget(self.camera_8)

        self.camera_9 = QLabel()
        self.camera_9.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_9.setScaledContents(True)
        self.camera_9.installEventFilter(self)
        self.camera_9.setObjectName("Camera_9")
        self.list_of_cameras_state["Camera_9"] = "Normal"

        self.QScrollArea_9 = QScrollArea()
        self.QScrollArea_9.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_9.setWidgetResizable(True)
        self.QScrollArea_9.setWidget(self.camera_9)

        self.camera_10 = QLabel()
        self.camera_10.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_10.setScaledContents(True)
        self.camera_10.installEventFilter(self)
        self.camera_10.setObjectName("Camera_10")
        self.list_of_cameras_state["Camera_10"] = "Normal"

        self.QScrollArea_10 = QScrollArea()
        self.QScrollArea_10.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_10.setWidgetResizable(True)
        self.QScrollArea_10.setWidget(self.camera_10)

        self.camera_11 = QLabel()
        self.camera_11.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_11.setScaledContents(True)
        self.camera_11.installEventFilter(self)
        self.camera_11.setObjectName("Camera_11")
        self.list_of_cameras_state["Camera_11"] = "Normal"

        self.QScrollArea_11 = QScrollArea()
        self.QScrollArea_11.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_11.setWidgetResizable(True)
        self.QScrollArea_11.setWidget(self.camera_11)

        self.camera_12 = QLabel()
        self.camera_12.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_12.setScaledContents(True)
        self.camera_12.installEventFilter(self)
        self.camera_12.setObjectName("Camera_12")
        self.list_of_cameras_state["Camera_12"] = "Normal"

        self.QScrollArea_12 = QScrollArea()
        self.QScrollArea_12.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_12.setWidgetResizable(True)
        self.QScrollArea_12.setWidget(self.camera_12)

        # Set the UI elements for this Widget class.
        self.__SetupUI()

        self.CaptureIpCameraFramesWorker_1 = CaptureIpCameraFramesWorker(
            self.url_1, conf)
        self.CaptureIpCameraFramesWorker_1.ImageUpdated.connect(
            lambda image: self.ShowCamera1(image))

        self.CaptureIpCameraFramesWorker_2 = CaptureIpCameraFramesWorker(
            self.url_2, conf)
        self.CaptureIpCameraFramesWorker_2.ImageUpdated.connect(
            lambda image: self.ShowCamera2(image))

        self.CaptureIpCameraFramesWorker_3 = CaptureIpCameraFramesWorker(
            self.url_3, conf)
        self.CaptureIpCameraFramesWorker_3.ImageUpdated.connect(
            lambda image: self.ShowCamera3(image))

        self.CaptureIpCameraFramesWorker_4 = CaptureIpCameraFramesWorker(
            self.url_4, conf)
        self.CaptureIpCameraFramesWorker_4.ImageUpdated.connect(
            lambda image: self.ShowCamera4(image))

        self.CaptureIpCameraFramesWorker_5 = CaptureIpCameraFramesWorker(
            self.url_5, conf)
        self.CaptureIpCameraFramesWorker_5.ImageUpdated.connect(
            lambda image: self.ShowCamera5(image))

        self.CaptureIpCameraFramesWorker_6 = CaptureIpCameraFramesWorker(
            self.url_6, conf)
        self.CaptureIpCameraFramesWorker_6.ImageUpdated.connect(
            lambda image: self.ShowCamera6(image))

        self.CaptureIpCameraFramesWorker_7 = CaptureIpCameraFramesWorker(
            self.url_7, conf)
        self.CaptureIpCameraFramesWorker_7.ImageUpdated.connect(
            lambda image: self.ShowCamera7(image))

        self.CaptureIpCameraFramesWorker_8 = CaptureIpCameraFramesWorker(
            self.url_8, conf)
        self.CaptureIpCameraFramesWorker_8.ImageUpdated.connect(
            lambda image: self.ShowCamera8(image))

        self.CaptureIpCameraFramesWorker_9 = CaptureIpCameraFramesWorker(
            self.url_9, conf)
        self.CaptureIpCameraFramesWorker_9.ImageUpdated.connect(
            lambda image: self.ShowCamera9(image))

        self.CaptureIpCameraFramesWorker_10 = CaptureIpCameraFramesWorker(
            self.url_10, conf)
        self.CaptureIpCameraFramesWorker_10.ImageUpdated.connect(
            lambda image: self.ShowCamera10(image))

        self.CaptureIpCameraFramesWorker_11 = CaptureIpCameraFramesWorker(
            self.url_11, conf)
        self.CaptureIpCameraFramesWorker_11.ImageUpdated.connect(
            lambda image: self.ShowCamera11(image))

        self.CaptureIpCameraFramesWorker_12 = CaptureIpCameraFramesWorker(
            self.url_12, conf)
        self.CaptureIpCameraFramesWorker_12.ImageUpdated.connect(
            lambda image: self.ShowCamera12(image))

        # Start the thread getIpCameraFrameWorker_1.
        if self.url_1 != " ":
            self.CaptureIpCameraFramesWorker_1.start()

        if self.url_2 != " ":
            self.CaptureIpCameraFramesWorker_2.start()

        if self.url_3 != " ":
            self.CaptureIpCameraFramesWorker_3.start()

        if self.url_4 != " ":
            self.CaptureIpCameraFramesWorker_4.start()

        if self.url_5 != " ":
            self.CaptureIpCameraFramesWorker_5.start()

        if self.url_6 != " ":
            self.CaptureIpCameraFramesWorker_6.start()

        if self.url_7 != " ":
            self.CaptureIpCameraFramesWorker_7.start()

        if self.url_8 != " ":
            self.CaptureIpCameraFramesWorker_8.start()

        if self.url_9 != " ":
            self.CaptureIpCameraFramesWorker_9.start()

        if self.url_10 != " ":
            self.CaptureIpCameraFramesWorker_10.start()

        if self.url_11 != " ":
            self.CaptureIpCameraFramesWorker_11.start()

        if self.url_12 != " ":
            self.CaptureIpCameraFramesWorker_12.start()

    def __SetupUI(self) -> None:
        # Create an instance of a QGridLayout layout.
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(self.QScrollArea_1, 0, 0)
        grid_layout.addWidget(self.QScrollArea_2, 0, 1)
        grid_layout.addWidget(self.QScrollArea_3, 0, 2)
        grid_layout.addWidget(self.QScrollArea_4, 0, 3)
        grid_layout.addWidget(self.QScrollArea_5, 1, 0)
        grid_layout.addWidget(self.QScrollArea_6, 1, 1)
        grid_layout.addWidget(self.QScrollArea_7, 1, 2)
        grid_layout.addWidget(self.QScrollArea_8, 1, 3)
        grid_layout.addWidget(self.QScrollArea_9, 2, 0)
        grid_layout.addWidget(self.QScrollArea_10, 2, 1)
        grid_layout.addWidget(self.QScrollArea_11, 2, 2)
        grid_layout.addWidget(self.QScrollArea_12, 2, 3)

        # Create a widget instance.
        self.widget = QWidget(self)
        self.widget.setLayout(grid_layout)

        # Set the central widget.
        self.setCentralWidget(self.widget)
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setStyleSheet("QMainWindow {background: 'black';}")

        self.setWindowIcon(QIcon(QPixmap(icon_path)))
        self.setWindowTitle("AEye")

    @ QtCore.pyqtSlot()
    def ShowCamera1(self, frame: QImage) -> None:
        self.camera_1.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera2(self, frame: QImage) -> None:
        self.camera_2.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera3(self, frame: QImage) -> None:
        self.camera_3.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera4(self, frame: QImage) -> None:
        self.camera_4.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera5(self, frame: QImage) -> None:
        self.camera_5.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera6(self, frame: QImage) -> None:
        self.camera_6.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera7(self, frame: QImage) -> None:
        self.camera_7.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera8(self, frame: QImage) -> None:
        self.camera_8.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera9(self, frame: QImage) -> None:
        self.camera_9.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera10(self, frame: QImage) -> None:
        self.camera_10.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera11(self, frame: QImage) -> None:
        self.camera_11.setPixmap(QPixmap.fromImage(frame))

    @ QtCore.pyqtSlot()
    def ShowCamera12(self, frame: QImage) -> None:
        self.camera_12.setPixmap(QPixmap.fromImage(frame))

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """
        Method to capture the events for objects with an event filter installed.
        :param source: The object for whom an event took place.
        :param event: The event that took place.
        :return: True if event is handled.
        """
        #
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if source.objectName() == 'Camera_1':
                #
                if self.list_of_cameras_state["Camera_1"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_1"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_1"] = "Normal"

            elif source.objectName() == 'Camera_2':
                #
                if self.list_of_cameras_state["Camera_2"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_2"] = "Maximized"
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_2"] = "Normal"

            elif source.objectName() == 'Camera_3':
                #
                if self.list_of_cameras_state["Camera_3"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_1.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_3"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_1.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_3"] = "Normal"

            elif source.objectName() == 'Camera_4':
                #
                if self.list_of_cameras_state["Camera_4"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_1.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_4"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_1.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_4"] = "Normal"

            elif source.objectName() == 'Camera_5':
                #
                if self.list_of_cameras_state["Camera_5"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_1.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_5"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_1.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_5"] = "Normal"

            elif source.objectName() == 'Camera_6':
                #
                if self.list_of_cameras_state["Camera_6"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_1.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_6"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_1.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_6"] = "Normal"

            elif source.objectName() == 'Camera_7':
                #
                if self.list_of_cameras_state["Camera_7"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_1.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_7"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_1.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_7"] = "Normal"

            elif source.objectName() == 'Camera_8':
                #
                if self.list_of_cameras_state["Camera_8"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_1.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_8"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_1.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_8"] = "Normal"

            elif source.objectName() == 'Camera_9':
                #
                if self.list_of_cameras_state["Camera_9"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_1.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_9"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_1.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_9"] = "Normal"

            elif source.objectName() == 'Camera_10':
                #
                if self.list_of_cameras_state["Camera_10"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_1.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_10"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_1.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_10"] = "Normal"

            elif source.objectName() == 'Camera_11':
                #
                if self.list_of_cameras_state["Camera_11"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_1.hide()
                    self.QScrollArea_12.hide()
                    self.list_of_cameras_state["Camera_11"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_1.show()
                    self.QScrollArea_12.show()
                    self.list_of_cameras_state["Camera_11"] = "Normal"

            elif source.objectName() == 'Camera_12':
                #
                if self.list_of_cameras_state["Camera_12"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_1.hide()
                    self.list_of_cameras_state["Camera_12"] = "Maximized"
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_1.show()
                    self.list_of_cameras_state["Camera_12"] = "Normal"

            else:
                return super(MainWindow, self).eventFilter(source, event)
            return True
        else:
            return super(MainWindow, self).eventFilter(source, event)

    def closeEvent(self, event) -> None:

        # event.ignore()
        event.accept()


class Login_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(384, 597)

        Dialog.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        Dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(25, 25, 330, 550))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 330, 550))
        self.label.setStyleSheet("background-color:rgba(50, 150, 225, 240);\n"
                                 "border-radius:20px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setGeometry(QtCore.QRect(50, 280, 230, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                    "border:none;\n"
                                    "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                    "color:rgba(0, 0, 0, 255);\n"
                                    "padding-bottom:7px;\n"
                                    "")
        self.lineEdit.setText("")
        self.lineEdit.setCursorPosition(0)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(50, 360, 230, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                      "border:none;\n"
                                      "border-bottom:2px solid rgba(0, 0, 0, 155);\n"
                                      "color:rgba(0, 0, 0, 255);\n"
                                      "padding-bottom:7px;\n"
                                      "")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setDragEnabled(False)
        self.lineEdit_2.setClearButtonEnabled(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(50, 440, 230, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("QPushButton#pushButton{    \n"
                                      "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));\n"
                                      "    color:rgba(255, 255, 255, 210);\n"
                                      "    border-radius:5px;\n"
                                      "}\n"
                                      "QPushButton#pushButton:hover{    \n"
                                      "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
                                      "}\n"
                                      "QPushButton#pushButton:pressed{    \n"
                                      "    padding-left:5px;\n"
                                      "    padding-top:5px;\n"
                                      "    background-color:rgba(105, 118, 132, 200);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton#pushButton_2, #pushButton_3, #pushButton_4, #pushButton_5{    \n"
                                      "    background-color: rgba(0, 0, 0, 0);\n"
                                      "    color:rgba(85, 98, 112, 255);\n"
                                      "}\n"
                                      "QPushButton#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover{    \n"
                                      "    color:rgba(155, 168, 182, 220);\n"
                                      "}\n"
                                      "QPushButton#pushButton_2:pressed, #pushButton_3:pressed, #pushButton_4:pressed, #pushButton_5:pressed{    \n"
                                      "    padding-left:5px;\n"
                                      "    padding-top:5px;\n"
                                      "    color:rgba(115, 128, 142, 255);\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(60, 30, 220, 220))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(logo_path))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(lambda: self.check_password(Dialog))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", " User Name"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", " Password"))
        self.pushButton.setText(_translate("Dialog", "L o g I n"))

    def check_password(self, Dialog):
        msg = QMessageBox()

        login = login_auth(self.lineEdit.text().strip(), self.lineEdit_2.text().strip())

        if not login:
            msg.setText('Incorrect Username or Password')
            msg.exec_()
        else:
            try:
                os.environ["SCHOOL_ID"] = login['localId']
                # print(os.environ["SCHOOL_ID"])
                doc_ref = store.collection('schools').document(login['localId'])
                status = doc_ref.get().get("status")

                if status:
                    # print("Logged In")
                    Popen(f'python {main_path}/api.py')

                    Dialog.close()
                    self.open_dialog()
                else:
                    msg.setText('Verification Key Expired.')
                    msg.exec_()
            except:
                pass

    def open_dialog(self):

        def print_cam_urls(cam_urls):
            self.textForm.close()
            self.open_main_window(cam_urls)

        self.textForm = QtWidgets.QWidget()
        self.textForm.setWindowIcon(QIcon(QPixmap(icon_path)))
        self.ui = Ui_Form()
        self.ui.setupUi(self.textForm)
        self.ui.pushButton.clicked.connect(lambda: self.ui.ok_button_fn(print_cam_urls, self.textForm))
        self.textForm.show()

    def open_main_window(self, inputs):
        main_window = QtWidgets.QMainWindow()
        window = MainWindow(inputs)
        window.show()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QWidget()
    Dialog.setWindowIcon(QIcon(QPixmap(icon_path)))
    ui = Login_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
