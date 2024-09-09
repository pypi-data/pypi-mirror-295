# mmk_ai/scoring.py


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, auc
import matplotlib.pyplot as plt



def calculate_scores(y_true, y_pred, average='binary'):
    """
    Calculates and returns common classification performance metrics including accuracy, precision, recall, and F1 score.

    Parameters:
    -----------
    y_true : array-like
        True labels or binary label indicators.
    y_pred : array-like
        Predicted labels, as returned by a classifier.
    average : str, optional
        This parameter is required for multiclass/multilabel targets. Default is 'binary'.
        - 'binary': Only report results for the class specified by pos_label.
        - 'micro': Calculate metrics globally by counting the total true positives, false negatives, and false positives.
        - 'macro': Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
        - 'weighted': Calculate metrics for each label, and find their average, weighted by support (the number of true instances for each label).
        - 'samples': Calculate metrics for each instance, and find their average.

    Returns:
    --------
    scores : dict
        A dictionary containing the calculated scores:
        - 'Accuracy': Accuracy of the model.
        - 'Precision': Precision of the model.
        - 'Recall': Recall of the model.
        - 'F1 Score': F1 score of the model.

    Example:
    --------
    >>> scores = calculate_scores(y_test, y_pred)
    >>> print(scores)
    {'Accuracy': 0.95, 'Precision': 0.96, 'Recall': 0.94, 'F1 Score': 0.95}
    """
    scores = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, average=average),
        "Recall": recall_score(y_true, y_pred, average=average),
        "F1 Score": f1_score(y_true, y_pred, average=average)
    }
    return scores


def plot_roc_curve(model, X_test, y_test):
    """
    Plots the Receiver Operating Characteristic (ROC) curve for a given model on the test data.

    This function calculates the ROC curve and the Area Under the Curve (AUC) score, then plots the ROC curve.

    Parameters:
    -----------
    model : sklearn.base.BaseEstimator
        The trained machine learning model.
    X_test : pandas.DataFrame or numpy.ndarray
        The test features.
    y_test : pandas.Series or numpy.ndarray
        The true labels of the test data.

    Returns:
    --------
    None
        This function does not return anything. It directly displays the ROC curve.

    Example:
    --------
    >>> plot_roc_curve(trained_model, X_test, y_test)
    [Displays ROC curve]
    """
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()
