from utils import (
    calculate_mission_score, assign_mission_rating, 
    get_aircraft_data, get_target_data, get_weather_data, get_time_data
)
import sys

def find_match(user_input, valid_options):
    """Find case-insensitive match in valid options"""
    user_lower = user_input.lower()
    
    # Direct case-insensitive match
    for option in valid_options:
        if option.lower() == user_lower:
            return option
    
    # Partial match (starts with)
    for option in valid_options:
        if option.lower().startswith(user_lower):
            return option
    
    return None

def validate_inputs(aircraft, target, weather, time_of_day):
    """Validate and correct user inputs"""
    aircraft_data = get_aircraft_data()
    target_data = get_target_data()
    weather_data = get_weather_data()
    time_data = get_time_data()
    
    # Find correct matches
    correct_aircraft = find_match(aircraft, list(aircraft_data.keys()))
    correct_target = find_match(target, list(target_data.keys()))
    correct_weather = find_match(weather, list(weather_data.keys()))
    correct_time = find_match(time_of_day, list(time_data.keys()))
    
    errors = []
    if not correct_aircraft:
        errors.append(f"Aircraft '{aircraft}' not found. Available: {list(aircraft_data.keys())}")
    if not correct_target:
        errors.append(f"Target '{target}' not found. Available: {list(target_data.keys())}")
    if not correct_weather:
        errors.append(f"Weather '{weather}' not found. Available: {list(weather_data.keys())}")
    if not correct_time:
        errors.append(f"Time '{time_of_day}' not found. Available: {list(time_data.keys())}")
    
    if errors:
        print("VALIDATION ERRORS:")
        for error in errors:
            print(f"- {error}")
        return None
    
    return correct_aircraft, correct_target, correct_weather, correct_time

def show_options():
    """Show all available options for command line usage"""
    aircraft_data = get_aircraft_data()
    target_data = get_target_data()
    weather_data = get_weather_data()
    time_data = get_time_data()
    
    print("AVAILABLE OPTIONS:")
    print("="*50)
    
    print("Aircraft:", ", ".join(aircraft_data.keys()))
    print("Targets:", ", ".join(target_data.keys()))  
    print("Weather:", ", ".join(weather_data.keys()))
    print("Time:", ", ".join(time_data.keys()))
    
    print("\nUSAGE (case-insensitive):")
    print("python mission_planner.py <aircraft> <target> <weather> <time>")
    print("\nEXAMPLES:")
    print("python mission_planner.py F-35A military_base clear night")
    print("python mission_planner.py b-2 nuclear_facility storm afternoon")
    print("python mission_planner.py a-10 wooden_house clear early_morning")

def assess_mission(aircraft, target, weather, time_of_day):
    """Assess a specific mission"""
    dest_prob, civ_risk = calculate_mission_score(aircraft, target, weather, time_of_day)
    rating = assign_mission_rating(dest_prob, civ_risk)
    
    print(f"\nMISSION ASSESSMENT:")
    print("="*40)
    print(f"Aircraft: {aircraft}")
    print(f"Target: {target.replace('_', ' ').title()}")
    print(f"Weather: {weather.replace('_', ' ').title()}")
    print(f"Time: {time_of_day.replace('_', ' ').title()}")
    print("-"*40)
    print(f"Success Probability: {dest_prob}%")
    print(f"Civilian Risk: {civ_risk}%")
    print(f"Mission Rating: {rating}")
    print("="*40)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_options()
    elif len(sys.argv) == 5:
        user_aircraft, user_target, user_weather, user_time = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
        
        # Validate and correct inputs
        validated = validate_inputs(user_aircraft, user_target, user_weather, user_time)
        
        if validated:
            aircraft, target, weather, time_of_day = validated
            assess_mission(aircraft, target, weather, time_of_day)
        else:
            print("\nUse 'python mission_planner.py' to see all available options")
    else:
        print("Error: Need exactly 4 parameters")
        show_options()