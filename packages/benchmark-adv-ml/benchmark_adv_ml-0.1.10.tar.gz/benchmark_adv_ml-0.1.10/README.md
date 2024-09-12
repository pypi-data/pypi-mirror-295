# Benchmark-Adv-ML

**Benchmark-Adv-ML** is a Python package designed to facilitate advanced benchmarking of machine learning models. It provides a comprehensive pipeline to evaluate model stability, generate predictions, and visualize results through various plots, including AUC curves, feature importance, and radar charts.

## Features

- **Model Stability Evaluation**: Automatically runs multiple machine learning models (Logistic Regression, SVC, RandomForestClassifier) across multiple runs.
- **Prediction and Metrics**: Generates and saves predictions, feature importance, and various metrics for each model and run.
- **Aggregation of Results**: Aggregates results across runs and models for comprehensive analysis.
- **Visualization**: Generates plots including AUC curves, AUC box plots, feature importance plots, and radar charts to compare model performance.

## Installation

You can install the package directly from PyPI:

```bash
pip install benchmark-adv-ml
```

## Usage in Unix

```bash
benchmark-adv-ml --data ./your_dataset.csv --output ./final_results --prelim_output ./prelim_results --n_runs 10 --seed 42
```

## Useage in python 

```bash
python -m benchmark_adv_ml --data ./Raisin_Dataset.data --output ./final_results --prelim_output ./prelim_results --n_runs 10 --seed 42
```

## Command-Line Arguments

--data: Path to the existing CSV file containing the dataset.
--output: Directory to save the final results and plots.
--target : Target column name in the dataset. ( default : 'label')
--prelim_output: Directory to save the preliminary results (predictions).
--n_runs: Number of runs for model stability evaluation (default is 20).
--seed: Seed for random state (default is 42).


## Example 

```bash
benchmark-adv-ml --data ./your_dataset.csv --output ./final_results --prelim_output ./prelim_results --n_runs 10 --seed 42
```

### Dependencies 
Python 3.11+
seaborn
scikit-learn
pandas
numpy
matplotlib

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author 
Vatsal Pate - VatsalPatel18


