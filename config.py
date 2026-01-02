"""
Configuration for Clinical Trial Dashboard
"""

# DQI Weights
DQI_WEIGHTS = {
    'visit_completion': 0.30,
    'query_resolution': 0.25,
    'data_quality': 0.20,
    'timeliness': 0.15,
    'safety': 0.10
}

# Thresholds
THRESHOLDS = {
    'dqi_critical': 60,
    'dqi_warning': 75,
    'clean_patient_percentage': 70,
    'max_open_queries': 10,
    'max_missing_visits': 3
}

# Sites
SITES = [
    'Site_A_Delhi',
    'Site_B_Mumbai', 
    'Site_C_Chennai',
    'Site_D_Kolkata',
    'Site_E_Bangalore'
]

# Regions
REGIONS = {
    'Site_A_Delhi': 'North',
    'Site_B_Mumbai': 'West',
    'Site_C_Chennai': 'South',
    'Site_D_Kolkata': 'East',
    'Site_E_Bangalore': 'South'
}

# CRAs
CRAS = [
    'CRA_John_Smith',
    'CRA_Sarah_Johnson',
    'CRA_Michael_Chen',
    'CRA_Priya_Sharma',
    'CRA_Robert_Davis'
]

# Trial Info - CORRECTED
TRIAL_INFO = {
    'name': 'Novartis Clinical Intelligence Platform',
    'phase': 'Phase 3',
    'therapeutic_area': 'Oncology',
    'start_date': '2024-01-15',
    'expected_end_date': '2025-12-31',
    'total_sites': 5,
    'target_patients': 250
}