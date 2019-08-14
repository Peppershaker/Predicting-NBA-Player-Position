import numpy as np

def top_k_accuracy_score(y_true, y_pred_proba, k):
    """
    Calculates the top k accuracy score and returns it as a float.

    Args:
        y_true : np.array
            ground truth labels in int. Can be one hot encoding (2d) or a 
            single list of labels (1d).

        y_pred_proba : np.array
            predicted class probabilities

    Returns:
        top_k_accuracy_score : float
            top k accuracy score
    """

    if len(y_true.shape) == 2:
        y_true = np.argmax(y_true, axis=1)

    sorted_y_pred = np.fliplr(np.argsort(y_pred_proba, axis=1))[:,:k]

    num_correct = 0

    for idx, y in enumerate(y_true):
        if y in sorted_y_pred[idx][:k]:
            num_correct += 1

    return num_correct / len(y_true)
