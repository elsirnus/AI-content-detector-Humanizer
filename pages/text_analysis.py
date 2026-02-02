"""
Direct text input analysis page for AI detection and analysis
"""
import streamlit as st
import pandas as pd
import altair as alt
from utils.ai_detection_utils import classify_text_hf
from utils.pdf_utils import word_count

def show_text_analysis_page():
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Main", type="secondary"):
            st.session_state["current_page"] = "Main"
            st.rerun()

    st.title("📝 Direct Text Analysis & Detection")

    st.markdown("""
    ### Analyze Text Content Directly
    
    Paste or type your text directly to analyze whether it contains AI-generated content.
    Perfect for quick analysis without uploading PDF files.
    """)

    st.markdown("---")

    # Text input area
    col1, col2 = st.columns([3, 1])
    with col1:
        user_text = st.text_area(
            "Paste your text here:",
            height=250,
            placeholder="Enter or paste your text content for AI detection analysis..."
        )
    
    with col2:
        st.metric("Word Count", word_count(user_text) if user_text else 0)
        st.metric("Sentence Count", len([s for s in user_text.split('.') if s.strip()]) if user_text else 0)

    # Analysis options
    st.markdown("### Analysis Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        confidence_threshold = st.slider(
            "Confidence Threshold (%)",
            min_value=0,
            max_value=100,
            value=50,
            step=5
        )
    
    with col2:
        show_sentence_level = st.checkbox("Show Sentence-Level Analysis", value=True)
    
    with col3:
        show_visualization = st.checkbox("Show Charts", value=True)

    # Analyze button
    if st.button("🔍 Analyze Text", type="primary", use_container_width=True):
        if not user_text.strip():
            st.error("Please enter some text to analyze.")
        else:
            with st.spinner("Analyzing text..."):
                try:
                    # Classify the entire text
                    result = classify_text_hf(user_text)
                    
                    # Display overall results
                    st.markdown("### 📊 Overall Detection Results")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        human_prob = result.get('human_prob', 0)
                        st.metric("Human Probability", f"{human_prob*100:.1f}%")
                    
                    with col2:
                        ai_prob = result.get('ai_prob', 0)
                        st.metric("AI Probability", f"{ai_prob*100:.1f}%")
                    
                    with col3:
                        mixed_prob = result.get('mixed_prob', 0)
                        st.metric("Mixed Probability", f"{mixed_prob*100:.1f}%")
                    
                    with col4:
                        label = result.get('label', 'Unknown')
                        st.metric("Classification", label)
                    
                    # Visualization
                    if show_visualization:
                        st.markdown("### 📈 Probability Distribution")
                        
                        chart_data = pd.DataFrame({
                            'Category': ['Human', 'AI', 'Mixed'],
                            'Probability': [
                                human_prob * 100,
                                ai_prob * 100,
                                mixed_prob * 100
                            ]
                        })
                        
                        chart = alt.Chart(chart_data).mark_bar().encode(
                            x=alt.X('Category:N', title='Content Type'),
                            y=alt.Y('Probability:Q', title='Probability (%)', scale=alt.Scale(domain=[0, 100])),
                            color=alt.Color('Category:N', scale=alt.Scale(
                                domain=['Human', 'AI', 'Mixed'],
                                range=['#00CC96', '#FF6B6B', '#FFB366']
                            )),
                            tooltip=['Category', 'Probability']
                        ).properties(
                            height=400,
                            width=600
                        )
                        
                        st.altair_chart(chart, use_container_width=True)
                    
                    # Sentence-level analysis
                    if show_sentence_level:
                        st.markdown("### 🔬 Sentence-Level Analysis")
                        
                        sentences = [s.strip() for s in user_text.split('.') if s.strip()]
                        
                        if sentences:
                            results_data = []
                            
                            for idx, sentence in enumerate(sentences, 1):
                                sentence_result = classify_text_hf(sentence)
                                results_data.append({
                                    'Sentence #': idx,
                                    'Text': sentence[:100] + "..." if len(sentence) > 100 else sentence,
                                    'Classification': sentence_result.get('label', 'Unknown'),
                                    'Confidence': f"{max(sentence_result.get('human_prob', 0), sentence_result.get('ai_prob', 0), sentence_result.get('mixed_prob', 0))*100:.1f}%"
                                })
                            
                            results_df = pd.DataFrame(results_data)
                            
                            # Color code the results
                            def color_classification(val):
                                if val == 'Human':
                                    return 'background-color: #90EE90'
                                elif val == 'AI':
                                    return 'background-color: #FFB6C6'
                                else:
                                    return 'background-color: #FFE4B5'
                            
                            st.dataframe(
                                results_df.style.applymap(color_classification, subset=['Classification']),
                                use_container_width=True,
                                height=400
                            )
                            
                            # Download results
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Analysis Results (CSV)",
                                data=csv,
                                file_name="text_analysis_results.csv",
                                mime="text/csv"
                            )
                    
                    st.success("✅ Analysis complete!")
                
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    st.info("Please try with shorter text or a different format.")

    st.markdown("---")
    st.info("""
    💡 **Tips for best results:**
    - Paste complete sentences for accurate classification
    - Longer texts provide more context for better detection
    - The analysis runs sentence-by-sentence for detailed insights
    - Download results for further analysis or documentation
    """)
