import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Hospital Cybersecurity Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize all session states
if 'risk_data' not in st.session_state:
    st.session_state.risk_data = pd.DataFrame({
        'Category': ['Network Security', 'Access Control', 'Data Protection', 'Employee Training'],
        'Risk Score': [75, 70, 55, 85],
        'Priority': ['High', 'High', 'Medium', 'Critical']
    })

if 'vuln_data' not in st.session_state:
    st.session_state.vuln_data = pd.DataFrame({
        'Vulnerability': ['SQL Injection', 'Weak Passwords', 'Unpatched Systems', 'Phishing'],
        'Severity': ['Critical', 'Medium', 'Medium', 'Medium'],
        'Status': ['Open', 'Resolved', 'Open', 'Open'],
        'Discovery Date': ['2024-12-04', '2024-12-03', '2024-12-02', '2024-12-01']
    })

if 'phases' not in st.session_state:
    st.session_state.phases = pd.DataFrame({
        'Phase': ['Immediate (0-30 days)', 'Immediate (0-30 days)', 'Immediate (0-30 days)',
                'Short-term (1-3 months)', 'Short-term (1-3 months)', 'Short-term (1-3 months)',
                'Long-term (3-12 months)', 'Long-term (3-12 months)', 'Long-term (3-12 months)'],
        'Task': ['Emergency patch management', 'Temporary access restriction', 'Initial training deployment',
                'Advanced security tool implementation', 'Comprehensive training program', 'Initial policy refinement',
                'Continuous monitoring systems', 'Advanced threat hunting', 'Regular security assessments'],
        'Progress': [85, 90, 70, 45, 30, 60, 20, 15, 10]
    })

if 'recommendations_data' not in st.session_state:
    st.session_state.recommendations_data = pd.DataFrame({
        'Recommendation': [
            'Implement Multi-Factor Authentication',
            'Update Firewall Rules',
            'Deploy EDR Solution',
            'Conduct Security Training',
            'Implement Zero Trust Architecture'
        ],
        'Priority': ['Critical', 'High', 'High', 'Medium', 'Critical'],
        'Status': ['In Progress', 'Planned', 'Completed', 'In Progress', 'Planned'],
        'Estimated Completion': ['2024-12-15', '2024-12-30', '2024-12-01', 
                               '2025-01-15', '2025-01-30']
    })

# Custom CSS
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 1rem}
    .element-container {margin-bottom: 1rem}
    [data-testid="stMetricValue"] {font-size: clamp(1rem, 2vw, 1.2rem)}
    [data-testid="stMetricLabel"] {font-size: clamp(0.8rem, 1.5vw, 1rem)}
    .stTabs [data-baseweb="tab-list"] {gap: 1rem}
    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 10px;
        white-space: pre-wrap;
    }
    .delete-button, .edit-button {
        border: none;
        color: inherit;
        padding: 2px 6px;
        border-radius: 4px;
        cursor: pointer;
    }
    .delete-button:hover {
        color: red;
        background: rgba(255, 0, 0, 0.1);
    }
    .edit-button:hover {
        color: blue;
        background: rgba(0, 0, 255, 0.1);
    }
    @media (max-width: 640px) {
        .block-container {padding: 1rem}
        .stTabs [data-baseweb="tab"] {font-size: 0.8rem}
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.subheader("Project Team")
    st.write("**Project Lead:** Mamun Ahmed (CIO)")
    st.write("**Security Analyst:** JP Marvin")
    st.write("**IT Manager:** Paul Borner")
    st.write("**Cybersecurity Specialist:** Lassana Bility")
    st.markdown("---")
    st.write("**Course:** Cybersecurity Risk Management")
    st.write("**Instructor:** Professor Manoj Akula")
    st.write("**Date:** December 6, 2024")

# Main content
st.title("🏥 Detroit Metropolitan Hospital")
st.header("Cybersecurity Risk Management Dashboard")

# Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "Risk Assessment", 
    "Vulnerability Analysis", 
    "Implementation Timeline",
    "Security Recommendations"
])

