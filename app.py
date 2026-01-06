# app.py - PROFESSIONAL PHARMACEUTICAL DASHBOARD VERSION
from login import main_login
from utils.helpers import DataHelper
from calculations import load_and_process_data
from config import DEFAULT_TRIAL, ACTIVE_TRIALS
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
import time
import plotly.graph_objects as go
import plotly.express as px

import streamlit as st

# THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Clinical Intelligence Platform",
    page_icon="🏥",
    layout="wide",  # <-- THIS IS CRITICAL
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.novartis.com',
        'Report a bug': None,
        'About': "Clinical Trial Intelligence Dashboard v1.0"
    }
)


st.markdown("""
<style>
    /* ========== FIXED & CLEANED CSS ========== */
    
    /* Main container styling - REMOVE DUPLICATES */
    .main-header {
        font-size: 28px;
        color: #1f3c88;
        font-weight: 700;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .sub-header {
        font-size: 14px;
        color: #6c757d;
        margin-bottom: 25px;
    }
    
    /* Pharmaceutical style cards */
    .pharma-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    
    .pharma-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.12);
    }
    
    /* Metrics cards */
    .metric-card-pharma {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 3px 15px rgba(31, 60, 136, 0.1);
        height: 100%;
    }
    
    .metric-value-pharma {
        font-size: 36px;
        font-weight: 800;
        color: #1f3c88;
        margin: 10px 0;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    
    .metric-label-pharma {
        font-size: 14px;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Progress bars */
    .progress-container-pharma {
        background: #e9ecef;
        height: 10px;
        border-radius: 5px;
        margin: 15px 0;
        overflow: hidden;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .progress-bar-pharma {
        height: 100%;
        border-radius: 5px;
        background: linear-gradient(90deg, #1f3c88 0%, #0d1b2a 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Professional tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #f8f9fa;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        color: #495057;
        transition: all 0.3s;
        padding: 0 20px;
        border: 1px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(31, 60, 136, 0.05);
        border-color: rgba(31, 60, 136, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1f3c88 0%, #0d1b2a 100%);
        color: white !important;
        box-shadow: 0 3px 10px rgba(31, 60, 136, 0.2);
        border-color: #1f3c88;
    }
    
    /* Header styling - FIXED */
    .pharma-header {
        background: linear-gradient(135deg, #1f3c88 0%, #0d1b2a 100%) !important;
        padding: 25px 30px !important;
        border-radius: 20px !important;
        margin: -20px -20px 30px -20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
        position: relative !important;
        overflow: visible !important;
        width: 100% !important;
    }
    
    .pharma-header h1,
    .pharma-header span,
    .pharma-header div {
        color: white !important;
    }
    
    /* Sidebar styling - FIXED */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
        box-shadow: 2px 0 10px rgba(0,0,0,0.05);
        width: 200px !important;
        min-width: 200px !important;
        max-width: 200px !important;
    }
    
    /* Main content width adjustment - CRITICAL FIX */
    .stApp {
        width: 100vw !important;
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }
    
    .main .block-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: 1rem 2rem !important;
        transition: margin-left 0.3s ease !important;
    }
    
    /* When sidebar is EXPANDED - FIXED */
    section[data-testid="stSidebar"][aria-expanded="true"] ~ .main .block-container {
        margin-left: 200px !important;
        width: calc(100vw - 200px) !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* When sidebar is COLLAPSED - FIXED */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
    }
    
    section[data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container {
        margin-left: 0 !important;
        width: 100vw !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Hide sidebar content when collapsed */
    section[data-testid="stSidebar"][aria-expanded="false"] > div {
        display: none !important;
    }
    
    /* Remove Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #1f3c88;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #0d1b2a;
    }
    
    /* Responsive tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        flex-wrap: wrap;
    }
    
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            flex: 1 0 calc(33.333% - 4px) !important;
            font-size: 12px !important;
            height: 45px !important;
            padding: 0 8px !important;
            margin-bottom: 4px;
        }
        
        /* Mobile sidebar */
        section[data-testid="stSidebar"] {
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
        }
        
        section[data-testid="stSidebar"][aria-expanded="true"] ~ .main .block-container {
            margin-left: 280px !important;
            width: calc(100vw - 280px) !important;
        }
    }
    
    @media (max-width: 480px) {
        .stTabs [data-baseweb="tab"] {
            flex: 1 0 calc(50% - 4px) !important;
            font-size: 11px !important;
            height: 40px !important;
        }
        
        .pharma-header {
            padding: 15px !important;
        }
        
        .metric-card-pharma {
            padding: 15px !important;
        }
        
        .metric-value-pharma {
            font-size: 28px !important;
        }
    }
    
    /* Make images/charts responsive */
    .stPlotlyChart, .stDataFrame, img {
        max-width: 100% !important;
        height: auto !important;
    }
    
    /* Responsive columns */
    .stColumn {
        min-width: 0 !important;
    }
    
    /* Ensure content doesn't overflow */
    * {
        box-sizing: border-box !important;
    }
    
    /* Responsive table */
    div[data-testid="stDataFrameResizable"] {
        overflow-x: auto !important;
    }
</style>
""", unsafe_allow_html=True)



def is_mobile():
    """Detect if user is on mobile device"""
    try:
        user_agent = st.query_params.get("user_agent", "")
        if not user_agent:
            return False
        mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'tablet']
        return any(keyword in user_agent.lower() for keyword in mobile_keywords)
    except:
        return False

