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

def prepare_features(df):
    """
    Convert text data to numerical features for machine learning
    
    Args:
        df: Raw training data with text values
        
    Returns:
        X: Feature matrix (numbers only)
        y_dest: Destruction probability targets
        y_civ: Civilian risk targets  
        y_rating: Mission rating targets
    """
    
    print("Converting text data to numerical features...")
    
    # Import the data functions to get specifications
    from utils import get_aircraft_data, get_target_data, get_weather_data, get_time_data
    
    aircraft_data = get_aircraft_data()
    target_data = get_target_data()
    weather_data = get_weather_data()
    time_data = get_time_data()
    
    # Extract numerical features for each row
    features = []
    
    for _, row in df.iterrows():
        # Aircraft features
        aircraft_specs = aircraft_data[row['aircraft']]
        aircraft_precision = aircraft_specs['precision']
        aircraft_stealth = 1 if aircraft_specs['stealth'] else 0
        
        # Target features  
        target_specs = target_data[row['target']]
        target_difficulty = target_specs['difficulty']
        
        # Weather features
        weather_modifier = weather_data[row['weather']]['precision_modifier']
        
        # Time features
        time_modifier = time_data[row['time_of_day']]['civilian_modifier']
        
        # Combine into feature vector
        feature_row = [
            aircraft_precision,
            aircraft_stealth, 
            target_difficulty,
            weather_modifier,
            time_modifier
        ]
        
        features.append(feature_row)
    
    # Convert to arrays
    X = np.array(features)
    y_dest = df['destruction_probability'].values
    y_civ = df['civilian_risk'].values
    y_rating = df['mission_rating'].values
    
    print(f"Created feature matrix: {X.shape}")
    print(f"Feature names: ['aircraft_precision', 'aircraft_stealth', 'target_difficulty', 'weather_modifier', 'time_modifier']")
    
    return X, y_dest, y_civ, y_rating


if __name__ == "__main__":
    # Load the data
    df = load_training_data()
    print("\nFirst few rows:")
    print(df.head())
    
    # Convert to numerical features
    X, y_dest, y_civ, y_rating = prepare_features(df)
    print(f"\nFeature matrix shape: {X.shape}")
    print("First few feature rows:")
    print(X[:3])