# mmk_ai/visualization.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import math
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from pandas.plotting import scatter_matrix

COLOR_THEMES = [
    "viridis", "plasma", "inferno", "magma", "cividis",
    "twilight", "turbo", "deep", "paired", "set2"
]

def scatter_plot(df, x_column, y_column, hue=None, theme="viridis"):
    """
    Creates a scatter plot for two features in the DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    x_column : str
        The name of the feature to plot on the x-axis.
    y_column : str
        The name of the feature to plot on the y-axis.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.
    theme : str, optional
        The color theme to use for the scatter plot. Default is "viridis".

    Returns:
    --------
    None
        Displays the scatter plot.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=x_column, y=y_column, data=df, hue=hue, palette=theme)
    plt.title(f'Scatter Plot of {x_column} vs {y_column}')
    plt.show()

def violin_plot(df, x_column, y_column, hue=None, theme="viridis"):
    """
    Creates a violin plot for visualizing the distribution of data across categories.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    x_column : str
        The name of the categorical feature for the x-axis.
    y_column : str
        The name of the continuous feature for the y-axis.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.
    theme : str, optional
        The color theme to use for the violin plot. Default is "viridis".

    Returns:
    --------
    None
        Displays the violin plot.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    plt.figure(figsize=(10, 7))
    sns.violinplot(x=x_column, y=y_column, data=df, hue=hue, palette=theme)
    plt.title(f'Violin Plot of {x_column} vs {y_column}')
    plt.show()

def bar_plot(df, x_column, y_column, hue=None, theme="viridis"):
    """
    Creates a bar plot for categorical and numerical variables.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    x_column : str
        The name of the categorical feature for the x-axis.
    y_column : str
        The name of the numerical feature for the y-axis.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.
    theme : str, optional
        The color theme to use for the bar plot. Default is "viridis".

    Returns:
    --------
    None
        Displays the bar plot.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    plt.figure(figsize=(10, 7))
    sns.barplot(x=x_column, y=y_column, data=df, hue=hue, palette=theme)
    plt.title(f'Bar Plot of {x_column} vs {y_column}')
    plt.show()

def line_plot(df, x_column, y_column, hue=None, theme="viridis"):
    """
    Creates a line plot for time-series or continuous data.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    x_column : str
        The name of the feature to plot on the x-axis.
    y_column : str
        The name of the feature to plot on the y-axis.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.
    theme : str, optional
        The color theme to use for the line plot. Default is "viridis".

    Returns:
    --------
    None
        Displays the line plot.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    plt.figure(figsize=(10, 7))
    sns.lineplot(x=x_column, y=y_column, data=df, hue=hue, palette=theme)
    plt.title(f'Line Plot of {x_column} vs {y_column}')
    plt.show()