@st.cache_data
def load_data(disease=None):
    """Load and cache data with optional disease filter"""
    
    import pandas as pd
    import numpy as np
    import random
    
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Create COMPLETE dataset
    diseases = ['Oncology', 'Cardiology', 'Neurology', 'Endocrinology']
    sites = ['Site_A', 'Site_B', 'Site_C', 'Site_D', 'Site_E']
    num_patients = 300  # Changed from 500 to 300 for better display
    
    # Create patients DataFrame with ALL required columns
    # Create patients DataFrame with REALISTIC clinical trial values
    patients = pd.DataFrame({
        'patient_id': [f'PAT-{i:04d}' for i in range(1, num_patients + 1)],
        'site_id': [random.choice(sites) for _ in range(num_patients)],
        'subject_status': random.choices(
            ['Active', 'Completed', 'Screening', 'Withdrawn'], 
            weights=[60, 25, 10, 5], k=num_patients  # More active, fewer withdrawn
        ),
        'clean_status': random.choices(['Clean', 'Not Clean'], weights=[30, 70], k=num_patients),
        'dqi_score': np.random.normal(78, 8, num_patients).clip(60, 95).astype(int),  # Normal distribution
        'disease': random.choices(diseases, weights=[40, 25, 20, 15], k=num_patients),
        'risk_level': random.choices(['Low', 'Medium', 'High'], weights=[60, 30, 10], k=num_patients),  # Mostly low risk
        
        # REALISTIC VALUES BELOW:
        'missing_visits': np.random.choice([0, 1, 2], num_patients, p=[0.7, 0.2, 0.1]),  # Mostly 0
        'open_queries': np.random.choice([0, 1, 2, 3], num_patients, p=[0.6, 0.2, 0.15, 0.05]),  # Mostly 0-1
        'safety_issues': np.random.choice([0, 1], num_patients, p=[0.85, 0.15]),  # 85% have 0
        'adverse_events': np.random.choice([0, 1, 2], num_patients, p=[0.8, 0.15, 0.05]),
        'visits_completed': np.random.randint(2, 10, num_patients),  # 2-9 visits
        'forms_verified': np.random.randint(5, 25, num_patients),   # 5-24 forms (NOT 0-100!)
        'protocol_deviations': np.random.choice([0, 1], num_patients, p=[0.9, 0.1]),  # 90% have 0
        'total_queries': np.random.choice([0, 1, 2, 3, 4], num_patients, p=[0.4, 0.3, 0.15, 0.1, 0.05]),
        'enrollment_date': pd.date_range(start='2023-01-01', periods=num_patients, freq='D').date
        })
    
    # Add queries_resolved column
    patients['queries_resolved'] = patients.apply(
        lambda row: random.randint(0, row['total_queries']), axis=1
    )
    
    # Create sites data
    sites_df = pd.DataFrame({
        'site_id': sites,
        'region': ['North', 'South', 'East', 'West', 'Central'],
        'total_patients_enrolled': [60, 58, 62, 61, 59],  # Reduced to match 300 total
        'clean_percentage': [35.2, 42.1, 38.5, 40.7, 37.8],
        'avg_dqi': [77.2, 75.8, 79.1, 76.5, 78.3],
        'total_open_queries': np.random.randint(10, 30, 5),  # Reduced
        'total_safety_issues': np.random.randint(2, 10, 5),  # Reduced
        'performance_status': ['Good', 'Average', 'Excellent', 'Average', 'Good']
    })
    
    # Create queries data
    num_queries = 150  # Reduced
    queries_df = pd.DataFrame({
        'query_id': [f'QRY-{i:05d}' for i in range(1, num_queries + 1)],
        'patient_id': random.choices(patients['patient_id'].tolist(), k=num_queries),
        'disease': random.choices(diseases, k=num_queries),
        'query_type': random.choices(
            ['Data Entry', 'Missing Value', 'Safety', 'Protocol'], 
            weights=[40, 30, 15, 15], k=num_queries
        ),
        'query_status': random.choices(['Open', 'Resolved'], weights=[40, 60], k=num_queries),
        'query_priority': random.choices(['Low', 'Medium', 'High'], 
                                         weights=[50, 30, 20], k=num_queries),
        'created_date': pd.date_range(start='2023-06-01', periods=num_queries, freq='h'),
        'assigned_to': random.choices(['Dr. Smith', 'Dr. Johnson', 'Dr. Williams'], 
                                      k=num_queries)
    })
    
    # Add resolved_date
    queries_df['resolved_date'] = queries_df.apply(
        lambda row: row['created_date'] + pd.Timedelta(hours=random.randint(1, 72)) 
        if row['query_status'] == 'Resolved' else pd.NaT,
        axis=1
    )
    
    # If disease filter is provided, filter the data
    if disease and 'disease' in patients.columns:
        filtered_patients = patients[patients['disease'] == disease].copy()  # ADD .copy()
        filtered_patients = filtered_patients.reset_index(drop=True)  # RESET INDEX
        
        # Update patient IDs to be sequential after filtering
        filtered_patients['patient_id'] = [f'PAT-{i:04d}' for i in range(1, len(filtered_patients) + 1)]
        
        site_ids = filtered_patients['site_id'].unique()
        filtered_sites = sites_df[sites_df['site_id'].isin(site_ids)].copy()
        filtered_queries = queries_df[queries_df['disease'] == disease].copy()
        
        # Also update query IDs to be sequential
        if len(filtered_queries) > 0:
            filtered_queries = filtered_queries.reset_index(drop=True)
            filtered_queries['query_id'] = [f'QRY-{i:05d}' for i in range(1, len(filtered_queries) + 1)]
        
        return filtered_patients, filtered_sites, filtered_queries
    
    # For unfiltered data, also ensure it's sequential
    patients = patients.reset_index(drop=True)
    return patients, sites_df, queries_df

