
def main():
    """Main program interface"""
    print("=" * 60)
    print("STRIKE MISSION ASSESSMENT SYSTEM")
    print("=" * 60)
    print()

    while True:
        print("Select an option:")
        print("1. Assess Mission with Specific Aircraft")
        print("2. Compare Aircraft Options")
        print("3. Exit")

        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "1":
            assess_specific_mission()
        elif choice == "2":
            compare_aircraft_options()
        elif choice == "3":
            print("Mission planning complete. Stay safe out there.")
            break
        else:
            print("Invalid choice. Please enter 1-3.")

        print("\n" + "-" * 60 + "\n")


def assess_specific_mission():
    """Assess a mission with user-selected aircraft"""
    print("\n=== MISSION ASSESSMENT ===")

    # Get user selections
    aircraft = select_aircraft()
    target = select_target()
    weather = select_weather()
    time_of_day = select_time()

    # Calculate mission scores
    destruction_prob, civilian_risk = calculate_mission_score(aircraft, target, weather, time_of_day)

    # Get mission rating
    rating = assign_mission_rating(destruction_prob, civilian_risk)

    # Generate and display report
    generate_mission_report(aircraft, target, weather, time_of_day, destruction_prob, civilian_risk, rating)


def compare_aircraft_options():
    """Compare all aircraft for a specific mission"""
    print("\n=== AIRCRAFT COMPARISON ===")

    target = select_target()
    weather = select_weather()
    time_of_day = select_time()

    print(f"\nMission Parameters:")
    print(f"Target: {target.replace('_', ' ').title()}")
    print(f"Weather: {weather.replace('_', ' ').title()}")
    print(f"Time: {time_of_day.replace('_', ' ').title()}")

    # Add mission difficulty assessment
    target_data = get_target_data()
    target_specs = target_data[target]
    print(f"Target Difficulty: {target_specs['difficulty']}/10")
    print(f"Civilian Risk Level: {target_specs['civilian_risk'].replace('_', ' ').title()}")

    print("\nAircraft Comparison:")
    print("-" * 90)
    print(f"{'Aircraft':<12} {'Rating':<8} {'Target %':<10} {'Civ Risk %':<12} {'Best For':<25}")
    print("-" * 90)

    aircraft_data = get_aircraft_data()
    target_data = get_target_data()
    target_specs = target_data[target]

    for aircraft_name in aircraft_data.keys():
        dest_prob, civ_risk = calculate_mission_score(aircraft_name, target, weather, time_of_day)
        rating = assign_mission_rating(dest_prob, civ_risk)

        # Smart contextual notes
        specs = aircraft_data[aircraft_name]
        if specs["stealth"] and target_specs["civilian_risk"] in ["high", "very_high"]:
            context = "Stealth advantage"
        elif target_specs["difficulty"] >= 7 and specs["payload"] in ["heavy", "very_heavy"]:
            context = "Heavy payload suitable"
        elif specs["precision"] >= 95:
            context = "High precision"
        elif aircraft_name == "A-10" and target_specs["difficulty"] <= 3:
            context = "Good for soft targets"
        elif aircraft_name == "AC-130" and target_specs["civilian_risk"] == "low":
            context = "Extended loiter time"
        else:
            context = get_aircraft_notes(aircraft_name, rating)

        print(f"{aircraft_name:<12} {rating:<8} {dest_prob:<10.1f} {civ_risk:<12.1f} {context:<25}")


