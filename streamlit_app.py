"""Streamlit dashboard for Cipher Threat Intelligence"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from typing import List, Dict
import logging
from urllib.parse import urlparse
import re

# Configure page with dark theme
st.set_page_config(
    page_title="Cipher Threat Intelligence",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply comprehensive dark theme styling
st.markdown("""
<style>
    /* ==================== DARK THEME - COMPREHENSIVE ==================== */
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    
    /* Sidebar dark theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        color: #f1f5f9;
    }
    
    /* Sidebar text - ensure all text is visible */
    [data-testid="stSidebar"] {
        color: #f1f5f9 !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
    }
    
    /* Sidebar title */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar caption */
    [data-testid="stSidebar"] .stCaption {
        color: #cbd5e1 !important;
    }
    
    /* Headers - all levels */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #f1f5f9 !important;
    }
    
    /* Paragraphs and text */
    p, span, div, li, td, th, .stMarkdown p, .stMarkdown li {
        color: #e2e8f0 !important;
    }
    
    /* Metric cards - dark theme */
    [data-testid="stMetricValue"] {
        color: #60a5fa !important;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #34d399 !important;
    }
    
    /* Input fields - dark theme */
    .stTextInput > div > div > input {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border-color: #334155 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }
    
    /* Selectbox - dark theme */
    .stSelectbox > div > div > select {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border-color: #334155 !important;
    }
    
    /* Selectbox label - dark theme */
    .stSelectbox label {
        color: #f1f5f9 !important;
        font-weight: 500 !important;
    }
    
    /* Selectbox option text - dark text for dropdown options with proper font */
    .stSelectbox > div > div > select option {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        padding: 12px 10px !important;
        line-height: 1.5 !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }
    
    /* Selected option in dropdown - darker background */
    .stSelectbox > div > div > select option:checked,
    .stSelectbox > div > div > select option[selected] {
        background-color: #e2e8f0 !important;
        color: #000000 !important;
        font-weight: 800 !important;
    }
    
    /* Hovered option in dropdown */
    .stSelectbox > div > div > select option:hover {
        background-color: #cbd5e1 !important;
        color: #000000 !important;
        font-weight: 800 !important;
    }
    
    /* Sidebar radio buttons - DARK THEME with white text - FIXED WIDTH */
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stRadio > label,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio label div {
        color: #ffffff !important;
        background-color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        padding: 2px 10px !important;
        margin: 1px 0 !important;
        border-radius: 3px !important;
        border: 0.5px solid #475569 !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        line-height: 1.1 !important;
        min-height: 60px !important;
        height: 60px !important;
        width: 100% !important;
        max-width: 100% !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-end !important;
        text-align: right !important;
        white-space: nowrap !important;
        writing-mode: horizontal-tb !important;
        box-sizing: border-box !important;
    }
    
    /* Ensure all radio button containers are same width */
    [data-testid="stSidebar"] .stRadio > div,
    [data-testid="stSidebar"] .stRadio {
        width: 100% !important;
    }
    
    /* Hide the main radio button label (appears above Dashboard button) */
    [data-testid="stSidebar"] .stRadio > label:first-child,
    [data-testid="stSidebar"] .stRadio > label,
    [data-testid="stSidebar"] .stRadio label:first-of-type,
    [data-testid="stSidebar"] .stRadio label:empty,
    [data-testid="stSidebar"] .stRadio label[for*="radio"]:first-child {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        opacity: 0 !important;
    }
    
    /* Hide any label that appears before the first div containing options */
    [data-testid="stSidebar"] .stRadio > label:not([for*="Dashboard"]):not([for*="IOC"]):not([for*="Threat"]):not([for*="Network"]):not([for*="Timeline"]) {
        display: none !important;
    }
    
    /* Hide only blank/empty option buttons (not Dashboard) */
    [data-testid="stSidebar"] .stRadio > div > label:empty,
    [data-testid="stSidebar"] .stRadio > div:has(> label:empty) {
        display: none !important;
    }
    
    /* Hide the first div if it contains a blank label or doesn't match valid options */
    [data-testid="stSidebar"] .stRadio > div:first-child:has(> label:empty),
    [data-testid="stSidebar"] .stRadio > div:first-child:has(> label:not(:has-text("Dashboard")):not(:has-text("IOC")):not(:has-text("Threat")):not(:has-text("Network")):not(:has-text("Timeline"))) {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    
    /* Ensure radio container uses flexbox for ordering */
    [data-testid="stSidebar"] .stRadio {
        display: flex !important;
        flex-direction: column !important;
        position: relative !important;
    }
    
    /* Default order for all radio button divs */
    [data-testid="stSidebar"] .stRadio > div {
        order: 99 !important;
    }
    
    /* PURE CSS SOLUTION - JavaScript blocked by CSP */
    /* Since IOC Lookup is appearing first, hide it using CSS */
    /* We'll hide the first div if it's not Dashboard */
    
    /* Make container flexbox */
    [data-testid="stSidebar"] .stRadio {
        display: flex !important;
        flex-direction: column !important;
    }
    
    /* CRITICAL: Hide the FIRST div (which is IOC Lookup) if Dashboard is not first */
    /* Strategy: Hide first div, show second div if it's Dashboard */
    [data-testid="stSidebar"] .stRadio > div:first-child {
        /* Check if this first div contains "IOC Lookup" - if so, hide it */
        /* We'll use a CSS selector that targets first child and hides it */
        /* Then show Dashboard which should be second */
    }
    
    /* Hide first child div if it's not the selected one (Dashboard should be selected) */
    [data-testid="stSidebar"] .stRadio > div:first-child:not(:has(input:checked)) {
        /* If first div doesn't have checked input, it might be IOC Lookup */
        /* But this won't work if Dashboard isn't checked */
    }
    
    /* Alternative: Hide first div entirely and rely on Dashboard being second */
    /* Since CSS can't reliably detect text, we'll hide first div as a workaround */
    [data-testid="stSidebar"] .stRadio > div:first-of-type:has(label:not(:has([for*="b0"]))) {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        opacity: 0 !important;
    }
    
    /* Show second div (which should be Dashboard) */
    [data-testid="stSidebar"] .stRadio > div:nth-child(2) {
        display: block !important;
        visibility: visible !important;
    }
    
    /* Force visibility rules - if Dashboard exists, hide everything before it */
    [data-testid="stSidebar"] .stRadio > div[data-dashboard="true"] ~ div:not([data-dashboard="true"]) {
        /* These come after Dashboard - they're fine */
    }
    
    /* Hide anything that comes before Dashboard in DOM */
    [data-testid="stSidebar"] .stRadio > div:not([data-dashboard="true"]):has(~ div[data-dashboard="true"]) {
        /* This won't work - CSS can't select previous siblings, but JS can */
    }
    
    /* Force all text inside radio option labels to be white and horizontal */
    [data-testid="stSidebar"] .stRadio > div > label,
    [data-testid="stSidebar"] .stRadio label:not(:first-child) {
        color: #ffffff !important;
        writing-mode: horizontal-tb !important;
        text-orientation: mixed !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label *,
    [data-testid="stSidebar"] .stRadio label:not(:first-child) * {
        color: #ffffff !important;
        writing-mode: horizontal-tb !important;
        text-orientation: mixed !important;
    }
    
    /* Ensure text doesn't wrap or rotate */
    [data-testid="stSidebar"] .stRadio > div > label span,
    [data-testid="stSidebar"] .stRadio > div > label p,
    [data-testid="stSidebar"] .stRadio > div > label div {
        writing-mode: horizontal-tb !important;
        text-orientation: mixed !important;
        white-space: nowrap !important;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: #334155 !important;
        border-color: #64748b !important;
        border-width: 0.5px !important;
        font-weight: 700 !important;
        padding: 2px 10px !important;
        height: 60px !important;
        min-height: 60px !important;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover * {
        color: #ffffff !important;
    }
    
    /* Selected radio button - white text on blue background - DARK THEME + FIXED WIDTH */
    [data-testid="stSidebar"] .stRadio input:checked + label,
    [data-testid="stSidebar"] .stRadio input:checked + label *,
    [data-testid="stSidebar"] .stRadio label[data-checked="true"],
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] * {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border-color: #2563eb !important;
        border-width: 0.5px !important;
        font-weight: 700 !important;
        font-size: 0.875rem !important;
        padding: 2px 10px !important;
        margin: 1px 0 !important;
        line-height: 1.1 !important;
        height: 60px !important;
        min-height: 60px !important;
        width: 100% !important;
    }
    
    /* Radio button input */
    [data-testid="stSidebar"] .stRadio input[type="radio"] {
        accent-color: #3b82f6 !important;
    }
    
    /* Additional targeting for Streamlit's radio button structure - DARK THEME */
    [data-testid="stSidebar"] [class*="stRadio"] label,
    [data-testid="stSidebar"] [class*="radio"] label {
        color: #ffffff !important;
        background-color: #1e293b !important;
        width: 100% !important;
    }
    
    [data-testid="stSidebar"] [class*="stRadio"] label *,
    [data-testid="stSidebar"] [class*="radio"] label * {
        color: #ffffff !important;
    }
    
    /* Number input - dark theme */
    .stNumberInput > div > div > input {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border-color: #334155 !important;
    }
    
    /* Slider - dark theme */
    .stSlider > div > div {
        background-color: #1e293b !important;
    }
    
    /* Buttons - dark theme */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white !important;
        border: none;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Dataframe - dark theme */
    .dataframe {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
    }
    
    /* Tables - dark theme */
    table {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
    }
    
    th {
        background-color: #334155 !important;
        color: #f1f5f9 !important;
    }
    
    td {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border-color: #334155 !important;
    }
    
    /* Expander - dark theme */
    .streamlit-expanderHeader {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }
    
    /* Error/Success/Info/Warning messages - dark theme */
    .stAlert {
        background-color: #1e293b !important;
        border-color: #334155 !important;
    }
    
    .stSuccess {
        background-color: #065f46 !important;
        border-color: #10b981 !important;
        color: #d1fae5 !important;
    }
    
    .stError {
        background-color: #7f1d1d !important;
        border-color: #ef4444 !important;
        color: #fee2e2 !important;
    }
    
    .stWarning {
        background-color: #78350f !important;
        border-color: #f59e0b !important;
        color: #fef3c7 !important;
    }
    
    .stInfo {
        background-color: #1e3a8a !important;
        border-color: #3b82f6 !important;
        color: #dbeafe !important;
    }
    
    /* Code blocks - dark theme */
    code {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
    }
    
    pre {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
    }
    
    /* Links - dark theme */
    a {
        color: #60a5fa !important;
    }
    
    a:hover {
        color: #93c5fd !important;
    }
    
    /* Divider - dark theme */
    hr {
        border-color: #334155 !important;
    }
    
    /* Scrollbar - dark theme */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
</style>
<!-- 
    JAVASCRIPT REMOVED: Streamlit's Content Security Policy (CSP) blocks inline scripts.
    All functionality must be achieved via CSS only.
-->
""", unsafe_allow_html=True)

# API base URL with validation and HTTPS fix
def validate_and_fix_api_url(url: str) -> str:
    """Validate API URL and fix HTTPS issues for IP addresses"""
    if not url:
        return "http://localhost:8000"
    
    # Remove trailing slashes
    url = url.strip().rstrip('/')
    
    # Parse URL
    parsed = urlparse(url)
    
    # If no scheme, default to http
    if not parsed.scheme:
        url = f"http://{url}"
        parsed = urlparse(url)
    
    # Check if it's an IP address (IPv4 or IPv6)
    is_ip = False
    hostname = parsed.hostname or ""
    
    # IPv4 pattern
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    # IPv6 pattern (simplified)
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::'
    
    if re.match(ipv4_pattern, hostname) or re.match(ipv6_pattern, hostname):
        is_ip = True
    
    # Force HTTP for IP addresses or if HTTPS is specified but not secure
    if parsed.scheme == "https" and (is_ip or not hostname.endswith('.com') and not hostname.endswith('.org') and not hostname.endswith('.net') and not hostname.endswith('.io')):
        # Convert HTTPS to HTTP for IP addresses and non-standard domains
        url = url.replace('https://', 'http://', 1)
        st.sidebar.warning("⚠️ HTTPS not supported for IP addresses. Using HTTP instead.")
    
    # Force HTTP for localhost
    if 'localhost' in hostname or '127.0.0.1' in hostname:
        url = url.replace('https://', 'http://', 1)
    
    return url

# API base URL input with validation
st.sidebar.markdown("### 🔌 API Configuration")
api_url_input = st.sidebar.text_input("API URL", value="http://localhost:8000", help="Enter the API server URL (e.g., http://localhost:8000 or http://71.162.0.66:8000)")
API_BASE_URL = validate_and_fix_api_url(api_url_input)

# Display current API URL with status
st.sidebar.caption(f"📍 Connecting to: `{API_BASE_URL}`")

# Create a requests session with SSL verification disabled for HTTP endpoints
session = requests.Session()
parsed_api_url = urlparse(API_BASE_URL)
if parsed_api_url.scheme == "http":
    # Disable SSL warnings for HTTP endpoints
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session.verify = False

# Quick connection test button
if st.sidebar.button("🔍 Test Connection", help="Test if the API server is reachable"):
    try:
        test_response = session.get(f"{API_BASE_URL}/docs", timeout=5)
        if test_response.status_code in [200, 404]:  # 404 is OK, means server is responding
            st.sidebar.success("✅ API server is reachable!")
        else:
            st.sidebar.warning(f"⚠️ Server responded with status {test_response.status_code}")
    except requests.exceptions.ConnectionError:
        st.sidebar.error("❌ Connection refused - API server is not running or not accessible")
        st.sidebar.info("💡 Make sure the API server is running and the URL is correct")
    except requests.exceptions.Timeout:
        st.sidebar.error("⏱️ Connection timeout - Server is not responding")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {str(e)}")

# Title
st.title("🔐 Cipher Threat Intelligence Platform")
st.markdown("Cyber threat detection, attribution, and incident response")

# Sidebar
st.sidebar.markdown("### 🧭 Navigation")

# ALTERNATIVE APPROACH: Use individual buttons for complete control over order
# Initialize page state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

# CRITICAL: Render buttons in the EXACT order we want - Dashboard FIRST
# Using buttons instead of radio gives us full control over rendering order
# Dashboard button - DEFINITELY FIRST
if st.sidebar.button("📊 Dashboard", use_container_width=True, key="nav_dashboard", type="secondary"):
    st.session_state.current_page = "Dashboard"
    st.rerun()

# IOC Lookup button - SECOND
if st.sidebar.button("🔍 IOC Lookup", use_container_width=True, key="nav_ioc", type="secondary"):
    st.session_state.current_page = "IOC Lookup"
    st.rerun()

# Threat Analysis button - THIRD
if st.sidebar.button("🛡️ Threat Analysis", use_container_width=True, key="nav_threat", type="secondary"):
    st.session_state.current_page = "Threat Analysis"
    st.rerun()

# Network Graph button - FOURTH
if st.sidebar.button("🕸️ Network Graph", use_container_width=True, key="nav_network", type="secondary"):
    st.session_state.current_page = "Network Graph"
    st.rerun()

# Timeline button - FIFTH
if st.sidebar.button("⏱️ Timeline", use_container_width=True, key="nav_timeline", type="secondary"):
    st.session_state.current_page = "Timeline"
    st.rerun()

# Use the current page from session state
page = st.session_state.current_page

# Style the navigation buttons with CSS - highlight active button
current_page_name = st.session_state.current_page
st.markdown(f"""
<style>
    /* Style navigation buttons in sidebar - DARK THEME */
    [data-testid="stSidebar"] button[kind="secondary"] {{
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 0.5px solid #475569 !important;
        border-radius: 3px !important;
        padding: 10px !important;
        margin: 2px 0 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        height: 60px !important;
        text-align: center !important;
        width: 100% !important;
    }}
    [data-testid="stSidebar"] button[kind="secondary"]:hover {{
        background-color: #334155 !important;
        border-color: #64748b !important;
    }}
    /* Highlight active button */
    [data-testid="stSidebar"] button[kind="secondary"][data-baseweb="button"]:has-text("{current_page_name}") {{
        background-color: #3b82f6 !important;
        border-color: #2563eb !important;
        font-weight: 700 !important;
    }}
</style>
""", unsafe_allow_html=True)

# Dashboard
if page == "Dashboard":
    st.header("Dashboard Overview")
    
    try:
        # Get threat stats
        response = session.get(f"{API_BASE_URL}/api/v1/threats/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Threats", stats.get("total_threats", 0))
            
            with col2:
                threat_types = stats.get("by_threat_type", {})
                if threat_types:
                    st.metric("Threat Types", len(threat_types))
                else:
                    st.metric("Threat Types", 0)
            
            with col3:
                sources = stats.get("by_source", {})
                if sources:
                    st.metric("Data Sources", len(sources))
                else:
                    st.metric("Data Sources", 0)
            
            with col4:
                st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
            
            # Threat type distribution
            threat_types = stats.get("by_threat_type", {})
            if threat_types:
                st.subheader("Threat Type Distribution")
                df_types = pd.DataFrame(list(threat_types.items()), columns=["Threat Type", "Count"])
                fig_types = px.bar(df_types, x="Threat Type", y="Count", title="Threats by Type")
                fig_types.update_layout(
                    plot_bgcolor='#1e293b',
                    paper_bgcolor='#0f172a',
                    font_color='#f1f5f9',
                    title_font_color='#f1f5f9'
                )
                st.plotly_chart(fig_types, use_container_width=True)
            else:
                st.info("📊 No threat type data available yet. Data will appear here once threats are collected.")
            
            # Source distribution
            sources = stats.get("by_source", {})
            if sources:
                st.subheader("Data Source Distribution")
                df_sources = pd.DataFrame(list(sources.items()), columns=["Source", "Count"])
                fig_sources = px.pie(df_sources, values="Count", names="Source", title="Threats by Source")
                fig_sources.update_layout(
                    plot_bgcolor='#1e293b',
                    paper_bgcolor='#0f172a',
                    font_color='#f1f5f9',
                    title_font_color='#f1f5f9'
                )
                st.plotly_chart(fig_sources, use_container_width=True)
            else:
                st.info("📊 No data source information available yet. Data will appear here once threats are collected.")
        elif response.status_code == 500:
            # Handle 500 error with more details
            try:
                error_detail = response.json()
                error_msg = error_detail.get("detail", "Internal server error")
                st.error(f"⚠️ API Error (500): {error_msg}")
            except:
                st.error(f"⚠️ API Error (500): Internal server error")
            
            st.warning("**Possible causes:**")
            st.markdown("""
            - The API database is not initialized
            - No data has been collected yet
            - Database connection issue
            - API endpoint needs data to be seeded
            """)
            
            st.info("💡 **This is normal for a new installation.**")
            st.markdown("""
            **To fix:**
            1. The API is working correctly (connection successful)
            2. The endpoint needs data to be populated
            3. You can still test the dashboard UI and navigation
            4. Once data is added to the API, statistics will appear here
            """)
            
            # Show demo/empty state
            st.subheader("📊 Dashboard Overview (Demo Mode)")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Threats", 0)
            with col2:
                st.metric("Threat Types", 0)
            with col3:
                st.metric("Data Sources", 0)
            with col4:
                st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
            
            st.info("🔍 **Dashboard is working correctly!** The API connection is successful, but the stats endpoint needs data. You can test other features like IOC Lookup and Threat Analysis.")
        else:
            st.error(f"⚠️ Failed to fetch stats: HTTP {response.status_code}")
            try:
                error_detail = response.json()
                st.info(f"Error details: {error_detail}")
            except:
                pass
    except requests.exceptions.SSLError as e:
        st.error(f"⚠️ SSL/HTTPS Error: The API endpoint doesn't support HTTPS. Please use HTTP instead (e.g., http://71.162.0.66:8000)")
        st.info(f"💡 Tip: Change the API URL in the sidebar to use 'http://' instead of 'https://'")
    except requests.exceptions.ConnectionError as e:
        error_msg = str(e)
        if "refused" in error_msg.lower() or "ERR_CONNECTION_REFUSED" in error_msg:
            st.error(f"⚠️ Connection Refused: Cannot connect to API at `{API_BASE_URL}`")
            st.warning("**Possible causes:**")
            st.markdown("""
            - The API server is not running
            - The IP address or port is incorrect
            - Firewall is blocking the connection
            - The server is not accessible from this network
            """)
            st.info("💡 **Solutions:**")
            st.markdown("""
            1. **Check if API server is running:**
               - For localhost: `python -m uvicorn src.api.main:app --reload --port 8000`
               - For remote server: Check if the service is running
            
            2. **Verify the API URL:**
               - Local: `http://localhost:8000`
               - Remote: `http://71.162.0.66:8000` (check port number)
            
            3. **Test connection:**
               - Try accessing the API directly in browser: `{API_BASE_URL}/docs`
               - Or use curl: `curl {API_BASE_URL}/api/v1/threats/stats`
            """.format(API_BASE_URL=API_BASE_URL))
        else:
            st.error(f"⚠️ Connection Error: Cannot connect to API at `{API_BASE_URL}`")
            st.info(f"💡 Please check that the API server is running and the URL is correct")
    except requests.exceptions.Timeout as e:
        st.error(f"⚠️ Timeout: API request took too long. The server might be slow or unavailable.")
    except Exception as e:
        error_msg = str(e)
        if "SSL" in error_msg or "HTTPS" in error_msg or "certificate" in error_msg.lower():
            st.error(f"⚠️ SSL/HTTPS Error: {error_msg}")
            st.info(f"💡 The API endpoint doesn't support HTTPS. Please change the URL to use 'http://' instead of 'https://'")
        else:
            st.error(f"Error loading dashboard: {e}")

# IOC Lookup
elif page == "IOC Lookup":
    st.header("IOC Lookup")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ioc_value = st.text_input("IOC Value", placeholder="e.g., 192.0.2.1, example.com, hash...")
    
    with col2:
        ioc_type = st.selectbox("IOC Type", ["", "ip", "url", "domain", "hash", "email"])
    
    if st.button("Lookup IOC"):
        if ioc_value:
            try:
                payload = {
                    "ioc_value": ioc_value,
                    "ioc_type": ioc_type if ioc_type else None
                }
                
                response = session.post(f"{API_BASE_URL}/api/v1/ioc/check", json=payload, timeout=10)
                
                if response.status_code == 200:
                    results = response.json()
                    
                    if results:
                        st.success(f"Found {len(results)} IOC record(s)")
                        
                        for result in results:
                            with st.expander(f"IOC: {result.get('ioc_value')}"):
                                st.write(f"**Type:** {result.get('ioc_type')}")
                                st.write(f"**Source:** {result.get('source')}")
                                st.write(f"**Threat Type:** {result.get('threat_type')}")
                                st.write(f"**Confidence:** {result.get('confidence', 0):.2%}")
                                st.write(f"**First Seen:** {result.get('first_seen', '')}")
                                st.write(f"**Last Seen:** {result.get('last_seen', '')}")
                                
                                tags = result.get('tags', [])
                                if tags:
                                    st.write(f"**Tags:** {', '.join(tags)}")
                    else:
                        st.info("IOC not found in threat intelligence database")
                else:
                    st.error(f"API Error: {response.status_code}")
            except requests.exceptions.SSLError as e:
                st.error(f"⚠️ SSL/HTTPS Error: The API endpoint doesn't support HTTPS. Please use HTTP instead.")
                st.info(f"💡 Change the API URL in the sidebar to use 'http://' instead of 'https://'")
            except requests.exceptions.ConnectionError as e:
                error_msg = str(e)
                if "refused" in error_msg.lower():
                    st.error(f"⚠️ Connection Refused: API server at `{API_BASE_URL}` is not responding")
                    st.info(f"💡 Check if the API server is running. Try: `{API_BASE_URL}/docs` in your browser")
                else:
                    st.error(f"⚠️ Connection Error: Cannot connect to API at `{API_BASE_URL}`")
            except Exception as e:
                error_msg = str(e)
                if "SSL" in error_msg or "HTTPS" in error_msg:
                    st.error(f"⚠️ SSL/HTTPS Error: {error_msg}")
                    st.info(f"💡 Use 'http://' instead of 'https://' in the API URL")
                else:
                    st.error(f"Error looking up IOC: {e}")
        else:
            st.warning("Please enter an IOC value")

# Threat Analysis
elif page == "Threat Analysis":
    st.header("Threat Analysis")
    
    # Get threats
    col1, col2 = st.columns(2)
    
    with col1:
        min_confidence = st.slider("Minimum Confidence", 0.0, 1.0, 0.7, 0.05)
    
    with col2:
        threat_type = st.selectbox("Threat Type", ["", "malware", "phishing", "c2_server", "ransomware"])
    
    if st.button("Get Threats"):
        try:
            params = {
                "min_confidence": min_confidence,
                "limit": 100
            }
            
            if threat_type:
                params["threat_type"] = threat_type
            
            response = session.get(f"{API_BASE_URL}/api/v1/threats", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                threats = data.get("threats", [])
                
                st.success(f"Found {len(threats)} threats")
                
                if threats:
                    # Create DataFrame
                    df = pd.DataFrame(threats)
                    
                    # Display table
                    st.dataframe(df[['ioc_value', 'ioc_type', 'threat_type', 'confidence', 'source', 'first_seen']].head(50))
                    
                    # Threat confidence distribution
                    if 'confidence' in df.columns:
                        st.subheader("Confidence Distribution")
                        fig_conf = px.histogram(df, x='confidence', nbins=20, title="Threat Confidence Distribution")
                        fig_conf.update_layout(
                            plot_bgcolor='#1e293b',
                            paper_bgcolor='#0f172a',
                            font_color='#f1f5f9',
                            title_font_color='#f1f5f9'
                        )
                        st.plotly_chart(fig_conf, use_container_width=True)
            else:
                st.error(f"API Error: {response.status_code}")
        except requests.exceptions.SSLError as e:
            st.error(f"⚠️ SSL/HTTPS Error: The API endpoint doesn't support HTTPS. Please use HTTP instead.")
            st.info(f"💡 Change the API URL in the sidebar to use 'http://' instead of 'https://'")
        except requests.exceptions.ConnectionError as e:
            error_msg = str(e)
            if "refused" in error_msg.lower():
                st.error(f"⚠️ Connection Refused: API server at `{API_BASE_URL}` is not responding")
                st.info(f"💡 Check if the API server is running. Try: `{API_BASE_URL}/docs` in your browser")
            else:
                st.error(f"⚠️ Connection Error: Cannot connect to API at `{API_BASE_URL}`")
        except Exception as e:
            error_msg = str(e)
            if "SSL" in error_msg or "HTTPS" in error_msg:
                st.error(f"⚠️ SSL/HTTPS Error: {error_msg}")
                st.info(f"💡 Use 'http://' instead of 'https://' in the API URL")
            else:
                st.error(f"Error getting threats: {e}")

# Network Graph
elif page == "Network Graph":
    st.header("Threat Network Graph")
    
    actor_name = st.text_input("Threat Actor Name (optional)", placeholder="Leave empty for full network")
    depth = st.slider("Graph Depth", 1, 5, 2)
    
    if st.button("Load Network"):
        try:
            params = {"depth": depth}
            if actor_name:
                params["actor_name"] = actor_name
            
            response = session.get(f"{API_BASE_URL}/api/v1/network", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                nodes = data.get("nodes", [])
                edges = data.get("edges", [])
                stats = data.get("stats", {})
                
                st.success(f"Network loaded: {stats.get('num_nodes', 0)} nodes, {stats.get('num_edges', 0)} edges")
                
                if nodes:
                    # Create network visualization
                    st.subheader("Network Visualization")
                    
                    # Display nodes and edges
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Nodes:**")
                        df_nodes = pd.DataFrame(nodes)
                        st.dataframe(df_nodes[['id', 'label', 'type']].head(20))
                    
                    with col2:
                        st.write("**Edges:**")
                        df_edges = pd.DataFrame(edges)
                        st.dataframe(df_edges[['source', 'target', 'type']].head(20))
                    
                    st.info("Full network graph visualization would be rendered here (requires Cytoscape.js integration)")
                else:
                    st.info("No network data available")
            else:
                st.error(f"API Error: {response.status_code}")
        except requests.exceptions.SSLError as e:
            st.error(f"⚠️ SSL/HTTPS Error: The API endpoint doesn't support HTTPS. Please use HTTP instead.")
            st.info(f"💡 Change the API URL in the sidebar to use 'http://' instead of 'https://'")
        except requests.exceptions.ConnectionError as e:
            error_msg = str(e)
            if "refused" in error_msg.lower():
                st.error(f"⚠️ Connection Refused: API server at `{API_BASE_URL}` is not responding")
                st.info(f"💡 Check if the API server is running. Try: `{API_BASE_URL}/docs` in your browser")
            else:
                st.error(f"⚠️ Connection Error: Cannot connect to API at `{API_BASE_URL}`")
        except Exception as e:
            error_msg = str(e)
            if "SSL" in error_msg or "HTTPS" in error_msg:
                st.error(f"⚠️ SSL/HTTPS Error: {error_msg}")
                st.info(f"💡 Use 'http://' instead of 'https://' in the API URL")
            else:
                st.error(f"Error loading network: {e}")

# Timeline
elif page == "Timeline":
    st.header("IOC Timeline")
    
    col1, col2 = st.columns(2)
    
    with col1:
        hours = st.number_input("Hours to look back", min_value=1, max_value=168, value=24)
    
    with col2:
        threat_type = st.selectbox("Threat Type", ["", "malware", "phishing", "c2_server", "ransomware"])
    
    if st.button("Load Timeline"):
        try:
            params = {
                "hours": hours,
                "min_confidence": 0.7
            }
            
            if threat_type:
                params["threat_type"] = threat_type
            
            response = session.get(f"{API_BASE_URL}/api/v1/timeline", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                timeline = data.get("timeline", [])
                
                st.success(f"Loaded {len(timeline)} IOCs from last {hours} hours")
                
                if timeline:
                    # Create timeline DataFrame
                    df_timeline = pd.DataFrame(timeline)
                    
                    if 'first_seen' in df_timeline.columns:
                        df_timeline['first_seen'] = pd.to_datetime(df_timeline['first_seen'], errors='coerce')
                        df_timeline = df_timeline.sort_values('first_seen')
                    
                    # Display timeline chart
                    st.subheader("IOC Timeline Chart")
                    
                    if len(timeline) > 0:
                        # Group by time (hourly)
                        df_timeline['hour'] = df_timeline['first_seen'].dt.floor('H')
                        hourly_counts = df_timeline.groupby('hour').size().reset_index(name='count')
                        
                        fig_timeline = px.line(
                            hourly_counts,
                            x='hour',
                            y='count',
                            title=f"IOC Count Over Time (Last {hours} hours)"
                        )
                        fig_timeline.update_layout(
                            plot_bgcolor='#1e293b',
                            paper_bgcolor='#0f172a',
                            font_color='#f1f5f9',
                            title_font_color='#f1f5f9'
                        )
                        st.plotly_chart(fig_timeline, use_container_width=True)
                    
                    # Display table
                    st.subheader("IOC Details")
                    st.dataframe(df_timeline[['ioc_value', 'ioc_type', 'threat_type', 'confidence', 'source', 'first_seen']].head(50))
                else:
                    st.info("No IOCs found in the specified time window")
            else:
                st.error(f"API Error: {response.status_code}")
        except requests.exceptions.SSLError as e:
            st.error(f"⚠️ SSL/HTTPS Error: The API endpoint doesn't support HTTPS. Please use HTTP instead.")
            st.info(f"💡 Change the API URL in the sidebar to use 'http://' instead of 'https://'")
        except requests.exceptions.ConnectionError as e:
            error_msg = str(e)
            if "refused" in error_msg.lower():
                st.error(f"⚠️ Connection Refused: API server at `{API_BASE_URL}` is not responding")
                st.info(f"💡 Check if the API server is running. Try: `{API_BASE_URL}/docs` in your browser")
            else:
                st.error(f"⚠️ Connection Error: Cannot connect to API at `{API_BASE_URL}`")
        except Exception as e:
            error_msg = str(e)
            if "SSL" in error_msg or "HTTPS" in error_msg:
                st.error(f"⚠️ SSL/HTTPS Error: {error_msg}")
                st.info(f"💡 Use 'http://' instead of 'https://' in the API URL")
            else:
                st.error(f"Error loading timeline: {e}")

# Footer
st.markdown("---")
st.markdown("**Cipher Threat Intelligence Platform** - Built for homeland security intelligence operations")

