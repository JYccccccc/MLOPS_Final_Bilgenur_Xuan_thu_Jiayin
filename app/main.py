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
from prometheus_client import Counter, Histogram, generate_latest
from time import time
import os
from train import train_model, get_training_logs

current_model = None
model_metadata = {
    "model_name": "modelMnist1",
    "version": "v1.0",
    "accuracy": None,
    "loss": None,
    "training_params": {}
}
training_logs = []

# Definie Flask
app = Flask(__name__)

def track_metrics(endpoint):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time()
            REQUEST_COUNT.labels(method=request.method, endpoint=endpoint).inc()
            response = func(*args, **kwargs)
            duration = time() - start_time
            REQUEST_DURATION.labels(endpoint=endpoint).observe(duration)
            return response
        return wrapper
    return decorator

# Flask API routier, pour charger le modele
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if 'image' not in data:
            return jsonify({"error": "Invalid input", "message": "Image data is required."}), 400
        
        image_array = np.array(data['image']).reshape(1, 28, 28, 1)
        image_array = image_array / 255.0  # normalization
        model = keras.models.load_model('save/modelMnist1.keras')
        prediction = model.predict(image_array)
        probabilities = prediction.tolist()[0]
        output = np.argmax(probabilities)
        return jsonify({
            "prediction": int(output),
            "probabilities": probabilities
        })
    except Exception as e:
        return jsonify({"error": "Prediction error", "message": str(e)}), 500

# Metrics
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('api_request_duration_seconds', 'API request duration', ['endpoint'])

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/health', methods=['GET'])
def health():
    try:
        
        api_status = "Healthy"

        
        try:
            database_status = "Connected"
        except Exception as e:
            database_status = f"Error: {str(e)}"

        other_services_status = {
            "MLFlow": "Healthy"  
        }

        response = {
            "status": "Healthy" if database_status == "Connected" and all(
                status == "Healthy" for status in other_services_status.values()) else "Unhealthy",
            "details": {
                "api_status": api_status,
                "database_status": database_status,
                "other_services_status": other_services_status,
            }
        }
        return jsonify(response), 200 if response["status"] == "Healthy" else 503

    except Exception as e:
        response = {
            "status": "Unhealthy",
            "details": {
                "error": str(e)
            }
        }
        return jsonify(response), 500

@app.route('/model/info', methods=['GET'])
def get_model_info():
    return jsonify(model_metadata)

@app.route('/train', methods=['POST'])
def train():
    global current_model, model_metadata, training_logs
    data = request.get_json()
    batch_size = data.get('batch_size', 32)
    epochs = data.get('epochs', 10)
    optimizer = data.get('optimizer', 'adam')

    # training
    model, history, logs = train_model(batch_size=batch_size, epochs=epochs, optimizer=optimizer)
    
    #mis a jour les infos de modele
    current_model = model
    model_metadata["accuracy"] = history['accuracy'][-1]
    model_metadata["loss"] = history['loss'][-1]
    model_metadata["training_params"] = {
        "batch_size": batch_size,
        "epochs": epochs,
        "optimizer": optimizer
    }
    training_logs = logs

    return jsonify({
        "status": "Entraînement démarré",
        "message": f"L'entraînement a démarré avec batch_size={batch_size}, epochs={epochs}, optimizer='{optimizer}'."
    })

@app.route('/logs', methods=['GET'])
def get_logs():
    """retouner trainning logs"""
    return jsonify({"logs": training_logs})

@app.route('/user', methods=['GET', 'POST'])
def manage_user():
    """gerer information d'utilisateur"""
    if request.method == 'GET':
        user_info = {
            "user_id": "12345",
            "username": "john_doe",
            "role": "admin",
            "last_login": "2024-12-20T10:00:00Z"
        }
        return jsonify(user_info)
    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')

        if not username or not password:
            return jsonify({
                "error": "BadRequest",
                "message": "Nom d'utilisateur et mot de passe sont obligatoires."
            }), 400

        return jsonify({
            "status": "Utilisateur créé",
            "message": f"L'utilisateur '{username}' a été créé avec succès."
        })


@app.route('/model/deploy', methods=['POST'])
def deploy_model():
    """environement de producter"""
    global current_model
    if not current_model:
        return jsonify({
            "error": "NoModel",
            "message": "Aucun modèle n'est disponible pour le déploiement."
        }), 400

    version = "v2.0"
    model_metadata["version"] = version
    return jsonify({
        "status": "Déploiement réussi",
        "message": f"Le modèle version {version} a été déployé avec succès."
    })

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

    #import sys
    #from PyQt5.QtWidgets import QApplication
    #app = QApplication(sys.argv)
    #mainWindow = MainWidget()
    #mainWindow.show()
    #sys.exit(app.exec_())
