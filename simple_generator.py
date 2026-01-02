import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_simple_data():
    """Generate simple but complete dataset"""
    
    print("Generating complete dataset...")
    
    # Region mapping
    region_map = {
        'Site_A_Delhi': 'North',
        'Site_B_Mumbai': 'West', 
        'Site_C_Chennai': 'South',
        'Site_D_Kolkata': 'East',
        'Site_E_Bangalore': 'South'
    }
    
    sites_list = list(region_map.keys())
    
    # 1. PATIENT DATA (200 patients)
    patients = []
    
    for i in range(1, 201):
        site = random.choice(sites_list)
        is_clean = random.random() < 0.35  # 35% clean
        
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
            'forms_verified': is_clean,
            'forms_signed': is_clean,
        }
        patients.append(patient)
    
    patient_df = pd.DataFrame(patients)
    patient_df.to_csv('data/patients.csv', index=False)
    print(f"✅ Patients: {len(patient_df)}")
    
    # 2. SITE DATA (with region)
    site_data = []
    for site in sites_list:
        site_patients = patient_df[patient_df['site_id'] == site]
        
        site_info = {
            'site_id': site,
            'site_name': site.replace('_', ' '),
            'region': region_map[site],  # CRITICAL: region column
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
    print(f"✅ Sites: {len(site_df)} (with region data)")
    
    # 3. QUERY DATA
    query_types = ['Data Error', 'Missing Value', 'Safety Issue']
    queries = []
    
    for i in range(1, 101):
        patient = random.choice(patients)
        query_date = datetime.now() - timedelta(days=random.randint(1, 100))
        
        query = {
            'query_id': f'Q{str(i).zfill(5)}',
            'patient_id': patient['patient_id'],
            'site_id': patient['site_id'],
            'query_type': random.choice(query_types),
            'query_priority': random.choice(['Low', 'Medium', 'High']),
            'query_status': 'Open' if random.random() < 0.7 else 'Resolved',
            'query_created_date': query_date.strftime('%Y-%m-%d'),
            'query_age_days': (datetime.now() - query_date).days,
            'assigned_to': f'CRA_{random.randint(1, 5)}',
        }
        queries.append(query)
    
    query_df = pd.DataFrame(queries)
    query_df.to_csv('data/queries.csv', index=False)
    print(f"✅ Queries: {len(query_df)}")
    
    print("=" * 50)
    print("🎯 Dataset generation complete!")
    print("   • Patients: 200")
    print("   • Sites: 5 (with region)")
    print("   • Queries: 100")
    print("=" * 50)
    print("✅ Run: streamlit run app.py")

if __name__ == "__main__":
    generate_simple_data()
    