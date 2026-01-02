import pandas as pd
import numpy as np
from datetime import datetime
from config import DQI_WEIGHTS, THRESHOLDS

class ClinicalTrialCalculator:
    """Core calculations for clinical trial metrics"""
    
    @staticmethod
        
        
    def calculate_clean_patient_status(patient):
        """Determine if a patient is 'Clean' - SIMPLIFIED VERSION"""
        try:
            # SIMPLIFIED CHECK - Only check key fields that exist in your data
            conditions = [
                patient.get('missing_visits', 1) == 0,           # No missing visits
                patient.get('open_queries', 1) == 0,             # No open queries
                patient.get('safety_issues', 1) == 0,            # No safety issues
                patient.get('forms_verified', False) == True,    # Forms verified
            ]
            
            # For debugging - print first patient's status
            if patient.get('patient_id', '') == 'P001':
                print(f"🔍 DEBUG Patient P001 conditions:")
                print(f"  missing_visits: {patient.get('missing_visits', 'N/A')}")
                print(f"  open_queries: {patient.get('open_queries', 'N/A')}")
                print(f"  safety_issues: {patient.get('safety_issues', 'N/A')}")
                print(f"  forms_verified: {patient.get('forms_verified', 'N/A')}")
                print(f"  All conditions met? {all(conditions)}")
            
            return 'Clean' if all(conditions) else 'Not Clean'
        except Exception as e:
            print(f"❌ Error in clean status calculation: {e}")
            return 'Not Clean'
    
    @staticmethod
    def calculate_data_quality_index(patient):
        """Calculate Data Quality Index (0-100)"""
        try:
            # Component 1: Visit Completion (30%)
            if patient.get('total_visits_expected', 0) > 0:
                visit_score = 100 * (patient.get('visits_completed', 0) / patient.get('total_visits_expected', 1))
            else:
                visit_score = 100
            
            # Component 2: Query Resolution (25%)
            if patient.get('total_queries', 0) > 0:
                query_score = 100 * (patient.get('queries_resolved', 0) / patient.get('total_queries', 1))
            else:
                query_score = 100
            
            # Component 3: Data Quality (20%)
            max_errors = 5
            quality_score = max(0, 100 - (patient.get('non_conformant_data', 0) / max_errors * 100))
            
            # Component 4: Timeliness (15%)
            timeliness_score = 0
            if patient.get('forms_verified', False) and patient.get('forms_signed', False):
                timeliness_score = 100
            elif patient.get('forms_verified', False):
                timeliness_score = 80
            else:
                timeliness_score = 50
            
            # Component 5: Safety (10%)
            safety_score = 100 if patient.get('safety_issues', 0) == 0 else 30
            
            # Apply weights
            dqi = (
                visit_score * DQI_WEIGHTS['visit_completion'] +
                query_score * DQI_WEIGHTS['query_resolution'] +
                quality_score * DQI_WEIGHTS['data_quality'] +
                timeliness_score * DQI_WEIGHTS['timeliness'] +
                safety_score * DQI_WEIGHTS['safety']
            )
            
            return round(max(0, min(100, dqi)), 1)
            
        except Exception as e:
            print(f"Error calculating DQI: {e}")
            return 50.0
    
    @staticmethod
    def calculate_site_performance(site_patients):
        """Calculate aggregated metrics for a site"""
        if len(site_patients) == 0:
            return {}
        
        total_patients = len(site_patients)
        clean_patients = len(site_patients[site_patients['clean_status'] == 'Clean'])
        
        # Averages
        avg_dqi = site_patients['dqi_score'].mean() if 'dqi_score' in site_patients.columns else 0
        
        # Sums
        total_open_queries = site_patients['open_queries'].sum() if 'open_queries' in site_patients.columns else 0
        total_safety_issues = site_patients['safety_issues'].sum() if 'safety_issues' in site_patients.columns else 0
        total_adverse_events = site_patients['adverse_events'].sum() if 'adverse_events' in site_patients.columns else 0
        
        # Performance classification
        if avg_dqi < THRESHOLDS['dqi_critical']:
            performance = 'Critical'
            priority = 'High'
        elif avg_dqi < THRESHOLDS['dqi_warning']:
            performance = 'Warning'
            priority = 'Medium'
        else:
            performance = 'Good'
            priority = 'Low'
        
        # Clean percentage
        clean_percentage = (clean_patients / total_patients) * 100 if total_patients > 0 else 0
        
        return {
            'site_id': site_patients['site_id'].iloc[0] if 'site_id' in site_patients.columns else 'Unknown',
            'total_patients': total_patients,
            'clean_patients': clean_patients,
            'clean_percentage': round(clean_percentage, 1),
            'avg_dqi': round(avg_dqi, 1),
            'total_open_queries': total_open_queries,
            'total_safety_issues': total_safety_issues,
            'total_adverse_events': total_adverse_events,
            'performance_status': performance,
            'priority_level': priority,
            'needs_attention': performance in ['Critical', 'Warning']
        }
    
    @staticmethod
    def process_patient_dataframe(df):
        """Process entire patient dataframe with all calculations"""
        if len(df) == 0:
            return df
        
        # Create a copy
        processed_df = df.copy()
        
        # Calculate clean status
        processed_df['clean_status'] = processed_df.apply(
            ClinicalTrialCalculator.calculate_clean_patient_status, axis=1
        )
        
        # Calculate DQI
        processed_df['dqi_score'] = processed_df.apply(
            ClinicalTrialCalculator.calculate_data_quality_index, axis=1
        )
        
        # Calculate risk level
        processed_df['risk_level'] = processed_df['dqi_score'].apply(
            lambda x: 'High' if x < 60 else ('Medium' if x < 75 else 'Low')
        )
        
        return processed_df
    
    @staticmethod
    def enhance_site_data(sites_df, patients_df):
        """Add calculated columns to site data"""
        if sites_df.empty or patients_df.empty:
            return sites_df
        
        # Create a copy
        enhanced_sites = sites_df.copy()
        
        # Ensure required columns exist
        if 'clean_percentage' not in enhanced_sites.columns:
            enhanced_sites['clean_percentage'] = 0.0
        if 'avg_dqi' not in enhanced_sites.columns:
            enhanced_sites['avg_dqi'] = 0.0
        if 'total_open_queries' not in enhanced_sites.columns:
            enhanced_sites['total_open_queries'] = 0
        if 'performance_status' not in enhanced_sites.columns:
            enhanced_sites['performance_status'] = 'Unknown'
        
        # Calculate site-level metrics from patient data
        for idx, site_row in enhanced_sites.iterrows():
            site_id = site_row['site_id']
            site_patients = patients_df[patients_df['site_id'] == site_id]
            
            if len(site_patients) > 0:
                # Calculate clean percentage
                clean_count = len(site_patients[site_patients['clean_status'] == 'Clean'])
                clean_percentage = (clean_count / len(site_patients)) * 100
                
                # Calculate average DQI
                avg_dqi = site_patients['dqi_score'].mean() if 'dqi_score' in site_patients.columns else 0
                
                # Calculate total open queries
                total_open_queries = site_patients['open_queries'].sum() if 'open_queries' in site_patients.columns else 0
                
                # Determine performance status
                if avg_dqi < 60:
                    performance_status = 'Critical'
                elif avg_dqi < 75:
                    performance_status = 'Warning'
                else:
                    performance_status = 'Good'
                
                # Update the row
                enhanced_sites.at[idx, 'clean_percentage'] = round(clean_percentage, 1)
                enhanced_sites.at[idx, 'avg_dqi'] = round(avg_dqi, 1)
                enhanced_sites.at[idx, 'total_open_queries'] = total_open_queries
                enhanced_sites.at[idx, 'performance_status'] = performance_status
        
        return enhanced_sites


def load_and_process_data():
    """Load and process all datasets"""
    try:
        # Load data
        patients = pd.read_csv('data/patients.csv')
        sites = pd.read_csv('data/sites.csv')
        queries = pd.read_csv('data/queries.csv')
        
        # Process patient data
        calculator = ClinicalTrialCalculator()
        patients_processed = calculator.process_patient_dataframe(patients)
        
        # Enhance site data with calculated columns - FIXED LINE
        sites_enhanced = calculator.enhance_site_data(sites, patients_processed)
        
        return patients_processed, sites_enhanced, queries
        
    except Exception as e:
        print(f"Error loading data: {e}")
        # Return empty dataframes
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()