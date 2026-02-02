"""
Statistics and Analytics Dashboard
"""
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime, timedelta

def show_statistics_page():
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Main", type="secondary"):
            st.session_state["current_page"] = "Main"
            st.rerun()

    st.title("📊 Statistics & Analytics Dashboard")

    st.markdown("""
    ### Application Usage & Performance Analytics
    
    Track your AI detection and text humanization activities with detailed statistics and insights.
    """)

    st.markdown("---")

    # Initialize session state for stats
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []

    # Create mock data for demonstration
    if "demo_stats_initialized" not in st.session_state:
        # Create sample statistics
        categories = ['Human', 'AI', 'Mixed']
        sample_data = {
            'Date': pd.date_range(end=datetime.now(), periods=30, freq='D'),
            'Documents_Analyzed': np.random.randint(1, 10, 30),
            'Total_Words': np.random.randint(500, 5000, 30),
            'AI_Percentage': np.random.randint(10, 80, 30),
            'Human_Percentage': np.random.randint(10, 80, 30),
        }
        st.session_state.demo_stats = pd.DataFrame(sample_data)
        st.session_state.demo_stats_initialized = True

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Overview", 
        "📊 Detailed Charts", 
        "📋 Content Analysis",
        "⏱️ Activity Timeline"
    ])

    with tab1:
        st.subheader("Key Metrics Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_analyses = len(st.session_state.demo_stats)
            st.metric("Total Analyses", total_analyses, "+5 this week")
        
        with col2:
            total_words = st.session_state.demo_stats['Total_Words'].sum()
            st.metric("Total Words Processed", f"{total_words:,.0f}", f"+{total_words//7:,.0f} daily avg")
        
        with col3:
            avg_ai_percentage = st.session_state.demo_stats['AI_Percentage'].mean()
            st.metric("Avg AI Content %", f"{avg_ai_percentage:.1f}%", f"±{st.session_state.demo_stats['AI_Percentage'].std():.1f}%")
        
        with col4:
            documents_analyzed = st.session_state.demo_stats['Documents_Analyzed'].sum()
            st.metric("Documents Analyzed", documents_analyzed, f"+{documents_analyzed//7} daily avg")
        
        st.markdown("---")
        
        # Content classification pie chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Content Classification Distribution")
            
            classification_data = pd.DataFrame({
                'Type': ['Human', 'AI', 'Mixed'],
                'Count': [
                    np.random.randint(10, 50),
                    np.random.randint(10, 50),
                    np.random.randint(5, 30)
                ]
            })
            
            pie_chart = alt.Chart(classification_data).mark_arc().encode(
                theta='Count:Q',
                color=alt.Color('Type:N', scale=alt.Scale(
                    domain=['Human', 'AI', 'Mixed'],
                    range=['#00CC96', '#FF6B6B', '#FFB366']
                )),
                tooltip=['Type', 'Count']
            ).properties(height=400)
            
            st.altair_chart(pie_chart, use_container_width=True)
        
        with col2:
            st.subheader("Classification Breakdown")
            
            breakdown_data = pd.DataFrame({
                'Classification': ['Human', 'AI', 'Mixed'],
                'Percentage': [45, 35, 20],
                'Documents': [180, 140, 80]
            })
            
            st.dataframe(breakdown_data, use_container_width=True)

    with tab2:
        st.subheader("Detailed Analytics Charts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Daily Analysis Trend")
            
            line_chart = alt.Chart(st.session_state.demo_stats).mark_line(point=True).encode(
                x=alt.X('Date:T', title='Date'),
                y=alt.Y('Documents_Analyzed:Q', title='Documents Analyzed'),
                tooltip=['Date:T', 'Documents_Analyzed:Q']
            ).properties(height=400)
            
            st.altair_chart(line_chart, use_container_width=True)
        
        with col2:
            st.markdown("#### AI Content Percentage Trend")
            
            ai_chart = alt.Chart(st.session_state.demo_stats).mark_area(
                line=True,
                point=True,
                opacity=0.7
            ).encode(
                x=alt.X('Date:T', title='Date'),
                y=alt.Y('AI_Percentage:Q', title='AI Content %', scale=alt.Scale(domain=[0, 100])),
                color=alt.value('#FF6B6B'),
                tooltip=['Date:T', 'AI_Percentage:Q']
            ).properties(height=400)
            
            st.altair_chart(ai_chart, use_container_width=True)

    with tab3:
        st.subheader("Content Analysis Statistics")
        
        # Top categories
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Most Analyzed Content Types")
            
            content_types = pd.DataFrame({
                'Type': ['Academic Papers', 'Articles', 'Reports', 'Emails', 'Other'],
                'Count': [45, 38, 25, 18, 12]
            })
            
            bar_chart = alt.Chart(content_types).mark_bar().encode(
                x=alt.X('Count:Q', title='Number of Documents'),
                y=alt.Y('Type:N', sort='-x', title='Content Type'),
                color=alt.value('#4C72B0'),
                tooltip=['Type', 'Count']
            ).properties(height=400)
            
            st.altair_chart(bar_chart, use_container_width=True)
        
        with col2:
            st.markdown("#### AI Detection Confidence Distribution")
            
            confidence_data = pd.DataFrame({
                'Range': ['0-25%', '25-50%', '50-75%', '75-100%'],
                'Count': [30, 45, 65, 40]
            })
            
            confidence_chart = alt.Chart(confidence_data).mark_bar().encode(
                x=alt.X('Range:N', title='Confidence Range'),
                y=alt.Y('Count:Q', title='Number of Samples'),
                color=alt.Color('Count:Q', scale=alt.Scale(scheme='viridis')),
                tooltip=['Range', 'Count']
            ).properties(height=400)
            
            st.altair_chart(confidence_chart, use_container_width=True)

    with tab4:
        st.subheader("Recent Activity Timeline")
        
        # Activity data
        activity_data = pd.DataFrame({
            'Timestamp': pd.date_range(end=datetime.now(), periods=20, freq='H'),
            'Activity': [
                'PDF Analysis Completed',
                'Text Humanization Applied',
                'PDF Analysis Completed',
                'Batch Processing Started',
                'Text Analysis Completed',
                'PDF Annotation Generated',
                'Text Humanization Applied',
                'Statistics Report Generated',
                'PDF Analysis Completed',
                'Document Comparison Done',
                'Text Analysis Completed',
                'PDF Annotation Generated',
                'Text Humanization Applied',
                'Batch Processing Completed',
                'PDF Analysis Completed',
                'Text Analysis Completed',
                'PDF Annotation Generated',
                'Statistics Report Generated',
                'Text Humanization Applied',
                'Document Comparison Done'
            ],
            'Status': ['Success'] * 20,
            'Duration': [f"{np.random.randint(5, 120)}s" for _ in range(20)]
        })
        
        activity_data = activity_data.sort_values('Timestamp', ascending=False)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.dataframe(activity_data, use_container_width=True, height=400)
        
        with col2:
            st.markdown("#### Activity Summary")
            
            success_count = len(activity_data[activity_data['Status'] == 'Success'])
            failed_count = len(activity_data[activity_data['Status'] == 'Failed'])
            
            st.metric("Successful Operations", success_count)
            st.metric("Failed Operations", failed_count)
            st.metric("Success Rate", f"{(success_count/(success_count+failed_count)*100):.1f}%")
        
        # Export activity report
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = activity_data.to_csv(index=False)
            st.download_button(
                label="📥 Download Activity Report (CSV)",
                data=csv,
                file_name=f"activity_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            if st.button("🔄 Refresh Statistics"):
                st.rerun()

    st.markdown("---")
    st.info("""
    📊 **Dashboard Features:**
    - Real-time activity tracking
    - Content classification metrics
    - Performance analytics
    - Historical trends and comparisons
    - Exportable reports
    """)
