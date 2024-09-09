# mmk_ai/data_preprocessing.py


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    -----------
    file_path : str
        The path to the CSV file that needs to be loaded.

    Returns:
    --------
    pandas.DataFrame
        The DataFrame containing the data from the CSV file.
    
    Example:
    --------
    >>> df = load_csv("data.csv")
    >>> print(df.head())
    """
    return pd.read_csv(file_path)

def preprocess_data(df, target_column):
    """
    Preprocess the dataset by scaling numeric features and encoding categorical features, 
    then split the data into training and testing sets.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the dataset.
    target_column : str
        The name of the column to be used as the target variable.

    Returns:
    --------
    tuple
        A tuple containing the following four elements:
        - X_train: Training features after preprocessing.
        - X_test: Testing features after preprocessing.
        - y_train: Training target values.
        - y_test: Testing target values.

    Notes:
    ------
    - Numeric features are scaled using `StandardScaler`.
    - Categorical features are one-hot encoded using `OneHotEncoder`.

    Example:
    --------
    >>> X_train, X_test, y_train, y_test = preprocess_data(df, target_column="target")
    >>> print(X_train.shape, X_test.shape)
    """
    # Hedef sütunu çıkartarak sayısal ve kategorik sütunları belirle
    numeric_features = df.drop(columns=[target_column]).select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df.drop(columns=[target_column]).select_dtypes(include=['object']).columns.tolist()

    # X ve y'yi ayır
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Sayısal ve kategorik sütunları ayır
    X_numeric = X[numeric_features]
    X_categorical = X[categorical_features]

    # Sayısal sütunları ölçekle
    scaler = StandardScaler()
    X_numeric_scaled = scaler.fit_transform(X_numeric)

    # Kategorik sütunları one-hot encode ile dönüştür
    encoder = OneHotEncoder(sparse=False)
    X_categorical_encoded = encoder.fit_transform(X_categorical)

    # Sayısal ve kategorik sütunları birleştir
    X_preprocessed = pd.DataFrame(X_numeric_scaled, columns=numeric_features)
    X_preprocessed = pd.concat([X_preprocessed, pd.DataFrame(X_categorical_encoded)], axis=1)

    # Eğitim ve test kümelerine ayır
    return train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)
