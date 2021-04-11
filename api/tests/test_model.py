import sys
from pathlib import Path
from decimal import *

parent = Path(__file__).resolve().parents[1]
sys.path.append(str(parent)+'/code/flaskr/')
from model import *

def test_model():
    assert load_model() is True

def test_get_prediction():
    prediction = get_prediction("1.02", "2.03", "Apartment", "Big bedroom", "1", "1")
    assert prediction is "1.02"
