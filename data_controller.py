# data_controller.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class DataController:
    """Allows manual control over data generation"""
    
    @staticmethod
    def create_custom_patient(site, is_clean=True, patient_number=1):
        """Create a patient with specific characteristics"""
        
        if is_clean:
            # CLEAN PATIENT
            patient = {
                'patient_id': f'P{str(patient_number).zfill(3)}',
                'subject_id': f'SUB{patient_number:04d}',
                'site_id': site,
                'subject_status': 'Active',
                'enrollment_date': datetime.now().strftime('%Y-%m-%d'),
                'last_visit_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                
                # Perfect metrics (Clean)
                'total_visits_expected': 12,
                'visits_completed': 12,
                'missing_visits': 0,
                'total_pages_expected': 85,
                'pages_completed': 85,
                'missing_pages': 0,
                'total_queries': 0,
                'open_queries': 0,
                'queries_resolved': 0,
                'non_conformant_data': 0,
                'data_entry_errors': 0,
                'lab_issues': 0,
                'safety_issues': 0,
                'adverse_events': 0,
                'serious_adverse_events': 0,
                'forms_verified': True,
                'forms_signed': True,
                'sdv_completed': True,
                'frozen_locked': True,
                'coding_backlog': 0,
                'overdue_crfs': 0,
                'protocol_deviations': 0,
                'screen_failure': False,
                'early_termination': False,
                
                # Calculated fields
                'clean_status': 'Clean',
                'dqi_score': 95.0,
                'risk_level': 'Low',
                'visit_compliance_percentage': 100.0,
                'page_completion_percentage': 100.0,
                'query_resolution_percentage': 100.0,
                'data_quality_percentage': 100.0
            }
        else:
            # NON-CLEAN PATIENT (with issues)
            patient = {
                'patient_id': f'P{str(patient_number).zfill(3)}',
                'subject_id': f'SUB{patient_number:04d}',
                'site_id': site,
                'subject_status': np.random.choice(['Active', 'Completed', 'Dropped'], p=[0.7, 0.2, 0.1]),
                'enrollment_date': (datetime.now() - timedelta(days=np.random.randint(30, 180))).strftime('%Y-%m-%d'),
                'last_visit_date': (datetime.now() - timedelta(days=np.random.randint(1, 29))).strftime('%Y-%m-%d'),
                
                # Issues (Not Clean)
                'total_visits_expected': 12,
                'visits_completed': np.random.randint(6, 10),
                'missing_visits': np.random.randint(1, 4),
                'total_pages_expected': 85,
                'pages_completed': np.random.randint(60, 80),
                'missing_pages': np.random.randint(5, 25),
                'total_queries': np.random.randint(3, 8),
                'open_queries': np.random.randint(1, 4),
                'queries_resolved': lambda x: x['total_queries'] - x['open_queries'],
                'non_conformant_data': np.random.randint(1, 3),
                'data_entry_errors': np.random.randint(0, 2),
                'lab_issues': np.random.randint(0, 2),
                'safety_issues': np.random.randint(0, 1),
                'adverse_events': np.random.randint(0, 2),
                'serious_adverse_events': 0,
                'forms_verified': np.random.choice([True, False], p=[0.3, 0.7]),
                'forms_signed': np.random.choice([True, False], p=[0.2, 0.8]),
                'sdv_completed': np.random.choice([True, False], p=[0.4, 0.6]),
                'frozen_locked': np.random.choice([True, False], p=[0.5, 0.5]),
                'coding_backlog': np.random.randint(1, 4),
                'overdue_crfs': np.random.randint(0, 2),
                'protocol_deviations': np.random.randint(0, 1),
                'screen_failure': False,
                'early_termination': False,
                
                # Calculated fields
                'clean_status': 'Not Clean',
                'dqi_score': np.random.randint(40, 65),
                'risk_level': np.random.choice(['Medium', 'High'], p=[0.7, 0.3]),
                'visit_compliance_percentage': round((np.random.randint(6, 10) / 12) * 100, 1),
                'page_completion_percentage': round((np.random.randint(60, 80) / 85) * 100, 1),
                'query_resolution_percentage': round(((np.random.randint(3, 8) - np.random.randint(1, 4)) / np.random.randint(3, 8)) * 100, 1),
                'data_quality_percentage': round(100 - (np.random.randint(1, 3) * 20), 1)
            }
            patient['queries_resolved'] = patient['total_queries'] - patient['open_queries']
        
        return patient
    
    @staticmethod
    def generate_controlled_dataset():
        """Generate data with user control"""
        
        sites = ['Site_A_Delhi', 'Site_B_Mumbai', 'Site_C_Chennai', 
                 'Site_D_Kolkata', 'Site_E_Bangalore']
        
        patients = []
        patient_number = 1
        
        # Create sidebar controls
        st.sidebar.markdown("### 🎛️ Data Configuration")
        
        # 1. Number of patients
        num_patients = st.sidebar.slider(
            "Number of Patients",
            min_value=10,
            max_value=500,
            value=100,
            step=10
        )
        
        # 2. Clean vs Not Clean ratio
        clean_ratio = st.sidebar.slider(
            "Clean Patients Ratio",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Percentage of patients that are 'Clean'"
        )
        
        # 3. Sites distribution
        st.sidebar.markdown("#### Site Distribution")
        site_distribution = {}
        for site in sites:
            site_distribution[site] = st.sidebar.slider(
                f"Patients at {site}",
                min_value=0,
                max_value=100,
                value=20,
                step=5
            )
        
        # Generate patients based on settings
        for site, count in site_distribution.items():
            site_clean_count = int(count * clean_ratio)
            site_not_clean_count = count - site_clean_count
            
            # Add clean patients
            for i in range(site_clean_count):
                if patient_number > num_patients:
                    break
                patient = DataController.create_custom_patient(site, is_clean=True, patient_number=patient_number)
                patients.append(patient)
                patient_number += 1
            
            # Add not-clean patients
            for i in range(site_not_clean_count):
                if patient_number > num_patients:
                    break
                patient = DataController.create_custom_patient(site, is_clean=False, patient_number=patient_number)
                patients.append(patient)
                patient_number += 1
        
        df = pd.DataFrame(patients)
        return df