# Strike Mission Assessment System

#### Video Demo: https://www.youtube.com/watch?v=s91aLLvMv90
#### Name: Ioan Barber
#### GitHub Username: ioanb16
#### edX Username: ioanbarber
#### Location: UK
#### Date: 15/09/2025

#### Description:

The Strike Mission Assessment System is a comprehensive Python-based calculator designed to evaluate the viability of precision military strikes while prioritizing the minimization of collateral damage. This project was developed as my final project for CS50's Introduction to Programming with Python (CS50P), combining my passion for aerospace defense technology with ethical considerations in modern warfare.

## Personal Motivation

My interest in defense and aerospace stems from my family's military heritage and early exposure to the defense industry. My great-grandfather served in the First Parachute Regiment, my aunt served in the RAF, and my mother worked in the defense industry - I remember visiting her workplace as a child and being fascinated by the technology and precision involved. This early exposure, combined with video games and films that sparked my imagination about military aviation, cultivated a deep interest in aerospace defense technology.

Currently entering my third year of an integrated master's degree in mathematics, operations research, and statistics at Cardiff University, I'm passionate about problem-solving and optimization. I love the challenge of finding elegant solutions to complex problems, and I'm particularly fascinated by how mathematical precision and optimization can be applied to minimize harm while achieving military objectives. My goal is to work in the defense industry, applying these mathematical skills to real-world aerospace and defense challenges.

The recent precision strikes, such as the surgical operations against strategic targets using advanced platforms like B-2 stealth bombers, demonstrate that modern warfare increasingly demands mathematical precision rather than brute force. This project embodies that philosophy - if military action is necessary, it should be conducted with maximum precision and minimum collateral damage.

## Project Overview

In modern military operations, precision is paramount. The goal is not just to neutralize targets effectively, but to do so with minimal risk to civilian populations and infrastructure. This program addresses that challenge by providing a comprehensive assessment system that evaluates mission parameters and assigns ratings from S-Rank (excellent) to F-Rank (abort mission).

The system takes into account multiple critical factors:
- Aircraft capabilities including stealth characteristics and precision ratings
- Target type and difficulty level
- Weather conditions affecting precision
- Time of day and civilian activity patterns
- Blast radius and collateral damage calculations

## Features

### 1. Mission Assessment with Specific Aircraft
Users can select a specific aircraft and evaluate how it would perform against a chosen target under given conditions. The system provides detailed scoring and recommendations for improvement.

### 2. Aircraft Recommendation Engine
Given mission parameters (target, weather, timing), the system analyzes all available aircraft and recommends the optimal choice for maximum mission success with minimal civilian risk.

### 3. Aircraft Comparison Tool
Compare how different aircraft would perform for the same mission, displayed in an easy-to-read table format showing ratings, success probabilities, and civilian risk assessments.

### 4. Comprehensive Rating System

I chose an S-to-F ranking system because it's intuitive and widely recognized in modern culture, making the results easier to interpret than raw percentages. This familiar grading approach provides clear, actionable guidance:

- **S-Rank**: Perfect mission (>95% success, <5% civilian risk)
- **A-Rank**: Excellent mission (>85% success, <20% civilian risk)
- **B-Rank**: Good mission (>75% success, <40% civilian risk)
- **C-Rank**: Acceptable mission (>60% success, <60% civilian risk) - requires senior approval
- **D-Rank**: Poor mission (>40% success, <80% civilian risk) - not recommended
- **F-Rank**: Abort mission (unacceptable risk or failure probability)

## Aircraft Selection

I carefully selected nine aircraft based on a combination of personal interest, gaming nostalgia, and technical variety. The A-10 Warthog holds a special place in this collection - it's my personal favorite aircraft due to its distinctive and intimidating sound, and I wanted to include it before it's phased out of service. The AC-130 Gunship brings back memories from childhood gaming, particularly Call of Duty: Modern Warfare 3, where it was an iconic presence. Similarly, the A-10 featured memorably in Black Ops 2.

The remaining aircraft were chosen to provide comprehensive variety across generations and capabilities, while the NGAD-X represents something both exciting and somewhat unsettling - a glimpse into what the next generation of warfare technology might bring.

### Current Generation Stealth Fighters
- **B-2 Spirit**: Ultimate precision bomber with maximum stealth
- **F-22 Raptor**: Air superiority fighter with excellent precision
- **F-35A Lightning II**: Multi-role stealth fighter
- **Su-57 Felon**: Russian 5th-generation fighter

