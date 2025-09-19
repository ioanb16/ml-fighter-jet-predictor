"""
Test file for Strike Mission Assessment System
CS50P Final Project Tests
"""

import pytest
from project import (
    calculate_mission_score,
    assign_mission_rating,
    find_optimal_aircraft,
    get_aircraft_data,
    get_target_data,
    get_weather_data,
    get_civilian_risk_score
)


def test_calculate_mission_score():
    """Test mission score calculations"""
    # Test that function returns valid ranges
    dest_prob, civ_risk = calculate_mission_score("B-2", "wooden_house", "clear", "early_morning")
    assert 0 <= dest_prob <= 100
    assert 0 <= civ_risk <= 100

    dest_prob, civ_risk = calculate_mission_score("Eurofighter", "nuclear_facility", "storm", "afternoon")
    assert 0 <= dest_prob <= 100
    assert 0 <= civ_risk <= 100

    dest_prob, civ_risk = calculate_mission_score("F-35A", "military_base", "light_rain", "night")
    assert 0 <= dest_prob <= 100
    assert 0 <= civ_risk <= 100


def test_assign_mission_rating():
    """Test mission rating assignment"""
    # Test S-Rank (perfect mission)
    assert assign_mission_rating(98.0, 2.0) == "S-RANK"

    # Test A-Rank (very good mission)
    assert assign_mission_rating(90.0, 10.0) == "A-RANK"

    # Test B-Rank (good mission)
    assert assign_mission_rating(85.0, 25.0) == "B-RANK"

    # Test C-Rank (acceptable mission)
    assert assign_mission_rating(75.0, 45.0) == "C-RANK"

    # Test D-Rank (poor mission)
    assert assign_mission_rating(65.0, 65.0) == "D-RANK"

    # Test F-Rank (abort mission)
    assert assign_mission_rating(30.0, 85.0) == "F-RANK"
    assert assign_mission_rating(95.0, 85.0) == "F-RANK"  # High civilian risk
    assert assign_mission_rating(30.0, 10.0) == "F-RANK"  # Low success rate


def test_find_optimal_aircraft():
    """Test aircraft recommendation system"""
    # Test easy target with clear weather - should recommend high precision aircraft
    best_aircraft, best_rating, all_results = find_optimal_aircraft("wooden_house", "clear", "early_morning")

    # Should get a good rating
    assert best_rating in ["S-RANK", "A-RANK", "B-RANK"]

    # Should return results for all aircraft
    aircraft_data = get_aircraft_data()
    assert len(all_results) == len(aircraft_data)

    # Best aircraft should be one with high precision (but now considers practical factors)
    assert best_aircraft in ["B-2", "F-35A", "F-22", "NGAD-X", "A-10"]  # A-10 might win for soft targets now

    # Test difficult conditions - should still return a recommendation
    best_aircraft, best_rating, all_results = find_optimal_aircraft("nuclear_facility", "storm", "afternoon")
    assert best_aircraft is not None
    assert best_rating in ["S-RANK", "A-RANK", "B-RANK", "C-RANK", "D-RANK", "F-RANK"]


def test_data_functions():
    """Test data integrity"""
    # Test aircraft data
    aircraft_data = get_aircraft_data()
    assert len(aircraft_data) > 0
    for aircraft, specs in aircraft_data.items():
        assert "precision" in specs
        assert "payload" in specs
        assert "stealth" in specs
        assert 0 <= specs["precision"] <= 100
        assert isinstance(specs["stealth"], bool)

    # Test target data
    target_data = get_target_data()
    assert len(target_data) > 0
    for target, specs in target_data.items():
        assert "difficulty" in specs
        assert "civilian_risk" in specs
        assert 1 <= specs["difficulty"] <= 10
        assert specs["civilian_risk"] in ["very_low", "low", "medium", "high", "very_high"]

    # Test weather data
    weather_data = get_weather_data()
    assert len(weather_data) > 0
    for weather, specs in weather_data.items():
        assert "precision_modifier" in specs
        assert 0.0 <= specs["precision_modifier"] <= 1.0


def test_get_civilian_risk_score():
    """Test civilian risk score conversion"""
    assert get_civilian_risk_score("very_low") == 5
    assert get_civilian_risk_score("low") == 15
    assert get_civilian_risk_score("medium") == 35
    assert get_civilian_risk_score("high") == 55
    assert get_civilian_risk_score("very_high") == 75
    assert get_civilian_risk_score("invalid") == 50  # Default value


