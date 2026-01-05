"""
Configuration for Multi-Disease Clinical Trial Dashboard
"""

# ========== DQI CALCULATION WEIGHTS ==========
DQI_WEIGHTS = {
    'visit_completion': 0.30,
    'query_resolution': 0.25,
    'data_quality': 0.20,
    'timeliness': 0.15,
    'safety': 0.10
}

# ========== THRESHOLDS FOR ALERTS ==========
THRESHOLDS = {
    'dqi_critical': 60,
    'dqi_warning': 75,
    'clean_patient_percentage': 70,
    'max_open_queries': 10,
    'max_missing_visits': 3
}

# ========== AVAILABLE THERAPEUTIC AREAS ==========
THERAPEUTIC_AREAS = {
    'oncology': {
        'name': 'Oncology',
        'description': 'Cancer Treatment Trials',
        'common_diseases': ['Breast Cancer', 'Lung Cancer', 'Colorectal Cancer', 'Prostate Cancer'],
        'icon': '🦠',
        'color': '#e63946'
    },
    'cardiology': {
        'name': 'Cardiology', 
        'description': 'Heart Disease Trials',
        'common_diseases': ['Hypertension', 'Coronary Artery Disease', 'Heart Failure', 'Arrhythmia'],
        'icon': '❤️',
        'color': '#e63946'
    },
    'endocrinology': {
        'name': 'Endocrinology',
        'description': 'Diabetes & Hormone Trials',
        'common_diseases': ['Type 2 Diabetes', 'Type 1 Diabetes', 'Obesity', 'Thyroid Disorders'],
        'icon': '🩺',
        'color': '#2a9d8f'
    },
    'neurology': {
        'name': 'Neurology',
        'description': 'Brain & Nervous System Trials',
        'common_diseases': ['Alzheimer\'s', 'Parkinson\'s', 'Multiple Sclerosis', 'Epilepsy'],
        'icon': '🧠',
        'color': '#264653'
    },
    'respiratory': {
        'name': 'Respiratory',
        'description': 'Lung Disease Trials',
        'common_diseases': ['Asthma', 'COPD', 'Pulmonary Fibrosis', 'Bronchitis'],
        'icon': '🌬️',
        'color': '#1d3557'
    },
    'immunology': {
        'name': 'Immunology',
        'description': 'Autoimmune Disease Trials',
        'common_diseases': ['Rheumatoid Arthritis', 'Lupus', 'Psoriasis', 'Crohn\'s Disease'],
        'icon': '🛡️',
        'color': '#7209b7'
    }
}

# ========== CLINICAL SITES ==========
SITES = [
    'Site_A_Delhi',
    'Site_B_Mumbai', 
    'Site_C_Chennai',
    'Site_D_Kolkata',
    'Site_E_Bangalore',
    'Site_F_Hyderabad',
    'Site_G_Pune',
    'Site_H_Ahmedabad'
]

# ========== REGIONS MAPPING ==========
REGIONS = {
    'Site_A_Delhi': 'North',
    'Site_B_Mumbai': 'West',
    'Site_C_Chennai': 'South',
    'Site_D_Kolkata': 'East',
    'Site_E_Bangalore': 'South',
    'Site_F_Hyderabad': 'South',
    'Site_G_Pune': 'West',
    'Site_H_Ahmedabad': 'West'
}

# ========== CLINICAL RESEARCH ASSOCIATES ==========
CRAS = [
    'CRA_John_Smith',
    'CRA_Sarah_Johnson',
    'CRA_Michael_Chen',
    'CRA_Priya_Sharma',
    'CRA_Robert_Davis',
    'CRA_Maria_Garcia',
    'CRA_David_Wilson',
    'CRA_Emma_Thompson'
]

