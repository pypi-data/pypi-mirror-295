# mmk_ai/evaluation.py


from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the performance of a trained model on the test data and displays a classification report and confusion matrix.
    
    This function performs the following steps:
    1. Predicts the target values using the provided model and test features.
    2. Prints a classification report showing precision, recall, f1-score, and support for each class.
    3. Computes and visualizes the confusion matrix using a heatmap.

    Parameters:
    -----------
    model : sklearn.base.BaseEstimator
        The trained machine learning model to be evaluated.
    X_test : pandas.DataFrame or numpy.ndarray
        The features of the test set.
    y_test : pandas.Series or numpy.ndarray
        The true target values of the test set.

    Returns:
    --------
    None
        This function does not return anything. It prints the classification report to the console and displays a confusion matrix heatmap.

    Example:
    --------
    >>> evaluate_model(trained_model, X_test, y_test)
    Classification Report:
                 precision    recall  f1-score   support

              0       0.95      0.90      0.92       100
              1       0.89      0.94      0.92       100

       accuracy                           0.92       200
      macro avg       0.92      0.92      0.92       200
   weighted avg       0.92      0.92      0.92       200

    [Displays confusion matrix heatmap]
    """
    y_pred = model.predict(X_test)

    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d')
    plt.title('Confusion Matrix')
    plt.show()