# Risk Assessment Tab
with tab1:
    st.subheader("Risk Assessment by Category")
    
    # Add new risk category
    with st.expander("Add New Risk Category"):
        with st.form("new_risk"):
            col1, col2, col3 = st.columns(3)
            with col1:
                category = st.text_input("Category Name")
            with col2:
                risk_score = st.number_input("Risk Score", 0, 100, 50)
            with col3:
                priority = st.selectbox("Priority", ["Critical", "High", "Medium"])
            
            if st.form_submit_button("Add Risk Category"):
                new_risk = pd.DataFrame({
                    'Category': [category],
                    'Risk Score': [risk_score],
                    'Priority': [priority]
                })
                st.session_state.risk_data = pd.concat([st.session_state.risk_data, new_risk], ignore_index=True)
                st.success("Risk category added!")
                st.rerun()

    # Display and edit existing risks
    for index, row in st.session_state.risk_data.iterrows():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            st.write(row['Category'])
        with col2:
            st.write(f"Score: {row['Risk Score']}")
        with col3:
            st.write(f"Priority: {row['Priority']}")
        with col4:
            if st.button('🗑️', key=f'risk_delete_{index}'):
                st.session_state.risk_data = st.session_state.risk_data.drop(index).reset_index(drop=True)
                st.rerun()

    # Display risk chart
    fig = px.bar(st.session_state.risk_data, 
                 x='Category', 
                 y='Risk Score',
                 color='Priority',
                 color_discrete_map={
                     'Critical': 'red',
                     'High': 'orange',
                     'Medium': 'yellow'
                 })
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Display metrics
    cols = st.columns(3)
    with cols[0]:
        st.metric("Overall Risk Score", "79/100", "High Risk")
    with cols[1]:
        st.metric("Critical Vulnerabilities", "3", "+1 from last month")
    with cols[2]:
        st.metric("Security Incidents", "12", "-3 from last month")

# Vulnerability Analysis Tab
with tab2:
    st.subheader("Vulnerability Analysis")
    
    system = st.selectbox(
        "Select System to Analyze",
        ["Network Infrastructure", "Patient Records", "Payment Systems", "IoT Devices"]
    )
    
    # Add new vulnerability
    with st.expander("Add New Vulnerability"):
        with st.form("new_vulnerability"):
            col1, col2, col3 = st.columns(3)
            with col1:
                vuln_name = st.text_input("Vulnerability Name")
            with col2:
                severity = st.selectbox("Severity", ["Critical", "High", "Medium"])
            with col3:
                status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            
            if st.form_submit_button("Add Vulnerability"):
                new_vuln = pd.DataFrame({
                    'Vulnerability': [vuln_name],
                    'Severity': [severity],
                    'Status': [status],
                    'Discovery Date': [datetime.now().strftime('%Y-%m-%d')]
                })
                st.session_state.vuln_data = pd.concat([st.session_state.vuln_data, new_vuln], ignore_index=True)
                st.success("Vulnerability added!")
                st.rerun()

    # Display vulnerabilities with delete option
    for index, row in st.session_state.vuln_data.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
        with col1:
            st.write(row['Vulnerability'])
        with col2:
            st.write(row['Severity'])
        with col3:
            st.write(row['Status'])
        with col4:
            st.write(row['Discovery Date'])
        with col5:
            if st.button('🗑️', key=f'vuln_delete_{index}'):
                st.session_state.vuln_data = st.session_state.vuln_data.drop(index).reset_index(drop=True)
                st.rerun()

    # Vulnerability metrics
    st.subheader("Vulnerability Metrics")
    metrics_cols = st.columns(2)
    with metrics_cols[0]:
        fig_severity = px.pie(
            st.session_state.vuln_data, 
            names='Severity', 
            title='Vulnerabilities by Severity',
            color_discrete_sequence=['#ff4b4b', '#ffa600', '#ffeb3b']
        )
        fig_severity.update_layout(height=350)
        st.plotly_chart(fig_severity, use_container_width=True)
    
    with metrics_cols[1]:
        fig_status = px.pie(
            st.session_state.vuln_data, 
            names='Status', 
            title='Vulnerabilities by Status',
            color_discrete_sequence=['#ff4b4b', '#36b37e', '#ffeb3b']
        )
        fig_status.update_layout(height=350)
        st.plotly_chart(fig_status, use_container_width=True)

