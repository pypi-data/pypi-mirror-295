# mmk_ai/easy_train.py 


from mmk_ai.data_preprocessing import preprocess_data, load_csv
from mmk_ai.model_training import train_model_threaded
from mmk_ai.evaluation import evaluate_model
from mmk_ai.scoring import calculate_scores, plot_roc_curve
import concurrent.futures

def easy_train(data_path):
    """
    Loads the dataset, preprocesses it, and trains multiple machine learning models in parallel.
    
    This function performs the following steps:
    1. Loads the dataset from the specified CSV file.
    2. Preprocesses the data by splitting it into training and testing sets, and scaling the features.
    3. Trains multiple machine learning models concurrently using a thread pool.
    4. Evaluates each trained model, calculates performance metrics, and plots ROC curves if applicable.
    5. Returns a dictionary containing the trained models and their corresponding performance metrics.

    Parameters:
    -----------
    data_path : str
        The file path of the dataset in CSV format that will be used for training.

    Returns:
    --------
    results : dict
        A dictionary containing the trained models and their corresponding performance metrics.
        Example:
        {
            'RandomForestClassifier': {
                'model': RandomForestClassifier(),
                'score': 0.85,
                'scores': {
                    'Accuracy': 0.85,
                    'Precision': 0.86,
                    ...
                }
            },
            ...
        }

    Example:
    --------
    >>> results = easy_train("data.csv")
    >>> for model_name, result in results.items():
    >>>     print(f"Model: {model_name}, Score: {result['score']}")
    """
    # 1. Adım: Veriyi Yükleme
    data = load_csv(data_path)
    
    # 2. Adım: Veri Ön İşleme
    target_column = data.columns[-1]  # Son sütun hedef olarak varsayılır
    X_train, X_test, y_train, y_test = preprocess_data(data, target_column)
    
    # 3. Adım: Eğitilecek Modellerin İsimleri
    model_names = [
        'RandomForestClassifier',
        'GradientBoostingClassifier',
        'SVC',
        'LogisticRegression',
        'KNeighborsClassifier',
        'DecisionTreeClassifier'
    ]
    
    # 4. Adım: Model Eğitimi için Thread Pool
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_model = {executor.submit(train_model_threaded, X_train, X_test, y_train, y_test, model_name): model_name for model_name in model_names}
        for future in concurrent.futures.as_completed(future_to_model):
            model_name = future_to_model[future]
            try:
                model, score = future.result()
                results[model_name] = {
                    "model": model,
                    "score": score
                }
                print(f"{model_name} Training Completed. Score: {score}")
                
                # Model Değerlendirme
                evaluate_model(model, X_test, y_test)
                
                # Değerlendirme Metrikleri ve ROC Eğrisi
                scores = calculate_scores(y_test, model.predict(X_test))
                results[model_name]["scores"] = scores
                print(f"Scores for {model_name}: {scores}")
                
                if model_name.endswith('Classifier'):
                    plot_roc_curve(model, X_test, y_test)
            
            except Exception as exc:
                print(f"{model_name} generated an exception: {exc}")
    
    return results
