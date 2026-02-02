# main.py
import streamlit as st
from pages.ai_detection import show_pdf_detection_page
from pages.humanize_text import show_humanize_page
from pages.text_analysis import show_text_analysis_page
from pages.statistics_dashboard import show_statistics_page
from pages.document_comparison import show_document_comparison_page
from pages.batch_processing import show_batch_processing_page

# Custom CSS for Outstanding UI
def inject_custom_css():
    custom_css = """
    <style>
        /* Main theme colors */
        :root {
            --primary: #FF6B6B;
            --secondary: #4ECDC4;
            --accent: #FFE66D;
            --dark: #2C3E50;
            --light: #F8F9FA;
            --success: #95E1D3;
        }
        
        /* Global Styling */
        * {
            margin: 0;
            padding: 0;
        }
        
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Main container */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #2C3E50;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        h1 {
            font-size: 3em;
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        
        /* Card styling */
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 5px solid #FF6B6B;
            margin: 15px 0;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .card-secondary {
            border-left-color: #4ECDC4;
        }
        
        .card-accent {
            border-left-color: #FFE66D;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #FF6B6B, #FF8A80);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1em;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
        }
        
        /* Feature cards */
        .feature-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 10px 0;
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            border-top: 4px solid;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.15);
        }
        
        .feature-1 { border-top-color: #FF6B6B; }
        .feature-2 { border-top-color: #4ECDC4; }
        .feature-3 { border-top-color: #FFE66D; }
        .feature-4 { border-top-color: #95E1D3; }
        .feature-5 { border-top-color: #C7CEEA; }
        .feature-6 { border-top-color: #FCCB90; }
        
        /* Divider */
        hr {
            background: linear-gradient(to right, transparent, #FF6B6B, transparent);
            height: 2px;
            border: none;
            margin: 30px 0;
        }
        
        /* Text styling */
        p {
            color: #555;
            line-height: 1.8;
        }
        
        /* Subheader */
        .subheader {
            color: #FF6B6B;
            font-size: 1.5em;
            font-weight: 700;
            margin-bottom: 15px;
        }
        
        /* Icon styling */
        .icon {
            font-size: 2.5em;
            margin-right: 10px;
        }
        
        /* Info box */
        .info-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        /* Success box */
        .success-box {
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
            color: #2C3E50;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-weight: 600;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            background-color: transparent;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="AI Content Detector & Humanizer - Professional Suite",
        layout="wide", 
        initial_sidebar_state="collapsed",
        menu_items=None
    )
    
    # Inject custom CSS
    inject_custom_css()

    # Initialize the current page in session_state if not present
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Main"

    # Display the chosen page
    if st.session_state["current_page"] == "PDF Detection & Annotation":
        show_pdf_detection_page()
    elif st.session_state["current_page"] == "Humanize AI Text":
        show_humanize_page()
    elif st.session_state["current_page"] == "Direct Text Analysis":
        show_text_analysis_page()
    elif st.session_state["current_page"] == "Statistics Dashboard":
        show_statistics_page()
    elif st.session_state["current_page"] == "Document Comparison":
        show_document_comparison_page()
    elif st.session_state["current_page"] == "Batch Processing":
        show_batch_processing_page()
    else:
        show_main_page()


def show_main_page():
    st.title("📊 AI Content Detector & Humanizer Suite")
    st.markdown("---")

    st.markdown("""
    ## Welcome to the Complete AI Text Tools Suite!
    
    A comprehensive platform for analyzing, detecting, and transforming AI-generated content.
    Choose from 6 powerful tools to enhance your text analysis workflow.
    """)

    # Row 1: Original Tools
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 PDF Detection & Annotation")
        st.markdown("""
        - **Upload PDF documents** and analyze AI-generated content
        - **Classify each sentence** as AI-written or human-written
        - **Download annotated PDFs** with color-coded highlighting
        - **Visualize detection results** with interactive charts
        """)

        if st.button("Go to PDF Detection →", type="primary", use_container_width=True):
            st.session_state["current_page"] = "PDF Detection & Annotation"
            st.rerun()

    with col2:
        st.subheader("✍️ Humanize AI Text")
        st.markdown("""
        - **Transform AI-generated text** into natural human-like content
        - **Improve readability** and flow of your text
        - **Maintain original meaning** while enhancing style
        - **Support for various content types** (articles, emails, reports)
        """)

        if st.button("Go to Text Humanizer →", type="primary", use_container_width=True):
            st.session_state["current_page"] = "Humanize AI Text"
            st.rerun()

    st.markdown("---")

    # Row 2: New Tools
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📝 Direct Text Analysis")
        st.markdown("""
        - **Paste text directly** without uploading files
        - **Instant AI detection** on any content
        - **Sentence-level breakdown** of classifications
        - **Export results** as CSV
        """)

        if st.button("Go to Text Analysis →", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "Direct Text Analysis"
            st.rerun()

    with col2:
        st.subheader("⚡ Batch Processing")
        st.markdown("""
        - **Process multiple files** at once
        - **Support PDF & TXT files**
        - **Bulk analysis reports**
        - **Export in CSV/Excel/JSON**
        """)

        if st.button("Go to Batch Processing →", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "Batch Processing"
            st.rerun()

    with col3:
        st.subheader("🔗 Document Comparison")
        st.markdown("""
        - **Compare up to 3 documents**
        - **Similarity analysis**
        - **AI content distribution**
        - **Side-by-side metrics**
        """)

        if st.button("Go to Comparison →", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "Document Comparison"
            st.rerun()

    st.markdown("---")

    # Row 3: Analytics
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📊 Statistics Dashboard")
        st.markdown("""
        - **Real-time analytics** and metrics
        - **Usage history tracking**
        - **Performance insights**
        - **Exportable reports**
        """)

        if st.button("Go to Dashboard →", type="secondary", use_container_width=True):
            st.session_state["current_page"] = "Statistics Dashboard"
            st.rerun()

    with col1:
        col_empty = st.empty()

    st.markdown("---")
    st.markdown("""
    ### How to Get Started:
    1. **Choose a tool** from the options above based on your needs
    2. **Upload or paste** your content
    3. **Let AI algorithms** process and analyze
    4. **Download or export** your enhanced results
    
    **Note**: All processing happens securely - your data remains private.
    
    ### Feature Highlights:
    - 🤖 **Advanced AI Detection** - Powered by state-of-the-art models
    - 📊 **Real-time Analytics** - Track all your analyses
    - 🔒 **Privacy First** - No data stored externally
    - 📱 **User-Friendly Interface** - Intuitive design
    - ⚡ **Fast Processing** - Instant results
    """)

if __name__ == "__main__":
    main()