### Specialized Platforms
- **A-10 Warthog**: Close air support specialist with heavy payload
- **AC-130 Gunship**: Precision ground support with extended loiter capability

### Conventional Modern Fighters
- **F-15E Strike Eagle**: Proven heavy payload multirole fighter
- **Eurofighter Typhoon**: European collaborative fighter

### Next-Generation Technology
- **NGAD-X**: Projected 6th-generation fighter representing future capabilities based on the US Next Generation Air Dominance program

## File Structure

### project.py
The main program file containing all core functionality:

- **main()**: Primary interface with menu system allowing users to choose between assessment modes
- **assess_specific_mission()**: Handles user-selected aircraft mission evaluation
- **recommend_best_aircraft()**: Finds optimal aircraft for given mission parameters
- **compare_aircraft_options()**: Displays side-by-side aircraft performance comparison
- **calculate_mission_score()**: Core calculation engine that computes target destruction probability and civilian risk percentage based on aircraft precision, weather impact, target difficulty, and timing factors
- **assign_mission_rating()**: Converts numerical scores into letter ratings using predefined thresholds that heavily penalize high civilian risk
- **generate_mission_report()**: Creates detailed output reports with specific recommendations for mission improvement
- **find_optimal_aircraft()**: Analyzes all aircraft options and returns the best choice based on mission requirements

The file also contains selection functions that present options to users with clear descriptions and validate input, plus data functions that return specifications for aircraft, targets, weather conditions, and timing factors.

### test_project.py
Comprehensive test suite using pytest framework:

- **test_calculate_mission_score()**: Validates core calculation logic across various scenarios from optimal to worst-case
- **test_assign_mission_rating()**: Ensures rating assignments are correct across all rating levels and boundary conditions
- **test_find_optimal_aircraft()**: Tests the aircraft recommendation system with different mission parameters
- **test_data_functions()**: Validates data integrity and structure for all aircraft, targets, and environmental factors
- **test_get_civilian_risk_score()**: Tests risk level conversion functions
- **test_edge_cases()**: Handles boundary conditions and validates score ranges
- **test_mission_score_consistency()**: Ensures logical consistency in scoring (e.g., stealth aircraft have lower civilian risk)
- **test_specific_scenarios()**: Validates specific real-world scenarios

### requirements.txt
Lists the single external dependency: pytest for running the comprehensive test suite.

## Design Decisions

### Simplified Physics Model
While real ballistics calculations involve complex aerodynamic equations, I chose to use simplified mathematical models that capture the essential relationships between factors without overwhelming complexity. This keeps the project at an appropriate level for CS50P while still demonstrating the core concepts of multi-factor optimization.

### Conservative Rating System
The letter-grade rating system was designed to provide clear, actionable guidance while heavily prioritizing civilian safety. As technology advances, I believe we're moving beyond the era of the traditional foot soldier, yet we're still seeing tremendous loss of life in conflicts worldwide - both military and civilian casualties that could be prevented with better precision and planning.

While this might seem paradoxical given my passion for defense technology, I view advanced military capabilities primarily as deterrents rather than tools of destruction. The thresholds heavily penalize missions with high civilian risk because I believe that if military action becomes necessary, it should be conducted with surgical precision that minimizes all unnecessary loss of life. It's better to rate a potentially risky mission as lower quality and seek alternatives than to approve something that could cause preventable harm.

### User Interface Choice
I implemented a menu-driven command-line interface rather than a GUI to focus on the core algorithmic content while maintaining ease of use. The menu system is intuitive and allows for easy testing of different scenarios.

### Stealth Technology Modeling
Stealth aircraft receive bonuses not just for avoiding detection, but for reducing civilian panic and disruption. This reflects the reality that stealth operations can often be conducted with less collateral impact due to reduced enemy response and civilian evacuation.

### International Aircraft Selection
Including aircraft from different nations (US, European consortium, Russian) demonstrates the global nature of modern military aviation and provides interesting comparisons between different design philosophies and capabilities.

## Technical Implementation

### Calculation Algorithm
The core scoring algorithm combines multiple weighted factors:

1. **Base Precision**: Each aircraft has an inherent precision rating based on real-world capabilities
2. **Weather Impact**: Multiplier that reduces precision in poor conditions (storms reduce precision by 50%)
3. **Target Difficulty**: Harder targets reduce success probability based on structural complexity
4. **Civilian Risk Calculation**: Based on target location, timing, and aircraft stealth capabilities
5. **Time Modifiers**: Early morning operations have significantly lower civilian risk

