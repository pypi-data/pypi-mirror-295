# mmk_ai/model_training.py


from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import optuna
import joblib


def train_model_threaded(X_train, X_test, y_train, y_test, model_name):
    """
    Trains a specified machine learning model and returns its performance on the test set.
    
    This function trains the specified model on the training data, evaluates its performance 
    on the test data, and returns the trained model along with its accuracy score.

    Parameters:
    -----------
    X_train : pandas.DataFrame or numpy.ndarray
        The training features.
    X_test : pandas.DataFrame or numpy.ndarray
        The test features.
    y_train : pandas.Series or numpy.ndarray
        The training target values.
    y_test : pandas.Series or numpy.ndarray
        The test target values.
    model_name : str
        The name of the model to be trained. Must be one of the following:
        - 'RandomForestClassifier'
        - 'GradientBoostingClassifier'
        - 'SVC'
        - 'LogisticRegression'
        - 'KNeighborsClassifier'
        - 'DecisionTreeClassifier'

    Returns:
    --------
    model : sklearn.base.BaseEstimator
        The trained model.
    score : float
        The accuracy score of the model on the test data.

    Raises:
    -------
    ValueError
        If the provided model_name is not supported.

    Example:
    --------
    >>> model, score = train_model_threaded(X_train, X_test, y_train, y_test, 'RandomForestClassifier')
    >>> print(f"Trained Model: {model}, Accuracy: {score}")
    """
    models = {
        "RandomForestClassifier": RandomForestClassifier(),
        "GradientBoostingClassifier": GradientBoostingClassifier(),
        "SVC": SVC(probability=True),
        "LogisticRegression": LogisticRegression(),
        "KNeighborsClassifier": KNeighborsClassifier(),
        "DecisionTreeClassifier": DecisionTreeClassifier()
    }

    model = models.get(model_name)
    if model:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        if model_name.endswith('Classifier'):
            score = accuracy_score(y_test, y_pred)
        else:
            score = model.score(X_test, y_test)

        return model, score
    else:
        raise ValueError(f"Model {model_name} is not supported.")


def save_model(model, file_path):
    """
    Saves a trained model to a specified file path using joblib.

    Parameters:
    -----------
    model : sklearn.base.BaseEstimator
        The trained machine learning model to be saved.
    file_path : str
        The file path where the model will be saved.

    Returns:
    --------
    None

    Example:
    --------
    >>> save_model(trained_model, 'random_forest_model.pkl')
    """
    joblib.dump(model, file_path)


def load_model(file_path):
    """
    Loads a trained model from a specified file path using joblib.

    Parameters:
    -----------
    file_path : str
        The file path from which the model will be loaded.

    Returns:
    --------
    model : sklearn.base.BaseEstimator
        The loaded machine learning model.

    Example:
    --------
    >>> model = load_model('random_forest_model.pkl')
    >>> print(model)
    """
    return joblib.load(file_path)


def objective(trial, X_train, y_train):
    """
    Objective function for optimizing model hyperparameters using Optuna.
    
    This function defines the hyperparameter search space and computes the cross-validated 
    accuracy score for a given set of hyperparameters.

    Parameters:
    -----------
    trial : optuna.trial.Trial
        A trial object that is used to suggest hyperparameters.
    X_train : pandas.DataFrame or numpy.ndarray
        The training features.
    y_train : pandas.Series or numpy.ndarray
        The training target values.

    Returns:
    --------
    accuracy : float
        The mean accuracy score from cross-validation.

    Example:
    --------
    >>> study = optuna.create_study(direction='maximize')
    >>> study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=50)
    >>> print("Best trial:", study.best_trial.params)
    """
    model_name = trial.suggest_categorical('model_name', [
        'RandomForestClassifier',
        'GradientBoostingClassifier',
        'SVC',
        'LogisticRegression',
        'KNeighborsClassifier',
        'DecisionTreeClassifier'
    ])

    if model_name == 'RandomForestClassifier':
        n_estimators = trial.suggest_int('n_estimators', 10, 200)
        max_depth = trial.suggest_int('max_depth', 2, 32)
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)

    elif model_name == 'GradientBoostingClassifier':
        n_estimators = trial.suggest_int('n_estimators', 10, 200)
        learning_rate = trial.suggest_loguniform('learning_rate', 0.01, 0.3)
        model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate)

    elif model_name == 'SVC':
        C = trial.suggest_loguniform('C', 1e-10, 1e10)
        kernel = trial.suggest_categorical('kernel', ['linear', 'poly', 'rbf', 'sigmoid'])
        model = SVC(C=C, kernel=kernel)

    elif model_name == 'LogisticRegression':
        C = trial.suggest_loguniform('C', 1e-10, 1e10)
        solver = trial.suggest_categorical('solver', ['newton-cg', 'lbfgs', 'liblinear'])
        model = LogisticRegression(C=C, solver=solver)

    elif model_name == 'KNeighborsClassifier':
        n_neighbors = trial.suggest_int('n_neighbors', 2, 40)
        model = KNeighborsClassifier(n_neighbors=n_neighbors)

    elif model_name == 'DecisionTreeClassifier':
        max_depth = trial.suggest_int('max_depth', 2, 32)
        criterion = trial.suggest_categorical('criterion', ['gini', 'entropy'])
        model = DecisionTreeClassifier(max_depth=max_depth, criterion=criterion)

    score = cross_val_score(model, X_train, y_train, n_jobs=-1, cv=3)
    accuracy = score.mean()
    return accuracy


def optimize_hyperparameters(X_train, y_train, n_trials=50):
    """
    Optimizes the hyperparameters of a model using Optuna.

    This function runs multiple trials to find the best hyperparameter combination 
    that maximizes the model's cross-validated accuracy score.

    Parameters:
    -----------
    X_train : pandas.DataFrame or numpy.ndarray
        The training features.
    y_train : pandas.Series or numpy.ndarray
        The training target values.
    n_trials : int, optional
        The number of trials to run for hyperparameter optimization. Default is 50.

    Returns:
    --------
    dict
        The best hyperparameter combination found during the optimization.

    Example:
    --------
    >>> best_params = optimize_hyperparameters(X_train, y_train, n_trials=100)
    >>> print("Best Hyperparameters:", best_params)
    """
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=n_trials)

    print("Best model:", study.best_trial.params)
    return study.best_trial.params
