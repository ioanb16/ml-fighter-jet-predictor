Fighter Jet Mission Assessment: Rule-Based to Machine Learning
Author: Ioan Barber
Cardiff University - Mathematics, Operations Research & Statistics

Overview
This project transforms my CS50P final project (a rule-based fighter jet mission calculator) into a machine learning system. It demonstrates the evolution from algorithmic thinking to AI applications for defense/aerospace roles.

Original System: Rule-based calculator that evaluates fighter jet missions
New Goal: Convert to supervised learning, then advanced ML techniques

What It Does
Assesses fighter jet mission viability by predicting:

Target destruction probability
Civilian risk percentage
Mission rating (S-Rank to F-Rank)
Based on:

Aircraft type (9 options: F-35A, B-2, A-10, etc.)
Target difficulty (7 categories: bunkers, bases, facilities)
Weather conditions
Time of day
Project Phases
Phase 1: ML Foundation (Current)
Generate training data from rule-based system
Build regression models for success/risk prediction
Compare ML vs rule-based performance
Phase 2: Feature Engineering
Advanced feature interactions
Hyperparameter optimization
Multi-output models
Phase 3: Domain Enhancement
Real military factors (munitions, range, defenses)
Economic constraints
Operational limitations
Phase 4: Advanced AI
Computer vision for target recognition
Reinforcement learning for optimization
Interactive mission planning interface
Technical Stack
Current: Python, pytest
Phase 1: scikit-learn, pandas, matplotlib
Later Phases: TensorFlow/PyTorch, OpenCV, Streamlit



# Run original system
cd projectV1
python project.py
pytest test_project.py
Goals
Demonstrate algorithmic → AI progression
Build portfolio piece for defense/aerospace roles
Maintain ethical focus on precision warfare and civilian safety
Create production-ready ML system
This project emphasizes precision over destructive power, reflecting modern defense industry values where mathematical optimization minimizes collateral damage while achieving military objectives.

