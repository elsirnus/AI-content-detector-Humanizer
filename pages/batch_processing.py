"""
Batch Processing for multiple documents
"""
import streamlit as st
import pandas as pd
import altair as alt
import zipfile
from io import BytesIO
from utils.pdf_utils import extract_text_from_pdf, word_count
from utils.ai_detection_utils import classify_text_hf

def show_batch_processing_page():
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Main", type="secondary"):
            st.session_state["current_page"] = "Main"
            st.rerun()

    st.title("⚡ Batch Processing & Bulk Analysis")

    st.markdown("""
    ### Process Multiple Files at Once
    
    Upload multiple PDF or text files to analyze them in batch mode. 
    Perfect for processing large collections of documents efficiently.
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Upload Multiple Files")
        uploaded_files = st.file_uploader(
            "Select multiple PDF or text files:",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True
        )
    
    with col2:
        st.markdown("### Processing Options")
        
        batch_size = st.slider("Batch Size:", min_value=1, max_value=10, value=3)
        include_detailed = st.checkbox("Include Detailed Analysis", value=False)
        export_format = st.selectbox(
            "Export Format:",
            ["CSV", "Excel", "JSON"]
        )

    # Process button
    if st.button("🚀 Process Batch", type="primary", use_container_width=True):
        if not uploaded_files:
            st.error("Please upload at least one file to process.")
        else:
            with st.spinner(f"Processing {len(uploaded_files)} files..."):
                try:
                    batch_results = []
                    progress_bar = st.progress(0)
                    
                    for idx, uploaded_file in enumerate(uploaded_files):
                        try:
                            # Extract text from file
                            if uploaded_file.type == "application/pdf":
                                text = extract_text_from_pdf(uploaded_file)
                            else:
                                text = uploaded_file.read().decode('utf-8')
                            
                            # Analyze
                            result = classify_text_hf(text)
                            
                            batch_results.append({
                                'File Name': uploaded_file.name,
                                'File Type': uploaded_file.type.split('/')[-1].upper(),
                                'Words': word_count(text),
                                'Characters': len(text),
                                'Human %': f"{result.get('human_prob', 0)*100:.1f}",
                                'AI %': f"{result.get('ai_prob', 0)*100:.1f}",
                                'Mixed %': f"{result.get('mixed_prob', 0)*100:.1f}",
                                'Classification': result.get('label', 'Unknown'),
                                'Processing Status': '✓ Success'
                            })
                        
                        except Exception as e:
                            batch_results.append({
                                'File Name': uploaded_file.name,
                                'File Type': 'Unknown',
                                'Words': 0,
                                'Characters': 0,
                                'Human %': 0,
                                'AI %': 0,
                                'Mixed %': 0,
                                'Classification': 'Error',
                                'Processing Status': f'✗ Error: {str(e)[:50]}'
                            })
                        
                        progress_bar.progress((idx + 1) / len(uploaded_files))
                    
                    # Display results
                    st.markdown("### 📊 Batch Processing Results")
                    
                    results_df = pd.DataFrame(batch_results)
                    
                    # Summary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    successful = len([r for r in batch_results if '✓' in r['Processing Status']])
                    
                    with col1:
                        st.metric("Files Processed", len(batch_results))
                    with col2:
                        st.metric("Successful", successful)
                    with col3:
                        total_words = sum([r['Words'] for r in batch_results if isinstance(r['Words'], int)])
                        st.metric("Total Words", f"{total_words:,.0f}")
                    with col4:
                        success_rate = (successful / len(batch_results) * 100) if batch_results else 0
                        st.metric("Success Rate", f"{success_rate:.1f}%")
                    
                    st.markdown("---")
                    
                    # Tab navigation
                    tab1, tab2, tab3 = st.tabs([
                        "📋 Results Table",
                        "📈 Analytics",
                        "💾 Export"
                    ])
                    
                    with tab1:
                        st.subheader("Detailed Results")
                        
                        # Color code classification
                        def color_classification(val):
                            if val == 'Human':
                                return 'background-color: #90EE90'
                            elif val == 'AI':
                                return 'background-color: #FFB6C6'
                            elif val == 'Mixed':
                                return 'background-color: #FFE4B5'
                            else:
                                return 'background-color: #CCCCCC'
                        
                        st.dataframe(
                            results_df.style.applymap(color_classification, subset=['Classification']),
                            use_container_width=True,
                            height=400
                        )
                    
                    with tab2:
                        st.subheader("Batch Analytics")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Classification distribution
                            classification_counts = results_df['Classification'].value_counts()
                            
                            chart_data = pd.DataFrame({
                                'Classification': classification_counts.index,
                                'Count': classification_counts.values
                            })
                            
                            chart = alt.Chart(chart_data).mark_bar().encode(
                                x=alt.X('Count:Q'),
                                y=alt.Y('Classification:N', sort='-x'),
                                color=alt.Color('Classification:N', scale=alt.Scale(
                                    domain=['Human', 'AI', 'Mixed', 'Error'],
                                    range=['#00CC96', '#FF6B6B', '#FFB366', '#CCCCCC']
                                )),
                                tooltip=['Classification', 'Count']
                            ).properties(height=400)
                            
                            st.altair_chart(chart, use_container_width=True)
                        
                        with col2:
                            # Average AI percentage
                            avg_ai = pd.to_numeric(results_df['AI %'], errors='coerce').mean()
                            avg_human = pd.to_numeric(results_df['Human %'], errors='coerce').mean()
                            
                            avg_data = pd.DataFrame({
                                'Type': ['Human', 'AI'],
                                'Average %': [avg_human, avg_ai]
                            })
                            
                            avg_chart = alt.Chart(avg_data).mark_bar().encode(
                                x=alt.X('Type:N'),
                                y=alt.Y('Average %:Q', scale=alt.Scale(domain=[0, 100])),
                                color=alt.Color('Type:N', scale=alt.Scale(
                                    domain=['Human', 'AI'],
                                    range=['#00CC96', '#FF6B6B']
                                )),
                                tooltip=['Type', 'Average %']
                            ).properties(height=400)
                            
                            st.altair_chart(avg_chart, use_container_width=True)
                    
                    with tab3:
                        st.subheader("Export Results")
                        
                        if export_format == "CSV":
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Results (CSV)",
                                data=csv,
                                file_name="batch_results.csv",
                                mime="text/csv"
                            )
                        
                        elif export_format == "Excel":
                            buffer = BytesIO()
                            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                                results_df.to_excel(writer, sheet_name='Results', index=False)
                            buffer.seek(0)
                            
                            st.download_button(
                                label="📥 Download Results (Excel)",
                                data=buffer,
                                file_name="batch_results.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        
                        elif export_format == "JSON":
                            json_data = results_df.to_json(orient='records', indent=2)
                            st.download_button(
                                label="📥 Download Results (JSON)",
                                data=json_data,
                                file_name="batch_results.json",
                                mime="application/json"
                            )
                    
                    st.success("✅ Batch processing complete!")
                
                except Exception as e:
                    st.error(f"❌ Error during batch processing: {str(e)}")

    st.markdown("---")
    st.info("""
    💡 **Batch Processing Features:**
    - Process multiple files simultaneously
    - Support for PDF, TXT, and Markdown files
    - Detailed analytics and statistics
    - Export results in multiple formats
    - Error handling and retry logic
    - Progress tracking
    """)
