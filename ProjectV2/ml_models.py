import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder

def load_training_data(filename="sample_training_data.csv"):
    """
    Load the training dataset we generated
    
    Returns:
        pandas DataFrame
    """
    print(f"Loading training data from {filename}...")
    df = pd.read_csv(filename)
    print(f"Loaded {len(df)} training examples")
    print(f"Columns: {list(df.columns)}")
    return df

if __name__ == "__main__":
    # Load the data
    df = load_training_data()
    print("\nFirst few rows:")
    print(df.head())