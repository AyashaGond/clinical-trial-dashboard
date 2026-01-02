# app.py - PROFESSIONAL VERSION
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta  # ← ADD THIS
import sys
import os
# ADD THESE LINES after other imports (around line 10)
import plotly.graph_objects as go
import plotly.express as px

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import project modules
from config import TRIAL_INFO
from calculations import load_and_process_data
from utils.helpers import DataHelper
from login import main_login

# Page configuration
st.set_page_config(
    page_title="Clinical Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.novartis.com',
        'Report a bug': None,
        'About': "Clinical Trial Intelligence Dashboard v1.0"
    }
)

# Custom CSS for professional interface
st.markdown("""
<style>
    /* Main container styling */
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
    
    /* Metrics cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #1a1a1a;
        margin: 5px 0;
    }
    
    .metric-label {
        font-size: 14px;
        color: #666;
        font-weight: 500;
    }
    
    .metric-trend {
        font-size: 12px;
        padding: 2px 8px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 5px;
    }
    
    .trend-up { background: #d4edda; color: #155724; }
    .trend-down { background: #f8d7da; color: #721c24; }
    .trend-neutral { background: #e2e3e5; color: #383d41; }
    
    /* Status indicators */
    .status-good { border-color: #28a745; }
    .status-warning { border-color: #ffc107; }
    .status-critical { border-color: #dc3545; }
    .status-info { border-color: #17a2b88; }
    
    /* Progress bars */
    .progress-container {
        background: #e9ecef;
        height: 8px;
        border-radius: 4px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 4px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #f8f9fa;
        padding: 5px;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 6px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #1f3c88;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Data table styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #dee2e6;
    }
    
    /* Remove Streamlit hamburger menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Make sidebar more visible */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 1px solid #dee2e6;
    }
    
    /* Sidebar section headers */
    .stSidebar h3 {
        color: #1f3c88;
        font-weight: 600;
        margin-top: 20px;
    }
    
    /* Sidebar widgets */
    .stSidebar .stSelectbox,
    .stSidebar .stMultiselect,
    .stSidebar .stSlider,
    .stSidebar .stRadio,
    .stSidebar .stDateInput {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 8px;
    }
    
    /* Ensure sidebar is wide enough */
    section[data-testid="stSidebar"] > div {
        padding: 20px;
        min-width: 280px !important;
    }
    
    /* Better sidebar toggle visibility */
    button[title="View fullscreen"] {
        background: #1f3c88;
        color: white;
        border-radius: 50%;
    }
    
    .navbar {
    background: white;
    padding: 15px 25px;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 20px;
    font-weight: 700;
    color: #1f3c88;
}

.user-profile {
    display: flex;
    align-items: center;
    gap: 15px;
}

.user-badge {
    background: #e9ecef;
    padding: 5px 12px;
    border-radius: 15px;
    font-size: 12px;
    font-weight: 600;
}

.notification-bell {
    position: relative;
    cursor: pointer;
    font-size: 20px;
}

.notification-count {
    position: absolute;
    top: -5px;
    right: -5px;
    background: #dc3545;
    color: white;
    font-size: 10px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache data"""
    return load_and_process_data()

    # Data Summary Section - ADD THIS
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Data Summary")
    
    # Show data statistics
    if not patients.empty:
        total_patients = len(patients)
        clean_patients = len(patients[patients['clean_status'] == 'Clean']) if 'clean_status' in patients.columns else 0
        active_patients = len(patients[patients['subject_status'] == 'Active']) if 'subject_status' in patients.columns else 0
        
        st.sidebar.info(f"""
        **Dataset Summary:**
        • **Total Patients:** {total_patients}
        • **Active Patients:** {active_patients}
        • **Clean Patients:** {clean_patients} ({(clean_patients/total_patients*100):.1f}%)
        • **Sites:** {len(patients['site_id'].unique()) if 'site_id' in patients.columns else 0}
        • **Queries:** {patients['open_queries'].sum() if 'open_queries' in patients.columns else 0}
        """)

def create_metric_card(title, value, delta=None, status="info", progress=None):
    """Create a professional metric card"""
    status_colors = {
        "good": "#28a745",
        "warning": "#ffc107", 
        "critical": "#dc3545",
        "info": "#17a2b8"
    }
    
    status_class = f"status-{status}"
    border_color = status_colors.get(status, "#17a2b8")
    
    card_html = f"""
    <div class="metric-card {status_class}" style="border-left-color: {border_color};">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
    """
    
    if delta:
        trend_class = "trend-up" if "+" in str(delta) else "trend-down"
        card_html += f'<div class="metric-trend {trend_class}">{delta}</div>'
    
    if progress is not None:
        progress_width = min(max(progress, 0), 100)
        progress_color = "#28a745" if progress >= 70 else ("#ffc107" if progress >= 50 else "#dc3545")
        card_html += f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress_width}%; background: {progress_color};"></div>
        </div>
        """
    
    card_html += "</div>"
    return card_html

def create_navigation_bar(user):
    """Create professional navigation bar using Streamlit native components"""
    
    # Create a container for the navbar
    navbar = st.container()
    
    with navbar:
        # Create columns for layout
        col1, col2, col3 = st.columns([2, 3, 2])
        
        with col1:
            # Logo and title
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 24px;">🏥</span>
                <span style="font-size: 20px; font-weight: 700; color: #1f3c88;">
                    Clinical Intelligence
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Right side: notifications and user info
            user_col1, user_col2, user_col3 = st.columns([1, 2, 1])
            
            with user_col1:
                # Notification bell with badge
                st.markdown("""
                <div style="position: relative; display: inline-block;">
                    <span style="font-size: 18px;">🔔</span>
                    <span style="position: absolute; top: -8px; right: -8px; background: #dc3545; 
                           color: white; font-size: 10px; width: 18px; height: 18px; border-radius: 50%; 
                           display: flex; align-items: center; justify-content: center; font-weight: bold;">
                        3
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with user_col2:
                # User info
                st.markdown(f"""
                <div style="text-align: right;">
                    <div style="font-weight: 600; font-size: 14px;">{user.get('name', 'System Administrator')}</div>
                    <div style="background: #e9ecef; padding: 3px 10px; border-radius: 12px; 
                         font-size: 11px; font-weight: 600; display: inline-block;">
                        {user.get('role', 'Admin')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with user_col3:
                # Logout button using Streamlit button
                if st.button("🚪", help="Logout", key="navbar_logout"):
                    st.session_state['logout_clicked'] = True
    
    # Add separator after navbar
    st.markdown("---")
    
    # Handle logout
    if st.session_state.get('logout_clicked', False):
        # Clear session and rerun
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
                    
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
                    mode='lines',
                    name=site,
                    line=dict(width=2)
                ))
                site_count += 1
        
        if site_count > 0:
            fig1.update_layout(
                title="DQI Trends by Site",
                height=300,
                xaxis_title="Patient Rank",
                yaxis_title="DQI Score",
                hovermode='x unified',
                template='plotly_white'
            )
        else:
            # Empty figure with message
            fig1.add_annotation(
                text="No data available for DQI trends",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    else:
        # Empty figure with message
        fig1.add_annotation(
            text="DQI data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # 2. Clean Status Pie Chart
    if 'clean_status' in patients.columns and len(patients) > 0:
        clean_counts = patients['clean_status'].value_counts()
        if len(clean_counts) > 0:
            fig2 = px.pie(
                values=clean_counts.values,
                names=clean_counts.index,
                title="Clean Status Distribution",
                color=clean_counts.index,
                color_discrete_map={'Clean': '#28a745', 'Not Clean': '#dc3545'},
                hole=0.4
            )
            fig2.update_layout(height=300)
        else:
            fig2.add_annotation(
                text="No clean status data",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
    else:
        fig2.add_annotation(
            text="Clean status data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    # 3. Site Performance Heatmap
    if not sites.empty and 'avg_dqi' in sites.columns and len(sites) > 0:
        fig3 = go.Figure(data=go.Heatmap(
            z=[sites['avg_dqi'].values],
            x=sites['site_id'].values,
            y=['DQI Score'],
            colorscale='RdYlGn',
            zmin=0,
            zmax=100,
            text=[sites['avg_dqi'].values],
            texttemplate='%{text:.1f}',
            textfont={"size": 14},
            hoverinfo='text',
            hovertext=[f"Site: {site}<br>DQI: {dqi:.1f}" for site, dqi in zip(sites['site_id'], sites['avg_dqi'])]
        ))
        fig3.update_layout(
            title="Site Performance Heatmap",
            height=200,
            xaxis_title="Site",
            margin=dict(l=20, r=20, t=40, b=20)
        )
    else:
        # Empty figure with message
        fig3 = go.Figure()
        fig3.add_annotation(
            text="Site performance data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        fig3.update_layout(height=200)
    
    return fig1, fig2, fig3

def main_dashboard():
    """Main dashboard function"""
    
    # Check login
    if not main_login():
        return
    
    user = st.session_state.get('user', {})
    
    # Navigation Bar
    create_navigation_bar(user)
    
    # Logout functionality
    if st.session_state.get('logout_btn', False):
        from login import LoginSystem
        login_system = LoginSystem()
        login_system.logout()
        st.session_state['logged_in'] = False
        st.rerun()
    
    # Load data
    with st.spinner("🔄 Loading clinical trial data..."):
        try:
            patients, sites, queries = load_data()
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.info("Please run 'python data_generator.py' first")
            return
    
    if patients.empty:
        st.warning("📊 No patient data found. Generating sample data...")
        return
    
    # Sidebar Filters
    with st.sidebar:
        st.markdown("### 🔍 Filters & Controls")
        
        # Site selection
        st.markdown("**Site Selection**")
        if 'site_id' in patients.columns:
            site_options = patients['site_id'].unique()
            selected_sites = st.multiselect(
                "Select sites",
                options=site_options,
                default=site_options[:3],
                label_visibility="collapsed"
            )
        else:
            selected_sites = []
        
        # Patient status
        st.markdown("**Patient Status**")
        if 'subject_status' in patients.columns:
            status_options = patients['subject_status'].unique()
            selected_status = st.multiselect(
                "Filter by status",
                options=status_options,
                default=['Active', 'Completed'],
                label_visibility="collapsed"
            )
        else:
            selected_status = []
        
        # Clean status toggle
        st.markdown("**Clean Status**")
        clean_filter = st.radio(
            "Show patients",
            options=['All', 'Clean Only', 'Issues Only'],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Risk level selector
        st.markdown("**Risk Level**")
        if 'risk_level' in patients.columns:
            risk_options = patients['risk_level'].unique()
            risk_filter = st.multiselect(
                "Select risk levels",
                options=risk_options,
                default=risk_options,
                label_visibility="collapsed"
            )
        else:
            risk_filter = []
        
        # DQI range slider
        st.markdown("**DQI Score Range**")
        if 'dqi_score' in patients.columns:
            min_dqi = int(patients['dqi_score'].min())
            max_dqi = int(patients['dqi_score'].max())
            dqi_range = st.slider(
                "Adjust DQI range",
                min_value=min_dqi,
                max_value=max_dqi,
                value=(max(min_dqi, 50), min(max_dqi, 100)),
                label_visibility="collapsed"
            )
        else:
            dqi_range = (0, 100)
        
        # Date range picker
        st.markdown("**Date Range**")
        if 'enrollment_date' in patients.columns:
            try:
                patients['enrollment_date'] = pd.to_datetime(patients['enrollment_date'])
                min_date = patients['enrollment_date'].min().date()
                max_date = patients['enrollment_date'].max().date()
                
                date_range = st.date_input(
                    "Select date range",
                    value=(min_date, max_date),
                    label_visibility="collapsed"
                )
            except:
                date_range = (datetime.now().date() - timedelta(days=365), datetime.now().date())
        else:
            date_range = (datetime.now().date() - timedelta(days=365), datetime.now().date())
        
        st.markdown("---")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        with col2:
            if st.button("📥 Export", use_container_width=True):
                patients.to_csv('clinical_trial_export.csv', index=False)
                st.success("✅ Data exported!")
        
        # Trial info in sidebar
        st.markdown("---")
        with st.expander("📋 Trial Information", expanded=False):
            st.info(f"""
            **Therapeutic Area:** {TRIAL_INFO['therapeutic_area']}
            **Phase:** {TRIAL_INFO['phase']}
            **Target Enrollment:** {TRIAL_INFO['target_patients']}
            **Duration:** {TRIAL_INFO['start_date']} to {TRIAL_INFO['expected_end_date']}
            **User Role:** {user.get('role', 'User')}
            """)
    
    # Apply filters
    filtered_patients = patients.copy()
    
    if selected_sites and len(selected_sites) > 0:
        filtered_patients = filtered_patients[filtered_patients['site_id'].isin(selected_sites)]
    
    if selected_status and len(selected_status) > 0:
        filtered_patients = filtered_patients[filtered_patients['subject_status'].isin(selected_status)]
    
    if clean_filter == 'Clean Only':
        filtered_patients = filtered_patients[filtered_patients['clean_status'] == 'Clean']
    elif clean_filter == 'Issues Only':
        filtered_patients = filtered_patients[filtered_patients['clean_status'] == 'Not Clean']
    
    if risk_filter and len(risk_filter) > 0:
        filtered_patients = filtered_patients[filtered_patients['risk_level'].isin(risk_filter)]
    
    if 'dqi_score' in filtered_patients.columns:
        filtered_patients = filtered_patients[
            (filtered_patients['dqi_score'] >= dqi_range[0]) & 
            (filtered_patients['dqi_score'] <= dqi_range[1])
        ]
    
    # Calculate metrics
    summary = DataHelper.calculate_summary_statistics(filtered_patients)
    
    # Header
    st.markdown(f'<div class="main-header">🏥 Clinical Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Real-time monitoring and analytics for clinical trials • Role: {user.get("role", "User")}</div>', unsafe_allow_html=True)
    
    # Key Metrics Cards (4-column layout)
    st.markdown("### 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Total Patients Card
        total_patients = summary['total_patients']
        active_patients = len(filtered_patients[filtered_patients['subject_status'] == 'Active']) if 'subject_status' in filtered_patients.columns else 0
        delta = f"+{int(total_patients * 0.1)}" if total_patients > 0 else "0"
        st.markdown(create_metric_card(
            "Total Patients", 
            f"{total_patients:,}",
            delta=delta,
            status="info"
        ), unsafe_allow_html=True)
        st.caption(f"📈 {active_patients} active patients")
    
    with col2:
        # Clean Patients Card
        clean_pct = summary['clean_percentage']
        clean_count = summary['clean_patients']
        status = "good" if clean_pct >= 70 else ("warning" if clean_pct >= 50 else "critical")
        st.markdown(create_metric_card(
            "Clean Patients",
            f"{clean_pct}%",
            status=status,
            progress=clean_pct
        ), unsafe_allow_html=True)
        st.caption(f"🎯 Target: 70% • Current: {clean_count} patients")
    
    with col3:
        # Average DQI Card
        avg_dqi = summary['avg_dqi']
        dqi_status = "good" if avg_dqi >= 75 else ("warning" if avg_dqi >= 60 else "critical")
        trend = "▲ 2.5" if avg_dqi > 70 else ("▼ 1.2" if avg_dqi < 60 else "━")
        st.markdown(create_metric_card(
            "Average DQI",
            f"{avg_dqi:.1f}",
            delta=trend,
            status=dqi_status
        ), unsafe_allow_html=True)
        st.caption(f"📊 Score range: 0-100 • Threshold: 75")
    
    with col4:
        # Open Issues Card
        total_issues = summary['total_open_queries'] + summary['total_safety_issues']
        safety_issues = summary['total_safety_issues']
        status = "critical" if safety_issues > 0 else ("warning" if total_issues > 20 else "good")
        st.markdown(create_metric_card(
            "Open Issues",
            f"{total_issues:,}",
            status=status
        ), unsafe_allow_html=True)
        st.caption(f"🔴 {safety_issues} safety • 🟡 {summary['total_open_queries']} queries")
    
    st.markdown("---")
    
    # Main Tabs
    tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs([
        "📈 Performance Dashboard", 
        "👥 Patient Management",
        "🏥 Site Analytics",
        "🚨 Risk Monitoring",
        "🤖 AI Insights",
        "📊 Summary"  # ← NEW TAB
    ])
        
    # TAB 6: Data Summary
    with tab6:
        st.header("📊 Complete Data Summary")
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Patients", len(filtered_patients))
            st.caption(f"Active: {len(filtered_patients[filtered_patients['subject_status'] == 'Active'])}")
        
        with col2:
            clean_pct = (len(filtered_patients[filtered_patients['clean_status'] == 'Clean']) / len(filtered_patients)) * 100
            st.metric("Clean Patients", f"{clean_pct:.1f}%")
            st.caption(f"{len(filtered_patients[filtered_patients['clean_status'] == 'Clean'])} clean")
        
        with col3:
            avg_dqi = filtered_patients['dqi_score'].mean() if 'dqi_score' in filtered_patients.columns else 0
            st.metric("Avg DQI", f"{avg_dqi:.1f}")
            st.caption(f"Range: {filtered_patients['dqi_score'].min():.1f}-{filtered_patients['dqi_score'].max():.1f}")
        
        with col4:
            total_issues = filtered_patients['open_queries'].sum() if 'open_queries' in filtered_patients.columns else 0
            st.metric("Total Issues", total_issues)
            st.caption(f"Queries: {filtered_patients['open_queries'].sum()}")
        
        st.markdown("---")
        
        # Detailed metrics
        st.subheader("📈 Detailed Metrics")
        
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            # Visit metrics
            st.markdown("#### Visit Completion")
            avg_visits = filtered_patients['visits_completed'].mean() if 'visits_completed' in filtered_patients.columns else 0
            total_expected = filtered_patients['total_visits_expected'].sum() if 'total_visits_expected' in filtered_patients.columns else 0
            total_completed = filtered_patients['visits_completed'].sum() if 'visits_completed' in filtered_patients.columns else 0
            visit_completion = (total_completed / total_expected * 100) if total_expected > 0 else 0
            
            st.write(f"**Average visits per patient:** {avg_visits:.1f}")
            st.write(f"**Total visits completed:** {total_completed:,}")
            st.write(f"**Visit completion rate:** {visit_completion:.1f}%")
            
            # Page metrics
            st.markdown("#### Page Completion")
            avg_pages = filtered_patients['pages_completed'].mean() if 'pages_completed' in filtered_patients.columns else 0
            st.write(f"**Average pages per patient:** {avg_pages:.1f}")
        
        with metrics_col2:
            # Query metrics
            st.markdown("#### Query Analysis")
            total_queries = filtered_patients['total_queries'].sum() if 'total_queries' in filtered_patients.columns else 0
            open_queries = filtered_patients['open_queries'].sum() if 'open_queries' in filtered_patients.columns else 0
            resolved_queries = filtered_patients['queries_resolved'].sum() if 'queries_resolved' in filtered_patients.columns else 0
            resolution_rate = (resolved_queries / total_queries * 100) if total_queries > 0 else 0
            
            st.write(f"**Total queries:** {total_queries:,}")
            st.write(f"**Open queries:** {open_queries:,}")
            st.write(f"**Resolved queries:** {resolved_queries:,}")
            st.write(f"**Resolution rate:** {resolution_rate:.1f}%")
            
            # Safety metrics
            st.markdown("#### Safety Metrics")
            safety_issues = filtered_patients['safety_issues'].sum() if 'safety_issues' in filtered_patients.columns else 0
            adverse_events = filtered_patients['adverse_events'].sum() if 'adverse_events' in filtered_patients.columns else 0
            st.write(f"**Safety issues:** {safety_issues}")
            st.write(f"**Adverse events:** {adverse_events}")
        
        st.markdown("---")
        
        # Data quality summary
        st.subheader("🎯 Data Quality Summary")
        
        quality_metrics = [
            ("Forms Verified", 'forms_verified', True),
            ("Forms Signed", 'forms_signed', True),
            ("SDV Completed", 'sdv_completed', True),
            ("No Lab Issues", 'lab_issues', 0),
            ("No Protocol Deviations", 'protocol_deviations', 0)
        ]
        
        for metric_name, column, target_value in quality_metrics:
            if column in filtered_patients.columns:
                if isinstance(target_value, bool):
                    count = filtered_patients[column].sum()
                else:
                    count = len(filtered_patients[filtered_patients[column] == target_value])
                
                percentage = (count / len(filtered_patients)) * 100
                progress_color = "🟢" if percentage >= 80 else ("🟡" if percentage >= 60 else "🔴")
                
                st.write(f"{progress_color} **{metric_name}:** {percentage:.1f}% ({count}/{len(filtered_patients)})")
    # TAB 1: Performance Dashboard
    with tab1:
        st.header("Performance Analytics")
        
        # Create visualizations
        fig1, fig2, fig3 = create_visualizations(filtered_patients, sites)
        
        # Row 1: Charts
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
        
        # Row 2: Heatmap
        st.plotly_chart(fig3, use_container_width=True)
        
        # Row 3: Quick stats
        st.subheader("📋 Quick Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_visits = filtered_patients['visits_completed'].mean() if 'visits_completed' in filtered_patients.columns else 0
            st.metric("Avg Visits Completed", f"{avg_visits:.1f}")
        
        with col2:
            query_resolution = (filtered_patients['queries_resolved'].sum() / filtered_patients['total_queries'].sum() * 100) if 'total_queries' in filtered_patients.columns and filtered_patients['total_queries'].sum() > 0 else 0
            st.metric("Query Resolution", f"{query_resolution:.1f}%")
        
        with col3:
            forms_verified = (filtered_patients['forms_verified'].sum() / len(filtered_patients) * 100) if 'forms_verified' in filtered_patients.columns else 0
            st.metric("Forms Verified", f"{forms_verified:.1f}%")
        
        with col4:
            protocol_deviations = filtered_patients['protocol_deviations'].sum() if 'protocol_deviations' in filtered_patients.columns else 0
            st.metric("Protocol Deviations", protocol_deviations)
    
    # TAB 2: Patient Management
            # TAB 2: Patient Management
    with tab2:
        st.header("👥 Patient Management")
        
        # Show data statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Patients", len(filtered_patients))
        with col2:
            clean_count = len(filtered_patients[filtered_patients['clean_status'] == 'Clean'])
            st.metric("Clean Patients", clean_count)
        with col3:
            avg_dqi = filtered_patients['dqi_score'].mean() if 'dqi_score' in filtered_patients.columns else 0
            st.metric("Avg DQI", f"{avg_dqi:.1f}")
        with col4:
            total_queries = filtered_patients['open_queries'].sum() if 'open_queries' in filtered_patients.columns else 0
            st.metric("Open Queries", total_queries)
        
        st.markdown("---")
        
        # Column selector
        st.subheader("📋 Data Columns")
        
        # Define all possible columns
        all_columns = [
            # Basic Info
            'patient_id', 'subject_id', 'site_id', 'region', 
            'subject_status', 'enrollment_date', 'last_visit_date',
            
            # Visit Metrics
            'total_visits_expected', 'visits_completed', 'missing_visits',
            'visit_compliance_percentage', 'total_pages_expected', 
            'pages_completed', 'missing_pages', 'page_completion_percentage',
            
            # Query Metrics
            'total_queries', 'open_queries', 'queries_resolved',
            'query_resolution_percentage', 'query_age_days',
            
            # Data Quality
            'non_conformant_data', 'data_entry_errors', 'data_quality_percentage',
            'lab_issues', 'coding_backlog',
            
            # Safety
            'safety_issues', 'adverse_events', 'serious_adverse_events',
            'protocol_deviations',
            
            # Verification
            'forms_verified', 'forms_signed', 'sdv_completed', 'frozen_locked',
            'overdue_crfs',
            
            # Calculated
            'clean_status', 'dqi_score', 'risk_level'
        ]
        
        # Filter to only columns that exist
        existing_columns = [col for col in all_columns if col in filtered_patients.columns]
        
        # Default selected columns
        default_columns = [
            'patient_id', 'site_id', 'subject_status', 'clean_status',
            'dqi_score', 'risk_level', 'visits_completed', 'missing_visits',
            'open_queries', 'safety_issues', 'forms_verified'
        ]
        
        # Column selector
        selected_columns = st.multiselect(
            "Select columns to display",
            options=existing_columns,
            default=[col for col in default_columns if col in existing_columns],
            help="Choose which columns to show in the table"
        )
        
        # Search functionality
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            search_query = st.text_input(
                "🔍 Search patients...",
                placeholder="Search by ID, site, status, or any field"
            )
        
        with search_col2:
            items_per_page = st.selectbox(
                "Rows/page",
                [10, 25, 50, 100, 250],
                index=1
            )
        
        # Apply search
        if search_query and len(search_query) > 1:
            search_mask = filtered_patients.apply(
                lambda row: search_query.lower() in str(row).lower(), axis=1
            )
            display_df = filtered_patients[search_mask]
        else:
            display_df = filtered_patients
        
        # Show data count
        st.info(f"📊 **Displaying {len(display_df)} of {len(filtered_patients)} patients**")
        
        if len(display_df) > 0:
            # Sort options
            col1, col2 = st.columns(2)
            with col1:
                sort_by = st.selectbox(
                    "Sort by",
                    options=selected_columns,
                    index=selected_columns.index('dqi_score') if 'dqi_score' in selected_columns else 0
                )
            
            with col2:
                sort_order = st.radio(
                    "Sort order",
                    ["Descending ⬇️", "Ascending ⬆️"],
                    horizontal=True
                )
            
            # Sort data
            sorted_df = display_df.sort_values(
                sort_by,
                ascending=(sort_order == "Ascending ⬆️")
            )
            
            # Pagination
            total_pages = max(1, (len(sorted_df) + items_per_page - 1) // items_per_page)
            page_number = st.number_input(
                f"Page (1-{total_pages})",
                min_value=1,
                max_value=total_pages,
                value=1
            )
            
            start_idx = (page_number - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, len(sorted_df))
            
            # Display table
            st.dataframe(
                sorted_df.iloc[start_idx:end_idx][selected_columns],
                use_container_width=True,
                height=450
            )
            
            # Pagination info
            st.caption(f"📄 Showing patients {start_idx + 1} to {end_idx} of {len(sorted_df)}")
            
            # Export options
            st.markdown("---")
            st.subheader("📥 Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 Export to CSV", use_container_width=True):
                    sorted_df[selected_columns].to_csv('patient_export.csv', index=False)
                    st.success("✅ Exported to patient_export.csv")
            
            with col2:
                if st.button("📊 Export to Excel", use_container_width=True):
                    sorted_df[selected_columns].to_excel('patient_export.xlsx', index=False)
                    st.success("✅ Exported to patient_export.xlsx")
            
            with col3:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.info("Use Ctrl+C to copy from table above")
        
        else:
            st.warning("No patients match the current filters")
    
    # TAB 3: Site Analytics
        # TAB 3: Site Analytics
    with tab3:
        st.header("Site Performance Analytics")
        
        if not sites.empty and len(sites) > 0:
            # Site comparison grid
            st.subheader("Site Comparison")
            
            # Create site metrics grid - SAFE VERSION
            available_cols = []
            for col in ['site_id', 'region', 'total_patients_enrolled', 
                       'clean_percentage', 'avg_dqi', 'total_open_queries',
                       'performance_status']:
                if col in sites.columns:
                    available_cols.append(col)
            
            if available_cols:
                metrics_grid = sites[available_cols].copy()
                
                # Format for display - SAFE
                if 'clean_percentage' in metrics_grid.columns:
                    metrics_grid['clean_percentage'] = metrics_grid['clean_percentage'].apply(
                        lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
                    )
                
                if 'avg_dqi' in metrics_grid.columns:
                    metrics_grid['avg_dqi'] = metrics_grid['avg_dqi'].apply(
                        lambda x: f"{x:.1f}" if pd.notna(x) else "N/A"
                    )
                
                # Display with styling if performance_status exists
                if 'performance_status' in metrics_grid.columns:
                    st.dataframe(
                        metrics_grid.style.apply(
                            lambda x: ['background-color: #d4edda' if x['performance_status'] == 'Good' 
                                      else ('background-color: #fff3cd' if x['performance_status'] == 'Warning' 
                                            else 'background-color: #f8d7da') for _ in x],
                            axis=1
                        ),
                        use_container_width=True,
                        height=300
                    )
                else:
                    st.dataframe(metrics_grid, use_container_width=True, height=300)
            else:
                st.info("No site metrics columns available")
            
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
                        site_patients = filtered_patients[filtered_patients['site_id'] == selected_site]
                        
                        # Site details in columns - USE SAFE GET
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Total Patients", site_row.get('total_patients_enrolled', 0))
                            st.metric("Active Patients", len(site_patients[site_patients['subject_status'] == 'Active']) if 'subject_status' in site_patients.columns else 0)
                        
                        with col2:
                            st.metric("Clean Percentage", f"{site_row.get('clean_percentage', 0):.1f}%")
                            st.metric("Avg DQI", f"{site_row.get('avg_dqi', 0):.1f}")
                        
                        with col3:
                            st.metric("Open Issues", site_row.get('total_open_queries', 0))
                            st.metric("Safety Issues", site_row.get('total_safety_issues', 0))
                        
                        # Action recommendations
                        st.subheader("💡 Action Recommendations")
                        
                        recommendations = []
                        if site_row.get('clean_percentage', 0) < 70:
                            recommendations.append("🔸 **Improve data quality** - Provide additional training to site staff")
                        if site_row.get('total_open_queries', 0) > 15:
                            recommendations.append("🔸 **Reduce query backlog** - Allocate resources for query resolution")
                        if site_row.get('avg_dqi', 0) < 70:
                            recommendations.append("🔸 **Enhance monitoring** - Schedule additional monitoring visits")
                        
                        if recommendations:
                            for rec in recommendations:
                                st.info(rec)
                        else:
                            st.success("✅ Site is performing within acceptable parameters")
            else:
                st.info("No site ID data available")
        
        else:
            st.info("No site data available")
    
    # TAB 4: Risk Monitoring
    with tab4:
        st.header("Risk Monitoring & Alerts")
        
        # Risk Matrix
        st.subheader("📊 Risk Matrix")
        
        if 'risk_level' in filtered_patients.columns and 'clean_status' in filtered_patients.columns:
            risk_matrix = filtered_patients.groupby(['risk_level', 'clean_status']).size().unstack(fill_value=0)
            
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
            
            st.plotly_chart(fig_risk, use_container_width=True)
        
        # High-priority issues
        st.subheader("🚨 High-Priority Issues")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Safety issues
            safety_patients = filtered_patients[filtered_patients['safety_issues'] > 0]
            if not safety_patients.empty:
                st.error(f"**Safety Alerts:** {len(safety_patients)} patients have safety issues")
                for _, patient in safety_patients.head(3).iterrows():
                    with st.expander(f"⚠️ {patient.get('patient_id', 'Unknown')} - {patient.get('site_id', 'Unknown')}"):
                        st.write(f"**Patient ID:** {patient.get('patient_id', 'N/A')}")
                        st.write(f"**Site:** {patient.get('site_id', 'N/A')}")
                        st.write(f"**Safety Issues:** {patient.get('safety_issues', 0)}")
                        st.write(f"**Adverse Events:** {patient.get('adverse_events', 0)}")
                        st.write("**Action Required:** Immediate medical review")
            else:
                st.success("✅ No safety issues detected")
        
        with col2:
            # High-risk patients
            high_risk = filtered_patients[filtered_patients['risk_level'] == 'High']
            if not high_risk.empty:
                st.warning(f"**High-Risk Patients:** {len(high_risk)} patients require attention")
                for _, patient in high_risk.head(3).iterrows():
                    with st.expander(f"🔴 {patient.get('patient_id', 'Unknown')} - DQI: {patient.get('dqi_score', 0)}"):
                        st.write(f"**DQI Score:** {patient.get('dqi_score', 0)}")
                        st.write(f"**Clean Status:** {patient.get('clean_status', 'Unknown')}")
                        st.write(f"**Missing Visits:** {patient.get('missing_visits', 0)}")
                        st.write(f"**Open Queries:** {patient.get('open_queries', 0)}")
                        st.write("**Action:** Schedule follow-up within 7 days")
            else:
                st.success("✅ No high-risk patients")
        
        # Open queries monitoring
        st.subheader("❓ Query Monitoring Dashboard")
        
        if not queries.empty:
            open_queries = queries[queries['query_status'] == 'Open']
            
            if not open_queries.empty:
                # Query statistics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Open", len(open_queries))
                
                with col2:
                    avg_age = open_queries['query_age_days'].mean() if 'query_age_days' in open_queries.columns else 0
                    st.metric("Avg Age (days)", f"{avg_age:.1f}")
                
                with col3:
                    high_priority = len(open_queries[open_queries['query_priority'] == 'High']) if 'query_priority' in open_queries.columns else 0
                    st.metric("High Priority", high_priority)
                
                # Query table
                query_cols = []
                for col in ['query_id', 'patient_id', 'site_id', 'query_type', 'query_priority', 'query_age_days']:
                    if col in open_queries.columns:
                        query_cols.append(col)
                
                if query_cols:
                    st.dataframe(
                        open_queries[query_cols].sort_values('query_age_days', ascending=False),
                        use_container_width=True,
                        height=200
                    )
            else:
                st.success("✅ No open queries")
        else:
            st.info("No query data available")
    
    # TAB 5: AI Insights
    with tab5:
        st.header("AI-Powered Insights & Reports")
        
        # Predictive analytics
        st.subheader("📈 Predictive Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Enrollment prediction
            st.markdown("#### Enrollment Forecast")
            current = summary['total_patients']
            target = TRIAL_INFO['target_patients']
            progress = (current / target) * 100
            
            fig_enroll = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = progress,
                title = {'text': "Enrollment Progress"},
                gauge = {
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
            
            fig_enroll.update_layout(height=250)
            st.plotly_chart(fig_enroll, use_container_width=True)
            
            # Prediction
            days_remaining = (datetime.strptime(TRIAL_INFO['expected_end_date'], '%Y-%m-%d') - datetime.now()).days
            if days_remaining > 0:
                daily_rate = current / (365 - days_remaining) if (365 - days_remaining) > 0 else 0
                predicted = current + (daily_rate * days_remaining)
                st.info(f"📅 **Predicted enrollment:** {int(predicted)}/{target} ({(predicted/target*100):.1f}%)")
        
        with col2:
            # DQI trend prediction
            st.markdown("#### DQI Trend Prediction")
            
            # Simulated trend data
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            dqi_trend = np.random.normal(summary['avg_dqi'], 5, 30).clip(0, 100)
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=dates,
                y=dqi_trend,
                mode='lines+markers',
                name='Historical',
                line=dict(color='#1f3c88', width=2)
            ))
            
            # Add prediction
            future_dates = pd.date_range(start=datetime.now(), periods=7, freq='D')
            future_trend = np.linspace(dqi_trend[-1], min(dqi_trend[-1] + 2, 100), 7)
            
            fig_trend.add_trace(go.Scatter(
                x=future_dates,
                y=future_trend,
                mode='lines',
                name='Prediction',
                line=dict(color='#dc3545', width=2, dash='dash')
            ))
            
            fig_trend.update_layout(
                height=250,
                xaxis_title="Date",
                yaxis_title="DQI Score",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
            st.caption("📊 AI prediction suggests slight improvement over next 7 days")
        
        # Report generation
        st.subheader("📄 Report Generation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            report_type = st.selectbox(
                "Report Type",
                options=["Site Performance Report", "Patient Status Summary", 
                        "Data Quality Analysis", "Safety Monitoring Report", 
                        "Executive Summary"]
            )
            
            report_params = st.multiselect(
                "Include Parameters",
                options=["Patient Demographics", "Performance Metrics", "Issues & Alerts",
                        "Trend Analysis", "Recommendations", "Financial Impact"],
                default=["Performance Metrics", "Issues & Alerts", "Recommendations"]
            )
        
        with col2:
            format_type = st.radio(
                "Export Format",
                options=["PDF", "Excel", "HTML"],
                horizontal=True
            )
            
            schedule_report = st.checkbox("Schedule Report")
            
            if schedule_report:
                frequency = st.selectbox(
                    "Frequency",
                    options=["Daily", "Weekly", "Monthly", "Quarterly"]
                )
        
        # Generate report button
        if st.button("🔄 Generate Report", type="primary", use_container_width=True):
            with st.spinner("Generating AI-powered report..."):
                # Simulate report generation
                import time
                time.sleep(2)
                
                # Create report content
                report_content = f"""
                # AI-Generated Clinical Trial Report
                
                ## Report Details
                - **Type:** {report_type}
                - **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                - **Parameters:** {', '.join(report_params)}
                - **Format:** {format_type}
                
                ## Executive Summary
                - **Total Patients Analyzed:** {summary['total_patients']}
                - **Overall Clean Rate:** {summary['clean_percentage']}%
                - **Average DQI:** {summary['avg_dqi']:.1f}/100
                - **Critical Issues:** {summary['total_safety_issues']} safety, {summary['total_open_queries']} queries
                
                ## Key Findings
                1. Data quality is {'within acceptable limits' if summary['clean_percentage'] >= 70 else 'needs improvement'}
                2. {'No critical safety issues detected' if summary['total_safety_issues'] == 0 else 'Safety issues require immediate attention'}
                3. Query resolution rate: {((filtered_patients['queries_resolved'].sum() / filtered_patients['total_queries'].sum() * 100) if 'total_queries' in filtered_patients.columns and filtered_patients['total_queries'].sum() > 0 else 0):.1f}%
                
                ## AI Recommendations
                - {'Maintain current monitoring frequency' if summary['clean_percentage'] >= 70 else 'Increase monitoring visits for low-performing sites'}
                - {'Continue current processes' if summary['total_safety_issues'] == 0 else 'Schedule safety review meetings'}
                - {'Query resolution process is effective' if summary['total_open_queries'] < 20 else 'Allocate additional resources for query resolution'}
                
                ## Next Steps
                1. Review this report with clinical team
                2. Implement recommended actions
                3. Schedule follow-up review in 30 days
                """
                
                # Display report
                st.success("✅ Report generated successfully!")
                
                with st.expander("📋 Preview Report", expanded=True):
                    st.markdown(report_content)
                
                # Download options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"📥 Download {format_type} Report"):
                        st.info(f"Downloading {format_type} report...")
                        # In real implementation, generate actual file
                
                with col2:
                    if st.button("📧 Email Report"):
                        st.info("Report emailed to distribution list")
        
        # Anomaly detection
        st.subheader("🔍 Anomaly Detection")
        
        if 'dqi_score' in filtered_patients.columns:
            # Calculate anomalies (z-score > 2)
            mean_dqi = filtered_patients['dqi_score'].mean()
            std_dqi = filtered_patients['dqi_score'].std()
            
            if std_dqi > 0:
                filtered_patients['z_score'] = (filtered_patients['dqi_score'] - mean_dqi) / std_dqi
                anomalies = filtered_patients[abs(filtered_patients['z_score']) > 2]
                
                if not anomalies.empty:
                    st.warning(f"⚠️ **Anomalies Detected:** {len(anomalies)} patients with unusual DQI scores")
                    
                    for _, anomaly in anomalies.head(3).iterrows():
                        with st.expander(f"📊 {anomaly.get('patient_id', 'Unknown')} - DQI: {anomaly.get('dqi_score', 0)} (z-score: {anomaly.get('z_score', 0):.2f})"):
                            st.write(f"**Site:** {anomaly.get('site_id', 'N/A')}")
                            st.write(f"**Status:** {anomaly.get('subject_status', 'N/A')}")
                            st.write(f"**Clean Status:** {anomaly.get('clean_status', 'N/A')}")
                            st.write(f"**Risk Level:** {anomaly.get('risk_level', 'N/A')}")
                            st.write("**AI Insight:** This patient's DQI score significantly deviates from the average")
                else:
                    st.success("✅ No statistical anomalies detected")
        
        # Recommendation cards
        st.subheader("💡 AI Recommendations")
        
        insights = DataHelper.generate_ai_insights(filtered_patients, sites)
        
        if insights:
            for insight in insights:
                if insight['type'] == 'critical':
                    st.error(f"### 🔴 {insight['title']}")
                elif insight['type'] == 'warning':
                    st.warning(f"### 🟡 {insight['title']}")
                else:
                    st.success(f"### 🟢 {insight['title']}")
                
                st.write(insight['message'])
                st.info(f"**🤖 AI Recommendation:** {insight['recommendation']}")
        else:
            st.success("✅ All systems operating within optimal parameters")
            
            # Show positive insights
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("""
                **📊 Data Quality**
                Current data quality metrics are within acceptable ranges.
                Continue current quality control processes.
                """)
            
            with col2:
                st.info("""
                **🏥 Site Performance**
                All sites are meeting minimum performance standards.
                Consider sharing best practices between sites.
                """)
            
            with col3:
                st.info("""
                **🚨 Risk Management**
                No critical risks detected.
                Maintain current monitoring frequency.
                """)
    
    # Footer
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