def select_aircraft():
    """Display aircraft options and get user selection"""
    aircraft_data = get_aircraft_data()

    print("\nAvailable Aircraft:")
    for i, (name, specs) in enumerate(aircraft_data.items(), 1):
        stealth_str = "Stealth" if specs["stealth"] else "Non-stealth"
        print(f"{i}. {name} - Precision: {specs['precision']}%, Payload: {specs['payload']}, {stealth_str}")

    while True:
        try:
            choice = int(input("\nSelect aircraft (number): "))
            aircraft_list = list(aircraft_data.keys())
            if 1 <= choice <= len(aircraft_list):
                return aircraft_list[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def select_target():
    """Display target options and get user selection"""
    target_data = get_target_data()

    print("\nAvailable Targets:")
    for i, (name, specs) in enumerate(target_data.items(), 1):
        print(f"{i}. {name.replace('_', ' ').title()} - Difficulty: {specs['difficulty']}/10, Civilian Risk: {specs['civilian_risk']}")

    while True:
        try:
            choice = int(input("\nSelect target (number): "))
            target_list = list(target_data.keys())
            if 1 <= choice <= len(target_list):
                return target_list[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def select_weather():
    """Display weather options and get user selection"""
    weather_data = get_weather_data()

    print("\nWeather Conditions:")
    for i, (condition, specs) in enumerate(weather_data.items(), 1):
        impact = "No impact" if specs["precision_modifier"] == 1.0 else f"{int((1-specs['precision_modifier'])*100)}% precision reduction"
        print(f"{i}. {condition.replace('_', ' ').title()} - {impact}")

    while True:
        try:
            choice = int(input("\nSelect weather (number): "))
            weather_list = list(weather_data.keys())
            if 1 <= choice <= len(weather_list):
                return weather_list[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def select_time():
    """Display time options and get user selection"""
    time_options = {
        "early_morning": {"civilian_modifier": 0.2, "description": "02:00-06:00 (Minimal civilian activity)"},
        "morning": {"civilian_modifier": 0.7, "description": "06:00-12:00 (Moderate civilian activity)"},
        "afternoon": {"civilian_modifier": 1.0, "description": "12:00-18:00 (High civilian activity)"},
        "evening": {"civilian_modifier": 0.8, "description": "18:00-22:00 (Moderate civilian activity)"},
        "night": {"civilian_modifier": 0.4, "description": "22:00-02:00 (Low civilian activity)"}
    }

    print("\nTime of Day:")
    for i, (time_key, specs) in enumerate(time_options.items(), 1):
        print(f"{i}. {specs['description']}")

    while True:
        try:
            choice = int(input("\nSelect time (number): "))
            time_list = list(time_options.keys())
            if 1 <= choice <= len(time_list):
                return time_list[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def calculate_mission_score(aircraft, target, weather, time_of_day):
    """
    Calculate target destruction probability and civilian risk percentage

    Args:
        aircraft (str): Selected aircraft type
        target (str): Target type
        weather (str): Weather conditions
        time_of_day (str): Time of operation

    Returns:
        tuple: (destruction_probability, civilian_risk_percentage)
    """
    aircraft_data = get_aircraft_data()
    target_data = get_target_data()
    weather_data = get_weather_data()
    time_data = get_time_data()

    # Base aircraft precision
    base_precision = aircraft_data[aircraft]["precision"]

    # Weather impact on precision
    weather_modifier = weather_data[weather]["precision_modifier"]

    # Target difficulty impact
    target_difficulty = target_data[target]["difficulty"]
    difficulty_modifier = max(0.3, 1.0 - (target_difficulty * 0.08))  # Harder targets reduce success

    # Calculate destruction probability
    destruction_prob = min(99.9, base_precision * weather_modifier * difficulty_modifier)

    # Calculate civilian risk
    base_civilian_risk = get_civilian_risk_score(target_data[target]["civilian_risk"])
    time_modifier = time_data[time_of_day]["civilian_modifier"]
    stealth_modifier = 0.7 if aircraft_data[aircraft]["stealth"] else 1.0  # Stealth reduces detection/civilian panic

    civilian_risk = min(95.0, base_civilian_risk * time_modifier * stealth_modifier)

    return round(destruction_prob, 1), round(civilian_risk, 1)


def assign_mission_rating(destruction_prob, civilian_risk):
    """
    Assign mission rating based on destruction probability and civilian risk

    Args:
        destruction_prob (float): Target destruction probability percentage
        civilian_risk (float): Civilian risk percentage

    Returns:
        str: Mission rating (S, A, B, C, D, F)
    """
    # F-Rank: Unacceptable civilian risk or very low success
    if civilian_risk > 80 or destruction_prob < 40:
        return "F-RANK"

    # D-Rank: High civilian risk or low success
    if civilian_risk > 60 or destruction_prob < 60:
        return "D-RANK"

    # C-Rank: Moderate risk, acceptable success
    if civilian_risk > 40 or destruction_prob < 75:
        return "C-RANK"

    # B-Rank: Low risk, good success
    if civilian_risk > 20 or destruction_prob < 85:
        return "B-RANK"

    # A-Rank: Very low risk, high success
    if civilian_risk > 5 or destruction_prob < 95:
        return "A-RANK"

    # S-Rank: Minimal risk, near-perfect success
    return "S-RANK"


def generate_mission_report(aircraft, target, weather, time_of_day, destruction_prob, civilian_risk, rating):
    """Generate detailed mission assessment report"""
    print("\n" + "=" * 60)
    print("MISSION ASSESSMENT REPORT")
    print("=" * 60)
    print(f"Aircraft: {aircraft}")
    print(f"Target: {target.replace('_', ' ').title()}")
    print(f"Weather: {weather.replace('_', ' ').title()}")
    print(f"Time: {time_of_day.replace('_', ' ').title()}")
    print("-" * 60)
    print(f"Target Destruction Probability: {destruction_prob}%")
    print(f"Civilian Risk Assessment: {civilian_risk}%")
    print(f"OVERALL MISSION RATING: {rating}")
    print("-" * 60)

    # Add rating explanation
    rating_explanations = {
        "S-RANK": "EXCELLENT - Mission approved. Minimal risk, maximum effectiveness.",
        "A-RANK": "VERY GOOD - Mission approved. Low risk, high effectiveness.",
        "B-RANK": "GOOD - Mission approved. Acceptable risk levels.",
        "C-RANK": "ACCEPTABLE - Requires senior approval. Moderate risk.",
        "D-RANK": "POOR - Mission not recommended. High risk or low effectiveness.",
        "F-RANK": "ABORT - Mission rejected. Unacceptable risk or failure probability."
    }

    print(f"Assessment: {rating_explanations[rating]}")

    # Add recommendations if rating is poor
    if rating in ["C-RANK", "D-RANK", "F-RANK"]:
        print("\nRECOMMENDATIONS FOR IMPROVEMENT:")
        if civilian_risk > 40:
            print("- Consider operating during early morning hours (02:00-06:00)")
            print("- Use stealth aircraft to reduce civilian panic")
        if destruction_prob < 80:
            # Only suggest better weather if current weather isn't already clear
            if weather != "clear":
                print("- Wait for better weather conditions")

            # Smart aircraft recommendations based on current selection
            aircraft_data = get_aircraft_data()
            current_precision = aircraft_data[aircraft]["precision"]
            current_payload = aircraft_data[aircraft]["payload"]

            # Only suggest higher precision if not already using the most precise
            if current_precision < 98:  # B-2 and NGAD-X are highest precision
                print("- Consider using higher-precision aircraft")

            # For hardened targets, suggest heavy payload if not already using one
            if target in ["nuclear_facility", "concrete_bunker"]:
                if current_payload not in ["heavy", "very_heavy"]:
                    print("- Consider using heavier payload aircraft or specialized bunker-buster munitions")
                else:
                    print("- Target is extremely hardened - even heavy munitions have limited effectiveness")
                    print("- Consider multiple coordinated strikes or alternative objectives")


def find_optimal_aircraft(target, weather, time_of_day):
    """
    Find the best aircraft for given mission parameters

    Returns:
        tuple: (best_aircraft_name, best_rating, all_results_dict)
    """
    aircraft_data = get_aircraft_data()
    target_data = get_target_data()
    results = {}
    best_score = -1
    best_aircraft = None
    best_rating = None

    rating_scores = {"S-RANK": 6, "A-RANK": 5, "B-RANK": 4, "C-RANK": 3, "D-RANK": 2, "F-RANK": 1}

    for aircraft_name in aircraft_data.keys():
        dest_prob, civ_risk = calculate_mission_score(aircraft_name, target, weather, time_of_day)
        rating = assign_mission_rating(dest_prob, civ_risk)
        results[aircraft_name] = (rating, dest_prob, civ_risk)

        # Smart scoring: consider both rating and aircraft suitability
        base_score = rating_scores[rating]

        # Realistic limitations for B-2
        if aircraft_name == "B-2":
            # B-2 is expensive and rare - penalize for routine targets
            if target in ["wooden_house", "warehouse"]:
                base_score -= 2  # Overkill for simple targets
            # B-2 has limited availability
            base_score -= 0.5  # Always slightly penalize due to scarcity

        # NGAD-X is experimental - penalize for reliability
        if aircraft_name == "NGAD-X":
            base_score -= 1  # Experimental platform risk

        # Bonus for appropriate aircraft-target matching
        aircraft_specs = aircraft_data[aircraft_name]
        target_specs = target_data[target]

        # A-10 excels at soft targets
        if aircraft_name == "A-10" and target_specs["difficulty"] <= 3:
            base_score += 1

        # AC-130 excels at extended operations
        if aircraft_name == "AC-130" and target_specs["civilian_risk"] == "low":
            base_score += 0.8

        # F-15E and F-35A are reliable workhorses
        if aircraft_name in ["F-15E", "F-35A"] and target_specs["difficulty"] in [4, 5, 6]:
            base_score += 0.5

        # Stealth bonus for high civilian risk targets
        if target_specs["civilian_risk"] in ["high", "very_high"] and aircraft_specs["stealth"]:
            base_score += 0.5

        # Payload bonus for difficult targets
        if target_specs["difficulty"] >= 7:
            if aircraft_specs["payload"] in ["heavy", "very_heavy"]:
                base_score += 0.3

        # Precision bonus for hardened targets
        if target_specs["difficulty"] >= 8 and aircraft_specs["precision"] >= 95:
            base_score += 0.2

        if base_score > best_score:
            best_score = base_score
            best_aircraft = aircraft_name
            best_rating = rating

    return best_aircraft, best_rating, results


# Data functions
def get_aircraft_data():
    """Return aircraft specifications"""
    return {
        "B-2": {"precision": 98, "payload": "very_heavy", "stealth": True},
        "A-10": {"precision": 75, "payload": "heavy", "stealth": False},
        "AC-130": {"precision": 88, "payload": "very_heavy", "stealth": False},
        "Su-57": {"precision": 90, "payload": "medium", "stealth": True},
        "Eurofighter": {"precision": 85, "payload": "medium", "stealth": False},
        "F-22": {"precision": 95, "payload": "light", "stealth": True},
        "F-15E": {"precision": 85, "payload": "heavy", "stealth": False},
        "F-35A": {"precision": 95, "payload": "medium", "stealth": True},
        "NGAD-X": {"precision": 99, "payload": "medium", "stealth": True}
    }


def get_target_data():
    """Return target specifications"""
    return {
        "wooden_house": {"difficulty": 1, "civilian_risk": "very_high"},
        "concrete_bunker": {"difficulty": 8, "civilian_risk": "low"},
        "nuclear_facility": {"difficulty": 9, "civilian_risk": "very_high"},
        "military_base": {"difficulty": 6, "civilian_risk": "medium"},
        "bridge": {"difficulty": 4, "civilian_risk": "low"},
        "command_center": {"difficulty": 7, "civilian_risk": "medium"},
        "warehouse": {"difficulty": 3, "civilian_risk": "high"}
    }


def get_weather_data():
    """Return weather impact data"""
    return {
        "clear": {"precision_modifier": 1.0},
        "light_rain": {"precision_modifier": 0.9},
        "heavy_rain": {"precision_modifier": 0.7},
        "windy": {"precision_modifier": 0.85},
        "storm": {"precision_modifier": 0.5},
        "fog": {"precision_modifier": 0.6}
    }


def get_time_data():
    """Return time of day impact data"""
    return {
        "early_morning": {"civilian_modifier": 0.2},
        "morning": {"civilian_modifier": 0.7},
        "afternoon": {"civilian_modifier": 1.0},
        "evening": {"civilian_modifier": 0.8},
        "night": {"civilian_modifier": 0.4}
    }


def get_civilian_risk_score(risk_level):
    """Convert risk level to numerical score"""
    risk_mapping = {
        "very_low": 5,
        "low": 15,
        "medium": 35,
        "high": 55,
        "very_high": 75
    }
    return risk_mapping.get(risk_level, 50)


def get_aircraft_notes(aircraft, rating):
    """Get brief notes about aircraft performance"""
    aircraft_data = get_aircraft_data()
    specs = aircraft_data[aircraft]

    if rating in ["S-RANK", "A-RANK"]:
        if specs["stealth"]:
            return "Excellent/stealth"
        else:
            return "Excellent choice"
    elif rating == "B-RANK":
        if specs["precision"] >= 90:
            return "Good/high precision"
        else:
            return "Good option"
    elif rating == "C-RANK":
        if specs["stealth"]:
            return "Consider alternatives"
        else:
            return "Risky/non-stealth"
    else:
        if specs["precision"] < 80:
            return "Low precision"
        else:
            return "Not recommended"


if __name__ == "__main__":
    main()
