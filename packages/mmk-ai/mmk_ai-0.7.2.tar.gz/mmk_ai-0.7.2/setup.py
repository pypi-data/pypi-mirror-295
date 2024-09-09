from setuptools import setup, find_packages

setup(
    name="mmk_ai",
    version="0.7.2",
    description="A custom AI library for data preprocessing, visualization, model training, and evaluation.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Mustafa Kapıcı",
    author_email="m.mustafakapici@gmail.com",
    url="https://github.com/mmustafakapici/mmk_ai",  # GitHub repo adresinizi buraya ekleyin
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "scikit-learn",
        "seaborn",
        "plotly",
        "joblib",
        "tqdm",
        "optuna"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