# ========== ACTIVE TRIALS (DEMO DATA) ==========
ACTIVE_TRIALS = [
    {
        'trial_id': 'NOV-2024-001',
        'name': 'NovoCardio HTN Study',
        'phase': 'Phase 3',
        'therapeutic_area': 'cardiology',
        'disease': 'Hypertension',
        'start_date': '2024-01-15',
        'expected_end_date': '2025-12-31',
        'total_sites': 8,
        'target_patients': 400,
        'enrolled_patients': 325,
        'status': 'Active',
        'icon': '❤️'
    },
    {
        'trial_id': 'NOV-2024-002',
        'name': 'DiaCare Diabetes Trial',
        'phase': 'Phase 2',
        'therapeutic_area': 'endocrinology',
        'disease': 'Type 2 Diabetes',
        'start_date': '2024-03-01',
        'expected_end_date': '2026-02-28',
        'total_sites': 12,
        'target_patients': 600,
        'enrolled_patients': 480,
        'status': 'Active',
        'icon': '🩺'
    },
    {
        'trial_id': 'NOV-2024-003',
        'name': 'OncoBreast Study',
        'phase': 'Phase 3',
        'therapeutic_area': 'oncology',
        'disease': 'Breast Cancer',
        'start_date': '2023-11-01',
        'expected_end_date': '2025-10-31',
        'total_sites': 15,
        'target_patients': 800,
        'enrolled_patients': 720,
        'status': 'Active',
        'icon': '🦠'
    },
    {
        'trial_id': 'NOV-2024-004',
        'name': 'NeuroAlz Trial',
        'phase': 'Phase 2',
        'therapeutic_area': 'neurology',
        'disease': 'Alzheimer\'s Disease',
        'start_date': '2024-06-01',
        'expected_end_date': '2026-05-31',
        'total_sites': 10,
        'target_patients': 500,
        'enrolled_patients': 320,
        'status': 'Active',
        'icon': '🧠'
    },
    {
        'trial_id': 'NOV-2024-005',
        'name': 'RespiraCOPD Study',
        'phase': 'Phase 3',
        'therapeutic_area': 'respiratory',
        'disease': 'COPD',
        'start_date': '2024-02-01',
        'expected_end_date': '2026-01-31',
        'total_sites': 8,
        'target_patients': 450,
        'enrolled_patients': 380,
        'status': 'Active',
        'icon': '🌬️'
    },
    {
        'trial_id': 'NOV-2024-006',
        'name': 'ImmunoRA Trial',
        'phase': 'Phase 2',
        'therapeutic_area': 'immunology',
        'disease': 'Rheumatoid Arthritis',
        'start_date': '2024-04-15',
        'expected_end_date': '2026-04-14',
        'total_sites': 6,
        'target_patients': 300,
        'enrolled_patients': 220,
        'status': 'Active',
        'icon': '🛡️'
    }
]

# ========== DEFAULT TRIAL FOR DEMO ==========
DEFAULT_TRIAL = ACTIVE_TRIALS[0]  # Use first trial as default

# Add these configurations at the end of config.py:

# UI Theme Colors
THEME_COLORS = {
    'primary': "#0f2b78",
    'secondary': "#0A2848",
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': "#1da3b8",
    'light': '#f8f9fa',
    'dark': "#acb1b6",
}

# Therapeutic Areas for Disease Switcher
THERAPEUTIC_AREAS = {
    'Oncology': {
        'name': 'Oncology',
        'phase': 'Phase 3',
        'icon': '🩺',
        'color': '#dc3545',
        'description': 'Cancer Treatment Trials'
    },
    'Cardiology': {
        'name': 'Cardiology',
        'phase': 'Phase 2',
        'icon': '❤️',
        'color': '#dc3545',
        'description': 'Heart Disease Studies'
    },
    'Endocrinology': {
        'name': 'Endocrinology',
        'phase': 'Phase 3',
        'icon': '💉',
        'color': '#1f3c88',
        'description': 'Diabetes Treatment Trials'
    },
    'Neurology': {
        'name': 'Neurology',
        'phase': 'Phase 1',
        'icon': '🧠',
        'color': '#6f42c1',
        'description': 'Neurological Disorder Studies'
    }
}

# Default trial
DEFAULT_TRIAL = {
    'name': 'Clinical Intelligence Platform',
    'therapeutic_area': 'Oncology',  # FIXED: Must match THERAPEUTIC_AREAS keys
    'phase': 'Phase 3',
    'target_patients': 250,
    'total_sites': 5,
    'start_date': '2024-01-15',
    'expected_end_date': '2025-12-31'
}