def scatter_matrix_plot(df, theme="viridis"):
    """
    Creates a scatter matrix for visualizing relationships between multiple variables.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    theme : str, optional
        The color theme to use for the scatter matrix. Default is "viridis".

    Returns:
    --------
    None
        Displays the scatter matrix.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    pd.plotting.scatter_matrix(df, alpha=0.2, figsize=(12, 12), diagonal='kde')
    plt.suptitle('Scatter Matrix')
    plt.show()

def univariate_visualization(df, theme="viridis"):
    """
    Performs univariate analysis for each feature in the DataFrame and visualizes it using histograms.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    theme : str, optional
        The color theme to use for the visualizations. Default is "viridis".

    Returns:
    --------
    None
        Displays histograms for each feature in the dataset.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    num_columns = df.shape[1]
    num_rows = math.ceil(num_columns / 3)

    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 6 * num_rows))
    axes = axes.flatten()

    for i, column in enumerate(df.columns):
        sns.histplot(df[column], bins=30, ax=axes[i], kde=False, color=sns.color_palette(theme)[0])
        axes[i].set_title(f'Univariate Analysis of {column}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def bivariate_visualization(df, target_column, hue=None, theme="viridis"):
    """
    Performs bivariate analysis between each feature and the target variable, visualized using box plots.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features and the target variable.
    target_column : str
        The name of the target column in the dataset.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.
    theme : str, optional
        The color theme to use for the visualizations. Default is "viridis".

    Returns:
    --------
    None
        Displays box plots for each feature against the target variable.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    num_columns = len([col for col in df.columns if col != target_column])
    num_rows = math.ceil(num_columns / 3)

    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 6 * num_rows))
    axes = axes.flatten()

    for i, column in enumerate(df.columns):
        if column != target_column:
            if hue:
                sns.boxplot(x=target_column, y=column, data=df, ax=axes[i], hue=hue, palette=theme)
            else:
                sns.boxplot(x=target_column, y=column, data=df, ax=axes[i], color=sns.color_palette(theme)[0])
            axes[i].set_title(f'Bivariate Analysis of {column} vs {target_column}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def multivariate_visualization(df, hue=None, theme="viridis"):
    """
    Performs multivariate analysis on the dataset using pair plots.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.
    theme : str, optional
        The color theme to use for the visualizations. Default is "viridis".

    Returns:
    --------
    None
        Displays pair plots for the features in the dataset.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    if hue is None:
        sns.pairplot(df)  # `palette` kullanılmıyor
    else:
        sns.pairplot(df, hue=hue, palette=theme.lower())  # `palette` yalnızca `hue` varsa kullanılıyor

    plt.title('Multivariate Analysis')
    plt.show()

def correlation_heatmap(df, theme="coolwarm"):
    """
    Plots a correlation heatmap for the features in the dataset.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    theme : str, optional
        The color theme to use for the heatmap. Default is "coolwarm".

    Returns:
    --------
    None
        Displays a heatmap showing the correlations between the features.
    """
    plt.figure(figsize=(12, 10))
    corr_matrix = df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap=theme)
    plt.title("Correlation Matrix")
    plt.show()

def interactive_heatmap(df, theme="viridis"):
    """
    Plots an interactive correlation heatmap for the features in the dataset using Plotly.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    theme : str, optional
        The color theme to use for the heatmap. Default is "viridis".

    Returns:
    --------
    None
        Displays an interactive heatmap showing the correlations between the features.
    """
    corr_matrix = df.corr().values
    labels = df.columns.tolist()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=labels,
        y=labels,
        colorscale=theme
    ))
    fig.update_layout(title="Interactive Correlation Matrix")
    fig.show()

