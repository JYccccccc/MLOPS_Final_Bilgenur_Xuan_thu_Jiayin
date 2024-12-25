import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.train import train_model
def test_train_model():

    batch_size = 32
    epochs = 1
    optimizer = "adam"
    model, history, logs = train_model(batch_size=batch_size, epochs=epochs, optimizer=optimizer)

    assert model is not None
    assert "accuracy" in history
    assert len(history['accuracy']) == epochs
    assert "loss" in history
