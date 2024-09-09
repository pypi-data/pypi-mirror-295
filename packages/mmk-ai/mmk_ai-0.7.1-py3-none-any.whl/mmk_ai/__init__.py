# mmk_ai/__init__.py:

__version__ = "0.6.0"

# Modülleri içe aktar
from .data_preprocessing import load_csv, preprocess_data
from .visualization import (
    univariate_visualization,
    bivariate_visualization,
    multivariate_visualization,
    correlation_heatmap,
    interactive_heatmap,
    kde_plot,
    boxen_plot,
    count_plot,
    scatter_3d_plot
)
from .model_training import train_model_threaded, optimize_hyperparameters, save_model, load_model
from .evaluation import evaluate_model
from .scoring import calculate_scores, plot_roc_curve
from .auto_train import auto_train
from .easy_train import easy_train

# Sabitleri tanımla
DEFAULT_SEED = 42

# Başlatma fonksiyonu
def init():
    print(f"mmk_ai package initialized. Version: {__version__}")

# Başlatma işlemini gerçekleştir
init()
