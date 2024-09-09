# mmk_ai/auto_train.py

from mmk_ai.data_preprocessing import preprocess_data
from mmk_ai.visualization import univariate_visualization, bivariate_visualization, multivariate_visualization, correlation_heatmap, interactive_heatmap
from mmk_ai.model_training import optimize_hyperparameters, train_model_threaded, save_model
from mmk_ai.evaluation import evaluate_model
from mmk_ai.scoring import calculate_scores, plot_roc_curve
import concurrent.futures
import csv
import os

def auto_train(data, target_column, model_names, save_model_paths=None, csv_export_paths=None, visualization_theme="Viridis", n_trials=50):
    """
    Trains multiple models simultaneously, optimizes hyperparameters using Optuna, and returns the results.
    
    This function performs the following steps:
    1. Visualizes the data using various plots.
    2. Preprocesses the data by splitting it into training and testing sets.
    3. Optimizes the hyperparameters of the models using Optuna.
    4. Trains the specified models concurrently using a thread pool.
    5. Evaluates each trained model.
    6. Calculates performance metrics and plots ROC curves if applicable.
    7. Saves the trained models if save paths are provided.
    8. Exports the results to CSV files if export paths are provided.

    Parameters:
    -----------
    data : pandas.DataFrame
        The dataset to be processed and used for training.
    target_column : str
        The name of the column in the dataset to be used as the target variable.
    model_names : list of str
        A list of model names to be trained. Example: ['RandomForestClassifier', 'SVC'].
    save_model_paths : dict, optional
        A dictionary where the keys are model names and the values are file paths to save the trained models.
        Example: {'RandomForestClassifier': 'random_forest.pkl', 'SVC': 'svc.pkl'}. Default is None.
    csv_export_paths : dict, optional
        A dictionary where the keys are model names and the values are file paths to export the training results as CSV files.
        Example: {'RandomForestClassifier': 'random_forest_results.csv', 'SVC': 'svc_results.csv'}. Default is None.
    visualization_theme : str, optional
        The color theme to use for visualizations. Default is 'Viridis'.
    n_trials : int, optional
        The number of trials to run for hyperparameter optimization using Optuna. Default is 50.

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

    Notes:
    ------
    - This function assumes that the dataset has already been cleaned and is ready for processing.
    - If the target column is categorical, it should be encoded before passing to this function.
    - Models that end with 'Classifier' will have their ROC curves plotted if possible.
    
    Example:
    --------
    >>> results = auto_train(data, target_column="target", model_names=["RandomForestClassifier", "SVC"])
    >>> print(results)
    """
    
    # 1. Adım: Veri Görselleştirme
    print("Performing Univariate Visualization...")
    univariate_visualization(data, theme=visualization_theme)
    
    print("Performing Bivariate Visualization...")
    bivariate_visualization(data, target_column, theme=visualization_theme)
    
    print("Performing Multivariate Visualization...")
    multivariate_visualization(data, theme=visualization_theme)
    
    print("Generating Correlation Heatmap...")
    correlation_heatmap(data)
    
    print("Generating Interactive Heatmap...")
    interactive_heatmap(data)
    
    # 2. Adım: Veri Ön İşleme
    print("Preprocessing Data...")
    X_train, X_test, y_train, y_test = preprocess_data(data, target_column)
    
    # 3. Adım: Optuna ile Hiperparametre Optimizasyonu
    print("Optimizing Hyperparameters with Optuna...")
    best_params = optimize_hyperparameters(X_train, y_train, n_trials=n_trials)
    
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
                
                # 5. Adım: Model Değerlendirme
                print(f"Evaluating Model: {model_name}...")
                evaluate_model(model, X_test, y_test)
                
                # 6. Adım: Değerlendirme Metrikleri ve ROC Eğrisi
                print(f"Calculating Scores for {model_name}...")
                scores = calculate_scores(y_test, model.predict(X_test))
                results[model_name]["scores"] = scores
                print(f"Scores for {model_name}: {scores}")
                
                if model_name.endswith('Classifier'):
                    print(f"Plotting ROC Curve for {model_name}...")
                    plot_roc_curve(model, X_test, y_test)
                
                # 7. Adım: Model Kaydetme
                if save_model_paths and model_name in save_model_paths:
                    print(f"Saving {model_name} to {save_model_paths[model_name]}...")
                    save_model(model, save_model_paths[model_name])
                
                # 8. Adım: Sonuçları CSV'ye Aktarma
                if csv_export_paths and model_name in csv_export_paths:
                    print(f"Exporting Results for {model_name} to {csv_export_paths[model_name]}...")
                    with open(csv_export_paths[model_name], mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Metric', 'Score'])
                        for metric, value in scores.items():
                            writer.writerow([metric, value])
            
            except Exception as exc:
                print(f"{model_name} generated an exception: {exc}")
    
    return results