def create_pharma_header(user):
    """Create clean pharmaceutical header with only platform name and login time"""

    # Use the blue color from your screenshot
    header_bg_color = "#0d1b2a"  # Professional blue
     
     # Check if mobile
    mobile = is_mobile()
    
    # Adjust font sizes based on device
    title_size = "22px" if mobile else "26px"
    subtitle_size = "12px" if mobile else "14px"
     
    # Create header with Streamlit components
    with st.container():
        col1, col2 = st.columns([6, 1])
        
        with col1:
            # SIMPLE header without disease info
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: flex-start;
                gap: 20px;
                margin-top: 10px;
            ">
                <div style="
                    background: linear-gradient(135deg, #1f3c88 0%, #0d1b2a 100%);
                    padding: 15px;
                    border-radius: 15px;
                    width: 90px;
                    height: 100px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 6px 12px rgba(0,0,0,0.25);
                    flex-shrink: 0;
                ">
                    <span style="font-size: 40px; color: white;">🏥</span>
                </div>
                <div>
                <div style="
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    height: 80px;  /* Match logo height */
                ">
                    <h1 style="
                        color: #1f3c88;
                        margin: 0px 0px 1px 0px;
                        font-size: 37px;
                        font-weight: 900;
                        letter-spacing: .5px;
                        line-height: 0.8;
                    ">Clinical Intelligence Platform</h1>
                    <div style="
                        color: #666;
                        font-size: 14px;
                        font-weight: 500;
                        line-height: 0.9;
                    ">
                        <div>Clinical Trial Monitoring Dashboard</div>
                        <div style="margin-top: 5px; color: #888; font-size: 13px;line-height: 1.1;margin-top: 0.2px;">
                        • Last login: {datetime.now().strftime('%H:%M')}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Empty column
            st.markdown("""
            <div style="height: 20px"></div>
            """, unsafe_allow_html=True)


def create_metric_card(title, value, delta=None, status="info", progress=None, icon=None):
    """Create a pharmaceutical metric card"""

    status_colors = {
        "good": "#28a745",
        "warning": "#ffc107",
        "critical": "#dc3545",
        "info": "#17a2b8",
        "primary": "#1f3c88"
    }

    border_color = status_colors.get(status, "#1f3c88")

    # Build HTML with pharmaceutical styling
    html = f"""
    <div class="metric-card-pharma">
        <div class="metric-label-pharma">
            {icon if icon else ""} {title}
        </div>
        <div class="metric-value-pharma">{value}</div>
    """

    if delta:
        trend_class = "trend-up-pharma" if "+" in str(delta) else (
            "trend-down-pharma" if "-" in str(delta) else "trend-neutral-pharma")
        html += f'<div class="metric-trend-pharma {trend_class}">{delta}</div>'

    if progress is not None:
        progress_width = min(max(progress, 0), 100)
        progress_color = "#28a745" if progress >= 70 else (
            "#ffc107" if progress >= 50 else "#dc3545")
        html += f"""<div class="progress-container-pharma">
            <div class="progress-bar-pharma" style="width: {progress_width}%; background: {progress_color};"></div>
        </div>
        """

    html += "</div>"
    return html


def create_visualizations(patients, sites):
    """Create professional visualizations"""

    # Initialize default figures
    fig1 = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()

    # 1. DQI Trend Chart
    if 'site_id' in patients.columns and 'dqi_score' in patients.columns and len(patients) > 0:
        fig1 = go.Figure()
        site_count = 0

        for site in patients['site_id'].unique()[:5]:  # Show top 5 sites
            site_data = patients[patients['site_id'] == site]
            if len(site_data) > 0:
                fig1.add_trace(go.Scatter(
                    x=list(range(len(site_data))),
                    y=site_data['dqi_score'].sort_values().values,
                    mode='lines+markers',
                    name=site,
                    line=dict(width=3),
                    marker=dict(size=8)
                ))
                site_count += 1

        if site_count > 0:
            fig1.update_layout(
                title=dict(text="DQI Trends by Site",
                           font=dict(size=16, color='#1f3c88')),
                height=350,
                xaxis_title="Patient Rank",
                yaxis_title="DQI Score",
                hovermode='x unified',
                template='plotly_white',
                plot_bgcolor='rgba(248,249,250,0.8)',
                paper_bgcolor='white',
                font=dict(family="Segoe UI, system-ui, sans-serif")
            )
        else:
            fig1.add_annotation(
                text="No data available for DQI trends",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )

    # 2. Clean Status Pie Chart
    if 'clean_status' in patients.columns and len(patients) > 0:
        clean_counts = patients['clean_status'].value_counts()
        if len(clean_counts) > 0:
            colors = ['#28a745' if x ==
                      'Clean' else '#dc3545' for x in clean_counts.index]
            fig2 = go.Figure(data=[go.Pie(
                labels=clean_counts.index,
                values=clean_counts.values,
                hole=0.4,
                marker=dict(colors=colors),
                textinfo='label+percent',
                textfont=dict(size=12),
                hovertemplate='<b>%{label}</b><br>Patients: %{value}<br>Percentage: %{percent}'
            )])
            fig2.update_layout(
                title=dict(text="Clean Status Distribution",
                           font=dict(size=16, color='#1f3c88')),
                height=350,
                showlegend=True,
                font=dict(family="Segoe UI, system-ui, sans-serif")
            )

    # 3. Site Performance Heatmap
    if not sites.empty and 'avg_dqi' in sites.columns and len(sites) > 0:
        sites_sorted = sites.sort_values('avg_dqi', ascending=False)
        fig3 = go.Figure(data=go.Heatmap(
            z=[sites_sorted['avg_dqi'].values],
            x=sites_sorted['site_id'].values,
            y=['DQI Score'],
            colorscale='RdYlGn',
            zmin=0,
            zmax=100,
            text=[sites_sorted['avg_dqi'].values],
            texttemplate='%{text:.1f}',
            textfont={"size": 12, "color": "black"},
            hoverinfo='text',
            hovertemplate='Site: %{x}<br>DQI: %{z:.1f}<extra></extra>'
        ))
        fig3.update_layout(
            title=dict(text="Site Performance Heatmap",
                       font=dict(size=16, color='#1f3c88')),
            height=250,
            xaxis_title="Site",
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(family="Segoe UI, system-ui, sans-serif")
        )

    return fig1, fig2, fig3


def create_sidebar_filters(patients, user, current_disease=None):
    """Create professional sidebar filters with user profile at bottom"""

    with st.sidebar:
        st.markdown("### 🔍 Filters & Controls")

        # Show current disease
        if current_disease:
            st.info(f"**Viewing:** {current_disease} Trials")
        
        # Site selection - NO DEFAULT SELECTIONS
        st.markdown("**Site Selection**")
        if 'site_id' in patients.columns:
            site_options = patients['site_id'].unique()
            selected_sites = st.multiselect(
                "Select sites",
                options=site_options,
                default=[],  # EMPTY ARRAY = NO DEFAULT SELECTIONS
                label_visibility="collapsed",
                placeholder="Select sites...",
                key="site_filter"
            )
        else:
            selected_sites = []

        # Patient status - NO DEFAULT SELECTIONS
        st.markdown("**Patient Status**")
        if 'subject_status' in patients.columns:
            status_options = patients['subject_status'].unique()
            selected_status = st.multiselect(
                "Filter by status",
                options=status_options,
                default=[],  # EMPTY ARRAY = NO DEFAULT SELECTIONS
                label_visibility="collapsed",
                placeholder="Select statuses...",
                key="status_filter"
            )
        else:
            selected_status = []

        # Clean status toggle - SET DEFAULT TO 'All'
        st.markdown("**Clean Status**")
        clean_filter = st.radio(
            "Show patients",
            options=['All', 'Clean Only', 'Issues Only'],
            horizontal=True,
            label_visibility="collapsed",
            index=0,  # 'All' is default
            key="clean_filter"
        )

        # Risk level selector - NO DEFAULT SELECTIONS
        st.markdown("**Risk Level**")
        if 'risk_level' in patients.columns:
            risk_options = patients['risk_level'].unique()
            risk_filter = st.multiselect(
                "Select risk levels",
                options=risk_options,
                default=[],  # EMPTY ARRAY = NO DEFAULT SELECTIONS
                label_visibility="collapsed",
                placeholder="Select risk levels...",
                key="risk_filter"
            )
        else:
            risk_filter = []

        # DQI range slider - SHOW FULL RANGE
        st.markdown("**DQI Score Range**")
        if 'dqi_score' in patients.columns:
            min_dqi = int(patients['dqi_score'].min())
            max_dqi = int(patients['dqi_score'].max())
            dqi_range = st.slider(
                "Adjust DQI range",
                min_value=min_dqi,
                max_value=max_dqi,
                value=(min_dqi, max_dqi),  # FULL RANGE AS DEFAULT
                label_visibility="collapsed",
                key="dqi_filter"
            )
        else:
            dqi_range = (0, 100)

        # Date range picker - SHOW FULL DATE RANGE
        st.markdown("**Date Range**")
        if 'enrollment_date' in patients.columns:
            try:
                patients['enrollment_date'] = pd.to_datetime(
                    patients['enrollment_date'])
                min_date = patients['enrollment_date'].min().date()
                max_date = patients['enrollment_date'].max().date()

                date_range = st.date_input(
                    "Select date range",
                    value=(min_date, max_date),  # FULL DATE RANGE AS DEFAULT
                    label_visibility="collapsed",
                    key="date_filter"
                )
            except:
                date_range = (datetime.now().date() -
                              timedelta(days=365), datetime.now().date())
        else:
            date_range = (datetime.now().date() -
                          timedelta(days=365), datetime.now().date())


        # Export Demo Feature
        st.markdown("---")
        with st.expander("📊 Export Demo & Reports", expanded=False):
            st.markdown("**Generate Professional Reports:**")

            report_type = st.selectbox(
                "Report Type",
                ["Executive Summary", "Site Performance",
                    "Data Quality", "Safety Analysis"],
                index=0,  # First item as default
                key="report_type"
            )

            format_type = st.radio(
                "Format",
                ["PDF", "Excel", "HTML"],
                horizontal=True,
                index=0,  # First item as default
                key="format_type"
            )

            if st.button("🔄 Generate Demo Report", type="secondary", key="generate_report"):
                with st.spinner(f"Creating {report_type} report..."):
                    time.sleep(2)
                    st.success(f"✅ {report_type} report generated!")

        # Trial info in sidebar
        st.markdown("---")
        with st.expander("📋 Trial Information", expanded=False):
            st.info(f"""
            **Therapeutic Area:** {DEFAULT_TRIAL['therapeutic_area']}
            **Phase:** {DEFAULT_TRIAL['phase']}
            **Target Enrollment:** {DEFAULT_TRIAL['target_patients']}
            **Duration:** {DEFAULT_TRIAL['start_date']} to {DEFAULT_TRIAL['expected_end_date']}
            **User Role:** {user.get('role', 'User')}
            """)

        # Add spacing
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

        # USER PROFILE SECTION AT BOTTOM (YouTube/Amazon style)
        st.markdown("---")

        # Create a container for the user profile
        profile_container = st.container()

        with profile_container:
            # User profile header (always visible)
            col1, col2, col3 = st.columns([1, 3, 1])

            with col1:
                # User avatar
                role_color = '#1f3c88' if user.get(
                    'role') == 'Admin' else '#28a745'
                st.markdown(f"""
                <div style="
                    background: {role_color};
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: 700;
                    font-size: 17px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    margin-top: 20px;
                ">{user.get('name', 'U')[0].upper()}</div>
                """, unsafe_allow_html=True)

            with col2:
                # User info
                st.markdown(f"""
                <div style="margin-top: 8px;">
                    <div style="font-size: 14px; font-weight: 600; color: #333;">{user.get('name', 'System User')}</div>
                    <div style="font-size: 12px; color: #666;">{user.get('role', 'User')}</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                # Three-dot menu button
                st.markdown("<div style='margin-top: 10px;'></div>",
                            unsafe_allow_html=True)
                if st.button("⋮", key="profile_menu_button", help="User menu"):
                    st.session_state['show_profile_menu'] = not st.session_state.get(
                        'show_profile_menu', False)

        # Profile menu dropdown (appears below when clicked)
        if st.session_state.get('show_profile_menu', False):
            st.markdown("---")
            st.markdown("### 👤 User Menu")

            # Menu items as buttons
            if st.button("👤 Your Profile", key="your_profile"):
                st.session_state['show_profile_settings'] = True
                st.session_state['show_profile_menu'] = False

            if st.button("⚙️ Settings", key="user_settings"):
                st.session_state['show_account_settings'] = True
                st.session_state['show_profile_menu'] = False

            if st.button("🔐 Security", key="user_security"):
                st.session_state['show_security_settings'] = True
                st.session_state['show_profile_menu'] = False

            if st.button("📊 Preferences", key="user_preferences"):
                st.session_state['show_preferences'] = True
                st.session_state['show_profile_menu'] = False

            st.markdown("---")

            if st.button("📖 Help & Support", key="user_help"):
                st.session_state['show_help'] = True
                st.session_state['show_profile_menu'] = False

            if st.button("💬 Send Feedback", key="user_feedback"):
                st.session_state['show_feedback'] = True
                st.session_state['show_profile_menu'] = False

            if st.button("🔄 Switch Account", key="switch_account"):
                st.session_state['show_switch_account'] = True
                st.session_state['show_profile_menu'] = False

            st.markdown("---")

            if st.button("🚪 Logout", type="primary", key="sidebar_logout"):
                # Clear session state and rerun
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        # Handle the profile settings expanders
        if st.session_state.get('show_profile_settings', False):
            with st.expander("👤 Profile Settings", expanded=True):
                st.subheader("Edit Profile")
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Full Name", value=user.get(
                        'name', ''), key="profile_name")
                with col2:
                    new_role = st.selectbox("Role", ["Admin", "Investigator", "Monitor", "Viewer"],
                                            index=["Admin", "Investigator", "Monitor", "Viewer"].index(
                                                user.get('role', 'User'))
                                            if user.get('role') in ["Admin", "Investigator", "Monitor", "Viewer"] else 0,
                                            key="profile_role")

                new_email = st.text_input("Email", value=user.get(
                    'email', ''), key="profile_email")
                new_phone = st.text_input("Phone", value=user.get(
                    'phone', ''), key="profile_phone")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Changes", key="save_profile", width='stretch'):
                        st.success("Profile updated successfully!")
                        st.session_state['show_profile_settings'] = False
                with col2:
                    if st.button("✖️ Cancel", key="cancel_profile", width='stretch'):
                        st.session_state['show_profile_settings'] = False

        if st.session_state.get('show_account_settings', False):
            with st.expander("⚙️ Account Settings", expanded=True):
                st.subheader("Account Configuration")
                notification_prefs = st.multiselect(
                    "Notifications",
                    ["Email Alerts", "SMS Notifications",
                        "Browser Notifications", "Weekly Reports"],
                    default=["Email Alerts", "Weekly Reports"],
                    key="notifications"
                )

                timezone = st.selectbox(
                    "Timezone", ["UTC", "EST", "CST", "PST", "IST"], key="timezone")
                date_format = st.selectbox(
                    "Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"], key="date_format")

                if st.button("💾 Save Preferences", key="save_account_settings", width='stretch'):
                    st.success("Account settings saved!")
                    st.session_state['show_account_settings'] = False

        if st.session_state.get('show_security_settings', False):
            with st.expander("🔐 Security Settings", expanded=True):
                st.subheader("Security Configuration")
                current_pass = st.text_input(
                    "Current Password", type="password", key="current_pass")
                new_pass = st.text_input(
                    "New Password", type="password", key="new_pass")
                confirm_pass = st.text_input(
                    "Confirm New Password", type="password", key="confirm_pass")

                two_factor = st.checkbox(
                    "Enable Two-Factor Authentication", value=True, key="two_factor")
                session_timeout = st.slider(
                    "Session Timeout (minutes)", 15, 240, 60, key="session_timeout")

                if st.button("🔒 Update Security", key="update_security", width='stretch'):
                    st.success("Security settings updated!")
                    st.session_state['show_security_settings'] = False

        if st.session_state.get('show_preferences', False):
            with st.expander("📊 Dashboard Preferences", expanded=True):
                st.subheader("Customize Dashboard")
                default_tab = st.selectbox(
                    "Default Tab on Login",
                    ["Performance Dashboard", "Patient Management", "Site Analytics",
                     "Risk Monitoring", "AI Insights", "Disease Analytics"],
                    key="default_tab"
                )

                theme = st.radio(
                    "Theme", ["Light", "Dark", "Auto"], key="theme")
                density = st.radio(
                    "Data Density", ["Comfortable", "Compact"], key="density")

                col1, col2 = st.columns(2)
                with col1:
                    show_tutorial = st.checkbox(
                        "Show Tutorial on Login", value=True, key="show_tutorial")
                with col2:
                    auto_refresh = st.checkbox(
                        "Auto-refresh Data", value=False, key="auto_refresh")

                if st.button("💾 Save Preferences", key="save_preferences", ):
                    st.success("Dashboard preferences saved!")
                    st.session_state['show_preferences'] = False

        if st.session_state.get('show_help', False):
            with st.expander("📖 Help & Support", expanded=True):
                st.subheader("Help Resources")
                st.info("""
                **Need Help?**
                - 📞 Support Hotline: 1-800-CLINICAL
                - 📧 Email: support@clinicalintel.com
                - 🏢 Office Hours: Mon-Fri 9AM-6PM EST
                
                **Quick Links:**
                - User Manual
                - Video Tutorials
                - FAQ Section
                - API Documentation
                """)

                issue_type = st.selectbox("Report an Issue",
                                          ["Technical Problem", "Data Issue",
                                              "Feature Request", "Other"],
                                          key="issue_type")
                issue_desc = st.text_area(
                    "Description", key="issue_desc", height=100)

                if st.button("📨 Submit Ticket", key="submit_ticket", width='stretch'):
                    st.success("Help ticket submitted!")
                    st.session_state['show_help'] = False

        if st.session_state.get('show_feedback', False):
            with st.expander("💬 Send Feedback", expanded=True):
                st.subheader("Send Feedback")
                feedback_type = st.selectbox("Feedback Type",
                                             ["Bug Report", "Feature Request",
                                                 "General Feedback", "Complaint"],
                                             key="feedback_type")
                feedback_desc = st.text_area(
                    "Your Feedback", key="feedback_desc", height=100)
                rating = st.slider("Rating", 1, 5, 5, key="rating")

                if st.button("📨 Submit Feedback", key="submit_feedback", width='stretch'):
                    st.success("Thank you for your feedback!")
                    st.session_state['show_feedback'] = False

        if st.session_state.get('show_switch_account', False):
            with st.expander("🔄 Switch Account", expanded=True):
                st.subheader("Switch Account")
                accounts = [
                    {"name": user.get('name', 'System User'), "role": user.get(
                        'role', 'User'), "current": True},
                    {"name": "John Researcher",
                        "role": "Principal Investigator", "current": False},
                    {"name": "Sarah Monitor",
                        "role": "Clinical Monitor", "current": False},
                    {"name": "Admin User", "role": "System Admin", "current": False}
                ]

                selected_account = st.selectbox(
                    "Select Account",
                    [acc["name"] + " (" + acc["role"] +
                     ")" for acc in accounts],
                    index=0,
                    key="selected_account"
                )

                if st.button("🔓 Switch", key="switch_account_btn", width='stretch'):
                    st.warning("Account switching requires re-authentication")
                    st.session_state['show_switch_account'] = False

    return selected_sites, selected_status, clean_filter, risk_filter, dqi_range, date_range


def main_dashboard():
    """Main dashboard function"""
    
    # Show loading state
    #with st.spinner("🔄 Loading Clinical Intelligence Platform..."):
     #   time.sleep(0.1)  # Small delay for better UX
    
    # Add viewport meta tag
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    """, unsafe_allow_html=True)
    
    # Check login
    if not main_login():
        return

    user = st.session_state.get('user', {})
    
    # Get current disease from session state (default to 'Oncology')
    current_disease = st.session_state.get('current_disease', 'Oncology')

    # Create clean header
    st.markdown("""
    <div style="
        background: #1f3c88;
        padding: 15px 20px;
        margin: -20px -20px 25px -20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        position: relative;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    ">
    """, unsafe_allow_html=True)

    create_pharma_header(user)

    st.markdown("</div>", unsafe_allow_html=True)
    

    # Load data WITH disease filter
    with st.spinner(f"🔄 Loading {current_disease} trial data..."):
        try:
            # Pass the current disease to filter data
            patients, sites, queries = load_data(current_disease)
        except Exception as e:
            st.error(f"Error loading {current_disease} data: {e}")
            st.info("Please run 'python data_generator.py' first")
            return

    if patients.empty:
        st.warning(f"📊 No {current_disease} patient data found.")
        # Offer to generate data
        if st.button(f"Generate {current_disease} Sample Data"):
            # You would call your data generator here
            st.info("Please run 'python data_generator.py' to generate data")
        return
    
    # Create sidebar filters - pass disease info
    selected_sites, selected_status, clean_filter, risk_filter, dqi_range, date_range = create_sidebar_filters(
        patients, user, current_disease)

    # Apply filters
    filtered_patients = patients.copy()

    if selected_sites and len(selected_sites) > 0:
        filtered_patients = filtered_patients[filtered_patients['site_id'].isin(
            selected_sites)]

    if selected_status and len(selected_status) > 0:
        filtered_patients = filtered_patients[filtered_patients['subject_status'].isin(
            selected_status)]

    if clean_filter == 'Clean Only':
        filtered_patients = filtered_patients[filtered_patients['clean_status'] == 'Clean']
    elif clean_filter == 'Issues Only':
        filtered_patients = filtered_patients[filtered_patients['clean_status'] == 'Not Clean']

    if risk_filter and len(risk_filter) > 0:
        filtered_patients = filtered_patients[filtered_patients['risk_level'].isin(
            risk_filter)]

    if 'dqi_score' in filtered_patients.columns:
        filtered_patients = filtered_patients[
            (filtered_patients['dqi_score'] >= dqi_range[0]) &
            (filtered_patients['dqi_score'] <= dqi_range[1])
        ]

    # Calculate metrics
    summary = DataHelper.calculate_summary_statistics(filtered_patients)

    # Add this RIGHT AFTER calculating summary in main_dashboard():
    #st.write("🔍 DEBUG - Forms Verified values:")
    #st.write(f"Min: {filtered_patients['forms_verified'].min()}")
    #st.write(f"Max: {filtered_patients['forms_verified'].max()}")
    #st.write(f"Mean: {filtered_patients['forms_verified'].mean()}")
    #st.write(f"Sum: {filtered_patients['forms_verified'].sum()}")
    #st.write(f"Count: {len(filtered_patients)}")
    
    # Key Metrics Cards - RESPONSIVE
    st.markdown("### 📊 Key Performance Indicators")
    
    # Check if mobile
    mobile = is_mobile()
    
    # Adjust number of columns based on device
    num_metric_cols = 2 if mobile else 4
    metric_cols = st.columns(num_metric_cols)
    
    # If mobile, show metrics in 2 columns with different arrangement
    if mobile:
        # Column 1 on mobile
        with metric_cols[0]:
            # Total Patients Card
            total_patients = summary['total_patients']
            active_patients = len(filtered_patients[filtered_patients['subject_status']
                              == 'Active']) if 'subject_status' in filtered_patients.columns else 0
            delta = f"+{int(total_patients * 0.1)}" if total_patients > 0 else "0"
            st.markdown(create_metric_card(
                "Total Patients",
                f"{total_patients:,}",
                delta=delta,
                status="primary",
                icon="👥"
            ), unsafe_allow_html=True)
            st.caption(f"📈 {active_patients} active")
        
        # Column 2 on mobile  
        with metric_cols[1]:
            # Clean Patients Card
            clean_pct = summary['clean_percentage']
            clean_count = summary['clean_patients']
            status = "good" if clean_pct >= 70 else (
                "warning" if clean_pct >= 50 else "critical")
            st.markdown(create_metric_card(
                "Clean Patients",
                f"{clean_pct}%",
                status=status,
                progress=clean_pct,
                icon="✅"
            ), unsafe_allow_html=True)
            st.caption(f"🎯 Target: 70%")
    
    else:  # Desktop - show all 4 metrics
        with metric_cols[0]:
            # Total Patients Card
            total_patients = summary['total_patients']
            active_patients = len(filtered_patients[filtered_patients['subject_status']
                              == 'Active']) if 'subject_status' in filtered_patients.columns else 0
            delta = f"+{int(total_patients * 0.1)}" if total_patients > 0 else "0"
            st.markdown(create_metric_card(
                "Total Patients",
                f"{total_patients:,}",
                delta=delta,
                status="primary",
                icon="👥"
            ), unsafe_allow_html=True)
            st.caption(f"📈 {active_patients} active patients")
        
        with metric_cols[1]:
            # Clean Patients Card
            clean_pct = summary['clean_percentage']
            clean_count = summary['clean_patients']
            status = "good" if clean_pct >= 70 else (
                "warning" if clean_pct >= 50 else "critical")
            st.markdown(create_metric_card(
                "Clean Patients",
                f"{clean_pct}%",
                status=status,
                progress=clean_pct,
                icon="✅"
            ), unsafe_allow_html=True)
            st.caption(f"🎯 Target: 70% • Current: {clean_count} patients")
        
        with metric_cols[2]:
            # Average DQI Card
            avg_dqi = summary['avg_dqi']
            dqi_status = "good" if avg_dqi >= 75 else (
                "warning" if avg_dqi >= 60 else "critical")
            trend = "▲ 2.5" if avg_dqi > 70 else ("▼ 1.2" if avg_dqi < 60 else "━")
            st.markdown(create_metric_card(
                "Average DQI",
                f"{avg_dqi:.1f}",
                delta=trend,
                status=dqi_status,
                icon="📊"
            ), unsafe_allow_html=True)
            st.caption(f"Score range: 0-100 • Threshold: 75")
        
        with metric_cols[3]:
            # Open Issues Card
            total_issues = summary['total_open_queries'] + \
                summary['total_safety_issues']
            safety_issues = summary['total_safety_issues']
            status = "critical" if safety_issues > 0 else (
                "warning" if total_issues > 20 else "good")
            st.markdown(create_metric_card(
                "Open Issues",
                f"{total_issues:,}",
                status=status,
                icon="🚨"
            ), unsafe_allow_html=True)
            st.caption(
                f"🔴 {safety_issues} safety • 🟡 {summary['total_open_queries']} queries")

    st.markdown("---")

    # Main Tabs - adjust based on device
    mobile = is_mobile()
    
    if mobile:
        # For mobile, use shorter tab names
        tab_labels = ["📈 Perf", "👥 Patients", "🏥 Sites", "🚨 Risk", "🤖 AI", "🧬 Disease"]
        tab1, tab2, tab3, tab4, tab5= st.tabs(tab_labels)
    else:
        # For desktop, use full names
        tab_labels = [
            "📈 Performance Dashboard",
            "👥 Patient Management",
            "🏥 Site Analytics",
            "🚨 Risk Monitoring",
            "🤖 AI Insights",
            
        ]
        tab1, tab2, tab3, tab4, tab5= st.tabs(tab_labels)
    
    # ... rest of your tabs code continues ...

        # TAB 1: Performance Dashboard
    with tab1:
        st.header("Performance Analytics")
        
        # Show filter status clearly
        if len(filtered_patients) != len(patients):
            st.success(f"✅ Filters active: Showing {len(filtered_patients)} of {len(patients)} patients")
        
        # Create visualizations (using FILTERED data for charts)
        fig1, fig2, fig3 = create_visualizations(filtered_patients, sites)

        # Row 1: Charts
        col1, col2 = st.columns([3, 2])

        with col1:
            st.plotly_chart(fig1, width='stretch')

        with col2:
            st.plotly_chart(fig2, width='stretch')

        # Row 2: Heatmap
        st.plotly_chart(fig3, width='stretch')

        # Row 3: Quick stats (using FILTERED data)
        st.subheader("📋 Quick Statistics (Filtered Data)")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_visits = filtered_patients['visits_completed'].mean(
            ) if 'visits_completed' in filtered_patients.columns else 0
            st.metric("Avg Visits Completed", f"{avg_visits:.1f}")

        with col2:
            query_resolution = (filtered_patients['queries_resolved'].sum() / filtered_patients['total_queries'].sum(
            ) * 100) if 'total_queries' in filtered_patients.columns and filtered_patients['total_queries'].sum() > 0 else 0
            st.metric("Query Resolution", f"{query_resolution:.1f}%")

        with col3:
            if 'forms_verified' in filtered_patients.columns:
                # If values are already 0-100%, just take mean
                forms_verified = filtered_patients['forms_verified'].mean()
                
                # If mean is > 100, values are wrong - cap at 100
                if forms_verified > 100:
                    forms_verified = 100
            else:
                forms_verified = 0
            st.metric("Forms Verified", f"{forms_verified:.1f}%")

        with col4:
            protocol_deviations = filtered_patients['protocol_deviations'].sum(
            ) if 'protocol_deviations' in filtered_patients.columns else 0
            st.metric("Protocol Deviations", protocol_deviations)
        
        # ========== DATABASE OVERVIEW ==========
        st.subheader("📋 Complete Database Overview")
        
        # Show TOTAL database counts
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Patients", len(patients))
        with col2:
            total_active = len(patients[patients['subject_status'] == 'Active']) if 'subject_status' in patients.columns else 0
            st.metric("Active Patients", total_active)
        with col3:
            total_clean = len(patients[patients['clean_status'] == 'Clean']) if 'clean_status' in patients.columns else 0
            st.metric("Clean Patients", total_clean)
        with col4:
            total_high_risk = len(patients[patients['risk_level'] == 'High']) if 'risk_level' in patients.columns else 0
            st.metric("High Risk Patients", total_high_risk)
        
        # Show ALL PATIENTS with pagination
        st.subheader("👥 Complete Patient Database")
        
        # Add search for ALL patients
        search_all = st.text_input("🔍 Search all patients...", 
                                 placeholder="Search in entire database",
                                 key="search_all_patients")
        
        if search_all and len(search_all) > 0:
            search_mask = patients.apply(
                lambda row: search_all.lower() in str(row).lower(), axis=1
            )
            display_all_patients = patients[search_mask]
        else:
            display_all_patients = patients
        
        # Select columns to show - CHECK WHICH COLUMNS EXIST
        # Common patient columns that should exist
        available_columns = []
        possible_columns = ['patient_id', 'site_id', 'subject_status', 
                           'clean_status', 'dqi_score', 'risk_level', 
                           'missing_visits', 'open_queries', 'visits_completed',
                           'total_queries', 'safety_issues']
        
        # Check which columns actually exist in the data
        for col in possible_columns:
            if col in patients.columns:
                available_columns.append(col)
        
        # If no columns found, use a basic set
        if not available_columns:
            available_columns = list(patients.columns[:5])  # First 5 columns
        
        # Show ALL patients with responsive container
        st.markdown(f"**Total records:** {len(display_all_patients)} patients")
        
        # Add pagination for all patients
        if len(display_all_patients) > 0:
            # Rows per page selector
            rows_per_page_all = st.selectbox("Rows per page:", 
                                           [10, 25, 50, 100, 250, 500],
                                           key="rows_per_page_all",
                                           index=3)  # Default to 100
            
            # Calculate pagination
            total_pages_all = max(1, (len(display_all_patients) // rows_per_page_all) + 1)
            page_all = st.number_input("Page:", 
                                     min_value=1, 
                                     max_value=total_pages_all,
                                     value=1,
                                     key="page_all")
            
            start_idx_all = (page_all - 1) * rows_per_page_all
            end_idx_all = min(start_idx_all + rows_per_page_all, len(display_all_patients))
            
            # Display ALL patients table with error handling
            try:
                st.markdown("""
                <div style="overflow-x: auto; margin: 0 -1rem; padding: 0 1rem;">
                """, unsafe_allow_html=True)
                
                st.dataframe(
                    display_all_patients.iloc[start_idx_all:end_idx_all][available_columns],
                    #width='stretch',
                    height=400
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.caption(f"Showing patients {start_idx_all + 1} to {end_idx_all} of {len(display_all_patients)}")
                
            except Exception as e:
                st.error(f"Error displaying data: {e}")
                # Show raw data as fallback
                st.write("Showing raw data (first 100 rows):")
                st.dataframe(display_all_patients.head(100))
            
            # Download all data button
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Download All Patients (CSV)", key="download_all"):
                    csv_all = display_all_patients.to_csv(index=False)
                    st.download_button(
                        label="Click to Download",
                        data=csv_all,
                        file_name="all_patients_database.csv",
                        mime="text/csv",
                        key="download_all_btn"
                    )
            
            with col2:
                if st.button("📊 Export All to Excel", key="export_all_excel"):
                    display_all_patients.to_excel('all_patients_database.xlsx', index=False)
                    st.success("✅ All patients exported to Excel!")
        
        # Show what percentage is filtered
        if len(filtered_patients) != len(patients):
            filter_percentage = (len(filtered_patients) / len(patients)) * 100
            st.info(f"📊 **Current filtered view:** {len(filtered_patients)} patients ({filter_percentage:.1f}% of total database)")
            
    # TAB 2: Patient Management
    with tab2:
        st.header("Patient Management")

        # Search and controls
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            search_query = st.text_input(
                "🔍 Search patients...", placeholder="Search by ID, site, or status")

        with col2:
            items_per_page = st.selectbox("Rows per page", [10, 25, 50, 100])

        with col3:
            if st.button("📋 Column Toggles"):
                st.session_state['show_column_toggles'] = not st.session_state.get(
                    'show_column_toggles', False)

        # Apply search
        if search_query and len(search_query) > 0:
            search_mask = filtered_patients.apply(
                lambda row: search_query.lower() in str(row).lower(), axis=1
            )
            display_patients = filtered_patients[search_mask]
        else:
            display_patients = filtered_patients

        # Column selection
        if st.session_state.get('show_column_toggles', False):
            st.subheader("Select Columns to Display")
            all_columns = display_patients.columns.tolist()
            default_columns = ['patient_id', 'site_id', 'subject_status',
                               'clean_status', 'dqi_score', 'risk_level']
            selected_columns = st.multiselect(
                "Choose columns",
                options=all_columns,
                default=default_columns
            )
        else:
            selected_columns = ['patient_id', 'site_id', 'subject_status',
                                'clean_status', 'dqi_score', 'risk_level', 'missing_visits', 'open_queries']

        # Display data table
        if len(display_patients) > 0:
            display_cols = [
                col for col in selected_columns if col in display_patients.columns]

            # Sort options - THIS MUST COME BEFORE USING sorted_df
            sort_by = st.selectbox("Sort by", options=display_cols, index=display_cols.index(
                'dqi_score') if 'dqi_score' in display_cols else 0)
            sort_order = st.radio(
                "Order", ["Descending", "Ascending"], horizontal=True)

            sorted_df = display_patients.sort_values(
                sort_by,
                ascending=(sort_order == "Ascending")
            )

            # Pagination
            total_rows = len(sorted_df)
            page_number = st.number_input("Page", min_value=1, value=1, max_value=max(
                1, (total_rows // items_per_page) + 1))
            
            start_idx = (page_number - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_rows)

            # Display table with responsive container - ONLY ONCE
            st.markdown("""
            <div style="overflow-x: auto; margin: 0 -1rem; padding: 0 1rem;">
            """, unsafe_allow_html=True)
            
            st.dataframe(
                sorted_df.iloc[start_idx:end_idx][display_cols],
                #width='stretch',
                height=400
            )
            
            st.markdown("</div>", unsafe_allow_html=True)

            st.caption(
                f"Showing rows {start_idx + 1} to {end_idx} of {total_rows}")

            # Export options
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Export to Excel", width='stretch'):
                    sorted_df[display_cols].to_excel(
                        'patient_data.xlsx', index=False)
                    st.success("✅ Exported to patient_data.xlsx")
                    
            with col2:
                csv = sorted_df[display_cols].to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="patient_data.csv",
                    mime="text/csv",
                    width='stretch'
                )
                
    # TAB 3: Site Analytics
    with tab3:
        st.header("Site Performance Analytics")

        if not sites.empty and len(sites) > 0:
            # Site comparison grid
            st.subheader("Site Comparison")

            available_cols = []
            for col in ['site_id', 'region', 'total_patients_enrolled',
                        'clean_percentage', 'avg_dqi', 'total_open_queries',
                        'performance_status']:
                if col in sites.columns:
                    available_cols.append(col)

            if available_cols:
                metrics_grid = sites[available_cols].copy()

                if 'clean_percentage' in metrics_grid.columns:
                    metrics_grid['clean_percentage'] = metrics_grid['clean_percentage'].apply(
                        lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
                    )

                if 'avg_dqi' in metrics_grid.columns:
                    metrics_grid['avg_dqi'] = metrics_grid['avg_dqi'].apply(
                        lambda x: f"{x:.1f}" if pd.notna(x) else "N/A"
                    )

                st.dataframe(
                    metrics_grid, width='stretch', height=300)

            # Site drill-down
            st.subheader("Site Drill-down Analysis")

            if 'site_id' in sites.columns:
                site_options = sorted(sites['site_id'].unique())
                selected_site = st.selectbox(
                    "Select site for detailed analysis",
                    options=site_options
                )

                if selected_site:
                    site_info = sites[sites['site_id'] == selected_site]
                    if not site_info.empty:
                        site_row = site_info.iloc[0]
                        site_patients = filtered_patients[filtered_patients['site_id']
                                                          == selected_site]

                        # Site details in columns
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Total Patients", site_row.get(
                                'total_patients_enrolled', 0))
                            st.metric("Active Patients", len(
                                site_patients[site_patients['subject_status'] == 'Active']) if 'subject_status' in site_patients.columns else 0)

                        with col2:
                            st.metric(
                                "Clean Percentage", f"{site_row.get('clean_percentage', 0):.1f}%")
                            st.metric(
                                "Avg DQI", f"{site_row.get('avg_dqi', 0):.1f}")

                        with col3:
                            st.metric("Open Issues", site_row.get(
                                'total_open_queries', 0))
                            st.metric("Safety Issues", site_row.get(
                                'total_safety_issues', 0))

    # TAB 4: Risk Monitoring
    with tab4:
        st.header("Risk Monitoring & Alerts")

        # Risk Matrix
        st.subheader("📊 Risk Matrix")

        if 'risk_level' in filtered_patients.columns and 'clean_status' in filtered_patients.columns:
            risk_matrix = filtered_patients.groupby(
                ['risk_level', 'clean_status']).size().unstack(fill_value=0)

            fig_risk = go.Figure(data=go.Heatmap(
                z=risk_matrix.values,
                x=risk_matrix.columns,
                y=risk_matrix.index,
                colorscale='Reds',
                text=risk_matrix.values,
                texttemplate='%{text}',
                textfont={"size": 14},
                hoverinfo='text'
            ))

            fig_risk.update_layout(
                height=300,
                title="Risk Level vs Clean Status Matrix",
                xaxis_title="Clean Status",
                yaxis_title="Risk Level"
            )

            st.plotly_chart(fig_risk)

    # TAB 5: AI Insights
    with tab5:
        st.header("AI-Powered Insights & Reports")

        # Predictive analytics
        st.subheader("📈 Predictive Analytics")

        col1, col2 = st.columns(2)

        with col1:
            # Enrollment prediction - FIXED
            st.markdown("#### Enrollment Forecast")
            current = summary['total_patients']
            target = DEFAULT_TRIAL['target_patients']
            
            # Calculate progress, but CAP at 100%
            progress = min((current / target) * 100, 100)  # <-- ADDED min() function
            
            # Show warning if over-enrolled
            if current > target:
                st.warning(f"⚠️ Over-enrolled by {current - target} patients")

            fig_enroll = go.Figure(go.Indicator(
                mode="gauge+number",
                value=progress,
                title={'text': "Enrollment Progress"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#1f3c88"},
                    'steps': [
                        {'range': [0, 70], 'color': "#f8d7da"},
                        {'range': [70, 90], 'color': "#fff3cd"},
                        {'range': [90, 100], 'color': "#d4edda"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                }
            ))
            
            fig_enroll.update_layout(height=250)  # <-- KEEP THIS, it belongs to fig_enroll
            st.plotly_chart(fig_enroll)  # <-- KEEP THIS, it belongs to col1

        with col2:
            # Risk prediction
            st.markdown("#### Risk Prediction")
            
            if 'risk_level' in filtered_patients.columns:
                risk_counts = filtered_patients['risk_level'].value_counts()
                total = len(filtered_patients)
                
                # Calculate percentages
                risk_data = {
                    'Low': (risk_counts.get('Low', 0) / total * 100),
                    'Medium': (risk_counts.get('Medium', 0) / total * 100),
                    'High': (risk_counts.get('High', 0) / total * 100)
                }
                
                fig_risk = go.Figure(data=[go.Bar(
                    x=list(risk_data.keys()),
                    y=list(risk_data.values()),
                    marker_color=['#28a745', '#ffc107', '#dc3545'],  # Green, Yellow, Red
                    text=[f"{v:.1f}%" for v in risk_data.values()],
                    textposition='auto',
                )])
                
                fig_risk.update_layout(
                    height=250,
                    title="Patient Risk Distribution",
                    yaxis_title="Percentage (%)",
                    yaxis_range=[0, 100]
                )
                
                st.plotly_chart(fig_risk, width='stretch')
            else:
                st.info("Risk level data not available")

        # Add another row for more AI insights
        st.markdown("---")
        st.subheader("📊 Predictive Analytics")

        col3, col4 = st.columns(2)

        with col3:
            # DQI Trend Prediction
            st.markdown("#### DQI Trend Forecast")
            
            if 'dqi_score' in filtered_patients.columns:
                # Simple trend calculation
                avg_dqi = filtered_patients['dqi_score'].mean()
                predicted = min(avg_dqi + 2.5, 100)  # Predict slight improvement
                
                fig_trend = go.Figure(go.Indicator(
                    mode="number+delta",
                    value=predicted,
                    delta={'reference': avg_dqi, 'position': "top"},
                    title={'text': "Predicted DQI (Next Month)"},
                    domain={'x': [0, 1], 'y': [0, 1]}
                ))
                
                fig_trend.update_layout(height=215)
                st.plotly_chart(fig_trend)
            else:
                st.info("DQI data not available")

        with col4:
            # Site Performance Prediction
            st.markdown("#### Site Performance Alert")
            
            if not sites.empty and 'performance_status' in sites.columns:
                poor_sites = sites[sites['performance_status'].isin(['Poor', 'Needs Improvement'])]
                
                if len(poor_sites) > 0:
                    st.error(f"🚨 {len(poor_sites)} sites need attention")
                    for idx, site in poor_sites.iterrows():
                        st.write(f"• **{site['site_id']}**: {site.get('performance_status', 'N/A')}")
                else:
                    st.success("✅ All sites performing well")
            else:
                st.info("Site performance data not available")
        
        # REMOVED THE DUPLICATE LINES - THEY WERE OUTSIDE ANY COLUMN AND REPEATING FIG_ENROLL
       
    # Footer
    st.markdown("---")
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    st.markdown(f"""
    <div style="text-align: center; color: #6c757d; font-size: 12px; padding: 20px;">
        <strong>Clinical Intelligence Platform v1.0</strong> • Secure Clinical Trial Management • 
        <a href="#" style="color: #1f3c88; text-decoration: none;">Help Center</a> • 
        <a href="#" style="color: #1f3c88; text-decoration: none;">Documentation</a> • 
        <a href="#" style="color: #1f3c88; text-decoration: none;">Privacy Policy</a>
        <br>
        Last updated: {current_time}
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main_dashboard()
