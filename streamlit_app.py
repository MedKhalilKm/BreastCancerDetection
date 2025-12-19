import streamlit as st
import requests
import streamlit.components.v1 as components

API_URL = "http://127.0.0.1:8000/predict"

# ======================
# Page Configuration
# ======================
st.set_page_config(
    page_title="OncoScan - AI Breast Cancer Detection",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default elements
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    [data-testid="stAppViewContainer"] {padding: 0 !important;}
</style>
""", unsafe_allow_html=True)

# ======================
# Initialize Session State
# ======================
if "page" not in st.session_state:
    st.session_state.page = "landing"

# ======================
# Landing Page HTML
# ======================
LANDING_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #f9f7f4 0%, #f0ede8 50%, #fce8e6 100%);
            color: #1a2332;
            min-height: 100vh;
        }
        
        /* Navigation */
        .navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 4rem;
            background: rgba(249, 247, 244, 0.95);
            border-bottom: 1px solid #e8e4df;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a2332;
            text-decoration: none;
        }
        
        .logo svg {
            width: 28px;
            height: 28px;
            color: #1a9988;
        }
        
        .nav-links {
            display: flex;
            gap: 2.5rem;
            list-style: none;
        }
        
        .nav-links a {
            color: #5a6577;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
        }
        
        .nav-links a:hover {
            color: #1a2332;
        }
        
        .nav-actions {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        
        .btn-login {
            color: #5a6577;
            text-decoration: none;
            font-weight: 500;
        }
        
        .btn-primary {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, #1a9988 0%, #2ab5a2 100%);
            color: white;
            font-weight: 600;
            font-size: 0.95rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(26, 153, 136, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(26, 153, 136, 0.4);
        }
        
        .btn-outline {
            display: inline-flex;
            align-items: center;
            padding: 0.75rem 1.5rem;
            background: transparent;
            color: #e8837c;
            font-weight: 600;
            font-size: 0.95rem;
            border-radius: 8px;
            border: 2px solid #e8837c;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .btn-outline:hover {
            background: #e8837c;
            color: white;
        }
        
        /* Hero Section */
        .hero {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 4rem 2rem;
            min-height: calc(100vh - 80px);
            position: relative;
        }
        
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.625rem 1.25rem;
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #e8e4df;
            border-radius: 50px;
            font-size: 0.875rem;
            font-weight: 500;
            color: #1a9988;
            margin-bottom: 2rem;
        }
        
        .hero-badge svg {
            width: 16px;
            height: 16px;
            color: #e8837c;
        }
        
        .hero-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 4rem;
            font-weight: 700;
            line-height: 1.15;
            color: #1a2332;
            margin-bottom: 1.5rem;
        }
        
        .highlight-teal {
            color: #1a9988;
        }
        
        .highlight-coral {
            color: #e8837c;
        }
        
        .hero-description {
            max-width: 700px;
            margin: 0 auto 2.5rem;
            font-size: 1.125rem;
            line-height: 1.75;
            color: #5a6577;
        }
        
        .hero-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 3rem;
        }
        
        .trust-badges {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2rem;
            padding-top: 2rem;
            border-top: 1px solid #e8e4df;
            max-width: 700px;
        }
        
        .badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: #5a6577;
        }
        
        .badge svg {
            width: 18px;
            height: 18px;
            color: #8892a2;
        }
        
        .stat-number {
            font-weight: 700;
            color: #e8837c;
        }
        
        .badge-divider {
            width: 1px;
            height: 24px;
            background: #e8e4df;
        }
        
        /* Floating decorations */
        .floating-dot {
            position: absolute;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #1a9988;
            opacity: 0.4;
        }
        
        .dot-1 { top: 20%; right: 25%; }
        .dot-2 { top: 35%; right: 30%; width: 8px; height: 8px; }
        
        /* Sections */
        .section {
            padding: 80px 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .section-tag {
            display: block;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 2px;
            color: #e8837c;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .section-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a2332;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .section-description {
            max-width: 600px;
            margin: 0 auto 3rem;
            font-size: 1.1rem;
            color: #5a6577;
            text-align: center;
        }
        
        /* Features */
        .features-section {
            background: #f5f3f0;
            padding: 80px 2rem;
            border-radius: 24px;
            margin: 2rem;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            max-width: 1200px;
            margin: 3rem auto 0;
        }
        
        .feature-card {
            background: white;
            padding: 2.5rem 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(26, 35, 50, 0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 30px rgba(26, 35, 50, 0.12);
        }
        
        .feature-icon {
            width: 56px;
            height: 56px;
            border-radius: 12px;
            background: linear-gradient(135deg, #e8f5f3, #d0ebe7);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
        }
        
        .feature-card h3 {
            font-size: 1.25rem;
            font-weight: 700;
            color: #1a2332;
            margin-bottom: 0.75rem;
        }
        
        .feature-card p {
            font-size: 0.95rem;
            line-height: 1.7;
            color: #5a6577;
        }
        
        /* Process */
        .process-steps {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 2rem;
            max-width: 1200px;
            margin: 3rem auto 0;
        }
        
        .process-step {
            text-align: center;
        }
        
        .step-circle {
            position: relative;
            width: 80px;
            height: 80px;
            margin: 0 auto 1.5rem;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(26, 153, 136, 0.1), rgba(26, 153, 136, 0.2));
            border: 2px solid #1a9988;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        .step-number {
            position: absolute;
            top: -8px;
            right: -8px;
            width: 28px;
            height: 28px;
            background: #e8837c;
            color: white;
            font-size: 0.7rem;
            font-weight: 700;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .process-step h4 {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1a2332;
            margin-bottom: 0.75rem;
        }
        
        .process-step p {
            font-size: 0.9rem;
            line-height: 1.6;
            color: #5a6577;
            max-width: 220px;
            margin: 0 auto;
        }
        
        /* Footer */
        .footer {
            background: #1a2332;
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            margin-top: 4rem;
        }
        
        .footer p {
            color: rgba(255, 255, 255, 0.6);
        }
        
        /* Responsive */
        @media (max-width: 992px) {
            .features-grid { grid-template-columns: repeat(2, 1fr); }
            .process-steps { grid-template-columns: repeat(2, 1fr); }
            .navbar { padding: 1rem 2rem; }
            .nav-links { display: none; }
        }
        
        @media (max-width: 768px) {
            .hero-title { font-size: 2.5rem; }
            .features-grid, .process-steps { grid-template-columns: 1fr; }
            .trust-badges { flex-direction: column; gap: 1rem; }
            .badge-divider { display: none; }
            .hero-buttons { flex-direction: column; align-items: center; }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <a href="#" class="logo">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
            OncoScan
        </a>
        <ul class="nav-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#process">How It Works</a></li>
            <li><a href="#about">About</a></li>
        </ul>
        <div class="nav-actions">
            <a href="#" class="btn-login">Log In</a>
            <a href="#" class="btn-primary" onclick="window.parent.postMessage('startAnalysis', '*')">Get Started</a>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero">
        <div class="floating-dot dot-1"></div>
        <div class="floating-dot dot-2"></div>
        
        <div class="hero-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
            </svg>
            AI-Powered Early Detection
        </div>
        
        <h1 class="hero-title">
            Detect Breast Cancer<br>
            <span class="highlight-teal">Earlier</span>,<br>
            Save Lives <span class="highlight-coral">Together</span>
        </h1>
        
        <p class="hero-description">
            Our advanced AI analyzes mammography scans with exceptional accuracy, 
            helping healthcare professionals identify tumors at their earliest, most treatable stages.
        </p>
        
        <div class="hero-buttons">
            <button class="btn-primary" onclick="window.parent.postMessage('startAnalysis', '*')">
                Start Analysis
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
            </button>
            <a href="#features" class="btn-outline">Learn More</a>
        </div>
        
        <div class="trust-badges">
            <div class="badge">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                HIPAA Compliant
            </div>
            <div class="badge-divider"></div>
            <div class="badge">
                <span class="stat-number">98.5%</span>&nbsp;Detection Accuracy
            </div>
            <div class="badge-divider"></div>
            <div class="badge">
                Trusted by <strong>&nbsp;500+&nbsp;</strong> Clinics
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
        <span class="section-tag">FEATURES</span>
        <h2 class="section-title">Advanced Detection,<br>Simplified Workflow</h2>
        <p class="section-description">
            Empowering healthcare professionals with cutting-edge tools to improve patient outcomes.
        </p>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <h3>AI-Powered Analysis</h3>
                <p>Deep learning algorithms trained on millions of scans deliver precise tumor detection and classification.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Rapid Results</h3>
                <p>Get comprehensive analysis results in under 60 seconds, enabling faster clinical decisions.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3>High Precision</h3>
                <p>Detects tumors as small as 2mm with industry-leading sensitivity and specificity rates.</p>
            </div>
        </div>
    </section>

    <!-- Process Section -->
    <section id="process" class="section">
        <span class="section-tag">PROCESS</span>
        <h2 class="section-title">How It Works</h2>
        <p class="section-description">
            From scan upload to actionable insights in four simple steps.
        </p>
        <div class="process-steps">
            <div class="process-step">
                <div class="step-circle">
                    📤
                    <span class="step-number">01</span>
                </div>
                <h4>Upload Scan</h4>
                <p>Securely upload mammography images in DICOM or standard image formats.</p>
            </div>
            <div class="process-step">
                <div class="step-circle">
                    🤖
                    <span class="step-number">02</span>
                </div>
                <h4>AI Analysis</h4>
                <p>Our neural network processes the scan, identifying potential areas of concern.</p>
            </div>
            <div class="process-step">
                <div class="step-circle">
                    📋
                    <span class="step-number">03</span>
                </div>
                <h4>Review Results</h4>
                <p>Receive detailed findings with annotated images and confidence scores.</p>
            </div>
            <div class="process-step">
                <div class="step-circle">
                    💬
                    <span class="step-number">04</span>
                </div>
                <h4>Collaborate</h4>
                <p>Share results with specialists and discuss treatment options with patients.</p>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <div class="footer">
        <p>© 2024 OncoScan - AI-Powered Breast Cancer Detection</p>
    </div>

    <script>
        // Handle button clicks to communicate with Streamlit
        document.querySelectorAll('button, .btn-primary').forEach(btn => {
            btn.addEventListener('click', function(e) {
                if (this.textContent.includes('Start') || this.textContent.includes('Get Started')) {
                    window.parent.postMessage('startAnalysis', '*');
                }
            });
        });
    </script>
</body>
</html>
"""

# ======================
# Prediction Page CSS
# ======================
def load_prediction_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f9f7f4 0%, #f0ede8 100%) !important;
    }
    
    .main .block-container {
        padding-top: 2rem !important;
        max-width: 900px !important;
    }
    
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #1a2332 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1a9988 0%, #2ab5a2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26, 153, 136, 0.4) !important;
    }
    
    .back-btn button {
        background: transparent !important;
        color: #1a9988 !important;
        border: 2px solid #1a9988 !important;
    }
    
    .stNumberInput label, .stTextInput label {
        color: #1a2332 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stForm {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(26, 35, 50, 0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# ======================
# Landing Page
# ======================
def show_landing_page():
    # Render the HTML landing page as a component
    components.html(LANDING_PAGE_HTML, height=2200, scrolling=True)
    
    # Listen for messages from the iframe
    # Using a hidden button that gets triggered by JavaScript
    if st.button("Go to Analysis", key="hidden_btn", type="primary"):
        st.session_state.page = "prediction"
        st.rerun()

# ======================
# Prediction Page
# ======================
def show_prediction_page():
    load_prediction_css()
    
    # Back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back Home"):
            st.session_state.page = "landing"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.title("🩺 Breast Cancer Diagnosis")
    st.markdown("Enter tumor characteristics to predict malignancy.")
    
    # ======================
    # Input form
    # ======================
    with st.form("cancer_form"):
        st.subheader("Mean Features")
        col1, col2 = st.columns(2)
        with col1:
            radius_mean = st.number_input("Radius Mean", value=14.0)
            texture_mean = st.number_input("Texture Mean", value=19.0)
            perimeter_mean = st.number_input("Perimeter Mean", value=90.0)
            area_mean = st.number_input("Area Mean", value=600.0)
            smoothness_mean = st.number_input("Smoothness Mean", value=0.10)
        with col2:
            compactness_mean = st.number_input("Compactness Mean", value=0.15)
            concavity_mean = st.number_input("Concavity Mean", value=0.10)
            concave_points_mean = st.number_input("Concave Points Mean", value=0.05)
            symmetry_mean = st.number_input("Symmetry Mean", value=0.18)
            fractal_dimension_mean = st.number_input("Fractal Dimension Mean", value=0.06)

        st.subheader("Standard Error Features")
        col1, col2 = st.columns(2)
        with col1:
            radius_se = st.number_input("Radius SE", value=0.5)
            texture_se = st.number_input("Texture SE", value=1.0)
            perimeter_se = st.number_input("Perimeter SE", value=3.0)
            area_se = st.number_input("Area SE", value=40.0)
            smoothness_se = st.number_input("Smoothness SE", value=0.005)
        with col2:
            compactness_se = st.number_input("Compactness SE", value=0.03)
            concavity_se = st.number_input("Concavity SE", value=0.04)
            concave_points_se = st.number_input("Concave Points SE", value=0.01)
            symmetry_se = st.number_input("Symmetry SE", value=0.02)
            fractal_dimension_se = st.number_input("Fractal Dimension SE", value=0.006)

        st.subheader("Worst Features")
        col1, col2 = st.columns(2)
        with col1:
            radius_worst = st.number_input("Radius Worst", value=18.0)
            texture_worst = st.number_input("Texture Worst", value=25.0)
            perimeter_worst = st.number_input("Perimeter Worst", value=120.0)
            area_worst = st.number_input("Area Worst", value=1000.0)
            smoothness_worst = st.number_input("Smoothness Worst", value=0.14)
        with col2:
            compactness_worst = st.number_input("Compactness Worst", value=0.30)
            concavity_worst = st.number_input("Concavity Worst", value=0.35)
            concave_points_worst = st.number_input("Concave Points Worst", value=0.12)
            symmetry_worst = st.number_input("Symmetry Worst", value=0.30)
            fractal_dimension_worst = st.number_input("Fractal Dimension Worst", value=0.08)

        submit = st.form_submit_button("🔍 Predict", use_container_width=True)

    # ======================
    # Prediction
    # ======================
    if submit:
        payload = {
            "radius_mean": radius_mean,
            "texture_mean": texture_mean,
            "perimeter_mean": perimeter_mean,
            "area_mean": area_mean,
            "smoothness_mean": smoothness_mean,
            "compactness_mean": compactness_mean,
            "concavity_mean": concavity_mean,
            "concave_points_mean": concave_points_mean,
            "symmetry_mean": symmetry_mean,
            "fractal_dimension_mean": fractal_dimension_mean,

            "radius_se": radius_se,
            "texture_se": texture_se,
            "perimeter_se": perimeter_se,
            "area_se": area_se,
            "smoothness_se": smoothness_se,
            "compactness_se": compactness_se,
            "concavity_se": concavity_se,
            "concave_points_se": concave_points_se,
            "symmetry_se": symmetry_se,
            "fractal_dimension_se": fractal_dimension_se,

            "radius_worst": radius_worst,
            "texture_worst": texture_worst,
            "perimeter_worst": perimeter_worst,
            "area_worst": area_worst,
            "smoothness_worst": smoothness_worst,
            "compactness_worst": compactness_worst,
            "concavity_worst": concavity_worst,
            "concave_points_worst": concave_points_worst,
            "symmetry_worst": symmetry_worst,
            "fractal_dimension_worst": fractal_dimension_worst
        }

        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()

                if result["prediction"] == "Malignant":
                    st.error(f"⚠️ **Malignant Tumor Detected**\n\nConfidence: {result['confidence']:.2%}")
                else:
                    st.success(f"✅ **Benign Tumor**\n\nConfidence: {result['confidence']:.2%}")
            else:
                st.error("❌ Error communicating with FastAPI server")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to FastAPI server. Make sure it's running on http://127.0.0.1:8000")

# ======================
# Main Router
# ======================
# Check for URL parameter to switch pages
query_params = st.query_params
if "page" in query_params and query_params["page"] == "analysis":
    st.session_state.page = "prediction"

if st.session_state.page == "landing":
    show_landing_page()
else:
    show_prediction_page()