def test_edge_cases():
    """Test edge cases and boundary conditions"""
    # Test with all aircraft types
    aircraft_data = get_aircraft_data()
    for aircraft in aircraft_data.keys():
        dest_prob, civ_risk = calculate_mission_score(aircraft, "military_base", "clear", "night")
        assert 0 <= dest_prob <= 100
        assert 0 <= civ_risk <= 100

    # Test rating functions return valid ratings
    assert assign_mission_rating(30.0, 50.0) in ["S-RANK", "A-RANK", "B-RANK", "C-RANK", "D-RANK", "F-RANK"]
    assert assign_mission_rating(50.0, 90.0) in ["S-RANK", "A-RANK", "B-RANK", "C-RANK", "D-RANK", "F-RANK"]
    assert assign_mission_rating(80.0, 10.0) in ["S-RANK", "A-RANK", "B-RANK", "C-RANK", "D-RANK", "F-RANK"]


def test_mission_score_consistency():
    """Test that mission scores are consistent and logical"""
    # Stealth aircraft should generally have lower civilian risk
    stealth_dest, stealth_civ = calculate_mission_score("F-35A", "military_base", "clear", "afternoon")
    non_stealth_dest, non_stealth_civ = calculate_mission_score("F-15E", "military_base", "clear", "afternoon")

    # Stealth should have lower civilian risk
    assert stealth_civ <= non_stealth_civ

    # Better weather should improve destruction probability
    clear_dest, _ = calculate_mission_score("F-35A", "military_base", "clear", "night")
    storm_dest, _ = calculate_mission_score("F-35A", "military_base", "storm", "night")
    assert clear_dest > storm_dest

    # Early morning should have lower civilian risk than afternoon
    morning_dest, morning_civ = calculate_mission_score("F-35A", "military_base", "clear", "early_morning")
    afternoon_dest, afternoon_civ = calculate_mission_score("F-35A", "military_base", "clear", "afternoon")
    assert morning_civ < afternoon_civ


def test_specific_scenarios():
    """Test specific scenarios based on debug output"""
    # Test B-2 with wooden house - should get A-RANK (90.2%, 10.5%)
    dest_prob, civ_risk = calculate_mission_score("B-2", "wooden_house", "clear", "early_morning")
    rating = assign_mission_rating(dest_prob, civ_risk)
    assert rating == "A-RANK"  # Based on debug output

    # Test Eurofighter with nuclear facility - should get F-RANK
    dest_prob, civ_risk = calculate_mission_score("Eurofighter", "nuclear_facility", "storm", "afternoon")
    rating = assign_mission_rating(dest_prob, civ_risk)
    assert rating == "F-RANK"  # Based on debug output

    # Test F-35A with military base - should get D-RANK
    dest_prob, civ_risk = calculate_mission_score("F-35A", "military_base", "light_rain", "night")
    rating = assign_mission_rating(dest_prob, civ_risk)
    assert rating == "D-RANK"  # Based on debug output


def test_new_aircraft():
    """Test that new aircraft are included properly"""
    aircraft_data = get_aircraft_data()

    # Test that all 9 aircraft are present
    expected_aircraft = ["B-2", "A-10", "AC-130", "Su-57", "Eurofighter", "F-22", "F-15E", "F-35A", "NGAD-X"]
    assert len(aircraft_data) == 9

    for aircraft in expected_aircraft:
        assert aircraft in aircraft_data

    # Test NGAD-X has highest precision
    assert aircraft_data["NGAD-X"]["precision"] == 99

    # Test A-10 has appropriate specs
    assert aircraft_data["A-10"]["precision"] == 75
    assert aircraft_data["A-10"]["payload"] == "heavy"
    assert aircraft_data["A-10"]["stealth"] == False


def test_realistic_aircraft_selection():
    """Test that aircraft selection considers practical factors"""
    # For a simple target, practical aircraft should be recommended
    best_aircraft, best_rating, all_results = find_optimal_aircraft("warehouse", "clear", "night")

    # Should consider practical factors, not just raw performance
    # Check that the recommendation makes sense
    assert best_aircraft in ["A-10", "F-35A", "F-15E", "AC-130", "Eurofighter", "Su-57"]  # Practical choices

    # For hardened targets, should still prefer capable aircraft
    best_aircraft, best_rating, all_results = find_optimal_aircraft("concrete_bunker", "clear", "early_morning")

    # Should prefer aircraft suitable for hardened targets
    aircraft_data = get_aircraft_data()
    recommended_specs = aircraft_data[best_aircraft]
    # Should be either high precision OR heavy payload (or both)
    assert recommended_specs["precision"] >= 80 or recommended_specs["payload"] in ["heavy", "very_heavy"]


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__])