def kde_plot(data, continuous_vars, hue=None, theme="viridis"):
    """
    Plots KDE (Kernel Density Estimate) plots for continuous variables.

    Parameters:
    -----------
    data : pandas.DataFrame
        The dataset containing the continuous variables.
    continuous_vars : list of str
        The list of continuous variables to plot.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.
    theme : str, optional
        The color theme to use for the visualizations. Default is "viridis".

    Returns:
    --------
    None
        Displays KDE plots for the specified continuous variables.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    num_vars = len(continuous_vars)
    num_rows = math.ceil(num_vars / 3)

    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 6 * num_rows))
    axes = axes.flatten()

    for i, var in enumerate(continuous_vars):
        sns.kdeplot(data=data, x=var, hue=hue, fill=True, ax=axes[i], palette=theme)
        axes[i].set_title(f'KDE Plot for {var}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def boxen_plot(data, continuous_vars, hue=None, theme="viridis"):
    """
    Plots boxen plots for continuous variables.

    Parameters:
    -----------
    data : pandas.DataFrame
        The dataset containing the continuous variables.
    continuous_vars : list of str
        The list of continuous variables to plot.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.
    theme : str, optional
        The color theme to use for the visualizations. Default is "viridis".

    Returns:
    --------
    None
        Displays boxen plots for the specified continuous variables.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    num_vars = len(continuous_vars)
    num_rows = math.ceil(num_vars / 3)

    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 6 * num_rows))
    axes = axes.flatten()

    for i, var in enumerate(continuous_vars):
        sns.boxenplot(data=data, x=var, hue=hue, ax=axes[i], palette=theme)
        axes[i].set_title(f'Boxen Plot for {var}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def count_plot(data, categorical_vars, hue=None, theme="viridis"):
    """
    Plots count plots for categorical variables.

    Parameters:
    -----------
    data : pandas.DataFrame
        The dataset containing the categorical variables.
    categorical_vars : list of str
        The list of categorical variables to plot.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.
    theme : str, optional
        The color theme to use for the visualizations. Default is "viridis".

    Returns:
    --------
    None
        Displays count plots for the specified categorical variables.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    num_vars = len(categorical_vars)
    num_rows = math.ceil(num_vars / 3)

    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 6 * num_rows))
    axes = axes.flatten()

    for i, var in enumerate(categorical_vars):
        sns.countplot(data=data, x=var, hue=hue, ax=axes[i], palette=theme)
        axes[i].set_title(f'Count Plot for {var}')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def scatter_3d_plot(data, continuous_vars, hue=None):
    """
    Plots a 3D scatter plot for three continuous variables.

    Parameters:
    -----------
    data : pandas.DataFrame
        The dataset containing the continuous variables.
    continuous_vars : list of str
        The list of three continuous variables to plot in 3D.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.

    Returns:
    --------
    None
        Displays a 3D scatter plot for the specified continuous variables.

    Raises:
    -------
    ValueError
        If the length of `continuous_vars` is less than 3.
    """
    if len(continuous_vars) < 3:
        raise ValueError("3D scatter plot requires at least 3 continuous variables.")

    fig = px.scatter_3d(data, x=continuous_vars[0], y=continuous_vars[1], z=continuous_vars[2], color=hue)
    fig.update_layout(title=f'3D Scatter Plot of {continuous_vars[0]}, {continuous_vars[1]}, {continuous_vars[2]}')
    fig.show()

def pca_visualization(df, n_components=2, theme="viridis"):
    """
    Performs PCA (Principal Component Analysis) on the dataset and visualizes the first two principal components.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    n_components : int, optional
        The number of principal components to compute. Default is 2.
    theme : str, optional
        The color theme to use for the visualizations. Default is "viridis".

    Returns:
    --------
    None
        Displays a scatter plot of the first two principal components.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(df)

    pc_df = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(n_components)])

    if n_components == 2:
        plt.figure(figsize=(10, 7))
        sns.scatterplot(x='PC1', y='PC2', data=pc_df, palette=theme)
        plt.title('PCA - First Two Principal Components')
        plt.show()
    elif n_components == 3:
        fig = px.scatter_3d(pc_df, x='PC1', y='PC2', z='PC3')
        fig.update_layout(title='PCA - First Three Principal Components')
        fig.show()
    else:
        print("PCA visualization supports only 2 or 3 components for plotting.")

def tsne_visualization(df, n_components=2, theme="viridis"):
    """
    Performs T-SNE (t-Distributed Stochastic Neighbor Embedding) on the dataset and visualizes the components.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    n_components : int, optional
        The number of dimensions to reduce the data to. Default is 2.
    theme : str, optional
        The color theme to use for the visualizations. Default is "viridis".

    Returns:
    --------
    None
        Displays a scatter plot of the T-SNE components.
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    tsne = TSNE(n_components=n_components, random_state=42)
    tsne_components = tsne.fit_transform(df)

    tsne_df = pd.DataFrame(data=tsne_components, columns=[f'TSNE{i+1}' for i in range(n_components)])

    if n_components == 2:
        plt.figure(figsize=(10, 7))
        sns.scatterplot(x='TSNE1', y='TSNE2', data=tsne_df, palette=theme)
        plt.title('T-SNE - First Two Components')
        plt.show()
    elif n_components == 3:
        fig = px.scatter_3d(tsne_df, x='TSNE1', y='TSNE2', z='TSNE3')
        fig.update_layout(title='T-SNE - First Three Components')
        fig.show()
    else:
        print("T-SNE visualization supports only 2 or 3 components for plotting.")

def pair_plot(df, hue=None, theme="viridis"):
    """
    Creates a pair plot to visualize the pairwise relationships in the dataset.

    Parameters:
    -----------
    df : pandas.DataFrame
        The dataset containing the features to visualize.
    hue : str, optional
        The name of the column to use for color encoding. Default is None.
    theme : str, optional
        The color theme to use for the pair plot. Default is "viridis".

    Returns:
    --------
    None
        Displays the pair plot for the features in the dataset.
    
    Example:
    --------
    >>> pair_plot(df, hue='species', theme='plasma')
    """
    if theme not in COLOR_THEMES:
        theme = "viridis"

    plt.figure(figsize=(12, 10))
    sns.pairplot(df, hue=hue, palette=theme.lower())
    plt.title('Pair Plot of Dataset')
    plt.show()