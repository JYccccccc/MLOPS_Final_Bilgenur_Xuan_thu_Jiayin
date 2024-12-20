from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSplitter, QComboBox,
    QLabel, QSpinBox, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QCheckBox
)
from PyQt5.QtGui import QPainter, QPen, QImage
from PyQt5.QtCore import Qt, QPoint
from tensorflow import keras
import numpy as np
from flask import Flask, request, jsonify
import threading

# Definie Flask
app = Flask(__name__)

# Flask API routier, pour charger le modele
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        image_array = np.array(data['image']).reshape(1, 28, 28, 1)
        image_array = image_array / 255.0  # normalisation
        model = keras.models.load_model('save/modelMnist1.keras')
        prediction = model.predict(image_array)
        output = np.argmax(prediction, axis=1)
        return jsonify({"prediction": int(output[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# PaintBoard
class PaintBoard(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.image = QImage(28, 28, QImage.Format_ARGB32)
        self.image.fill(Qt.white)

        self.penColor = QColor("black")
        self.penThickness = 1
        self.drawing = False
        self.lastPoint = QPoint()

        self.setFixedSize(280, 280)
        self.scene.setSceneRect(0, 0, 28, 28)
        self.scale(10, 10)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = self.mapToScene(event.pos()).toPoint()

    def mouseMoveEvent(self, event):
        if self.drawing:
            currentPoint = self.mapToScene(event.pos()).toPoint()
            painter = QPainter(self.image)
            pen = QPen(self.penColor, self.penThickness, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.lastPoint, currentPoint)
            self.lastPoint = currentPoint
            self.scene.clear()
            self.scene.addPixmap(QPixmap.fromImage(self.image))
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def clear(self):
        self.image.fill(Qt.white)
        self.scene.clear()
        self.scene.addPixmap(QPixmap.fromImage(self.image))

    def changePenColor(self, color):
        self.penColor = QColor(color)

    def changePenThickness(self, thickness):
        self.penThickness = thickness

    def getContentAsQImage(self):
        return self.image

# MainWidget
class MainWidget(QWidget):
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.__InitData()
        self.__InitView()

    def __InitData(self):
        self.__paintBoard = PaintBoard(self)
        self.__colorList = QColor.colorNames()

    def __InitView(self):
        self.setFixedSize(640, 480)
        self.setWindowTitle("Reconnaître des chiffres manuscrits")

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.__paintBoard)

        sub_layout = QVBoxLayout()
        sub_layout.setContentsMargins(5, 5, 5, 5)
        splitter = QSplitter(self)
        sub_layout.addWidget(splitter)

        self.__btn_Recognize = QPushButton("Reconnaître")
        self.__btn_Recognize.clicked.connect(self.on_btn_Recognize_Clicked)
        sub_layout.addWidget(self.__btn_Recognize)

        self.__btn_Clear = QPushButton("Nettoyer la table")
        self.__btn_Clear.clicked.connect(self.__paintBoard.clear)
        sub_layout.addWidget(self.__btn_Clear)

        self.__btn_Quit = QPushButton("Quit")
        self.__btn_Quit.clicked.connect(self.close)
        sub_layout.addWidget(self.__btn_Quit)

        main_layout.addLayout(sub_layout)

    def on_btn_Recognize_Clicked(self):
        savePath = "save/img/text.png"
        image = self.__paintBoard.getContentAsQImage()
        image.save(savePath)
        print(f"Image saved to: {savePath}")

        img = keras.preprocessing.image.load_img(savePath, target_size=(28, 28))
        img = img.convert('L')
        x = keras.preprocessing.image.img_to_array(img)
        x = abs(255 - x)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0
        new_model = keras.models.load_model('save/modelMnist1.keras')
        prediction = new_model.predict(x)
        output = np.argmax(prediction, axis=1)
        print("Les chiffres manuscrits sont reconnus comme：" + str(output[0]))

# Lancer flask
def start_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# lancer Qtpy
if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.setDaemon(True)
    flask_thread.start()

    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    mainWindow = MainWidget()
    mainWindow.show()
    sys.exit(app.exec_())
