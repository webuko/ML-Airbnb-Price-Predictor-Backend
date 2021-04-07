import sys
from pathlib import Path
parent = Path(__file__).resolve().parents[1]
sys.path.append(str(parent)+'/code/flaskr/')

from model import load_model

def test_load_model():
    model = load_model()
    assert model is not False