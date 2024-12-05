import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# At the top of main.py after imports:
if __name__ == "__main__":
    import os
    os.environ['NGROK_SKIP_BROWSER_WARNING'] = 'true'

st.set_page_config(page_title="Hospital Cybersecurity Dashboard", layout="wide")

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

st.title("🏥 Detroit Metropolitan Hospital")
st.header("Cybersecurity Risk Management Dashboard")

tab1, tab2, tab3, tab4 = st.tabs([
    "Risk Assessment", 
    "Vulnerability Analysis", 
    "Implementation Timeline",
    "Security Recommendations"
])

with tab1:
    risk_data = pd.DataFrame({
        'Category': ['Network Security', 'Access Control', 'Data Protection', 'Employee Training'],
        'Risk Score': [75, 70, 55, 85],
        'Priority': ['High', 'High', 'Medium', 'Critical']
    })
    
    st.subheader("Risk Assessment by Category")
    fig = px.bar(risk_data, 
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
    
    cols = st.columns(3)
    with cols[0]:
        st.metric("Overall Risk Score", "79/100", "High Risk", help="Overall security risk score based on all factors")
    with cols[1]:
        st.metric("Critical Vulnerabilities", "3", "+1 from last month", help="Number of critical security issues identified")
    with cols[2]:
        st.metric("Security Incidents", "12", "-3 from last month", help="Total reported security events")

with tab2:
    st.subheader("Vulnerability Analysis")
    
    system = st.selectbox(
        "Select System to Analyze",
        ["Network Infrastructure", "Patient Records", "Payment Systems", "IoT Devices"]
    )
    
    vuln_data = pd.DataFrame({
        'Vulnerability': ['SQL Injection', 'Weak Passwords', 'Unpatched Systems', 'Phishing'],
        'Severity': ['Critical', 'Medium', 'Medium', 'Medium'],
        'Status': ['Open', 'Resolved', 'Open', 'Open'],
        'Discovery Date': ['2024-12-04', '2024-12-03', '2024-12-02', '2024-12-01']
    })
    
    st.dataframe(vuln_data, hide_index=True, use_container_width=True)
    
    st.subheader("Vulnerability Metrics")
    metrics_cols = st.columns(2)
    
    with metrics_cols[0]:
        fig_severity = px.pie(
            vuln_data, 
            names='Severity', 
            title='Vulnerabilities by Severity',
            height=350,
            color_discrete_sequence=['#ff4b4b', '#ffa600', '#ffeb3b']
        )
        fig_severity.update_layout(
            legend=dict(orientation="h", y=1.2),
            margin=dict(t=80)
        )
        st.plotly_chart(fig_severity, use_container_width=True)
    
    with metrics_cols[1]:
        fig_status = px.pie(
            vuln_data, 
            names='Status', 
            title='Vulnerabilities by Status',
            height=350,
            color_discrete_sequence=['#ff4b4b', '#36b37e', '#ffeb3b']
        )
        fig_status.update_layout(
            legend=dict(orientation="h", y=1.2),
            margin=dict(t=80)
        )
        st.plotly_chart(fig_status, use_container_width=True)

with tab3:
    st.subheader("Implementation Timeline")
    
    phases = {
        "Immediate (0-30 days)": {
            "Emergency patch management": 85,
            "Temporary access restriction": 90,
            "Initial training deployment": 70
        },
        "Short-term (1-3 months)": {
            "Advanced security tool implementation": 45,
            "Comprehensive training program": 30,
            "Initial policy refinement": 60
        },
        "Long-term (3-12 months)": {
            "Continuous monitoring systems": 20,
            "Advanced threat hunting": 15,
            "Regular security assessments": 10
        }
    }
    
    for phase, tasks in phases.items():
        st.write(f"### {phase}")
        phase_progress = sum(tasks.values()) / len(tasks)
        st.progress(phase_progress/100)
        
        for task, progress in tasks.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(progress/100)
            with col2:
                st.write(f"{progress}%")
            st.write(f"- {task}")

with tab4:
    st.subheader("Security Recommendations")
    
    priority_filter = st.multiselect(
        "Filter by Priority",
        ["Critical", "High", "Medium"],
        default=["Critical", "High"]
    )
    
    recommendations = pd.DataFrame({
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
    
    filtered_recommendations = recommendations[
        recommendations['Priority'].isin(priority_filter)
    ]
    
    st.dataframe(
        filtered_recommendations.style.applymap(
            lambda x: 'background-color: #ffcdd2' if x == 'Critical' else (
                'background-color: #ffe0b2' if x == 'High' else ''
            ), 
            subset=['Priority']
        ),
        hide_index=True,
        use_container_width=True
    )
    
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

if __name__ == "__main__":
    pass