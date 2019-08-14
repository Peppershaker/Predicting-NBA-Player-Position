import pytest
import numpy as np
from src.top_k_accuracy import top_k_accuracy_score

def test_top_k_accuracy_score():

    # Class labels are 0 - 4
    y_true =  np.array([1,2,3,4])

    y_pred_proba = np.array([[0.30, 0.11, 0.40, 0.10, 0.09],
                             [0.16, 0.14, 0.30, 0.25, 0.15],
                             [0.40, 0.10, 0.20, 0.14, 0.16],
                             [0.04, 0.70, 0.06, 0.11, 0.09]])

    assert top_k_accuracy_score(y_true, y_pred_proba, k=5) == 1.0

    assert top_k_accuracy_score(y_true, y_pred_proba, k=1) == 0.25

    assert top_k_accuracy_score(y_true, y_pred_proba, k=2) ==  0.25

    assert top_k_accuracy_score(y_true, y_pred_proba, k=3) == 0.75

    assert top_k_accuracy_score(y_true, y_pred_proba, k=4) == 1.0

