import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report

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




def train_regression_models(X, y_dest, y_civ):
    """
    Train regression models to predict destruction probability and civilian risk
    
    Args:
        X: Feature matrix
        y_dest: Destruction probability targets
        y_civ: Civilian risk targets
        
    Returns:
        Dictionary of trained models and their performance
    """
    
    print("Training regression models...")
    
    # Split data into training and testing sets
    X_train, X_test, y_dest_train, y_dest_test, y_civ_train, y_civ_test = train_test_split(
        X, y_dest, y_civ, test_size=0.2, random_state=42
    )
    
    # Models to train
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    # Train models for destruction probability
    print("\nDestruction Probability Prediction:")
    for name, model in models.items():
        model.fit(X_train, y_dest_train)
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_dest_test, y_pred))
        score = model.score(X_test, y_dest_test)
        
        results[f'{name}_destruction'] = {
            'model': model,
            'rmse': rmse,
            'r2_score': score
        }
        
        print(f"{name:15} - RMSE: {rmse:.2f}%, R² Score: {score:.3f}")
    
    # Train models for civilian risk
    print("\nCivilian Risk Prediction:")
    for name, base_model in models.items():
        model = type(base_model)(**base_model.get_params()) if hasattr(base_model, 'get_params') else type(base_model)()
        model.fit(X_train, y_civ_train)
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_civ_test, y_pred))
        score = model.score(X_test, y_civ_test)
        
        results[f'{name}_civilian'] = {
            'model': model,
            'rmse': rmse,
            'r2_score': score
        }
        
        print(f"{name:15} - RMSE: {rmse:.2f}%, R² Score: {score:.3f}")
    
    return results



def train_classification_models(X, y_rating):
    """
    Train classification models to predict mission ratings
    
    Args:
        X: Feature matrix
        y_rating: Mission rating targets (S-RANK, A-RANK, etc.)
        
    Returns:
        Dictionary of trained models and their performance
    """
    
    print("Training classification models...")
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_rating, test_size=0.2, random_state=42
    )
    
    # Models to train
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    print("\nMission Rating Classification:")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'predictions': y_pred,
            'actual': y_test
        }
        
        print(f"{name:18} - Accuracy: {accuracy:.3f}")
        
        # Show detailed classification report
        print(f"\n{name} Classification Report:")
        print(classification_report(y_test, y_pred))
    
    return results


if __name__ == "__main__":
    # Load the data
    df = load_training_data()
    print("\nFirst few rows:")
    print(df.head())
    
    # Convert to numerical features
    X, y_dest, y_civ, y_rating = prepare_features(df)
    print(f"\nFeature matrix shape: {X.shape}")
    
    # Train regression models
    regression_results = train_regression_models(X, y_dest, y_civ)
    
    # Train classification models
    classification_results = train_classification_models(X, y_rating)