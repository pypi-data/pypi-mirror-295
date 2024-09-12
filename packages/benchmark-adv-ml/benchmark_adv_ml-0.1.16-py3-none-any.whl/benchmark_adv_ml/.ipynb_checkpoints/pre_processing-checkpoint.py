import pandas as pd
import numpy as np
import argparse
import os
from sklearn.model_selection import train_test_split

# Function to load data and preprocess it
def load_and_preprocess_data(file_path, target_column='label'):
    df = pd.read_csv(file_path, index_col=0)  # Ensure the index (sample names) is preserved
    df = df.apply(pd.to_numeric, errors='coerce')
    df.fillna(df.mean(), inplace=True)
    return df

# Function to split the data into training and testing sets, separately for each class
def split_data(df, target_column, test_size=0.2, random_state=None):
    # Separate the data by class
    df_class_0 = df[df[target_column] == 0]
    df_class_1 = df[df[target_column] == 1]

    # Split each class individually, retaining indices
    X_train_0, X_test_0, y_train_0, y_test_0 = train_test_split(
        df_class_0.drop(columns=[target_column]), 
        df_class_0[target_column], 
        test_size=test_size, 
        random_state=random_state
    )

    X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(
        df_class_1.drop(columns=[target_column]), 
        df_class_1[target_column], 
        test_size=test_size, 
        random_state=random_state
    )

    # Combine the splits back together
    X_train = pd.concat([X_train_0, X_train_1])
    y_train = pd.concat([y_train_0, y_train_1])
    X_test = pd.concat([X_test_0, X_test_1])
    y_test = pd.concat([y_test_0, y_test_1])

    # Ensure the indices (sample names) are preserved
    return {'train': {'X': X_train, 'y': y_train},
            'test': {'X': X_test, 'y': y_test}}

# Function to save the training and testing data into a specified output directory
def save_split_data(split_data_dict, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Define file paths
    preprocessed_file_train_X = os.path.join(output_dir, 'train_X.csv')
    preprocessed_file_train_y = os.path.join(output_dir, 'train_y.csv')
    preprocessed_file_test_X = os.path.join(output_dir, 'test_X.csv')
    preprocessed_file_test_y = os.path.join(output_dir, 'test_y.csv')
    
    # Save the data with indices (sample names)
    split_data_dict['train']['X'].to_csv(preprocessed_file_train_X)
    split_data_dict['train']['y'].to_csv(preprocessed_file_train_y)
    split_data_dict['test']['X'].to_csv(preprocessed_file_test_X)
    split_data_dict['test']['y'].to_csv(preprocessed_file_test_y)

    print(f"Training and testing data saved to {output_dir}")

# Command-line argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(description="Preprocess the dataset and optionally save the split data.")
    parser.add_argument('--data', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('--target', type=str, default='label', help='Target column name in the dataset.')
    parser.add_argument('--output', type=str, help='Directory to save the preprocessed data (optional).')
    parser.add_argument('--seed', type=int, default=None, help='Seed for random state of split.')
    parser.add_argument('--test_size', type=float, default=0.2, help='Proportion of the dataset to include in the test split.')
    parser.add_argument('--return_split', action='store_true', help='If set, the function will return the split data instead of saving it.')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Load and preprocess data
    df = load_and_preprocess_data(args.data, args.target)

    # Split the data with the provided test size and seed
    split_data_dict = split_data(df, args.target, test_size=args.test_size, random_state=args.seed)

    # Save the split data if an output directory is specified
    if args.output:
        save_split_data(split_data_dict, args.output)
    
    # If return_split is set, return the data (useful for real-time splits during model training)
    if args.return_split:
        train_X, train_y = split_data_dict['train']['X'], split_data_dict['train']['y']
        test_X, test_y = split_data_dict['test']['X'], split_data_dict['test']['y']
        print("Returning split data for further processing.")
        # Returning as dataframes with indices
        # In an actual implementation, you would typically handle this differently, depending on how you want to use the split data.
