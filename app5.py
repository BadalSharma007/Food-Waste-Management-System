"""
Smart Food Donation and Waste Management System
Enhanced Production-Ready Version with Modern UI/UX
"""

import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
import base64
import time

# Page Configuration
st.set_page_config(
    page_title="Smart Food Donation System",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Enhanced Custom CSS with Modern Design & Background Animation
def get_custom_css(theme='light'):
    if theme == 'dark':
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            :root {
                --primary: #818cf8;
                --primary-dark: #6366f1;
                --secondary: #a78bfa;
                --accent: #34d399;
                --bg-primary: #0f172a;
                --bg-secondary: #1e293b;
                --bg-card: rgba(30, 41, 59, 0.8);
                --text-primary: #f1f5f9;
                --text-secondary: #94a3b8;
                --text-muted: #64748b;
                --border: rgba(148, 163, 184, 0.1);
                --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
                --gradient-primary: linear-gradient(135deg, #818cf8 0%, #a78bfa 100%);
                --gradient-card: linear-gradient(135deg, rgba(129, 140, 248, 0.1) 0%, rgba(167, 139, 250, 0.1) 100%);
            }
            
            * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; -webkit-font-smoothing: antialiased; }
            .stApp { background: var(--bg-primary); }
            .main { background: transparent; position: relative; }
            
            .main::before {
                content: '';
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: 
                    radial-gradient(ellipse 80% 50% at 20% 40%, rgba(129, 140, 248, 0.15), transparent 50%),
                    radial-gradient(ellipse 60% 50% at 80% 60%, rgba(167, 139, 250, 0.12), transparent 50%),
                    radial-gradient(ellipse 50% 40% at 50% 90%, rgba(52, 211, 153, 0.08), transparent 50%);
                animation: bgFloat 25s ease-in-out infinite;
                pointer-events: none;
                z-index: 0;
            }
            
            @keyframes bgFloat {
                0%, 100% { transform: translate(0, 0) scale(1); }
                25% { transform: translate(2%, -2%) scale(1.02); }
                50% { transform: translate(-1%, 1%) scale(0.98); }
                75% { transform: translate(1%, 2%) scale(1.01); }
            }
            
            .block-container { position: relative; z-index: 1; padding-top: 2rem; max-width: 1400px; }
            
            .main-header {
                font-size: clamp(2.5rem, 5vw, 3.5rem);
                font-weight: 800;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                margin-bottom: 0.5rem;
                letter-spacing: -0.03em;
                animation: titleReveal 1s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            @keyframes titleReveal {
                from { opacity: 0; transform: translateY(-30px); filter: blur(10px); }
                to { opacity: 1; transform: translateY(0); filter: blur(0); }
            }
            
            .hero-section {
                text-align: center;
                padding: 3.5rem 2.5rem;
                background: var(--gradient-card);
                border: 1px solid var(--border);
                border-radius: 24px;
                margin-bottom: 3rem;
                backdrop-filter: blur(20px);
                animation: cardFloat 0.8s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .hero-section h2 { color: var(--primary); font-weight: 700; margin-bottom: 1rem; font-size: clamp(1.5rem, 3vw, 2rem); }
            .hero-section p { font-size: 1.125rem; color: var(--text-secondary); line-height: 1.7; max-width: 700px; margin: 0 auto; }
            
            @keyframes cardFloat {
                from { opacity: 0; transform: translateY(40px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .stat-card {
                background: var(--gradient-primary);
                padding: 1.75rem;
                border-radius: 20px;
                text-align: center;
                position: relative;
                overflow: hidden;
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                animation: statReveal 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
                box-shadow: var(--shadow-lg);
            }
            
            .stat-card:hover { transform: translateY(-8px) scale(1.02); box-shadow: 0 20px 40px rgba(129, 140, 248, 0.3); }
            .stat-card h2 { font-size: 2.75rem; font-weight: 800; color: white; margin: 0; }
            .stat-card p { margin: 0.5rem 0 0; color: rgba(255,255,255,0.9); font-weight: 500; }
            .stat-card p:last-child { font-size: 0.85rem; color: rgba(255,255,255,0.7); }
            
            @keyframes statReveal {
                from { opacity: 0; transform: translateY(30px) scale(0.95); }
                to { opacity: 1; transform: translateY(0) scale(1); }
            }
            
            .donation-card {
                background: var(--bg-card);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 1.5rem;
                margin: 1rem 0;
                backdrop-filter: blur(20px);
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .donation-card:hover { border-color: rgba(129, 140, 248, 0.3); transform: translateX(8px); box-shadow: var(--shadow-lg); }
            .donation-card h4 { color: var(--primary); margin: 0 0 0.75rem; font-weight: 600; }
            .donation-card p { color: var(--text-secondary); margin: 0.4rem 0; line-height: 1.6; }
            .donation-card strong { color: var(--text-primary); }
            
            .badge { display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.5rem 1rem; border-radius: 100px; font-size: 0.875rem; font-weight: 600; margin: 0.25rem; transition: all 0.3s ease; }
            .badge:hover { transform: translateY(-2px) scale(1.05); }
            .badge-gold { background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: #1c1917; }
            .badge-silver { background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%); color: #1e293b; }
            .badge-bronze { background: linear-gradient(135deg, #d97706 0%, #92400e 100%); color: white; }
            
            .metric-container {
                background: var(--bg-card);
                border: 1px solid var(--border);
                padding: 1.5rem;
                border-radius: 16px;
                backdrop-filter: blur(20px);
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                text-align: center;
            }
            
            .metric-container:hover { border-color: rgba(129, 140, 248, 0.3); transform: translateY(-4px); }
            .metric-container h2, .metric-container h3 { margin: 0 0 0.5rem; font-weight: 700; }
            .metric-container p { margin: 0; color: var(--text-secondary); font-size: 0.9rem; }
            
            .success-story {
                background: rgba(52, 211, 153, 0.08);
                border: 1px solid rgba(52, 211, 153, 0.2);
                border-left: 4px solid var(--accent);
                padding: 1.5rem;
                border-radius: 12px;
                margin: 1rem 0;
                transition: all 0.3s ease;
            }
            
            .success-story:hover { background: rgba(52, 211, 153, 0.12); transform: translateX(8px); }
            .success-story h4 { color: var(--accent); margin: 0 0 0.75rem; font-weight: 600; }
            .success-story p { color: var(--text-secondary); line-height: 1.7; margin: 0.5rem 0; }
            
            .how-it-works-card {
                text-align: center;
                padding: 2rem 1.5rem;
                background: var(--gradient-card);
                border: 1px solid var(--border);
                border-radius: 20px;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .how-it-works-card:hover { transform: translateY(-8px); border-color: rgba(129, 140, 248, 0.4); box-shadow: var(--shadow-lg); }
            .how-it-works-card .step-number { font-size: 3rem; margin-bottom: 1rem; display: block; }
            .how-it-works-card h3 { color: var(--primary); margin: 0.75rem 0; font-weight: 600; }
            .how-it-works-card p { color: var(--text-secondary); font-size: 0.95rem; line-height: 1.6; margin: 0; }
            
            .stButton>button {
                width: 100%;
                background: var(--gradient-primary);
                color: white;
                font-weight: 600;
                border: none;
                padding: 0.875rem 1.5rem;
                border-radius: 12px;
                font-size: 0.95rem;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                box-shadow: 0 4px 12px rgba(129, 140, 248, 0.4);
            }
            
            .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(129, 140, 248, 0.5); }
            
            .stProgress > div > div { background: var(--gradient-primary); border-radius: 10px; }
            
            .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; background: transparent; }
            .stTabs [data-baseweb="tab"] { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 0.75rem 1.5rem; font-weight: 500; color: var(--text-secondary); transition: all 0.3s ease; }
            .stTabs [data-baseweb="tab"]:hover { background: var(--gradient-card); color: var(--text-primary); }
            .stTabs [aria-selected="true"] { background: var(--gradient-primary) !important; border-color: transparent !important; color: white !important; }
            
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input { 
                background: var(--bg-secondary) !important; 
                border: 1px solid var(--border) !important; 
                border-radius: 12px !important; 
                color: var(--text-primary) !important; 
            }
            .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus, .stNumberInput>div>div>input:focus { 
                border-color: var(--primary) !important; 
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important; 
            }
            .stTextInput>div>div>input::placeholder, .stTextArea>div>div>textarea::placeholder {
                color: var(--text-muted) !important;
            }
            
            /* Labels */
            .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label, .stDateInput label, .stTimeInput label, .stFileUploader label {
                color: var(--text-primary) !important;
                font-weight: 500 !important;
            }
            
            /* Selectbox */
            .stSelectbox > div > div { 
                background: var(--bg-secondary) !important; 
                border: 1px solid var(--border) !important; 
                border-radius: 12px !important;
                color: var(--text-primary) !important;
            }
            .stSelectbox [data-baseweb="select"] > div { color: var(--text-primary) !important; }
            
            /* Multiselect and selectbox dropdown */
            [data-baseweb="popover"] { background: var(--bg-secondary) !important; border: 1px solid var(--border) !important; }
            [data-baseweb="menu"] { background: var(--bg-secondary) !important; }
            [data-baseweb="menu"] li { color: var(--text-primary) !important; }
            [data-baseweb="menu"] li:hover { background: var(--gradient-card) !important; }
            
            /* Expander */
            .streamlit-expanderHeader { 
                background: var(--bg-secondary) !important; 
                border: 1px solid var(--border) !important;
                border-radius: 12px !important;
                color: var(--text-primary) !important;
                font-weight: 500 !important;
            }
            .streamlit-expanderHeader:hover { background: var(--gradient-card) !important; }
            .streamlit-expanderContent { 
                background: var(--bg-secondary) !important; 
                border: 1px solid var(--border) !important;
                border-top: none !important;
                border-radius: 0 0 12px 12px !important;
            }
            
            /* Dataframe */
            .stDataFrame { background: var(--bg-secondary) !important; border-radius: 12px !important; }
            .stDataFrame [data-testid="stDataFrameResizable"] { background: var(--bg-secondary) !important; }
            
            /* Metric */
            [data-testid="stMetricValue"] { color: var(--text-primary) !important; }
            [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
            [data-testid="stMetricDelta"] { color: var(--accent) !important; }
            
            /* Sidebar */
            [data-testid="stSidebar"] { 
                background: var(--bg-secondary) !important; 
                border-right: 1px solid var(--border) !important; 
            }
            [data-testid="stSidebar"] * { color: var(--text-primary) !important; }
            [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] .stMarkdown span { color: var(--text-primary) !important; }
            [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: var(--text-primary) !important; }
            [data-testid="stSidebar"] hr { border-color: var(--border) !important; }
            
            /* Sidebar metrics */
            [data-testid="stSidebar"] [data-testid="stMetricValue"] { color: var(--primary) !important; }
            
            /* File uploader */
            .stFileUploader { background: var(--bg-secondary) !important; border-radius: 12px !important; }
            .stFileUploader > div { border: 2px dashed var(--border) !important; border-radius: 12px !important; }
            .stFileUploader label { color: var(--text-primary) !important; }
            
            /* Slider */
            .stSlider label { color: var(--text-primary) !important; }
            .stSlider [data-baseweb="slider"] { background: var(--border) !important; }
            
            /* Checkbox and Radio */
            .stCheckbox label, .stRadio label { color: var(--text-primary) !important; }
            
            /* Info/Warning/Success/Error boxes */
            .stAlert { border-radius: 12px !important; }
            [data-testid="stNotification"] { color: var(--text-primary) !important; }
            
            /* Scrollbar */
            ::-webkit-scrollbar { width: 8px; height: 8px; }
            ::-webkit-scrollbar-track { background: var(--bg-primary); }
            ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
            ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
            
            /* Footer */
            .footer { 
                text-align: center; 
                padding: 2rem; 
                color: var(--text-muted) !important; 
                border-top: 1px solid var(--border); 
                margin-top: 3rem; 
            }
            .footer p { margin: 0.25rem 0; color: var(--text-muted) !important; }
            
            /* Write and markdown specific */
            .element-container { color: var(--text-primary) !important; }
            [data-testid="stMarkdownContainer"] { color: var(--text-primary) !important; }
            [data-testid="stMarkdownContainer"] p { color: var(--text-primary) !important; }
            [data-testid="stMarkdownContainer"] h1, 
            [data-testid="stMarkdownContainer"] h2, 
            [data-testid="stMarkdownContainer"] h3, 
            [data-testid="stMarkdownContainer"] h4 { color: var(--text-primary) !important; }
            
            /* Image captions */
            .stImage > div > div > p { color: var(--text-secondary) !important; }
            
            /* Download button */
            .stDownloadButton button { 
                background: var(--bg-secondary) !important; 
                color: var(--primary) !important; 
                border: 1px solid var(--border) !important;
            }
            .stDownloadButton button:hover { 
                background: var(--gradient-card) !important; 
                border-color: var(--primary) !important;
            }
            
            /* Date and Time inputs */
            .stDateInput > div > div, .stTimeInput > div > div {
                background: var(--bg-secondary) !important;
                border: 1px solid var(--border) !important;
                border-radius: 12px !important;
            }
            .stDateInput input, .stTimeInput input {
                color: var(--text-primary) !important;
            }
            
            /* Plotly charts background */
            .js-plotly-plot .plotly .main-svg { background: transparent !important; }
        </style>
        """
    else:
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            :root {
                --primary: #6366f1;
                --primary-dark: #4f46e5;
                --secondary: #8b5cf6;
                --accent: #059669;
                --bg-primary: #f8fafc;
                --bg-secondary: #ffffff;
                --bg-card: #ffffff;
                --text-primary: #1e293b;
                --text-secondary: #475569;
                --text-muted: #64748b;
                --border: #e2e8f0;
                --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                --gradient-card: linear-gradient(135deg, rgba(99, 102, 241, 0.03) 0%, rgba(139, 92, 246, 0.03) 100%);
            }
            
            * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; -webkit-font-smoothing: antialiased; }
            
            /* Main app background */
            .stApp { background: var(--bg-primary) !important; }
            .main { background: transparent !important; position: relative; }
            
            /* Animated background */
            .main::before {
                content: '';
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: 
                    radial-gradient(ellipse 80% 50% at 20% 40%, rgba(99, 102, 241, 0.06), transparent 50%),
                    radial-gradient(ellipse 60% 50% at 80% 60%, rgba(139, 92, 246, 0.05), transparent 50%),
                    radial-gradient(ellipse 50% 40% at 50% 90%, rgba(5, 150, 105, 0.04), transparent 50%);
                animation: bgFloat 25s ease-in-out infinite;
                pointer-events: none;
                z-index: 0;
            }
            
            @keyframes bgFloat {
                0%, 100% { transform: translate(0, 0) scale(1); }
                25% { transform: translate(2%, -2%) scale(1.02); }
                50% { transform: translate(-1%, 1%) scale(0.98); }
                75% { transform: translate(1%, 2%) scale(1.01); }
            }
            
            .block-container { position: relative; z-index: 1; padding-top: 2rem; max-width: 1400px; }
            
            /* ===== GLOBAL TEXT COLORS FOR LIGHT MODE ===== */
            .stApp, .stApp p, .stApp span, .stApp div, .stApp label {
                color: var(--text-primary) !important;
            }
            
            /* Markdown text */
            .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
                color: var(--text-primary) !important;
            }
            
            /* Headers */
            h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; }
            
            /* Paragraphs and text */
            p, span, div, li, td, th { color: var(--text-primary); }
            
            /* Info, warning, success, error boxes */
            .stAlert > div { color: var(--text-primary) !important; }
            
            /* Main header with gradient */
            .main-header {
                font-size: clamp(2.5rem, 5vw, 3.5rem);
                font-weight: 800;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-align: center;
                margin-bottom: 0.5rem;
                letter-spacing: -0.03em;
                animation: titleReveal 1s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            @keyframes titleReveal {
                from { opacity: 0; transform: translateY(-30px); filter: blur(10px); }
                to { opacity: 1; transform: translateY(0); filter: blur(0); }
            }
            
            /* Hero section */
            .hero-section {
                text-align: center;
                padding: 3.5rem 2.5rem;
                background: var(--bg-secondary);
                border: 1px solid var(--border);
                border-radius: 24px;
                margin-bottom: 3rem;
                box-shadow: var(--shadow);
                position: relative;
                overflow: hidden;
                animation: cardFloat 0.8s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .hero-section::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: var(--gradient-primary); }
            .hero-section h2 { color: var(--primary) !important; font-weight: 700; margin-bottom: 1rem; font-size: clamp(1.5rem, 3vw, 2rem); -webkit-text-fill-color: var(--primary) !important; }
            .hero-section p { font-size: 1.125rem; color: var(--text-secondary) !important; line-height: 1.7; max-width: 700px; margin: 0 auto; }
            
            @keyframes cardFloat {
                from { opacity: 0; transform: translateY(40px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* Stat cards */
            .stat-card {
                background: var(--gradient-primary);
                padding: 1.75rem;
                border-radius: 20px;
                text-align: center;
                position: relative;
                overflow: hidden;
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                animation: statReveal 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards;
                box-shadow: 0 4px 20px rgba(99, 102, 241, 0.25);
            }
            
            .stat-card:hover { transform: translateY(-8px) scale(1.02); box-shadow: 0 20px 40px rgba(99, 102, 241, 0.35); }
            .stat-card h2 { font-size: 2.75rem; font-weight: 800; color: white !important; margin: 0; -webkit-text-fill-color: white !important; }
            .stat-card p { margin: 0.5rem 0 0; color: rgba(255,255,255,0.95) !important; font-weight: 500; }
            .stat-card p:last-child { font-size: 0.85rem; color: rgba(255,255,255,0.8) !important; }
            
            @keyframes statReveal {
                from { opacity: 0; transform: translateY(30px) scale(0.95); }
                to { opacity: 1; transform: translateY(0) scale(1); }
            }
            
            /* Donation cards */
            .donation-card {
                background: var(--bg-secondary);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: var(--shadow);
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            }
            
            .donation-card:hover { border-color: rgba(99, 102, 241, 0.4); transform: translateX(8px); box-shadow: var(--shadow-lg); }
            .donation-card h4 { color: var(--primary) !important; margin: 0 0 0.75rem; font-weight: 600; }
            .donation-card p { color: var(--text-secondary) !important; margin: 0.4rem 0; line-height: 1.6; }
            .donation-card strong { color: var(--text-primary) !important; }
            
            /* Badges */
            .badge { display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.5rem 1rem; border-radius: 100px; font-size: 0.875rem; font-weight: 600; margin: 0.25rem; transition: all 0.3s ease; box-shadow: var(--shadow); }
            .badge:hover { transform: translateY(-2px) scale(1.05); }
            .badge-gold { background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: #1c1917 !important; }
            .badge-silver { background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%); color: #1e293b !important; }
            .badge-bronze { background: linear-gradient(135deg, #d97706 0%, #92400e 100%); color: white !important; }
            
            /* Metric containers */
            .metric-container {
                background: var(--bg-secondary);
                border: 1px solid var(--border);
                padding: 1.5rem;
                border-radius: 16px;
                box-shadow: var(--shadow);
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                text-align: center;
            }
            
            .metric-container:hover { border-color: rgba(99, 102, 241, 0.4); transform: translateY(-4px); box-shadow: var(--shadow-lg); }
            .metric-container h2, .metric-container h3 { margin: 0 0 0.5rem; font-weight: 700; }
            .metric-container p { margin: 0; color: var(--text-secondary) !important; font-size: 0.9rem; }
            
            /* Success stories */
            .success-story {
                background: rgba(5, 150, 105, 0.05);
                border: 1px solid rgba(5, 150, 105, 0.2);
                border-left: 4px solid var(--accent);
                padding: 1.5rem;
                border-radius: 12px;
                margin: 1rem 0;
                transition: all 0.3s ease;
            }
            
            .success-story:hover { background: rgba(5, 150, 105, 0.08); transform: translateX(8px); box-shadow: var(--shadow); }
            .success-story h4 { color: var(--accent) !important; margin: 0 0 0.75rem; font-weight: 600; }
            .success-story p { color: var(--text-secondary) !important; line-height: 1.7; margin: 0.5rem 0; }
            
            /* How it works cards */
            .how-it-works-card {
                text-align: center;
                padding: 2rem 1.5rem;
                background: var(--bg-secondary);
                border: 1px solid var(--border);
                border-radius: 20px;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                box-shadow: var(--shadow);
            }
            
            .how-it-works-card:hover { transform: translateY(-8px); border-color: rgba(99, 102, 241, 0.4); box-shadow: var(--shadow-lg); }
            .how-it-works-card .step-number { font-size: 3rem; margin-bottom: 1rem; display: block; }
            .how-it-works-card h3 { color: var(--primary) !important; margin: 0.75rem 0; font-weight: 600; }
            .how-it-works-card p { color: var(--text-secondary) !important; font-size: 0.95rem; line-height: 1.6; margin: 0; }
            
            /* Buttons */
            .stButton>button {
                width: 100%;
                background: var(--gradient-primary);
                color: white !important;
                font-weight: 600;
                border: none;
                padding: 0.875rem 1.5rem;
                border-radius: 12px;
                font-size: 0.95rem;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
            }
            
            .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(99, 102, 241, 0.45); color: white !important; }
            
            /* Progress bar */
            .stProgress > div > div { background: var(--gradient-primary); border-radius: 10px; }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; background: transparent; }
            .stTabs [data-baseweb="tab"] { 
                background: var(--bg-secondary); 
                border: 1px solid var(--border); 
                border-radius: 12px; 
                padding: 0.75rem 1.5rem; 
                font-weight: 500; 
                color: var(--text-secondary) !important; 
                transition: all 0.3s ease; 
                box-shadow: var(--shadow); 
            }
            .stTabs [data-baseweb="tab"]:hover { background: var(--gradient-card); color: var(--text-primary) !important; }
            .stTabs [aria-selected="true"] { background: var(--gradient-primary) !important; border-color: transparent !important; color: white !important; }
            
            /* Form inputs */
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input { 
                background: var(--bg-secondary) !important; 
                border: 1px solid var(--border) !important; 
                border-radius: 12px !important; 
                color: var(--text-primary) !important; 
            }
            .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus, .stNumberInput>div>div>input:focus { 
                border-color: var(--primary) !important; 
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important; 
            }
            .stTextInput>div>div>input::placeholder, .stTextArea>div>div>textarea::placeholder {
                color: var(--text-muted) !important;
            }
            
            /* Labels */
            .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label, .stDateInput label, .stTimeInput label, .stFileUploader label {
                color: var(--text-primary) !important;
                font-weight: 500 !important;
            }
            
            /* Selectbox */
            .stSelectbox > div > div { 
                background: var(--bg-secondary) !important; 
                border: 1px solid var(--border) !important; 
                border-radius: 12px !important;
                color: var(--text-primary) !important;
            }
            .stSelectbox [data-baseweb="select"] > div { color: var(--text-primary) !important; }
            
            /* Multiselect and selectbox dropdown */
            [data-baseweb="popover"] { background: var(--bg-secondary) !important; border: 1px solid var(--border) !important; }
            [data-baseweb="menu"] { background: var(--bg-secondary) !important; }
            [data-baseweb="menu"] li { color: var(--text-primary) !important; }
            [data-baseweb="menu"] li:hover { background: var(--gradient-card) !important; }
            
            /* Expander */
            .streamlit-expanderHeader { 
                background: var(--bg-secondary) !important; 
                border: 1px solid var(--border) !important;
                border-radius: 12px !important;
                color: var(--text-primary) !important;
                font-weight: 500 !important;
            }
            .streamlit-expanderHeader:hover { background: var(--gradient-card) !important; }
            .streamlit-expanderContent { 
                background: var(--bg-secondary) !important; 
                border: 1px solid var(--border) !important;
                border-top: none !important;
                border-radius: 0 0 12px 12px !important;
            }
            
            /* Dataframe */
            .stDataFrame { background: var(--bg-secondary) !important; border-radius: 12px !important; }
            .stDataFrame [data-testid="stDataFrameResizable"] { background: var(--bg-secondary) !important; }
            
            /* Metric */
            [data-testid="stMetricValue"] { color: var(--text-primary) !important; }
            [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
            [data-testid="stMetricDelta"] { color: var(--accent) !important; }
            
            /* Sidebar */
            [data-testid="stSidebar"] { 
                background: var(--bg-secondary) !important; 
                border-right: 1px solid var(--border) !important; 
            }
            [data-testid="stSidebar"] * { color: var(--text-primary) !important; }
            [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] .stMarkdown span { color: var(--text-primary) !important; }
            [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: var(--text-primary) !important; }
            [data-testid="stSidebar"] hr { border-color: var(--border) !important; }
            
            /* Sidebar metrics */
            [data-testid="stSidebar"] [data-testid="stMetricValue"] { color: var(--primary) !important; }
            
            /* File uploader */
            .stFileUploader { background: var(--bg-secondary) !important; border-radius: 12px !important; }
            .stFileUploader > div { border: 2px dashed var(--border) !important; border-radius: 12px !important; }
            .stFileUploader label { color: var(--text-primary) !important; }
            
            /* Slider */
            .stSlider label { color: var(--text-primary) !important; }
            .stSlider [data-baseweb="slider"] { background: var(--border) !important; }
            
            /* Checkbox and Radio */
            .stCheckbox label, .stRadio label { color: var(--text-primary) !important; }
            
            /* Info/Warning/Success/Error boxes */
            .stAlert { border-radius: 12px !important; }
            [data-testid="stNotification"] { color: var(--text-primary) !important; }
            
            /* Scrollbar */
            ::-webkit-scrollbar { width: 8px; height: 8px; }
            ::-webkit-scrollbar-track { background: var(--bg-primary); }
            ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
            ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
            
            /* Footer */
            .footer { 
                text-align: center; 
                padding: 2rem; 
                color: var(--text-muted) !important; 
                border-top: 1px solid var(--border); 
                margin-top: 3rem; 
            }
            .footer p { margin: 0.25rem 0; color: var(--text-muted) !important; }
            
            /* Write and markdown specific */
            .element-container { color: var(--text-primary) !important; }
            [data-testid="stMarkdownContainer"] { color: var(--text-primary) !important; }
            [data-testid="stMarkdownContainer"] p { color: var(--text-primary) !important; }
            [data-testid="stMarkdownContainer"] h1, 
            [data-testid="stMarkdownContainer"] h2, 
            [data-testid="stMarkdownContainer"] h3, 
            [data-testid="stMarkdownContainer"] h4 { color: var(--text-primary) !important; }
            
            /* Image captions */
            .stImage > div > div > p { color: var(--text-secondary) !important; }
            
            /* Download button */
            .stDownloadButton button { 
                background: var(--bg-secondary) !important; 
                color: var(--primary) !important; 
                border: 1px solid var(--border) !important;
            }
            .stDownloadButton button:hover { 
                background: var(--gradient-card) !important; 
                border-color: var(--primary) !important;
            }
            
            /* Date and Time inputs */
            .stDateInput > div > div, .stTimeInput > div > div {
                background: var(--bg-secondary) !important;
                border: 1px solid var(--border) !important;
                border-radius: 12px !important;
            }
            .stDateInput input, .stTimeInput input {
                color: var(--text-primary) !important;
            }
            
            /* Plotly charts background */
            .js-plotly-plot .plotly .main-svg { background: transparent !important; }
        </style>
        """

st.markdown(get_custom_css(st.session_state.theme), unsafe_allow_html=True)

# Database Setup
@st.cache_resource
def init_database():
    conn = sqlite3.connect('food_donation.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        phone TEXT,
        role TEXT CHECK(role IN ('donor', 'ngo', 'admin')),
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        verified INTEGER DEFAULT 0,
        profile_pic TEXT,
        total_donations INTEGER DEFAULT 0,
        streak_days INTEGER DEFAULT 0,
        last_donation_date DATE
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS ngo_profiles (
        ngo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        organization_name TEXT NOT NULL,
        registration_number TEXT UNIQUE,
        address TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        verified INTEGER DEFAULT 0,
        capacity INTEGER DEFAULT 50,
        total_pickups INTEGER DEFAULT 0,
        rating REAL DEFAULT 5.0,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS donations (
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER NOT NULL,
        food_name TEXT NOT NULL,
        quantity TEXT NOT NULL,
        food_type TEXT,
        expiry_time TIMESTAMP NOT NULL,
        location TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        image_data TEXT,
        description TEXT,
        status TEXT DEFAULT 'pending',
        qr_code TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        collected_at TIMESTAMP,
        view_count INTEGER DEFAULT 0,
        FOREIGN KEY (donor_id) REFERENCES users(user_id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donation_id INTEGER NOT NULL,
        ngo_id INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        message TEXT,
        requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        accepted_at TIMESTAMP,
        collected_at TIMESTAMP,
        feedback TEXT,
        rating INTEGER,
        FOREIGN KEY (donation_id) REFERENCES donations(donation_id),
        FOREIGN KEY (ngo_id) REFERENCES ngo_profiles(ngo_id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS success_stories (
        story_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donation_id INTEGER,
        ngo_id INTEGER,
        title TEXT NOT NULL,
        story TEXT NOT NULL,
        impact_meals INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        featured INTEGER DEFAULT 0,
        FOREIGN KEY (donation_id) REFERENCES donations(donation_id),
        FOREIGN KEY (ngo_id) REFERENCES ngo_profiles(ngo_id)
    )''')
    
    # Create admin user
    admin_email = "admin@fooddonation.com"
    admin_pass = hash_password("admin123")
    try:
        c.execute('''INSERT OR IGNORE INTO users (email, password_hash, full_name, role, verified)
                     VALUES (?, ?, ?, ?, ?)''', (admin_email, admin_pass, "System Admin", "admin", 1))
    except Exception:
        pass
    
    conn.commit()
    return conn

# Utility Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    return hash_password(password) == password_hash

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def image_to_base64(uploaded_file):
    if uploaded_file is not None:
        return base64.b64encode(uploaded_file.getvalue()).decode()
    return None

def get_user_badges(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT total_donations, streak_days FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    badges = []
    if result:
        total, streak = result[0] or 0, result[1] or 0
        if total >= 50:
            badges.append(("🏆", "Gold Donor", "badge-gold"))
        elif total >= 20:
            badges.append(("🥈", "Silver Donor", "badge-silver"))
        elif total >= 5:
            badges.append(("🥉", "Bronze Donor", "badge-bronze"))
        if streak >= 7:
            badges.append(("🔥", f"{streak} Day Streak", "badge-gold"))
    return badges

# Authentication Functions
def register_user(conn, email, password, full_name, phone, role):
    c = conn.cursor()
    try:
        password_hash = hash_password(password)
        c.execute('''INSERT INTO users (email, password_hash, full_name, phone, role) VALUES (?, ?, ?, ?, ?)''',
                  (email, password_hash, full_name, phone, role))
        conn.commit()
        return True, c.lastrowid
    except sqlite3.IntegrityError:
        return False, "Email already exists"

def login_user(conn, email, password):
    c = conn.cursor()
    c.execute("SELECT user_id, password_hash, full_name, role, verified FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    if result and verify_password(password, result[1]):
        return True, {'user_id': result[0], 'name': result[2], 'role': result[3], 'verified': result[4], 'email': email}
    return False, None

# Home Page
def show_home_page(conn):
    st.markdown('<h1 class="main-header">🍱 Smart Food Donation System</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class='hero-section'>
        <h2>Connecting Surplus Food with Those Who Need It Most</h2>
        <p>Every year, millions of tons of food are wasted while many go hungry. Our platform bridges this gap by connecting food donors with NGOs and volunteers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM donations WHERE status='completed'")
    total_donations = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT user_id) FROM users WHERE role='ngo' AND verified=1")
    total_ngos = c.fetchone()[0]
    meals_saved = total_donations * 15
    food_saved_kg = total_donations * 5
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='stat-card'><h2>{total_donations}</h2><p>Donations Completed</p><p>🎯 Making Impact</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-card'><h2>{total_ngos}</h2><p>NGOs Partnered</p><p>❤️ Verified Partners</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stat-card'><h2>{meals_saved:,}</h2><p>Meals Served</p><p>🍽️ Lives Touched</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='stat-card'><h2>{food_saved_kg:,} kg</h2><p>Food Saved</p><p>🌍 Waste Reduced</p></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Success Stories
    st.markdown("### 🌟 Recent Success Stories")
    c.execute('''SELECT s.title, s.story, s.impact_meals, s.created_at, n.organization_name FROM success_stories s
                 JOIN ngo_profiles n ON s.ngo_id = n.ngo_id ORDER BY s.created_at DESC LIMIT 3''')
    stories = c.fetchall()
    if stories:
        for story in stories:
            created_date = story[3][:10] if story[3] else "N/A"
            st.markdown(f"""<div class='success-story'><h4>✨ {story[0]}</h4><p>{story[1]}</p>
                <p style='font-size: 0.9rem; color: var(--accent);'><strong>{story[4]}</strong> • {story[2]} meals served • {created_date}</p></div>""", unsafe_allow_html=True)
    else:
        st.info("🎯 Be part of our first success story! Start donating today.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CTA
    st.markdown("### 🎯 Join Our Mission Today")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎁 Donate Food Now", key="home_donate", use_container_width=True):
                st.session_state.page = "register"
                st.session_state.register_role = "donor"
                st.rerun()
        with col_b:
            if st.button("❤️ Join as NGO", key="home_ngo", use_container_width=True):
                st.session_state.page = "register"
                st.session_state.register_role = "ngo"
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # How it works
    st.markdown("### 📖 How It Works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='how-it-works-card'><span class='step-number'>1️⃣</span><h3>Post Donation</h3><p>Restaurants, events, or individuals post surplus food details with photos</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='how-it-works-card'><span class='step-number'>2️⃣</span><h3>NGOs Request</h3><p>Nearby NGOs get instant notifications and request pickup with one click</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='how-it-works-card'><span class='step-number'>3️⃣</span><h3>Food Delivered</h3><p>Food is collected using QR codes and distributed to those in need</p></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Live Feed
    st.markdown("### 🔴 Live Donation Feed")
    c.execute('''SELECT d.food_name, d.quantity, d.location, d.created_at, u.full_name FROM donations d
                 JOIN users u ON d.donor_id = u.user_id WHERE d.status = 'pending' ORDER BY d.created_at DESC LIMIT 5''')
    live_donations = c.fetchall()
    if live_donations:
        for don in live_donations:
            try:
                time_ago = (datetime.now() - datetime.strptime(don[3], '%Y-%m-%d %H:%M:%S')).seconds // 60
            except Exception:
                time_ago = 0
            st.markdown(f"<div class='donation-card'><h4>🍱 {don[0]}</h4><p><strong>Quantity:</strong> {don[1]} • <strong>Location:</strong> {don[2]}</p><p style='color: var(--accent);'>Posted {time_ago} min ago by {don[4]}</p></div>", unsafe_allow_html=True)
    else:
        st.info("💡 No active donations right now. Be the first to donate!")

# Donor Dashboard
def show_donor_dashboard(conn, user_id):
    st.markdown("## 🎁 Donor Dashboard")
    
    badges = get_user_badges(conn, user_id)
    if badges:
        badge_html = "".join([f"<span class='badge {b[2]}'>{b[0]} {b[1]}</span>" for b in badges])
        st.markdown(f"<div style='text-align: center; margin: 1.5rem 0;'><p style='color: var(--text-secondary); margin-bottom: 0.75rem;'>Your Achievements</p>{badge_html}</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Post Donation", "📋 My Donations", "📊 My Impact", "🌟 Success Stories"])
    
    with tab1:
        st.markdown("#### Create New Food Donation")
        with st.form("donation_form"):
            col1, col2 = st.columns(2)
            with col1:
                food_name = st.text_input("🍱 Food Item Name *", placeholder="e.g., Biryani, Pizza, Rice")
                quantity = st.text_input("📦 Quantity *", placeholder="e.g., 50 plates, 10 kg")
                food_type = st.selectbox("🍽️ Food Type *", ["Cooked Food", "Raw Food", "Packaged Food", "Fruits/Vegetables", "Bakery Items"])
            with col2:
                expiry_date = st.date_input("📅 Expiry Date", min_value=datetime.now().date(), value=datetime.now().date())
                expiry_time = st.time_input("⏰ Expiry Time", value=datetime.now().time())
                location = st.text_input("📍 Pickup Location *", placeholder="e.g., Green Valley Restaurant, Sector 18")
            
            uploaded_image = st.file_uploader("📸 Upload Food Image (Optional)", type=['jpg', 'jpeg', 'png'])
            if uploaded_image:
                st.image(uploaded_image, caption="Preview", width=300)
            
            description = st.text_area("📝 Additional Details", placeholder="Any special instructions...")
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("🌐 Latitude", value=28.5355, format="%.6f")
            with col2:
                longitude = st.number_input("🌐 Longitude", value=77.3910, format="%.6f")
            
            submit = st.form_submit_button("🚀 Post Donation", use_container_width=True)
            if submit:
                if food_name and quantity and location:
                    expiry_datetime = datetime.combine(expiry_date, expiry_time)
                    c = conn.cursor()
                    qr_data = f"DONATION-{datetime.now().strftime('%Y%m%d%H%M%S')}-{user_id}"
                    qr_code = generate_qr_code(qr_data)
                    image_data = image_to_base64(uploaded_image) if uploaded_image else None
                    c.execute('''INSERT INTO donations (donor_id, food_name, quantity, food_type, expiry_time, location, latitude, longitude, description, qr_code, image_data)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (user_id, food_name, quantity, food_type, expiry_datetime, location, latitude, longitude, description, qr_code, image_data))
                    c.execute("UPDATE users SET total_donations = total_donations + 1, last_donation_date = ? WHERE user_id = ?", (datetime.now().date(), user_id))
                    conn.commit()
                    st.success("✅ Donation posted successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("⚠️ Please fill all required fields (*)")
    
    with tab2:
        st.markdown("#### Your Posted Donations")
        status_filter = st.selectbox("Filter by Status", ["All", "pending", "accepted", "completed"])
        c = conn.cursor()
        if status_filter == "All":
            c.execute('''SELECT donation_id, food_name, quantity, location, status, created_at, qr_code, expiry_time, image_data
                         FROM donations WHERE donor_id = ? ORDER BY created_at DESC''', (user_id,))
        else:
            c.execute('''SELECT donation_id, food_name, quantity, location, status, created_at, qr_code, expiry_time, image_data
                         FROM donations WHERE donor_id = ? AND status = ? ORDER BY created_at DESC''', (user_id, status_filter))
        donations = c.fetchall()
        
        if donations:
            for don in donations:
                status_emoji = {"pending": "⏳", "accepted": "✅", "completed": "🎉", "expired": "❌"}
                with st.expander(f"{status_emoji.get(don[4], '📋')} {don[1]} - {don[2]} ({don[4].upper()})"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        if don[8]:
                            st.image(f"data:image/png;base64,{don[8]}", width=300)
                        st.write(f"**📍 Location:** {don[3]}")
                        st.write(f"**📅 Posted:** {don[5]}")
                        st.write(f"**⏰ Expires:** {don[7]}")
                        st.write(f"**📊 Status:** {don[4].upper()}")
                        
                        c.execute('''SELECT r.request_id, r.status, n.organization_name, u.phone, u.email
                                    FROM requests r JOIN ngo_profiles n ON r.ngo_id = n.ngo_id
                                    JOIN users u ON n.user_id = u.user_id WHERE r.donation_id = ?''', (don[0],))
                        requests = c.fetchall()
                        if requests:
                            st.write("**📞 Pickup Requests:**")
                            for req in requests:
                                st.markdown(f"<div class='donation-card' style='padding: 10px;'><strong>{req[2]}</strong> ({req[1]})<br>📧 {req[4]} | 📱 {req[3] or 'N/A'}</div>", unsafe_allow_html=True)
                                if req[1] == 'pending' and don[4] == 'pending':
                                    col_a, col_b = st.columns(2)
                                    with col_a:
                                        if st.button(f"✅ Accept", key=f"accept_{req[0]}"):
                                            c.execute("UPDATE requests SET status='accepted', accepted_at=? WHERE request_id=?", (datetime.now(), req[0]))
                                            c.execute("UPDATE donations SET status='accepted' WHERE donation_id=?", (don[0],))
                                            conn.commit()
                                            st.success("Request accepted!")
                                            st.rerun()
                                    with col_b:
                                        if st.button(f"❌ Reject", key=f"reject_{req[0]}"):
                                            c.execute("DELETE FROM requests WHERE request_id=?", (req[0],))
                                            conn.commit()
                                            st.rerun()
                        else:
                            st.info("No pickup requests yet")
                    with col2:
                        if don[6]:
                            st.image(f"data:image/png;base64,{don[6]}", caption="QR Code", width=150)
                            st.download_button("📥 Download QR", data=base64.b64decode(don[6]), file_name=f"donation_{don[0]}.png", mime="image/png", key=f"qr_{don[0]}")
        else:
            st.info("📭 No donations found. Create your first donation!")
    
    with tab3:
        st.markdown("#### Your Impact Dashboard")
        c = conn.cursor()
        c.execute('''SELECT COUNT(*), SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END), SUM(CASE WHEN status='accepted' THEN 1 ELSE 0 END)
                     FROM donations WHERE donor_id = ?''', (user_id,))
        result = c.fetchone()
        total = result[0] or 0
        completed = result[1] or 0
        pending = result[2] or 0
        accepted = result[3] or 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-container'><h2 style='color: var(--primary);'>{total}</h2><p>📊 Total Donations</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-container'><h2 style='color: var(--accent);'>{completed}</h2><p>✅ Completed</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-container'><h2 style='color: #f59e0b;'>{pending}</h2><p>⏳ Pending</p></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-container'><h2 style='color: #3b82f6;'>{accepted}</h2><p>🤝 Accepted</p></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-container'><h2 style='color: var(--primary);'>🍽️ {completed * 15:,}</h2><p>Estimated Meals Served</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-container'><h2 style='color: var(--accent);'>⚖️ {completed * 5} kg</h2><p>Estimated Food Saved</p></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        c.execute('''SELECT DATE(created_at) as date, COUNT(*) as count FROM donations WHERE donor_id = ?
                     GROUP BY DATE(created_at) ORDER BY date DESC LIMIT 30''', (user_id,))
        chart_data = c.fetchall()
        if chart_data:
            df = pd.DataFrame(chart_data, columns=['Date', 'Donations'])
            fig = px.line(df, x='Date', y='Donations', title='Your Donation Activity', markers=True)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("#### 🌟 Share Your Success Story")
        with st.form("success_story_form"):
            story_title = st.text_input("Story Title", placeholder="A memorable donation experience")
            story_text = st.text_area("Your Story", placeholder="Tell us about the impact...")
            submit_story = st.form_submit_button("✨ Share Story", use_container_width=True)
            if submit_story and story_title and story_text:
                st.success("✅ Story submitted for review!")
                st.balloons()

# NGO Dashboard
def show_ngo_dashboard(conn, user_id):
    st.markdown("## ❤️ NGO Dashboard")
    c = conn.cursor()
    c.execute("SELECT ngo_id, organization_name, verified, total_pickups FROM ngo_profiles WHERE user_id = ?", (user_id,))
    ngo_profile = c.fetchone()
    
    if not ngo_profile:
        st.warning("⚠️ Please complete your NGO profile first.")
        with st.form("ngo_profile_form"):
            st.markdown("#### Complete Your NGO Profile")
            org_name = st.text_input("Organization Name *")
            reg_number = st.text_input("Registration Number *")
            address = st.text_area("Complete Address *")
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Latitude", value=28.5355, format="%.6f")
            with col2:
                longitude = st.number_input("Longitude", value=77.3910, format="%.6f")
            capacity = st.number_input("Daily Capacity (meals)", min_value=10, value=50)
            submit = st.form_submit_button("✨ Submit Profile", use_container_width=True)
            if submit and org_name and reg_number and address:
                try:
                    c.execute('''INSERT INTO ngo_profiles (user_id, organization_name, registration_number, address, latitude, longitude, capacity)
                                VALUES (?, ?, ?, ?, ?, ?, ?)''', (user_id, org_name, reg_number, address, latitude, longitude, capacity))
                    conn.commit()
                    st.success("✅ Profile created! Waiting for admin verification.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("❌ Registration number already exists!")
        return
    
    ngo_id, org_name, verified, total_pickups = ngo_profile
    if not verified:
        st.warning("⏳ Your NGO profile is pending admin verification.")
        return
    
    st.success(f"✅ Welcome, {org_name}!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Total Pickups", total_pickups or 0)
    with col2:
        st.metric("🍽️ People Fed", (total_pickups or 0) * 15)
    with col3:
        c.execute("SELECT AVG(rating) FROM requests WHERE ngo_id = ? AND rating IS NOT NULL", (ngo_id,))
        avg_rating = c.fetchone()[0] or 5.0
        st.metric("⭐ Rating", f"{avg_rating:.1f}/5.0")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Browse Donations", "📦 My Requests", "📊 Impact", "🗺️ Map View"])
    
    with tab1:
        st.markdown("#### Available Food Donations")
        col1, col2, col3 = st.columns(3)
        with col1:
            food_filter = st.selectbox("Filter by Type", ["All", "Cooked Food", "Raw Food", "Packaged Food", "Fruits/Vegetables", "Bakery Items"])
        with col2:
            distance_filter = st.slider("Max Distance (km)", 1, 50, 20)
        with col3:
            search_term = st.text_input("🔍 Search", placeholder="Search food items...")
        
        c.execute("SELECT latitude, longitude FROM ngo_profiles WHERE ngo_id = ?", (ngo_id,))
        ngo_location = c.fetchone()
        ngo_lat, ngo_lon = ngo_location if ngo_location else (28.5355, 77.3910)
        
        # Fixed: Using parameterized queries to prevent SQL injection
        if food_filter == "All":
            if search_term:
                c.execute('''SELECT d.donation_id, d.food_name, d.quantity, d.food_type, d.location, d.expiry_time, 
                            d.latitude, d.longitude, d.description, u.full_name, u.phone, u.email, d.image_data 
                            FROM donations d JOIN users u ON d.donor_id = u.user_id 
                            WHERE d.status = 'pending' AND (d.food_name LIKE ? OR d.description LIKE ?)
                            ORDER BY d.created_at DESC''', (f'%{search_term}%', f'%{search_term}%'))
            else:
                c.execute('''SELECT d.donation_id, d.food_name, d.quantity, d.food_type, d.location, d.expiry_time, 
                            d.latitude, d.longitude, d.description, u.full_name, u.phone, u.email, d.image_data 
                            FROM donations d JOIN users u ON d.donor_id = u.user_id 
                            WHERE d.status = 'pending' ORDER BY d.created_at DESC''')
        else:
            if search_term:
                c.execute('''SELECT d.donation_id, d.food_name, d.quantity, d.food_type, d.location, d.expiry_time, 
                            d.latitude, d.longitude, d.description, u.full_name, u.phone, u.email, d.image_data 
                            FROM donations d JOIN users u ON d.donor_id = u.user_id 
                            WHERE d.status = 'pending' AND d.food_type = ? AND (d.food_name LIKE ? OR d.description LIKE ?)
                            ORDER BY d.created_at DESC''', (food_filter, f'%{search_term}%', f'%{search_term}%'))
            else:
                c.execute('''SELECT d.donation_id, d.food_name, d.quantity, d.food_type, d.location, d.expiry_time, 
                            d.latitude, d.longitude, d.description, u.full_name, u.phone, u.email, d.image_data 
                            FROM donations d JOIN users u ON d.donor_id = u.user_id 
                            WHERE d.status = 'pending' AND d.food_type = ? ORDER BY d.created_at DESC''', (food_filter,))
        
        donations = c.fetchall()
        
        if donations:
            for don in donations:
                distance = ((don[6] - ngo_lat)**2 + (don[7] - ngo_lon)**2)**0.5 * 111
                if distance <= distance_filter:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"""<div class='donation-card'>
                                <h4>🍱 {don[1]} ({don[2]})</h4>
                                <p><strong>Type:</strong> {don[3]} | <strong>Location:</strong> {don[4]}</p>
                                <p><strong>Expires:</strong> {don[5]} | <strong>Distance:</strong> ~{distance:.1f} km</p>
                                <p><strong>Contact:</strong> {don[9]} | 📧 {don[11]}</p>
                                {f"<p><strong>Description:</strong> {don[8]}</p>" if don[8] else ""}
                            </div>""", unsafe_allow_html=True)
                        with col2:
                            if don[12]:
                                st.image(f"data:image/png;base64,{don[12]}", width=150)
                        
                        # Check if already requested
                        c.execute("SELECT status FROM requests WHERE donation_id = ? AND ngo_id = ?", (don[0], ngo_id))
                        existing_request = c.fetchone()
                        if existing_request:
                            st.info(f"📋 Status: {existing_request[0].upper()}")
                        else:
                            if st.button(f"🚀 Request Pickup", key=f"req_{don[0]}", use_container_width=True):
                                c.execute("INSERT INTO requests (donation_id, ngo_id, status) VALUES (?, ?, 'pending')", (don[0], ngo_id))
                                conn.commit()
                                st.success("✅ Request sent successfully!")
                                st.rerun()
                        st.markdown("---")
        else:
            st.info("📭 No donations available matching your criteria.")
    
    with tab2:
        st.markdown("#### Your Pickup Requests")
        status_filter = st.selectbox("Filter", ["All", "pending", "accepted", "completed"], key="ngo_status_filter")
        
        if status_filter == "All":
            c.execute('''SELECT r.request_id, r.status, r.requested_at, d.food_name, d.quantity, d.location, 
                        d.expiry_time, u.full_name, u.phone, d.qr_code, d.donation_id
                        FROM requests r JOIN donations d ON r.donation_id = d.donation_id
                        JOIN users u ON d.donor_id = u.user_id WHERE r.ngo_id = ? ORDER BY r.requested_at DESC''', (ngo_id,))
        else:
            c.execute('''SELECT r.request_id, r.status, r.requested_at, d.food_name, d.quantity, d.location, 
                        d.expiry_time, u.full_name, u.phone, d.qr_code, d.donation_id
                        FROM requests r JOIN donations d ON r.donation_id = d.donation_id
                        JOIN users u ON d.donor_id = u.user_id WHERE r.ngo_id = ? AND r.status = ? 
                        ORDER BY r.requested_at DESC''', (ngo_id, status_filter))
        
        requests_list = c.fetchall()
        if requests_list:
            for req in requests_list:
                status_emoji = {"pending": "⏳", "accepted": "✅", "completed": "🎉", "rejected": "❌"}
                with st.expander(f"{status_emoji.get(req[1], '📋')} {req[3]} - {req[4]} ({req[1].upper()})"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**📍 Location:** {req[5]}")
                        st.write(f"**⏰ Expires:** {req[6]}")
                        st.write(f"**👤 Donor:** {req[7]} | 📱 {req[8] or 'N/A'}")
                        st.write(f"**📅 Requested:** {req[2]}")
                        
                        if req[1] == 'accepted':
                            if st.button("✅ Mark as Collected", key=f"collect_{req[0]}", use_container_width=True):
                                c.execute("UPDATE requests SET status='completed', collected_at=? WHERE request_id=?", 
                                         (datetime.now(), req[0]))
                                c.execute("UPDATE donations SET status='completed', collected_at=? WHERE donation_id=?", 
                                         (datetime.now(), req[10]))
                                c.execute("UPDATE ngo_profiles SET total_pickups = total_pickups + 1 WHERE ngo_id=?", (ngo_id,))
                                conn.commit()
                                st.success("🎉 Donation marked as collected!")
                                st.balloons()
                                st.rerun()
                    with col2:
                        if req[9] and req[1] == 'accepted':
                            st.image(f"data:image/png;base64,{req[9]}", caption="Scan QR", width=150)
        else:
            st.info("📭 No requests found.")
    
    with tab3:
        st.markdown("#### Your Impact Statistics")
        c.execute('''SELECT COUNT(*), 
                    SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END), 
                    SUM(CASE WHEN status='accepted' THEN 1 ELSE 0 END)
                    FROM requests WHERE ngo_id = ?''', (ngo_id,))
        stats = c.fetchone()
        total = stats[0] or 0
        completed = stats[1] or 0
        pending = stats[2] or 0
        accepted = stats[3] or 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-container'><h2 style='color: var(--primary);'>{total}</h2><p>📊 Total Requests</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-container'><h2 style='color: var(--accent);'>{completed}</h2><p>✅ Completed</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-container'><h2 style='color: #f59e0b;'>{pending}</h2><p>⏳ Pending</p></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-container'><h2 style='color: #3b82f6;'>{accepted}</h2><p>🤝 Accepted</p></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-container'><h2 style='color: var(--primary);'>🍽️ {completed * 15:,}</h2><p>People Fed</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-container'><h2 style='color: var(--accent);'>⚖️ {completed * 5} kg</h2><p>Food Distributed</p></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        c.execute('''SELECT DATE(r.collected_at) as date, COUNT(*) as count FROM requests r
                     WHERE r.ngo_id = ? AND r.status = 'completed' AND r.collected_at IS NOT NULL
                     GROUP BY DATE(r.collected_at) ORDER BY date DESC LIMIT 30''', (ngo_id,))
        chart_data = c.fetchall()
        if chart_data:
            df = pd.DataFrame(chart_data, columns=['Date', 'Pickups'])
            fig = px.bar(df, x='Date', y='Pickups', title='Your Pickup Activity')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("#### Donation Map View")
        c.execute('''SELECT d.food_name, d.quantity, d.latitude, d.longitude, d.location 
                    FROM donations d WHERE d.status = 'pending' ''')
        map_donations = c.fetchall()
        
        if map_donations:
            map_data = pd.DataFrame(map_donations, columns=['Food', 'Quantity', 'lat', 'lon', 'Location'])
            st.map(map_data)
            st.info(f"📍 Showing {len(map_donations)} available donations near you")
        else:
            st.info("📭 No donations to display on map")

# Admin Dashboard
def show_admin_dashboard(conn):
    st.markdown("## 🛡️ Admin Dashboard")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "👥 Users", "🏢 NGOs", "📦 Donations", "🌟 Stories"])
    
    c = conn.cursor()
    
    with tab1:
        st.markdown("#### Platform Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        c.execute("SELECT COUNT(*) FROM users")
        total_users = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM donations")
        total_donations = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM ngo_profiles WHERE verified=1")
        verified_ngos = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM donations WHERE status='completed'")
        completed = c.fetchone()[0]
        
        with col1:
            st.markdown(f"<div class='stat-card'><h2>{total_users}</h2><p>Total Users</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='stat-card'><h2>{total_donations}</h2><p>Total Donations</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='stat-card'><h2>{verified_ngos}</h2><p>Verified NGOs</p></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='stat-card'><h2>{completed}</h2><p>Completed</p></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            c.execute('''SELECT DATE(created_at) as date, COUNT(*) as count FROM donations
                         GROUP BY DATE(created_at) ORDER BY date DESC LIMIT 30''')
            data = c.fetchall()
            if data:
                df = pd.DataFrame(data, columns=['Date', 'Donations'])
                fig = px.line(df, x='Date', y='Donations', title='Donations Over Time', markers=True)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            c.execute('''SELECT role, COUNT(*) FROM users GROUP BY role''')
            data = c.fetchall()
            if data:
                df = pd.DataFrame(data, columns=['Role', 'Count'])
                fig = px.pie(df, values='Count', names='Role', title='User Distribution')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### User Management")
        c.execute('''SELECT user_id, email, full_name, role, status, verified, created_at FROM users ORDER BY created_at DESC''')
        users = c.fetchall()
        
        if users:
            df = pd.DataFrame(users, columns=['ID', 'Email', 'Name', 'Role', 'Status', 'Verified', 'Created'])
            st.dataframe(df, use_container_width=True)
            
            st.markdown("#### Update User Status")
            user_options = [f"{u[0]} - {u[2]} ({u[1]})" for u in users]
            if user_options:
                user_id_str = st.selectbox("Select User", user_options)
                if user_id_str:
                    selected_id = int(user_id_str.split(" - ")[0])
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Activate", key="activate_user"):
                            c.execute("UPDATE users SET status='active' WHERE user_id=?", (selected_id,))
                            conn.commit()
                            st.success("User activated!")
                            st.rerun()
                    with col2:
                        if st.button("🚫 Deactivate", key="deactivate_user"):
                            c.execute("UPDATE users SET status='inactive' WHERE user_id=?", (selected_id,))
                            conn.commit()
                            st.success("User deactivated!")
                            st.rerun()
    
    with tab3:
        st.markdown("#### NGO Verification")
        c.execute('''SELECT n.ngo_id, n.organization_name, n.registration_number, n.address, n.verified, u.email, u.full_name
                    FROM ngo_profiles n JOIN users u ON n.user_id = u.user_id ORDER BY n.verified, n.ngo_id DESC''')
        ngos = c.fetchall()
        
        if ngos:
            for ngo in ngos:
                status = "✅ Verified" if ngo[4] else "⏳ Pending"
                with st.expander(f"{status} {ngo[1]} ({ngo[2]})"):
                    st.write(f"**Organization:** {ngo[1]}")
                    st.write(f"**Registration Number:** {ngo[2]}")
                    st.write(f"**Address:** {ngo[3]}")
                    st.write(f"**Contact:** {ngo[6]} ({ngo[5]})")
                    
                    if not ngo[4]:
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Verify", key=f"verify_{ngo[0]}"):
                                c.execute("UPDATE ngo_profiles SET verified=1 WHERE ngo_id=?", (ngo[0],))
                                c.execute("UPDATE users SET verified=1 WHERE user_id=(SELECT user_id FROM ngo_profiles WHERE ngo_id=?)", (ngo[0],))
                                conn.commit()
                                st.success("NGO verified!")
                                st.rerun()
                        with col2:
                            if st.button("❌ Reject", key=f"reject_ngo_{ngo[0]}"):
                                c.execute("DELETE FROM ngo_profiles WHERE ngo_id=?", (ngo[0],))
                                conn.commit()
                                st.success("NGO rejected!")
                                st.rerun()
        else:
            st.info("No NGO profiles found.")
    
    with tab4:
        st.markdown("#### Donation Management")
        status_filter = st.selectbox("Filter by Status", ["All", "pending", "accepted", "completed", "expired"], key="admin_donation_filter")
        
        if status_filter == "All":
            c.execute('''SELECT d.donation_id, d.food_name, d.quantity, d.status, d.created_at, u.full_name, d.location
                        FROM donations d JOIN users u ON d.donor_id = u.user_id ORDER BY d.created_at DESC''')
        else:
            c.execute('''SELECT d.donation_id, d.food_name, d.quantity, d.status, d.created_at, u.full_name, d.location
                        FROM donations d JOIN users u ON d.donor_id = u.user_id WHERE d.status = ? ORDER BY d.created_at DESC''', (status_filter,))
        
        donations = c.fetchall()
        if donations:
            df = pd.DataFrame(donations, columns=['ID', 'Food', 'Quantity', 'Status', 'Created', 'Donor', 'Location'])
            st.dataframe(df, use_container_width=True)
            
            # Delete donation option
            st.markdown("#### Delete Donation")
            donation_options = [f"{d[0]} - {d[1]} by {d[5]}" for d in donations]
            if donation_options:
                selected_donation = st.selectbox("Select Donation", donation_options, key="delete_donation_select")
                if st.button("🗑️ Delete Selected Donation", key="delete_donation_btn"):
                    donation_id = int(selected_donation.split(" - ")[0])
                    c.execute("DELETE FROM requests WHERE donation_id=?", (donation_id,))
                    c.execute("DELETE FROM donations WHERE donation_id=?", (donation_id,))
                    conn.commit()
                    st.success("Donation deleted!")
                    st.rerun()
        else:
            st.info("No donations found.")
    
    with tab5:
        st.markdown("#### Success Stories Management")
        c.execute('''SELECT s.story_id, s.title, s.story, s.impact_meals, s.featured, s.created_at, n.organization_name
                    FROM success_stories s JOIN ngo_profiles n ON s.ngo_id = n.ngo_id ORDER BY s.created_at DESC''')
        stories = c.fetchall()
        
        if stories:
            for story in stories:
                featured = "⭐ Featured" if story[4] else "📝 Regular"
                with st.expander(f"{featured} {story[1]} by {story[6]}"):
                    st.write(story[2])
                    st.write(f"**Impact:** {story[3]} meals | **Created:** {story[5]}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if not story[4]:
                            if st.button("⭐ Feature", key=f"feature_{story[0]}"):
                                c.execute("UPDATE success_stories SET featured=1 WHERE story_id=?", (story[0],))
                                conn.commit()
                                st.rerun()
                        else:
                            if st.button("☆ Unfeature", key=f"unfeature_{story[0]}"):
                                c.execute("UPDATE success_stories SET featured=0 WHERE story_id=?", (story[0],))
                                conn.commit()
                                st.rerun()
                    with col2:
                        if st.button("🗑️ Delete", key=f"delete_story_{story[0]}"):
                            c.execute("DELETE FROM success_stories WHERE story_id=?", (story[0],))
                            conn.commit()
                            st.rerun()
        
        st.markdown("---")
        st.markdown("#### Add Success Story")
        with st.form("admin_story_form"):
            c.execute("SELECT ngo_id, organization_name FROM ngo_profiles WHERE verified=1")
            ngos = c.fetchall()
            if ngos:
                ngo_options = [f"{n[0]} - {n[1]}" for n in ngos]
                ngo_select = st.selectbox("Select NGO", ngo_options)
                title = st.text_input("Title")
                story_text = st.text_area("Story")
                impact = st.number_input("Meals Served", min_value=1, value=50)
                
                if st.form_submit_button("📝 Add Story", use_container_width=True):
                    if ngo_select and title and story_text:
                        ngo_id = int(ngo_select.split(" - ")[0])
                        c.execute("INSERT INTO success_stories (ngo_id, title, story, impact_meals, featured) VALUES (?, ?, ?, ?, 1)", 
                                 (ngo_id, title, story_text, impact))
                        conn.commit()
                        st.success("✅ Story added!")
                        st.rerun()
            else:
                st.warning("No verified NGOs available. Please verify an NGO first.")
                st.form_submit_button("📝 Add Story", disabled=True)

# Login Page
def show_login_page(conn):
    st.markdown('<h1 class="main-header">🍱 Smart Food Donation System</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='hero-section'><h2>Welcome Back!</h2><p>Login to continue your food donation journey</p></div>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("🚀 Login", use_container_width=True)
            with col_b:
                register_btn = st.form_submit_button("📝 Register", use_container_width=True)
            
            if submit:
                if email and password:
                    success, user_data = login_user(conn, email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = user_data
                        st.success(f"✅ Welcome back, {user_data['name']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password")
                else:
                    st.warning("⚠️ Please fill all fields")
            
            if register_btn:
                st.session_state.page = "register"
                st.rerun()

# Register Page
def show_register_page(conn):
    st.markdown('<h1 class="main-header">🍱 Smart Food Donation System</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='hero-section'><h2>Join Our Mission</h2><p>Create an account to start donating or receiving food</p></div>", unsafe_allow_html=True)
        
        default_role = st.session_state.get('register_role', 'donor')
        
        with st.form("register_form"):
            full_name = st.text_input("👤 Full Name *", placeholder="Enter your full name")
            email = st.text_input("📧 Email *", placeholder="Enter your email")
            phone = st.text_input("📱 Phone Number", placeholder="Enter your phone number")
            password = st.text_input("🔒 Password *", type="password", placeholder="Create a password (min 6 characters)")
            confirm_password = st.text_input("🔒 Confirm Password *", type="password", placeholder="Confirm your password")
            role = st.selectbox("🎭 Register as", ["donor", "ngo"], index=0 if default_role == "donor" else 1)
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("✨ Create Account", use_container_width=True)
            with col_b:
                back_btn = st.form_submit_button("🔙 Back to Login", use_container_width=True)
            
            if submit:
                if full_name and email and password and confirm_password:
                    if password != confirm_password:
                        st.error("❌ Passwords don't match!")
                    elif len(password) < 6:
                        st.error("❌ Password must be at least 6 characters!")
                    elif "@" not in email or "." not in email:
                        st.error("❌ Please enter a valid email address!")
                    else:
                        success, result = register_user(conn, email, password, full_name, phone, role)
                        if success:
                            st.success("✅ Account created successfully! Please login.")
                            time.sleep(2)
                            st.session_state.page = "login"
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
                else:
                    st.warning("⚠️ Please fill all required fields (*)")
            
            if back_btn:
                st.session_state.page = "login"
                st.rerun()

# Main Application
def main():
    conn = init_database()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🍱 Food Donation")
        st.markdown("---")
        
        # Theme toggle
        theme_label = "🌙 Dark Mode" if st.session_state.theme == 'light' else "☀️ Light Mode"
        if st.button(theme_label, use_container_width=True):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()
        
        st.markdown("---")
        
        if st.session_state.logged_in:
            st.markdown(f"**👤 {st.session_state.user['name']}**")
            st.markdown(f"*{st.session_state.user['role'].upper()}*")
            st.markdown("---")
            
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()
            
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.page = "home"
                st.rerun()
        else:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()
            
            if st.button("🔑 Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
            
            if st.button("📝 Register", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM donations WHERE status='pending'")
        active = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM donations WHERE status='completed'")
        completed = c.fetchone()[0]
        st.metric("🟢 Active Donations", active)
        st.metric("✅ Completed", completed)
    
    # Main content area
    if st.session_state.page == "home":
        show_home_page(conn)
    elif st.session_state.page == "login":
        show_login_page(conn)
    elif st.session_state.page == "register":
        show_register_page(conn)
    elif st.session_state.page == "dashboard":
        if st.session_state.logged_in:
            user = st.session_state.user
            if user['role'] == 'donor':
                show_donor_dashboard(conn, user['user_id'])
            elif user['role'] == 'ngo':
                show_ngo_dashboard(conn, user['user_id'])
            elif user['role'] == 'admin':
                show_admin_dashboard(conn)
        else:
            st.warning("⚠️ Please login to access the dashboard")
            st.session_state.page = "login"
            st.rerun()
    
    # Footer
    st.markdown("""
    <div class='footer'>
        <p>🍱 Smart Food Donation System</p>
        <p>Made with ❤️ for a better world | Reducing food waste, one donation at a time</p>
        <p>© 2025 All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()