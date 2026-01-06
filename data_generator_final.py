import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from config import SITES, REGIONS, CRAS, ACTIVE_TRIALS, THERAPEUTIC_AREAS

def generate_multi_disease_data():
    """Generate clinical trial data for multiple diseases"""
    
    print("🏥 Generating Multi-Disease Clinical Trial Dataset...")
    print("=" * 60)
    
    # Create data directory if needed
    import os
    os.makedirs('data', exist_ok=True)
    
    all_patients = []
    all_sites = []
    all_queries = []
    
    # Generate data for EACH trial
    for trial in ACTIVE_TRIALS:
        print(f"\n📊 Generating data for: {trial['name']}")
        print(f"   Disease: {trial['disease']}")
        
        # 1. PATIENT DATA FOR THIS TRIAL
        trial_patients = []
        patients_per_trial = trial['enrolled_patients']
        
        # Assign sites to this trial
        trial_sites = random.sample(SITES, min(trial['total_sites'], len(SITES)))
        
        for i in range(1, patients_per_trial + 1):
            site = random.choice(trial_sites)
            
            # Disease-specific parameters
            disease_type = trial['disease']
            therapeutic_area = trial['therapeutic_area']
            
            # Decide if patient is clean (varies by disease type)
            if therapeutic_area == 'oncology':
                clean_chance = 0.20  # Cancer trials have more issues
            elif therapeutic_area == 'cardiology':
                clean_chance = 0.35  # Heart disease trials
            elif therapeutic_area == 'endocrinology':
                clean_chance = 0.40  # Diabetes trials
            elif therapeutic_area == 'neurology':
                clean_chance = 0.25  # Neurology trials complex
            else:
                clean_chance = 0.30  # Default
            
            is_clean = random.random() < clean_chance
            
            # Generate patient based on disease type
            patient = generate_patient_by_disease(
                patient_id=f"{trial['trial_id']}-P{str(i).zfill(3)}",
                site=site,
                trial_id=trial['trial_id'],
                disease=disease_type,
                therapeutic_area=therapeutic_area,
                is_clean=is_clean
            )
            trial_patients.append(patient)
        
        trial_patient_df = pd.DataFrame(trial_patients)
        all_patients.append(trial_patient_df)
        
        # 2. SITE DATA FOR THIS TRIAL
        for site in trial_sites:
            site_patients = trial_patient_df[trial_patient_df['site_id'] == site]
            
            site_info = {
                'trial_id': trial['trial_id'],
                'trial_name': trial['name'],
                'disease': trial['disease'],
                'therapeutic_area': trial['therapeutic_area'],
                'site_id': site,
                'site_name': site.replace('_', ' '),
                'region': REGIONS[site],
                'cra_in_charge': random.choice(CRAS),
                'total_patients_enrolled': len(site_patients),
                'patients_active': len(site_patients[site_patients['subject_status'] == 'Active']),
                'total_open_queries': site_patients['open_queries'].sum(),
                'total_safety_issues': site_patients['safety_issues'].sum(),
                'total_adverse_events': site_patients['adverse_events'].sum(),
                'monitoring_visits_completed': random.randint(5, 20),
                'site_initiation_date': trial['start_date'],
            }
            all_sites.append(site_info)
        
        # 3. QUERY DATA FOR THIS TRIAL
        trial_queries = generate_queries_for_trial(trial_patient_df, trial['trial_id'])
        all_queries.extend(trial_queries)
        
        print(f"   ✅ Generated {len(trial_patient_df)} patients")
    
    # Combine all data
    patients_df = pd.concat(all_patients, ignore_index=True)
    sites_df = pd.DataFrame(all_sites)
    queries_df = pd.DataFrame(all_queries)
    
    # Save data
    patients_df.to_csv('data/patients.csv', index=False)
    sites_df.to_csv('data/sites.csv', index=False)
    queries_df.to_csv('data/queries.csv', index=False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 DATASET SUMMARY:")
    print(f"• Total Patients: {len(patients_df)}")
    print(f"• Total Trials: {len(ACTIVE_TRIALS)}")
    print(f"• Diseases Covered: {len(set([t['disease'] for t in ACTIVE_TRIALS]))}")
    print(f"• Therapeutic Areas: {len(set([t['therapeutic_area'] for t in ACTIVE_TRIALS]))}")
    print(f"• Total Sites: {len(sites_df['site_id'].unique())}")
    print(f"• Total Queries: {len(queries_df)}")
    
    # Disease-wise breakdown
    print("\n🧬 DISEASE-WISE BREAKDOWN:")
    for trial in ACTIVE_TRIALS:
        trial_patients = patients_df[patients_df['trial_id'] == trial['trial_id']]
        clean_patients = len(trial_patients[trial_patients['clean_status'] == 'Clean'])
        clean_percentage = (clean_patients / len(trial_patients)) * 100 if len(trial_patients) > 0 else 0
        print(f"  {trial['icon']} {trial['disease']}: {len(trial_patients)} patients ({clean_percentage:.1f}% clean)")
    
    print("=" * 60)
    print("✅ All data files saved in 'data/' folder")
    print("🎯 Ready to run the Multi-Disease Dashboard!")
    
    return patients_df, sites_df, queries_df

def generate_patient_by_disease(patient_id, site, trial_id, disease, therapeutic_area, is_clean):
    """Generate patient data specific to disease type"""
    
    # Base patient data
    patient = {
        'patient_id': patient_id,
        'trial_id': trial_id,
        'disease': disease,
        'therapeutic_area': therapeutic_area,
        'site_id': site,
        'region': REGIONS[site],
        'cra_assigned': random.choice(CRAS),
        'enrollment_date': (datetime.now() - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d'),
    }
    
    # Disease-specific parameters
    if therapeutic_area == 'oncology':
        # Cancer patients have more complex data
        patient['subject_status'] = random.choices(['Active', 'Completed', 'Dropped'], weights=[60, 20, 20])[0]
        if is_clean:
            patient.update({
                'missing_visits': 0,
                'open_queries': 0,
                'safety_issues': 0,
                'adverse_events': random.randint(0, 2),  # Cancer patients may have AEs even when clean
                'lab_issues': 0,
                'forms_verified': True,
                'forms_signed': True,
            })
        else:
            patient.update({
                'missing_visits': random.randint(1, 4),
                'open_queries': random.randint(1, 6),
                'safety_issues': random.randint(0, 3),
                'adverse_events': random.randint(1, 5),
                'lab_issues': random.randint(0, 3),
                'forms_verified': random.choice([True, False]),
                'forms_signed': random.choice([True, False]),
            })
    
    elif therapeutic_area == 'cardiology':
        # Heart disease patients
        patient['subject_status'] = random.choices(['Active', 'Completed', 'Dropped'], weights=[70, 25, 5])[0]
        if is_clean:
            patient.update({
                'missing_visits': 0,
                'open_queries': 0,
                'safety_issues': 0,
                'adverse_events': random.randint(0, 1),
                'lab_issues': 0,
                'forms_verified': True,
                'forms_signed': True,
            })
        else:
            patient.update({
                'missing_visits': random.randint(1, 3),
                'open_queries': random.randint(1, 4),
                'safety_issues': random.randint(0, 2),
                'adverse_events': random.randint(0, 3),
                'lab_issues': random.randint(0, 2),
                'forms_verified': random.choices([True, False], weights=[70, 30])[0],
                'forms_signed': random.choices([True, False], weights=[60, 40])[0],
            })
    
    elif therapeutic_area == 'endocrinology':
        # Diabetes patients
        patient['subject_status'] = random.choices(['Active', 'Completed', 'Dropped'], weights=[75, 20, 5])[0]
        if is_clean:
            patient.update({
                'missing_visits': 0,
                'open_queries': 0,
                'safety_issues': 0,
                'adverse_events': 0,
                'lab_issues': 0,
                'forms_verified': True,
                'forms_signed': True,
            })
        else:
            patient.update({
                'missing_visits': random.randint(1, 2),
                'open_queries': random.randint(1, 3),
                'safety_issues': random.randint(0, 1),
                'adverse_events': random.randint(0, 2),
                'lab_issues': random.randint(0, 1),
                'forms_verified': random.choices([True, False], weights=[80, 20])[0],
                'forms_signed': random.choices([True, False], weights=[75, 25])[0],
            })
    
    else:  # Default for other diseases
        patient['subject_status'] = random.choice(['Active', 'Completed', 'Dropped'])
        if is_clean:
            patient.update({
                'missing_visits': 0,
                'open_queries': 0,
                'safety_issues': 0,
                'adverse_events': 0,
                'lab_issues': 0,
                'forms_verified': True,
                'forms_signed': True,
            })
        else:
            patient.update({
                'missing_visits': random.randint(1, 3),
                'open_queries': random.randint(1, 5),
                'safety_issues': random.randint(0, 2),
                'adverse_events': random.randint(0, 3),
                'lab_issues': random.randint(0, 2),
                'forms_verified': random.choice([True, False]),
                'forms_signed': random.choice([True, False]),
            })
    
    # Common metrics
    patient['total_visits_expected'] = 12
    patient['visits_completed'] = random.randint(6, 12) if patient['subject_status'] == 'Active' else 12
    patient['total_pages_expected'] = 85
    patient['pages_completed'] = random.randint(70, 85) if is_clean else random.randint(50, 80)
    patient['missing_pages'] = patient['total_pages_expected'] - patient['pages_completed']
    patient['total_queries'] = patient['open_queries'] + random.randint(0, 3)
    patient['queries_resolved'] = patient['total_queries'] - patient['open_queries']
    patient['non_conformant_data'] = 0 if is_clean else random.randint(1, 4)
    patient['sdv_completed'] = True if is_clean else random.choice([True, False])
    patient['frozen_locked'] = True if is_clean else random.choice([True, False])
    patient['coding_backlog'] = random.randint(0, 2) if is_clean else random.randint(1, 6)
    patient['overdue_crfs'] = 0 if is_clean else random.randint(0, 3)
    patient['protocol_deviations'] = 0 if is_clean else random.randint(0, 2)
    
    # Clean status
    patient['clean_status'] = 'Clean' if is_clean else 'Not Clean'
    
    return patient

def generate_queries_for_trial(patient_df, trial_id):
    """Generate queries for a specific trial"""
    query_types = ['Data Entry Error', 'Missing Value', 'Out of Range', 
                   'Protocol Deviation', 'Lab Value Issue', 'Safety Concern',
                   'Visit Window Violation', 'Concomitant Medication']
    
    queries = []
    query_id = 10000  # Start ID
    
    for _, patient in patient_df.iterrows():
        if patient['open_queries'] > 0:
            for _ in range(patient['open_queries']):
                query_date = datetime.strptime(patient['enrollment_date'], '%Y-%m-%d') + \
                            timedelta(days=random.randint(0, 100))
                
                query = {
                    'query_id': f'Q{query_id}',
                    'trial_id': trial_id,
                    'patient_id': patient['patient_id'],
                    'site_id': patient['site_id'],
                    'disease': patient['disease'],
                    'query_type': random.choice(query_types),
                    'query_description': f'Query regarding {random.choice(["visit data", "lab results", "safety event", "medication"])} for {patient["disease"]} patient',
                    'query_priority': random.choice(['Low', 'Medium', 'High']),
                    'query_status': 'Open',
                    'query_created_date': query_date.strftime('%Y-%m-%d'),
                    'query_age_days': (datetime.now() - query_date).days,
                    'assigned_to': patient['cra_assigned'],
                }
                queries.append(query)
                query_id += 1
    
    # Add some resolved queries
    for _ in range(min(50, len(patient_df))):
        patient = patient_df.sample(1).iloc[0]
        query_date = datetime.strptime(patient['enrollment_date'], '%Y-%m-%d') + \
                    timedelta(days=random.randint(0, 100))
        
        query = {
            'query_id': f'Q{query_id}',
            'trial_id': trial_id,
            'patient_id': patient['patient_id'],
            'site_id': patient['site_id'],
            'disease': patient['disease'],
            'query_type': random.choice(query_types),
            'query_description': f'Resolved query about {random.choice(["medication", "vital signs", "patient history"])}',
            'query_priority': random.choice(['Low', 'Medium']),
            'query_status': 'Resolved',
            'query_created_date': query_date.strftime('%Y-%m-%d'),
            'query_resolved_date': (query_date + timedelta(days=random.randint(1, 14))).strftime('%Y-%m-%d'),
            'query_age_days': (datetime.now() - query_date).days,
            'assigned_to': patient['cra_assigned'],
        }
        queries.append(query)
        query_id += 1
    
    return queries

if __name__ == "__main__":
   generate_multi_disease_data()