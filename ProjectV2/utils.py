import sys
import os

# Add ProjectV1 to Python's path so we can import from it
sys.path.insert(0, '../ProjectV1')

# Import the functions we need from your original system
from project import (
    calculate_mission_score,
    assign_mission_rating,
    get_aircraft_data,
    get_target_data,
    get_weather_data,
    get_time_data
)


# Test function to verify imports work
def test_imports():
    """Test that all imports from original system work"""
    print("Testing imports from original system...")
    time_periods = get_time_data()
    print(f"Time periods loaded: {len(time_periods)} time slots")
    
    # Test getting data
    aircraft = get_aircraft_data()
    print(f"Aircraft data loaded: {len(aircraft)} aircraft types")
    
    # Test a sample calculation
    dest_prob, civ_risk = calculate_mission_score("F-35A", "military_base", "clear", "night")
    rating = assign_mission_rating(dest_prob, civ_risk)
    print(f"Sample mission: {dest_prob}% success, {civ_risk}% civilian risk, {rating}")
    
    print("All imports working correctly!")

if __name__ == "__main__":
    test_imports()