# Implementation Timeline Tab
with tab3:
    st.subheader("Implementation Timeline")
    
    # Add new task
    with st.expander("Add New Task"):
        with st.form("new_task"):
            col1, col2, col3 = st.columns(3)
            with col1:
                phase = st.selectbox("Phase", [
                    "Immediate (0-30 days)",
                    "Short-term (1-3 months)",
                    "Long-term (3-12 months)"
                ])
            with col2:
                task = st.text_input("Task Name")
            with col3:
                progress = st.number_input("Progress (%)", 0, 100, 0)
            
            if st.form_submit_button("Add Task"):
                new_task = pd.DataFrame({
                    'Phase': [phase],
                    'Task': [task],
                    'Progress': [progress]
                })
                st.session_state.phases = pd.concat([st.session_state.phases, new_task], ignore_index=True)
                st.success("Task added!")
                st.rerun()

    # Display tasks by phase
    for phase in st.session_state.phases['Phase'].unique():
        st.write(f"### {phase}")
        phase_data = st.session_state.phases[st.session_state.phases['Phase'] == phase]
        phase_progress = phase_data['Progress'].mean()
        st.progress(phase_progress/100)
        
        for index, row in phase_data.iterrows():
            col1, col2, col3, col4 = st.columns([3, 1, 0.5, 0.5])
            with col1:
                st.write(row['Task'])
            with col2:
                st.progress(row['Progress']/100)
            with col3:
                st.write(f"{row['Progress']}%")
            with col4:
                if st.button('🗑️', key=f'task_delete_{index}'):
                    st.session_state.phases = st.session_state.phases.drop(index).reset_index(drop=True)
                    st.rerun()

# Security Recommendations Tab
with tab4:
    st.subheader("Security Recommendations")
    
    priority_filter = st.multiselect(
        "Filter by Priority",
        ["Critical", "High", "Medium"],
        default=["Critical", "High"]
    )
    
    # Filter recommendations
    filtered_recommendations = st.session_state.recommendations_data[
        st.session_state.recommendations_data['Priority'].isin(priority_filter)
    ]
    
    # Display recommendations with delete buttons
    for index, row in filtered_recommendations.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 0.5])
        with col1:
            st.write(row['Recommendation'])
        with col2:
            st.write(row['Priority'])
        with col3:
            st.write(row['Status'])
        with col4:
            st.write(row['Estimated Completion'])
        with col5:
            if st.button('🗑️', key=f'rec_delete_{index}'):
                st.session_state.recommendations_data = st.session_state.recommendations_data.drop(index).reset_index(drop=True)
                st.rerun()
    
    # Add new recommendation
    st.write("### Add New Recommendation")
    with st.form("new_recommendation"):
        cols = st.columns([3, 1, 1, 1])
        with cols[0]:
            rec_text = st.text_input("Recommendation")
        with cols[1]:
            rec_priority = st.selectbox("Priority", ["Critical", "High", "Medium"])
        with cols[2]:
            rec_status = st.selectbox("Status", ["Planned", "In Progress", "Completed"])
        with cols[3]:
            rec_date = st.date_input("Estimated Completion")
        
        submitted = st.form_submit_button("Add Recommendation")
        
        if submitted and rec_text:
            new_recommendation = pd.DataFrame({
                'Recommendation': [rec_text],
                'Priority': [rec_priority],
                'Status': [rec_status],
                'Estimated Completion': [rec_date.strftime('%Y-%m-%d')]
            })
            st.session_state.recommendations_data = pd.concat([
                st.session_state.recommendations_data, 
                new_recommendation
            ],ignore_index=True)
            st.success("Recommendation added successfully!")

if __name__ == "__main__":
    pass