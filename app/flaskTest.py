from flask import Flask, request, jsonify
from threading import Thread

# Initial flask
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # recovoir data de requet
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    # retourner le resultat de predict
    prediction = "5"  # Souspose la resultat est '5'
    return jsonify({'prediction': prediction})

def start_flask():
    # Lancer flask
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# appeler Flask
if __name__ == "__main__":
    flask_thread = Thread(target=start_flask)
    flask_thread.start()