### Rating Thresholds
The rating system uses conservative thresholds prioritizing civilian safety:
- Any mission with >80% civilian risk automatically receives F-Rank
- Any mission with <40% success probability automatically receives F-Rank
- S-Rank requires both very high success (>95%) and very low civilian risk (<5%)

## Educational Value

This project demonstrates several key programming concepts covered in CS50P:
- **Function design and modular programming**: Clear separation of concerns with focused functions
- **Data structures**: Effective use of dictionaries and lists for aircraft and mission data
- **User input validation and error handling**: Robust input validation with clear error messages
- **Mathematical calculations and algorithmic thinking**: Multi-factor optimization algorithms
- **Testing methodologies**: Comprehensive pytest suite with edge cases and boundary testing
- **Code organization and documentation**: Clear documentation and logical code structure

## Ethical Considerations

While this project deals with military applications, it was designed with a strong emphasis on minimizing harm. The rating system heavily penalizes missions with high civilian risk, and the optimization algorithms prioritize precision and safety over raw destructive power.

The system encourages operators to:
- Choose optimal timing to minimize civilian presence (early morning operations)
- Select appropriate aircraft and munitions for the specific target
- Consider weather conditions that might affect precision
- Abort missions that pose unacceptable risks to civilians

This promotes the concept of "precision warfare" - the idea that if military action is necessary, it should be conducted with maximum precision to minimize unintended consequences.

## Usage Examples

### Example 1: Optimal Mission
```
Aircraft: NGAD-X (6th Generation Fighter)
Target: Military Base
Weather: Clear
Time: Early Morning (02:00-06:00)

Result: S-RANK
- Target Destruction: 98.1%
- Civilian Risk: 4.9%
- Assessment: Excellent mission, minimal risk, maximum effectiveness
```

### Example 2: Problematic Mission
```
Aircraft: A-10 Warthog
Target: Nuclear Facility
Weather: Storm
Time: Afternoon (12:00-18:00)

Result: F-RANK
- Target Destruction: 22.5%
- Civilian Risk: 82.5%
- Assessment: Mission abort - unacceptable risk and low success probability
- Recommendations: Use stealth aircraft, wait for better weather, operate during early morning hours
```

## Future Enhancements

While this project meets the CS50P requirements, potential expansions could include:
- **Real-time data integration**: Weather APIs for current conditions
- **Advanced ballistics modeling**: More sophisticated physics calculations
- **Machine learning optimization**: AI-powered mission planning
- **Geographic information systems**: Terrain and population density factors
- **Economic analysis**: Cost-effectiveness calculations
- **Historical mission database**: Learning from past operations

## Installation and Usage

1. Clone or download the project files
2. Install requirements: `pip install -r requirements.txt`
3. Run the program: `python project.py`
4. Run tests: `pytest test_project.py`

The program features an intuitive menu system guiding users through aircraft selection, target selection, environmental conditions, and timing options.

## Acknowledgments

This project was inspired by my family's military service and my academic focus on mathematics and operations research. Special recognition to my great-grandfather who served in the First Parachute Regiment, my aunt who served in the RAF, and my mother who worked in defense contracting.

The project emphasizes that in modern warfare, precision and minimal collateral damage are not just tactical advantages, but moral imperatives. As demonstrated by recent precision strikes against strategic targets, the goal is always maximum effectiveness with minimum unintended consequences.

## Learning Outcomes

Through this project, I gained experience in:
- **Algorithm design**: Creating multi-factor optimization systems
- **User interface development**: Building intuitive command-line interfaces
- **Comprehensive testing**: Writing robust test suites with edge case coverage
- **Domain knowledge application**: Combining programming skills with aerospace defense knowledge
- **Ethical software design**: Considering moral implications in technical solutions
- **Professional documentation**: Creating detailed README files and comprehensive code documentation
- **Project presentation**: Learning to explain technical concepts clearly for different audiences

CS50P proved to be an excellent foundation for beginners, providing the programming fundamentals needed to tackle complex projects like this. The most challenging aspect of this project was knowing when to stop - there are countless additional features I wanted to implement, from real-time weather integration to advanced ballistics modeling, but learning to define and stick to project scope was an important lesson.

This project represents a significant step forward in my personal ambition of working in the defense industry. It demonstrates that I can combine technical programming skills with domain expertise and ethical consideration to create tools that could genuinely contribute to more precise and responsible military operations. The emphasis on minimizing civilian casualties while achieving military objectives reflects the values that should guide modern defense technology development.
