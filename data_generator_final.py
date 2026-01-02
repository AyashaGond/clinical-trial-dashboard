import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


def create_clean_patient(patient_id, site):
    """Create a guaranteed clean patient"""
    from config import REGIONS, CRAS
    from datetime import datetime, timedelta
    
    return {
        'patient_id': patient_id,
        'subject_id': f'SUB{random.randint(1000, 9999)}',
        'site_id': site,
        'region': REGIONS[site],
        'cra_assigned': random.choice(CRAS),
        'subject_status': 'Active',
        'enrollment_date': (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d'),
        'last_visit_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        
        # PERFECT DATA - ALL CLEAN CONDITIONS MET
        'total_visits_expected': 12,
        'visits_completed': 12,        # All visits done
        'missing_visits': 0,           # ✅ NO missing visits
        'total_pages_expected': 85,
        'pages_completed': 85,         # All pages done
        'missing_pages': 0,            # ✅ NO missing pages
        'total_queries': 0,            # ✅ NO queries at all
        'open_queries': 0,             # ✅ NO open queries
        'queries_resolved': 0,
        'non_conformant_data': 0,      # ✅ NO data errors
        'data_entry_errors': 0,
        'lab_issues': 0,               # ✅ NO lab issues
        'safety_issues': 0,            # ✅ NO safety issues
        'adverse_events': 0,           # ✅ NO adverse events
        'serious_adverse_events': 0,
        'forms_verified': True,        # ✅ Forms verified
        'forms_signed': True,          # ✅ Forms signed
        'sdv_completed': True,         # ✅ SDV completed
        'frozen_locked': True,         # ✅ Forms locked
        'coding_backlog': 0,
        'overdue_crfs': 0,             # ✅ NO overdue
        'protocol_deviations': 0,      # ✅ NO deviations
        'screen_failure': False,
        'early_termination': False,
    }


def generate_final_data():
    """Generate complete dataset with all required columns"""
    
    print("Generating complete clinical trial dataset...")
    
    # Create directories
    import os
    os.makedirs('data', exist_ok=True)
    
    # 1. PATIENT DATA (250 patients)
    sites = ['Site_A_Delhi', 'Site_B_Mumbai', 'Site_C_Chennai', 'Site_D_Kolkata', 'Site_E_Bangalore']
    patients = []
    
    for i in range(1, 251):
        site = random.choice(sites)
        is_clean = random.random() < 0.40  # 30% clean
        
        patient = {
            'patient_id': f'P{str(i).zfill(3)}',
            'site_id': site,
            'subject_status': random.choice(['Active', 'Completed']),
            'clean_status': 'Clean' if is_clean else 'Not Clean',
            'dqi_score': random.randint(85, 100) if is_clean else random.randint(40, 75),
            'risk_level': 'Low' if is_clean else random.choice(['Medium', 'High']),
            'missing_visits': 0 if is_clean else random.randint(1, 4),
            'open_queries': 0 if is_clean else random.randint(1, 5),
            'safety_issues': 0 if is_clean else random.randint(0, 2),
            'adverse_events': random.randint(0, 1),
            'forms_verified': is_clean,
            'forms_signed': is_clean,
            'visits_completed': 12 if is_clean else random.randint(6, 11),
            'total_queries': random.randint(0, 3) if is_clean else random.randint(3, 12),
            'queries_resolved': 0,  # Will calculate below
            'non_conformant_data': 0 if is_clean else random.randint(1, 4),
            'enrollment_date': (datetime.now() - timedelta(days=random.randint(50, 200))).strftime('%Y-%m-%d'),
        }
        
        # Calculate resolved queries
        patient['queries_resolved'] = patient['total_queries'] - patient['open_queries']
        patients.append(patient)
    
    patient_df = pd.DataFrame(patients)
    patient_df.to_csv('data/patients.csv', index=False)
    print(f"✅ Patients: {len(patient_df)}")
    
    # 2. SITE DATA
    site_data = []
    for site in sites:
        site_patients = patient_df[patient_df['site_id'] == site]
        
        site_info = {
            'site_id': site,
            'site_name': site.replace('_', ' '),
            'total_patients_enrolled': len(site_patients),
            'clean_percentage': (len(site_patients[site_patients['clean_status'] == 'Clean']) / len(site_patients) * 100),
            'avg_dqi': site_patients['dqi_score'].mean(),
            'total_open_queries': site_patients['open_queries'].sum(),
            'total_safety_issues': site_patients['safety_issues'].sum(),
            'performance_status': 'Good' if site_patients['dqi_score'].mean() >= 75 else ('Warning' if site_patients['dqi_score'].mean() >= 60 else 'Critical')
        }
        site_data.append(site_info)
    
    site_df = pd.DataFrame(site_data)
    site_df.to_csv('data/sites.csv', index=False)
    print(f"✅ Sites: {len(site_df)}")
    
    # 3. QUERY DATA (with query_age_days)
    query_types = ['Data Entry Error', 'Missing Value', 'Protocol Deviation', 'Safety Concern']
    queries = []
    query_id = 1
    
    for _, patient in patient_df.iterrows():
        if patient['open_queries'] > 0:
            for _ in range(patient['open_queries']):
                query_date = datetime.strptime(patient['enrollment_date'], '%Y-%m-%d') + \
                            timedelta(days=random.randint(0, 100))
                
                age_days = (datetime.now() - query_date).days
                
                query = {
                    'query_id': f'Q{str(query_id).zfill(5)}',
                    'patient_id': patient['patient_id'],
                    'site_id': patient['site_id'],
                    'query_type': random.choice(query_types),
                    'query_priority': random.choice(['Low', 'Medium', 'High']),
                    'query_status': 'Open',
                    'query_created_date': query_date.strftime('%Y-%m-%d'),
                    'query_age_days': age_days,  # CRITICAL COLUMN
                    'assigned_to': f'CRA_{random.randint(1, 5)}',
                    'expected_resolution_date': (query_date + timedelta(days=random.randint(7, 30))).strftime('%Y-%m-%d'),
                }
                queries.append(query)
                query_id += 1
    
    # Add some resolved queries
    for _ in range(50):
        patient = random.choice(patients)
        query_date = datetime.strptime(patient['enrollment_date'], '%Y-%m-%d') + \
                    timedelta(days=random.randint(0, 150))
        
        age_days = (datetime.now() - query_date).days
        
        query = {
            'query_id': f'Q{str(query_id).zfill(5)}',
            'patient_id': patient['patient_id'],
            'site_id': patient['site_id'],
            'query_type': random.choice(query_types),
            'query_priority': random.choice(['Low', 'Medium']),
            'query_status': 'Resolved',
            'query_created_date': query_date.strftime('%Y-%m-%d'),
            'query_resolved_date': (query_date + timedelta(days=random.randint(1, 14))).strftime('%Y-%m-%d'),
            'query_age_days': age_days,  # CRITICAL COLUMN
            'assigned_to': f'CRA_{random.randint(1, 5)}',
        }
        queries.append(query)
        query_id += 1
    
    query_df = pd.DataFrame(queries)
    query_df.to_csv('data/queries.csv', index=False)
    print(f"✅ Queries: {len(query_df)}")
    print("=" * 50)
    print("🎯 Data generation complete! Run 'streamlit run app.py'")
    print("=" * 50)

if __name__ == "__main__":
    generate_final_data()