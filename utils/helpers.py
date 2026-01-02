import pandas as pd

class DataHelper:
    """Simple helper functions"""
    
    @staticmethod
    def calculate_summary_statistics(data):
        """Calculate summary statistics"""
        if len(data) == 0:
            return {
                'total_patients': 0,
                'clean_patients': 0,
                'clean_percentage': 0,
                'avg_dqi': 0,
                'total_open_queries': 0,
                'total_safety_issues': 0,
                'dqi_status': 'N/A',
                'clean_status': 'N/A'
            }
        
        summary = {
            'total_patients': len(data),
            'clean_patients': len(data[data['clean_status'] == 'Clean']) if 'clean_status' in data.columns else 0,
        }
        
        if summary['total_patients'] > 0:
            summary['clean_percentage'] = round((summary['clean_patients'] / summary['total_patients']) * 100, 1)
        else:
            summary['clean_percentage'] = 0
        
        summary['avg_dqi'] = round(data['dqi_score'].mean(), 1) if 'dqi_score' in data.columns else 0
        summary['total_open_queries'] = data['open_queries'].sum() if 'open_queries' in data.columns else 0
        summary['total_safety_issues'] = data['safety_issues'].sum() if 'safety_issues' in data.columns else 0
        
        # Status indicators
        summary['dqi_status'] = 'Good' if summary['avg_dqi'] >= 75 else \
                               ('Warning' if summary['avg_dqi'] >= 60 else 'Critical')
        summary['clean_status'] = 'Good' if summary['clean_percentage'] >= 70 else \
                                 ('Warning' if summary['clean_percentage'] >= 50 else 'Critical')
        
        return summary
    
    @staticmethod 
    def generate_ai_insights(patient_data, site_data):
        """Generate AI insights"""
        insights = []
        
        if len(site_data) > 0 and 'performance_status' in site_data.columns:
            critical_sites = site_data[site_data['performance_status'] == 'Critical']
            if len(critical_sites) > 0:
                insights.append({
                    'type': 'critical',
                    'title': 'Critical Sites Detected',
                    'message': f"{len(critical_sites)} sites need immediate attention",
                    'recommendation': 'Schedule priority monitoring visits.'
                })
        
        return insights