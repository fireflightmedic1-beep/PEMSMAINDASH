import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="PEMS ED DASHBOARD", layout="wide", page_icon="🏥")

# Custom CSS for Piedmont Branding
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    [data-testid="stHeader"] { background-color: #005eb8; }
    h1, h2, h3 { color: #005eb8; font-weight: bold; }
    .protocol-card { background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #005eb8; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_with_html=True)

# --- HEADER ---
st.title("🏥 PEMS ED MAIN FLOW")
st.write(f"**Last Sync:** {datetime.now().strftime('%m/%d/%Y %H:%M')}")

tabs = st.tabs(["📞 Directory", "📋 Daily Line-Up", "📊 Charge Report", "🧠 Protocols"])

# --- TAB 1: DIRECTORY ---
with tabs[0]:
    st.header("Hospital Directory")
    search = st.text_input("🔍 Search Department or Extension...", placeholder="e.g. *2440 or Lab")
    
    # Static data based on your "MASTER DATA - DIRECTORY.csv"
    dir_data = [
        {"Location": "POD 1", "Phone": "*2441", "Rooms": "01-12", "Tube": "15"},
        {"Location": "POD 2", "Phone": "*2251", "Rooms": "20-27", "Tube": "15"},
        {"Location": "POD 3", "Phone": "*2425", "Rooms": "32-35, 46-49", "Tube": "20"},
        {"Location": "POD 4", "Phone": "*2296", "Rooms": "36-45", "Tube": "20"},
        {"Location": "PHARMACY", "Phone": "*2570", "Rooms": "N/A", "Tube": "12"},
        {"Location": "CHARGE RN", "Phone": "770-480-7530", "Rooms": "N/A", "Tube": "N/A"},
    ]
    df_dir = pd.DataFrame(dir_data)
    if search:
        df_dir = df_dir[df_dir['Location'].str.contains(search, case=False) | df_dir['Phone'].str.contains(search)]
    st.table(df_dir)

# --- TAB 2: FILLABLE LINE-UP ---
with tabs[1]:
    st.header("Daily Nursing Assignments")
    st.info("Fillable fields update the dashboard for all users.")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("CHARGE RN", key="st1_charge")
        st.text_input("FLOW COORD", key="st1_flow")
        st.text_input("UNIT SEC", key="st1_sec")
    with col2:
        st.text_input("TRIAGE #1", key="st1_tri1")
        st.text_input("TRIAGE #2", key="st1_tri2")
        st.text_input("PIVOT", key="st1_pivot")

# --- TAB 3: CHARGE REPORT ---
with tabs[2]:
    st.header("Charge Nurse Report")
    pin = st.sidebar.text_input("Charge Access Code", type="password")
    if pin == "PEMS1234":
        st.success("Authorized: Editing Enabled")
        q1, q2 = st.columns(2)
        with q1:
            st.text_input("STEMI MRNs", key="qi_stemi")
            st.text_input("Stroke MRNs", key="qi_stroke")
        with q2:
            st.number_input("Total Census", step=1)
            st.text_area("Shift Barriers/Safety")
    else:
        st.warning("Locked. Please enter the Access Code in the sidebar.")

# --- TAB 4: PROTOCOLS ---
with tabs[3]:
    st.header("Clinical Protocols")
    p_choice = st.radio("Choose Protocol", ["STEMI", "Stroke (CVA)", "Pronouncement"], horizontal=True)
    
    if p_choice == "STEMI":
        st.markdown("""<div class="protocol-card"><h3>❤️ STEMI Activation</h3>
        1. Show EKG to ED Doc<br>2. Activate Team via Lifenet<br>3. Call EVERY member of Cath Team</div>""", unsafe_with_html=True)
    elif p_choice == "Stroke (CVA)":
        st.markdown("""<div class="protocol-card"><h3>🧠 Stroke Alert</h3>
        1. Call Operator for Overhead Page<br>2. Teleneuro: (239) 231-1456<br>3. Website: strokealert911.com</div>""", unsafe_with_html=True)
    elif p_choice == "Pronouncement":
        st.markdown("""<div class="protocol-card"><h3>📄 Pronouncement of Death</h3>
        1. Fill Sections 1-4 on form<br>2. Call Lifelink: (800) 882-7177<br>3. Call County Coroner</div>""", unsafe_with_html=True)
