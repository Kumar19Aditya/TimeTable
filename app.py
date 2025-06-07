import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="45-Day Study Timetable",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 2rem;
    }
    
    .summary-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .summary-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        min-width: 200px;
        flex: 1;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .summary-card h3 {
        margin: 0 0 10px 0;
        font-size: 1.2rem;
    }
    
    .summary-card p {
        margin: 5px 0;
        font-size: 0.9rem;
    }
    
    .legend-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 5px;
        background: #f8f9fa;
    }
    
    .legend-color {
        width: 20px;
        height: 20px;
        border-radius: 4px;
    }
    
    .api-color { background-color: blue; border-left: 4px solid #0000ff; }
    .stats-color { background-color: black; border-left: 4px solid #000000; }
    .llm-color { background-color: red; border-left: 4px solid #ff0000; }
    
    .week-header {
        background-color: #2c3e50;
        color: white;
        text-align: center;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .rest-day {
        background-color: #f8f9fa;
        color: #6c757d;
        font-style: italic;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
    }
    
    .progress-section {
        margin: 2rem 0;
    }
    
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .stDataFrame {
        width: 100% !important;
        overflow: visible !important;
    }
    
    .notes-section textarea {
        width: 100%;
        min-height: 100px;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 8px;
    }
    
    /* Ensure text color is black for Morning and Evening Session columns by default */
    [data-testid="stDataFrame"] tbody tr td:nth-child(4),
    [data-testid="stDataFrame"] tbody tr td:nth-child(5) {
        color: black !important;
    }
    
    /* Override text color for API sessions to red */
    [data-testid="stDataFrame"] tbody tr td.api-session {
        color: red !important;
    }
    
    /* Override text color for week headers */
    [data-testid="stDataFrame"] tbody tr:has(td.week-header) td {
        color: white !important;
    }
    
    /* Override text color for rest days */
    [data-testid="stDataFrame"] tbody tr:has(td.rest-day) td {
        color: #6c757d !important;
    }
    
    /* Ensure text is readable on dark backgrounds */
    [data-testid="stDataFrame"] tbody tr td.stats-session {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# File to store persistent data
DATA_FILE = "timetable_data.json"

# Load saved data from JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"checkbox_states": {}, "notes": {}}

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize persistent data
persistent_data = load_data()

# Initialize session state with loaded data
if 'checkbox_states' not in st.session_state:
    st.session_state.checkbox_states = persistent_data.get("checkbox_states", {})
if 'notes' not in st.session_state:
    st.session_state.notes = persistent_data.get("notes", {})

# App title
st.markdown('<div class="main-header"><h1>📚 45-Day Study Timetable</h1><p>API | Statistics | LLM</p></div>', unsafe_allow_html=True)

# Create schedule data with generic session names
schedule_data = []

# Session counters for each subject
api_session = 1
stats_session = 1
llm_session = 1

# Week 1
schedule_data.extend([
    {"Week": "WEEK 1", "Day": "", "Date": "", "Morning Session": "", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Day 1 (Monday)", "Date": "Jun 9", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 2 (Tuesday)", "Date": "Jun 10", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 3 (Wednesday)", "Date": "Jun 11", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 4 (Thursday)", "Date": "Jun 12", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 5 (Friday)", "Date": "Jun 13", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Saturday", "Date": "Jun 14", "Morning Session": "REST DAY", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 6 (Sunday)", "Date": "Jun 15", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

# Week 2
schedule_data.extend([
    {"Week": "WEEK 2", "Day": "", "Date": "", "Morning Session": "", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Day 7 (Monday)", "Date": "Jun 16", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 8 (Tuesday)", "Date": "Jun 17", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 9 (Wednesday)", "Date": "Jun 18", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 10 (Thursday)", "Date": "Jun 19", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 11 (Friday)", "Date": "Jun 20", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Saturday", "Date": "Jun 21", "Morning Session": "REST DAY", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 12 (Sunday)", "Date": "Jun 22", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

# Week 3
schedule_data.extend([
    {"Week": "WEEK 3", "Day": "", "Date": "", "Morning Session": "", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Day 13 (Monday)", "Date": "Jun 23", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 14 (Tuesday)", "Date": "Jun 24", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 15 (Wednesday)", "Date": "Jun 25", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 16 (Thursday)", "Date": "Jun 26", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 17 (Friday)", "Date": "Jun 27", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Saturday", "Date": "Jun 28", "Morning Session": "REST DAY", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 18 (Sunday)", "Date": "Jun 29", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

# Week 4
schedule_data.extend([
    {"Week": "WEEK 4", "Day": "", "Date": "", "Morning Session": "", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Day 19 (Monday)", "Date": "Jun 30", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 20 (Tuesday)", "Date": "Jul 1", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 21 (Wednesday)", "Date": "Jul 2", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 22 (Thursday)", "Date": "Jul 3", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 23 (Friday)", "Date": "Jul 4", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Saturday", "Date": "Jul 5", "Morning Session": "REST DAY", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 24 (Sunday)", "Date": "Jul 6", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

# Week 5
schedule_data.extend([
    {"Week": "WEEK 5", "Day": "", "Date": "", "Morning Session": "", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Day 25 (Monday)", "Date": "Jul 7", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 26 (Tuesday)", "Date": "Jul 8", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 27 (Wednesday)", "Date": "Jul 9", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 28 (Thursday)", "Date": "Jul 10", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 29 (Friday)", "Date": "Jul 11", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Saturday", "Date": "Jul 12", "Morning Session": "REST DAY", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 30 (Sunday)", "Date": "Jul 13", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

# Final Days
schedule_data.extend([
    {"Week": "FINAL DAYS", "Day": "", "Date": "", "Morning Session": "", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Day 40 (Thursday)", "Date": "Jul 24", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 41 (Friday)", "Date": "Jul 25", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
    {"Week": "", "Day": "Saturday", "Date": "Jul 26", "Morning Session": "REST DAY", "Evening Session": "", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 42 (Sunday)", "Date": "Jul 27", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 43 (Monday)", "Date": "Jul 28", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"📊 Statistics: Session {stats_session} (50 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

api_session += 1
stats_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 44 (Tuesday)", "Date": "Jul 29", "Morning Session": f"📊 Statistics: Session {stats_session} (50 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

stats_session += 1
llm_session += 1

schedule_data.extend([
    {"Week": "", "Day": "Day 45 (Wednesday)", "Date": "Jul 30", "Morning Session": f"🔧 API: Session {api_session} (45 min)", "Evening Session": f"🤖 LLM: Session {llm_session} (75 min)", "Morning Completed": "", "Evening Completed": "", "Notes": ""},
])

# Create DataFrame
df = pd.DataFrame(schedule_data)

# Calculate progress based on completed sessions
total_days = 45
api_sessions_completed = 0
stats_sessions_completed = 0
llm_sessions_completed = 0
total_sessions_completed = 0
total_sessions = 0  # Total number of sessions (Morning + Evening, excluding rest days)

# Count sessions and completions
for idx, row in df.iterrows():
    if 'REST DAY' in str(row['Morning Session']) or (not row['Morning Session'] and not row['Evening Session']):
        continue
    
    morning_key = f"morning_{idx}"
    evening_key = f"evening_{idx}"
    
    # Count total sessions
    if '🔧 API' in str(row['Morning Session']):
        total_sessions += 1
    elif '📊 Statistics' in str(row['Morning Session']):
        total_sessions += 1
    elif '🤖 LLM' in str(row['Morning Session']):
        total_sessions += 1
        
    if '🔧 API' in str(row['Evening Session']):
        total_sessions += 1
    elif '📊 Statistics' in str(row['Evening Session']):
        total_sessions += 1
    elif '🤖 LLM' in str(row['Evening Session']):
        total_sessions += 1
    
    # Count completed sessions
    if st.session_state.checkbox_states.get(morning_key, False):
        total_sessions_completed += 1
        if '🔧 API' in str(row['Morning Session']):
            api_sessions_completed += 1
        elif '📊 Statistics' in str(row['Morning Session']):
            stats_sessions_completed += 1
        elif '🤖 LLM' in str(row['Morning Session']):
            llm_sessions_completed += 1
    
    if st.session_state.checkbox_states.get(evening_key, False):
        total_sessions_completed += 1
        if '🔧 API' in str(row['Evening Session']):
            api_sessions_completed += 1
        elif '📊 Statistics' in str(row['Evening Session']):
            stats_sessions_completed += 1
        elif '🤖 LLM' in str(row['Evening Session']):
            llm_sessions_completed += 1

# Total sessions per subject (as per the summary cards)
total_api_sessions = 25
total_stats_sessions = 25
total_llm_sessions = 25

# Calculate progress percentages
api_progress = (api_sessions_completed / total_api_sessions) * 100
stats_progress = (stats_sessions_completed / total_stats_sessions) * 100
llm_progress = (llm_sessions_completed / total_llm_sessions) * 100
overall_progress = (total_sessions_completed / total_sessions) * 100 if total_sessions > 0 else 0

# Summary cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="summary-card">
        <h3>🔧 API</h3>
        <p><strong>19.0 Hours</strong></p>
        <p>25 Sessions × 45-50 min</p>
        <p>Progress: {api_progress:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    st.progress(api_progress / 100)

with col2:
    st.markdown(f"""
    <div class="summary-card">
        <h3>📊 Statistics</h3>
        <p><strong>~20 Hours</strong></p>
        <p>25 Sessions × 45-50 min</p>
        <p>Progress: {stats_progress:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    st.progress(stats_progress / 100)

with col3:
    st.markdown(f"""
    <div class="summary-card">
        <h3>🤖 LLM</h3>
        <p><strong>29.8 Hours</strong></p>
        <p>25 Sessions × 70-75 min</p>
        <p>Progress: {llm_progress:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    st.progress(llm_progress / 100)

# Legend
st.markdown("""
<div class="legend-container">
    <div class="legend-item">
        <div class="legend-color api-color"></div>
        <span>API</span>
    </div>
    <div class="legend-item">
        <div class="legend-color stats-color"></div>
        <span>Statistics</span>
    </div>
    <div class="legend-item">
        <div class="legend-color llm-color"></div>
        <span>LLM</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Display schedule
st.markdown("## 📅 Complete 45-Day Schedule")

# Custom styling for the dataframe
def style_dataframe(df):
    def apply_styles(row):
        styles = [''] * len(row)
        
        # Week headers
        if row['Week'] and not row['Day']:
            styles = ['background-color: #2c3e50; color: white; font-weight: bold; text-align: center'] * len(row)
            styles[0] += '; --cell-class: week-header'
        
        # Rest days
        elif 'REST DAY' in str(row['Morning Session']):
            styles = ['background-color: #f8f9fa; color: #6c757d; font-style: italic'] * len(row)
            styles[0] += '; --cell-class: rest-day'
        
        # Subject-based coloring for Morning Session
        elif '🔧 API' in str(row['Morning Session']):
            styles[3] = 'background-color: blue; border-left: 4px solid #0000ff; --cell-class: api-session'
        elif '📊 Statistics' in str(row['Morning Session']):
            styles[3] = 'background-color: black; border-left: 4px solid #000000; --cell-class: stats-session'
        elif '🤖 LLM' in str(row['Morning Session']):
            styles[3] = 'background-color: red; border-left: 4px solid #ff0000; --cell-class: llm-session'
            
        # Subject-based coloring for Evening Session
        if '🔧 API' in str(row['Evening Session']):
            styles[4] = 'background-color: blue; border-left: 4px solid #0000ff; --cell-class: api-session'
        elif '📊 Statistics' in str(row['Evening Session']):
            styles[4] = 'background-color: black; border-left: 4px solid #000000; --cell-class: stats-session'
        elif '🤖 LLM' in str(row['Evening Session']):
            styles[4] = 'background-color: red; border-left: 4px solid #ff0000; --cell-class: llm-session'
            
        return styles
    
    # Add checkboxes and notes for each row
    for idx, row in df.iterrows():
        if 'REST DAY' in str(row['Morning Session']) or (not row['Morning Session'] and not row['Evening Session']):
            df.at[idx, 'Morning Completed'] = ''
            df.at[idx, 'Evening Completed'] = ''
            df.at[idx, 'Notes'] = ''
        else:
            # Unique keys for checkboxes and notes
            morning_key = f"morning_{idx}"
            evening_key = f"evening_{idx}"
            notes_key = f"notes_{idx}"
            
            # Initialize checkbox states if not already set
            if morning_key not in st.session_state.checkbox_states:
                st.session_state.checkbox_states[morning_key] = False
            if evening_key not in st.session_state.checkbox_states:
                st.session_state.checkbox_states[evening_key] = False
            if notes_key not in st.session_state.notes:
                st.session_state.notes[notes_key] = ""
            
            # Add checkbox states to DataFrame
            df.at[idx, 'Morning Completed'] = '✅' if st.session_state.checkbox_states[morning_key] else '⬜'
            df.at[idx, 'Evening Completed'] = '✅' if st.session_state.checkbox_states[evening_key] else '⬜'
            df.at[idx, 'Notes'] = st.session_state.notes[notes_key]
            
    return df.style.apply(apply_styles, axis=1)

# Function to display the table and checkboxes/notes
def display_schedule_with_checkboxes():
    styled_df = style_dataframe(df.copy())
    st.dataframe(styled_df, use_container_width=True, height=len(df) * 35 + 100)  # Full view mode
    
    # Add checkboxes and notes below the table
    st.markdown("## 📋 Daily Progress and Notes")
    for idx, row in df.iterrows():
        if 'REST DAY' in str(row['Morning Session']) or (not row['Morning Session'] and not row['Evening Session']):
            continue
        
        st.markdown(f"### {row['Day']} - {row['Date']}")
        col1, col2 = st.columns([1, 3])
        
        with col1:
            morning_key = f"morning_{idx}"
            evening_key = f"evening_{idx}"
            
            morning_checked = st.checkbox(
                f"Morning: {row['Morning Session']}",
                value=st.session_state.checkbox_states.get(morning_key, False),
                key=morning_key
            )
            evening_checked = st.checkbox(
                f"Evening: {row['Evening Session']}",
                value=st.session_state.checkbox_states.get(evening_key, False),
                key=evening_key
            )
            
            # Update session state and save to file
            if morning_checked != st.session_state.checkbox_states.get(morning_key, False):
                st.session_state.checkbox_states[morning_key] = morning_checked
                save_data({"checkbox_states": st.session_state.checkbox_states, "notes": st.session_state.notes})
            
            if evening_checked != st.session_state.checkbox_states.get(evening_key, False):
                st.session_state.checkbox_states[evening_key] = evening_checked
                save_data({"checkbox_states": st.session_state.checkbox_states, "notes": st.session_state.notes})
        
        with col2:
            notes_key = f"notes_{idx}"
            notes = st.text_area(
                "Notes",
                value=st.session_state.notes.get(notes_key, ""),
                key=notes_key,
                placeholder="Add your notes or review here..."
            )
            
            # Update session state and save to file
            if notes != st.session_state.notes.get(notes_key, ""):
                st.session_state.notes[notes_key] = notes
                save_data({"checkbox_states": st.session_state.checkbox_states, "notes": st.session_state.notes})

# Display the schedule with checkboxes and notes
display_schedule_with_checkboxes()

# Progress tracking section
st.markdown("## 📈 Progress Tracking")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📚 Sessions Completed",
        value=f"{total_sessions_completed}/{total_sessions}",
        delta=f"{overall_progress:.1f}% Complete"
    )

with col2:
    st.metric(
        label="🎯 API Sessions",
        value=f"{api_sessions_completed}/{total_api_sessions}",
        delta=f"{api_progress:.1f}% Complete"
    )

with col3:
    st.metric(
        label="📊 Statistics Sessions", 
        value=f"{stats_sessions_completed}/{total_stats_sessions}",
        delta=f"{stats_progress:.1f}% Complete"
    )

# Progress visualization
fig = go.Figure()

subjects = ['API', 'Statistics', 'LLM']
progress_values = [api_progress, stats_progress, llm_progress]
colors = ['#27ae60', '#ffc107', '#007bff']

fig.add_trace(go.Bar(
    x=subjects,
    y=progress_values,
    marker_color=colors,
    text=[f'{val:.1f}%' for val in progress_values],
    textposition='auto',
))

fig.update_layout(
    title='📊 Subject Progress Overview',
    yaxis_title='Progress (%)',
    showlegend=False,
    height=400,
    yaxis=dict(range=[0, 100])
)

st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem;'>
    <p>📚 Stay consistent, track your progress, and achieve your learning goals!</p>
    <p><em>Remember: Rest days are important for knowledge consolidation.</em></p>
</div>
""", unsafe_allow_html=True)