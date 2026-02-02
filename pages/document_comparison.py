"""
Document Comparison & Similarity Analysis
"""
import streamlit as st
import pandas as pd
import altair as alt
from utils.ai_detection_utils import classify_text_hf
from utils.pdf_utils import word_count
from difflib import SequenceMatcher

def show_document_comparison_page():
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Main", type="secondary"):
            st.session_state["current_page"] = "Main"
            st.rerun()

    st.title("🔗 Document Comparison & Similarity Analysis")

    st.markdown("""
    ### Compare Multiple Documents
    
    Analyze and compare up to 3 documents to identify similarities, differences, 
    and AI content distribution across documents.
    """)

    st.markdown("---")

    # Input method selection
    col1, col2 = st.columns(2)
    with col1:
        comparison_mode = st.radio(
            "Select Comparison Mode:",
            ["Paste Text", "File Upload"],
            horizontal=True
        )

    # Initialize session state
    if "comparison_docs" not in st.session_state:
        st.session_state.comparison_docs = {}

    # Get documents based on mode
    num_docs = st.slider("Number of Documents to Compare:", min_value=2, max_value=3, value=2)

    documents = {}
    
    if comparison_mode == "Paste Text":
        st.markdown("### Enter Documents")
        
        cols = st.columns(num_docs)
        
        for i in range(num_docs):
            with cols[i]:
                st.markdown(f"#### Document {i+1}")
                documents[f"doc_{i+1}"] = st.text_area(
                    f"Paste text for document {i+1}:",
                    height=200,
                    key=f"text_doc_{i+1}",
                    placeholder=f"Enter text for document {i+1}..."
                )
    
    else:  # File Upload
        st.markdown("### Upload Documents")
        
        cols = st.columns(num_docs)
        
        for i in range(num_docs):
            with cols[i]:
                st.markdown(f"#### Document {i+1}")
                uploaded_file = st.file_uploader(
                    f"Upload document {i+1}:",
                    type=["txt", "md"],
                    key=f"file_doc_{i+1}"
                )
                
                if uploaded_file:
                    documents[f"doc_{i+1}"] = uploaded_file.read().decode('utf-8')
                else:
                    documents[f"doc_{i+1}"] = ""

    # Analysis button
    if st.button("🔍 Compare Documents", type="primary", use_container_width=True):
        # Validate inputs
        filled_docs = {k: v for k, v in documents.items() if v.strip()}
        
        if len(filled_docs) < 2:
            st.error("Please provide at least 2 documents to compare.")
        else:
            with st.spinner("Analyzing and comparing documents..."):
                try:
                    # Analyze each document
                    analysis_results = {}
                    
                    for doc_name, content in filled_docs.items():
                        result = classify_text_hf(content)
                        analysis_results[doc_name] = {
                            'content': content,
                            'word_count': word_count(content),
                            'sentence_count': len([s for s in content.split('.') if s.strip()]),
                            'human_prob': result.get('human_prob', 0),
                            'ai_prob': result.get('ai_prob', 0),
                            'mixed_prob': result.get('mixed_prob', 0),
                            'label': result.get('label', 'Unknown')
                        }
                    
                    # Display comparison results
                    st.markdown("### 📊 Comparison Results")
                    
                    # Tab navigation
                    tab1, tab2, tab3, tab4 = st.tabs([
                        "📈 Overview",
                        "🔍 Detailed Analysis",
                        "📋 Similarity Matrix",
                        "📑 Full Comparison"
                    ])
                    
                    with tab1:
                        st.subheader("Document Overview")
                        
                        # Create comparison dataframe
                        comparison_df = pd.DataFrame({
                            'Document': list(analysis_results.keys()),
                            'Word Count': [analysis_results[d]['word_count'] for d in analysis_results],
                            'Sentences': [analysis_results[d]['sentence_count'] for d in analysis_results],
                            'Human %': [f"{analysis_results[d]['human_prob']*100:.1f}%" for d in analysis_results],
                            'AI %': [f"{analysis_results[d]['ai_prob']*100:.1f}%" for d in analysis_results],
                            'Mixed %': [f"{analysis_results[d]['mixed_prob']*100:.1f}%" for d in analysis_results],
                            'Classification': [analysis_results[d]['label'] for d in analysis_results]
                        })
                        
                        st.dataframe(comparison_df, use_container_width=True)
                    
                    with tab2:
                        st.subheader("Detailed Analysis")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # AI Content comparison chart
                            ai_data = pd.DataFrame({
                                'Document': list(analysis_results.keys()),
                                'Human': [analysis_results[d]['human_prob']*100 for d in analysis_results],
                                'AI': [analysis_results[d]['ai_prob']*100 for d in analysis_results],
                                'Mixed': [analysis_results[d]['mixed_prob']*100 for d in analysis_results]
                            })
                            
                            chart_data = ai_data.melt(
                                id_vars=['Document'],
                                var_name='Type',
                                value_name='Percentage'
                            )
                            
                            chart = alt.Chart(chart_data).mark_bar().encode(
                                x=alt.X('Document:N'),
                                y=alt.Y('Percentage:Q', scale=alt.Scale(domain=[0, 100])),
                                color=alt.Color('Type:N', scale=alt.Scale(
                                    domain=['Human', 'AI', 'Mixed'],
                                    range=['#00CC96', '#FF6B6B', '#FFB366']
                                )),
                                tooltip=['Document', 'Type', 'Percentage']
                            ).properties(height=400)
                            
                            st.altair_chart(chart, use_container_width=True)
                        
                        with col2:
                            # Word count comparison
                            wc_data = pd.DataFrame({
                                'Document': list(analysis_results.keys()),
                                'Words': [analysis_results[d]['word_count'] for d in analysis_results]
                            })
                            
                            wc_chart = alt.Chart(wc_data).mark_bar().encode(
                                x=alt.X('Document:N'),
                                y=alt.Y('Words:Q'),
                                color=alt.value('#4C72B0'),
                                tooltip=['Document', 'Words']
                            ).properties(height=400)
                            
                            st.altair_chart(wc_chart, use_container_width=True)
                    
                    with tab3:
                        st.subheader("Similarity Matrix")
                        
                        # Calculate similarity between documents
                        docs_list = list(filled_docs.keys())
                        similarity_matrix = []
                        
                        for doc1 in docs_list:
                            row = []
                            for doc2 in docs_list:
                                if doc1 == doc2:
                                    similarity = 1.0
                                else:
                                    content1 = filled_docs[doc1]
                                    content2 = filled_docs[doc2]
                                    similarity = SequenceMatcher(None, content1, content2).ratio()
                                row.append(similarity * 100)
                            similarity_matrix.append(row)
                        
                        similarity_df = pd.DataFrame(
                            similarity_matrix,
                            index=docs_list,
                            columns=docs_list
                        )
                        
                        st.dataframe(similarity_df, use_container_width=True)
                        
                        st.info("""
                        📌 **Similarity Matrix Explanation:**
                        - 100% = Identical documents
                        - 75-99% = Highly similar
                        - 50-74% = Moderately similar
                        - 25-49% = Low similarity
                        - 0-24% = Very different
                        """)
                    
                    with tab4:
                        st.subheader("Full Document Comparison")
                        
                        for doc_name, data in analysis_results.items():
                            with st.expander(f"📄 {doc_name.upper()} - {data['label']}"):
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.metric("Words", data['word_count'])
                                with col2:
                                    st.metric("Sentences", data['sentence_count'])
                                with col3:
                                    st.metric("AI %", f"{data['ai_prob']*100:.1f}%")
                                with col4:
                                    st.metric("Human %", f"{data['human_prob']*100:.1f}%")
                                
                                st.markdown("**Content Preview:**")
                                st.text_area(
                                    "Document content:",
                                    value=data['content'][:500] + "..." if len(data['content']) > 500 else data['content'],
                                    height=150,
                                    disabled=True
                                )
                    
                    # Export comparison report
                    st.markdown("---")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = comparison_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Comparison Report (CSV)",
                            data=csv,
                            file_name="document_comparison.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        if st.button("🔄 Start New Comparison"):
                            st.rerun()
                    
                    st.success("✅ Comparison complete!")
                
                except Exception as e:
                    st.error(f"❌ Error during comparison: {str(e)}")
                    st.info("Please try with different documents or shorter text.")

    st.markdown("---")
    st.info("""
    💡 **Comparison Features:**
    - Compare up to 3 documents simultaneously
    - AI content distribution analysis
    - Document similarity detection
    - Statistical comparison metrics
    - Exportable comparison reports
    """)
