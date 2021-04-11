import sys
from pathlib import Path

parent = Path(__file__).resolve().parents[1]
sys.path.append(str(parent)+'/code/flaskr/')
from model import get_prediction, load_model

def test_model():
    assert load_model() is True

def test_get_prediction():
    prediction = get_prediction("1.02", "2.03", "Apartment", "Big bedroom", "1", "1")
    assert prediction == "1.02"
