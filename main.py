# main.py - Modern Premium UI Design
import streamlit as st
from pages.ai_detection import show_pdf_detection_page
from pages.humanize_text import show_humanize_page
from pages.text_analysis import show_text_analysis_page
from pages.statistics_dashboard import show_statistics_page
from pages.document_comparison import show_document_comparison_page
from pages.batch_processing import show_batch_processing_page

# Custom CSS for Premium Modern Design
def inject_custom_css():
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body, .main {
            background-color: #fafafa;
            font-family: 'Inter', sans-serif;
            color: #1f2937;
        }
        
        /* Typography */
        h1, h2, h3 {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
        }
        
        h1 {
            font-size: 3.5rem;
            color: #1f2937;
            line-height: 1.2;
            letter-spacing: -0.02em;
            margin-bottom: 1rem;
        }
        
        h2 {
            font-size: 2.25rem;
            color: #1f2937;
            margin: 2rem 0 1.5rem 0;
            line-height: 1.3;
        }
        
        h3 {
            font-size: 1.5rem;
            color: #1f2937;
            margin-bottom: 0.75rem;
        }
        
        p {
            color: #6b7280;
            line-height: 1.6;
            font-size: 1rem;
        }
        
        /* Gradient Text */
        .gradient-text {
            background: linear-gradient(135deg, #ff6b6b 0%, #14b8a6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Glass Effect Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 2px 15px -3px rgba(0, 0, 0, 0.07);
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.1);
            border-color: #3b82f6;
        }
        
        /* Feature Cards */
        .feature-card-premium {
            background: white;
            border-radius: 1.5rem;
            padding: 2rem;
            border: 1px solid #e5e7eb;
            box-shadow: 0 2px 15px -3px rgba(0, 0, 0, 0.07);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .feature-card-premium::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 150px;
            height: 150px;
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, transparent 70%);
            border-radius: 50% 0 0 50%;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .feature-card-premium:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.1);
            border-color: #3b82f6;
        }
        
        .feature-card-premium:hover::before {
            opacity: 1;
        }
        
        .feature-card-premium h3 {
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: #1f2937;
        }
        
        .feature-card-premium ul {
            list-style: none;
            padding: 0;
            margin: 1.5rem 0 0 0;
        }
        
        .feature-card-premium li {
            color: #6b7280;
            padding: 0.5rem 0;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        
        .feature-card-premium li:before {
            content: "✓ ";
            color: #3b82f6;
            font-weight: 700;
            margin-right: 0.5rem;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #ff6b6b 0%, #ff8a80 100%);
            color: white !important;
            border: none !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 0.75rem !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4) !important;
        }
        
        /* Mesh Gradient Background */
        .mesh-gradient {
            background-color: #fafafa;
            background-image: 
                radial-gradient(at 0% 0%, rgba(255, 107, 107, 0.1) 0, transparent 50%), 
                radial-gradient(at 100% 0%, rgba(20, 184, 166, 0.1) 0, transparent 50%);
        }
        
        /* Section Headers */
        .section-header {
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
        }
        
        .section-header span {
            color: #ff6b6b;
            font-weight: 600;
            font-size: 0.75rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        
        /* Benefits Grid */
        .benefits-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .benefit-item {
            text-align: center;
        }
        
        .benefit-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .benefit-item h4 {
            font-size: 1.125rem;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 0.5rem;
        }
        
        .benefit-item p {
            font-size: 0.9rem;
            color: #6b7280;
        }
        
        /* CTA Banner */
        .cta-banner-premium {
            background: linear-gradient(135deg, #ff6b6b 0%, #14b8a6 100%);
            color: white;
            border-radius: 1.5rem;
            padding: 3rem;
            text-align: center;
            margin: 3rem 0;
            box-shadow: 0 20px 40px -15px rgba(255, 107, 107, 0.3);
        }
        
        .cta-banner-premium h2 {
            color: white;
            margin-top: 0;
        }
        
        .cta-banner-premium p {
            color: rgba(255, 255, 255, 0.9);
        }
        
        /* Tips Section */
        .tips-premium {
            background: white;
            border-left: 4px solid #ff6b6b;
            border-radius: 1rem;
            padding: 2rem;
            margin: 2rem 0;
            box-shadow: 0 2px 15px -3px rgba(0, 0, 0, 0.07);
            border: 1px solid #e5e7eb;
        }
        
        .tips-premium h3 {
            margin-top: 0;
            color: #1f2937;
        }
        
        .tips-premium ul {
            list-style: none;
            padding: 0;
            margin: 1.5rem 0 0 0;
        }
        
        .tips-premium li {
            color: #6b7280;
            padding: 0.75rem 0;
            line-height: 1.6;
            font-size: 0.95rem;
        }
        
        .tips-premium li strong {
            color: #1f2937;
        }
        
        /* Footer */
        .footer-premium {
            text-align: center;
            padding: 2rem 0;
            border-top: 1px solid #e5e7eb;
            color: #9ca3af;
            font-size: 0.875rem;
            margin-top: 3rem;
        }
        
        /* Animations */
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-in {
            animation: slideUp 0.5s ease-out forwards;
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
    # Hero Section
    st.markdown("""
    <div class="mesh-gradient" style="padding: 3rem 0; border-radius: 1.5rem;">
        <div style="text-align: center;">
            <div style="display: inline-flex; align-items: center; gap: 0.5rem; 
                        background: rgba(255,255,255,0.9); padding: 0.5rem 1rem; 
                        border-radius: 9999px; border: 1px solid #ffb3b3; margin-bottom: 1.5rem;">
                <span style="width: 0.5rem; height: 0.5rem; border-radius: 50%; 
                            background: #ff6b6b;"></span>
                <span style="font-size: 0.875rem; font-weight: 600; color: #be1717;">
                    AI-Powered Content Analysis
                </span>
            </div>
            
            <h1 style="margin: 0; line-height: 1.2;">
                Detect & Humanize<br>
                <span class="gradient-text">AI Content</span> Instantly
            </h1>
            
            <p style="font-size: 1.125rem; max-width: 600px; margin: 1.5rem auto; color: #6b7280;">
                Professional suite for detecting AI-generated content and transforming it into 
                natural, human-like writing with enterprise-grade accuracy.
            </p>
            
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-top: 2rem;">
                <p style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #6b7280;">
                    ✓ No data storage
                </p>
                <p style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #6b7280;">
                    ✓ Real-time processing
                </p>
                <p style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #6b7280;">
                    ✓ 99.9% accuracy
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Navigation
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-top: 1px solid #e5e7eb; 
                border-bottom: 1px solid #e5e7eb; margin: 2rem 0;">
        <div style="text-align: center; margin-bottom: 1rem;">
            <span style="font-size: 0.875rem; font-weight: 600; color: #ff6b6b;">⚡ QUICK NAVIGATION</span>
            <p style="font-size: 0.875rem; color: #9ca3af; margin: 0.25rem 0 0 0;">Choose your tool below</p>
        </div>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <button style="padding: 0.5rem 1rem; background: #f3f4f6; border: 1px solid #e5e7eb; 
                          border-radius: 9999px; font-size: 0.875rem; font-weight: 500; 
                          cursor: pointer; transition: all 0.3s;">
                📄 PDF Detection
            </button>
            <button style="padding: 0.5rem 1rem; background: #f3f4f6; border: 1px solid #e5e7eb; 
                          border-radius: 9999px; font-size: 0.875rem; font-weight: 500; 
                          cursor: pointer; transition: all 0.3s;">
                ✍️ Text Humanization
            </button>
            <button style="padding: 0.5rem 1rem; background: #f3f4f6; border: 1px solid #e5e7eb; 
                          border-radius: 9999px; font-size: 0.875rem; font-weight: 500; 
                          cursor: pointer; transition: all 0.3s;">
                ⚡ Batch Processing
            </button>
            <button style="padding: 0.5rem 1rem; background: #f3f4f6; border: 1px solid #e5e7eb; 
                          border-radius: 9999px; font-size: 0.875rem; font-weight: 500; 
                          cursor: pointer; transition: all 0.3s;">
                📊 Dashboard
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Core Tools Section
    st.markdown("""
    <div class="section-header">
        <span style="color: #ff6b6b; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.1em; 
                    text-transform: uppercase;">Core Features</span>
        <h2 style="margin-top: 0.5rem;">Essential Analysis Tools</h2>
        <p style="color: #6b7280; margin-top: 0.5rem;">Powerful detection and transformation capabilities at your fingertips</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="feature-card-premium">
            <h3>🔍 PDF Detection & Annotation</h3>
            <p>Analyze PDFs for AI-generated content with sentence-level classification and interactive visualizations.</p>
            <ul>
                <li>Sentence-level classification</li>
                <li>Download annotated PDFs</li>
                <li>Real-time detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 Analyze PDF", key="btn_pdf", use_container_width=True):
            st.session_state["current_page"] = "PDF Detection & Annotation"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card-premium">
            <h3>✍️ Text Humanization</h3>
            <p>Transform AI-generated text into natural, human-like writing while preserving accuracy.</p>
            <ul>
                <li>Smart rewriting engine</li>
                <li>Citation protection</li>
                <li>Customizable intensity</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✨ Humanize Text", key="btn_humanize", use_container_width=True):
            st.session_state["current_page"] = "Humanize AI Text"
            st.rerun()
    
    # Advanced Tools Section
    st.markdown("""
    <div class="section-header" style="margin-top: 3rem;">
        <span style="color: #14b8a6; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.1em; 
                    text-transform: uppercase;">Advanced Capabilities</span>
        <h2 style="margin-top: 0.5rem;">Specialized Analysis Tools</h2>
        <p style="color: #6b7280; margin-top: 0.5rem;">Handle complex workflows with advanced processing</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="feature-card-premium" style="background: #f3f4f6; border-color: #fcd34d;">
            <h3>📝 Direct Text Analysis</h3>
            <p style="font-size: 0.95rem;">Instant AI detection on any text with breakdown and confidence charts.</p>
            <ul>
                <li>Paste & analyze instantly</li>
                <li>Sentence breakdown</li>
                <li>CSV export</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Text Analysis", key="btn_text", use_container_width=True):
            st.session_state["current_page"] = "Direct Text Analysis"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card-premium" style="background: #f3f4f6; border-color: #14b8a6;">
            <h3>⚡ Batch Processing</h3>
            <p style="font-size: 0.95rem;">Process multiple files simultaneously with parallel processing.</p>
            <ul>
                <li>Upload up to 10 files</li>
                <li>Parallel processing</li>
                <li>Multi-format export</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ Batch Process", key="btn_batch", use_container_width=True):
            st.session_state["current_page"] = "Batch Processing"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="feature-card-premium" style="background: #f3f4f6; border-color: #ff6b6b;">
            <h3>🔗 Document Comparison</h3>
            <p style="font-size: 0.95rem;">Compare 2-3 documents side-by-side with similarity analysis.</p>
            <ul>
                <li>Compare multiple documents</li>
                <li>Similarity matrix</li>
                <li>Detailed metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔗 Compare", key="btn_compare", use_container_width=True):
            st.session_state["current_page"] = "Document Comparison"
            st.rerun()
    
    # Analytics Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); 
                color: white; padding: 3rem; border-radius: 1.5rem; 
                margin: 3rem 0; box-shadow: 0 20px 40px -15px rgba(255, 107, 107, 0.3);">
        <div style="text-align: center;">
            <span style="color: #ff6b6b; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.1em; 
                        text-transform: uppercase;">Analytics & Insights</span>
            <h2 style="color: white; margin-top: 0.5rem;">📊 Statistics Dashboard</h2>
            <p style="color: rgba(255,255,255,0.8); margin-top: 1rem; font-size: 1.125rem;">
                Track usage patterns, performance metrics, and content trends with comprehensive analytics
            </p>
        </div>
    </div>
    
    <div style="background: white; border-radius: 1.5rem; padding: 2rem; 
                border: 1px solid #e5e7eb; box-shadow: 0 2px 15px -3px rgba(0,0,0,0.07);">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
            <div style="padding: 1.5rem; background: #f3f4f6; border-radius: 1rem; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
                <h4 style="margin: 0.5rem 0; font-weight: 600;">Real-time Analytics</h4>
                <p style="font-size: 0.875rem; color: #6b7280; margin: 0;">Monitor detection accuracy and metrics</p>
            </div>
            <div style="padding: 1.5rem; background: #f3f4f6; border-radius: 1rem; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📅</div>
                <h4 style="margin: 0.5rem 0; font-weight: 600;">Activity Timeline</h4>
                <p style="font-size: 0.875rem; color: #6b7280; margin: 0;">Historical view of all activities</p>
            </div>
            <div style="padding: 1.5rem; background: #f3f4f6; border-radius: 1rem; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📥</div>
                <h4 style="margin: 0.5rem 0; font-weight: 600;">Export Reports</h4>
                <p style="font-size: 0.875rem; color: #6b7280; margin: 0;">Download CSV and PDF reports</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Open Dashboard", key="btn_stats", use_container_width=True):
        st.session_state["current_page"] = "Statistics Dashboard"
        st.rerun()
    
    # Benefits Section
    st.markdown("""
    <div class="section-header" style="margin-top: 3rem; border: none;">
        <h2 style="margin-top: 0;">✨ Why Choose Our Suite?</h2>
        <p style="color: #6b7280; margin-top: 1rem; font-size: 1.125rem;">
            Built for professionals who demand accuracy, speed, and privacy
        </p>
    </div>
    
    <div class="benefits-grid">
        <div class="benefit-item">
            <div class="benefit-icon">🎯</div>
            <h4>Precision Detection</h4>
            <p>State-of-the-art AI models for accurate content classification</p>
        </div>
        
        <div class="benefit-item">
            <div class="benefit-icon">⚡</div>
            <h4>Lightning Fast</h4>
            <p>Process documents in seconds with optimized algorithms</p>
        </div>
        
        <div class="benefit-item">
            <div class="benefit-icon">🔒</div>
            <h4>100% Private</h4>
            <p>Local processing ensures your data never leaves your device</p>
        </div>
        
        <div class="benefit-item">
            <div class="benefit-icon">📊</div>
            <h4>Detailed Reports</h4>
            <p>Comprehensive analysis with exportable visualizations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Banner
    st.markdown("""
    <div class="cta-banner-premium">
        <h2>🚀 Ready to Get Started?</h2>
        <p>Choose a tool above to begin analyzing your content instantly. 
           Start with "Direct Text Analysis" for a quick demo.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Tips
    st.markdown("""
    <div class="tips-premium">
        <h3 style="margin-top: 0; display: flex; align-items: center; gap: 0.5rem;">
            💡 Quick Tips
        </h3>
        <ul>
            <li><strong>PDF Detection:</strong> Perfect for research papers and academic documents</li>
            <li><strong>Text Analysis:</strong> Best for quick checks on emails and articles</li>
            <li><strong>Batch Processing:</strong> Ideal for processing multiple documents at scale</li>
            <li><strong>Comparison:</strong> Compare original vs. humanized versions</li>
            <li><strong>Dashboard:</strong> Monitor analysis history and trends</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer-premium">
        <p>AI Content Detector & Humanizer • Professional Suite for Content Analysis</p>
        <p style="font-size: 0.8rem; color: #d1d5db; margin-top: 0.5rem;">
            © 2024 ContentGuard Suite. All rights reserved.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
