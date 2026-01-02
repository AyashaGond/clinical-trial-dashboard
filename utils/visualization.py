"""
Visualization functions for dashboard
"""
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

# Define COLORS if not in config
COLORS = {
    'primary': '#1f3c88',
    'secondary': '#6c757d',
    'success': '#28a745',
    'warning': '#ffc107',
    'critical': '#dc3545',
    'info': '#17a2b8',
    'good': '#28a745'
}

class DashboardVisualizer:
    """Create visualizations for dashboard"""
    
    @staticmethod
    def create_dqi_heatmap(site_data):
        """Create DQI heatmap for sites"""
        if site_data.empty:
            return go.Figure()
        
        # Sort by DQI
        site_data = site_data.sort_values('avg_dqi', ascending=True)
        
        fig = go.Figure(data=go.Heatmap(
            z=[site_data['avg_dqi'].values],
            x=site_data['site_id'],
            y=['DQI Score'],
            colorscale='RdYlGn',
            zmin=0,
            zmax=100,
            text=[site_data['avg_dqi'].round(1).astype(str)],
            texttemplate='%{text}',
            textfont={"size": 14},
            hoverinfo='text',
            hovertext=[f"<b>{site}</b><br>DQI: {dqi:.1f}/100<br>Status: {status}" 
                      for site, dqi, status in zip(site_data['site_id'], 
                                                   site_data['avg_dqi'],
                                                   site_data['performance_status'])]
        ))
        
        fig.update_layout(
            title="Data Quality Index (DQI) by Site",
            height=200,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Clinical Site",
            yaxis_title=""
        )
        
        return fig
    
    @staticmethod
    def create_performance_dashboard(site_data):
        """Create comprehensive performance dashboard"""
        
        # Create safe copies with default values
        site_data_safe = site_data.copy()
        
        # Ensure required columns exist
        required_columns = ['avg_dqi', 'clean_percentage', 'total_open_queries', 'total_safety_issues']
        for col in required_columns:
            if col not in site_data_safe.columns:
                site_data_safe[col] = 0
        
        fig = sp.make_subplots(
            rows=2, cols=2,
            subplot_titles=('DQI Distribution', 'Clean Patient %', 
                          'Open Queries', 'Safety Issues'),
            vertical_spacing=0.15,
            horizontal_spacing=0.15
        )
        
        # DQI Distribution
        fig.add_trace(
            go.Bar(
                x=site_data_safe['site_id'],
                y=site_data_safe['avg_dqi'],
                marker_color=site_data_safe['avg_dqi'].apply(
                    lambda x: '#28a745' if x >= 75 else ('#ffc107' if x >= 60 else '#dc3545')
                ),
                name='DQI Score'
            ),
            row=1, col=1
        )
        
        # Clean Patient Percentage
        fig.add_trace(
            go.Bar(
                x=site_data_safe['site_id'],
                y=site_data_safe['clean_percentage'],
                marker_color='#17a2b8',
                name='Clean %'
            ),
            row=1, col=2
        )
        
        # Open Queries
        fig.add_trace(
            go.Bar(
                x=site_data_safe['site_id'],
                y=site_data_safe['total_open_queries'],
                marker_color='#6c757d',
                name='Open Queries'
            ),
            row=2, col=1
        )
        
        # Safety Issues
        fig.add_trace(
            go.Bar(
                x=site_data_safe['site_id'],
                y=site_data_safe['total_safety_issues'],
                marker_color='#dc3545',
                name='Safety Issues'
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            title_text="Site Performance Dashboard",
            margin=dict(l=20, r=20, t=80, b=20)
        )
        
        # Update y-axis titles
        fig.update_yaxes(title_text="DQI Score", row=1, col=1)
        fig.update_yaxes(title_text="Percentage", row=1, col=2)
        fig.update_yaxes(title_text="Count", row=2, col=1)
        fig.update_yaxes(title_text="Count", row=2, col=2)
        
        return fig
    
    @staticmethod
    def create_patient_status_chart(patient_data):
        """Create patient status distribution charts - RENAME THIS METHOD"""
        if patient_data.empty:
            return go.Figure()
        
        # Create subplots
        fig = sp.make_subplots(
            rows=1, cols=2,
            specs=[[{'type': 'pie'}, {'type': 'pie'}]],
            subplot_titles=('Patient Status', 'Clean Status')
        )
        
        # Patient status pie
        status_counts = patient_data['subject_status'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                hole=0.4,
                name='Patient Status',
                marker_colors=[COLORS['info'], COLORS['good'], COLORS['critical']]
            ),
            row=1, col=1
        )
        
        # Clean status pie
        clean_counts = patient_data['clean_status'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=clean_counts.index,
                values=clean_counts.values,
                hole=0.4,
                name='Clean Status',
                marker_colors=[COLORS['good'], COLORS['critical']]
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            height=350,
            showlegend=True,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    @staticmethod
    def create_risk_matrix(patient_data):
        """Create risk level matrix"""
        if patient_data.empty:
            return go.Figure()
        
        # Create risk matrix
        risk_matrix = patient_data.groupby(['risk_level', 'clean_status']).size().unstack(fill_value=0)
        
        # Generate hover text - FIXED VERSION
        hover_texts = []
        for i, risk_level in enumerate(risk_matrix.index):
            row_texts = []
            for j, clean_status in enumerate(risk_matrix.columns):
                count = risk_matrix.iloc[i, j]
                row_texts.append(f"Risk Level: {risk_level}<br>Clean Status: {clean_status}<br>Patients: {count}")
            hover_texts.append(row_texts)
        
        fig = go.Figure(data=go.Heatmap(
            z=risk_matrix.values,
            x=risk_matrix.columns.tolist(),
            y=risk_matrix.index.tolist(),
            colorscale='Reds',
            text=risk_matrix.values,
            texttemplate='%{text}',
            textfont={"size": 14},
            hoverinfo='text',
            hovertext=hover_texts
        ))
        
        fig.update_layout(
            title="Risk Level vs Clean Status Matrix",
            xaxis_title="Clean Status",
            yaxis_title="Risk Level",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    @staticmethod
    def create_timeline_chart(patient_data):
        """Create enrollment trend chart - RENAME THIS METHOD"""
        if patient_data.empty or 'enrollment_date' not in patient_data.columns:
            return go.Figure()
        
        # Group by month
        patient_data['enrollment_month'] = patient_data['enrollment_date'].dt.to_period('M')
        monthly_data = patient_data.groupby('enrollment_month').size().reset_index(name='count')
        monthly_data['enrollment_month'] = monthly_data['enrollment_month'].dt.to_timestamp()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_data['enrollment_month'],
            y=monthly_data['count'],
            mode='lines+markers',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=8),
            name='Patient Enrollments'
        ))
        
        fig.update_layout(
            title="Patient Enrollment Trend",
            xaxis_title="Month",
            yaxis_title="Number of Patients",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig