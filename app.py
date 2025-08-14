import streamlit as st
import google.generativeai as genai
import os
import time
import base64
import pandas as pd
import altair as alt
from PIL import Image
from collections import deque
import random

# --- 1. PAGE CONFIGURATION & STYLING ---

st.set_page_config(
    page_title="AquaSentry Command Center",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to set the background image and custom CSS
def set_page_background_and_style():
    # Use a direct URL for the background image to reduce deployment size
    image_url = "https://a-z-animals.com/media/2022/01/shutterstock_1952629435-1024x650.jpg"
    
    # Custom CSS for styling the app
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{image_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main-content-wrapper {{
        background-color: rgba(10, 25, 40, 0.85); /* Dark blue overlay for content */
        color: #e0e0e0;
        padding: 2rem;
        border-radius: 10px;
    }}
    .st-emotion-cache-16txtl3 {{
        padding-top: 2rem; /* Adjust top padding */
    }}
    .st-emotion-cache-z5fcl4 {{
        background-color: rgba(10, 25, 40, 0.9); /* Sidebar background */
    }}
    .dashboard-card {{
        background: linear-gradient(145deg, rgba(20, 40, 60, 0.8), rgba(30, 50, 70, 0.8));
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5); /* Enhanced shadow for pop-up effect */
        border: 1px solid rgba(100, 150, 200, 0.3);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; /* Smooth transition for hover */
    }}
    .dashboard-card:hover {{
        transform: translateY(-5px); /* Lifts the card on hover */
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6); /* Increase shadow on hover */
    }}
    .metric-label {{
        color: #90caf9;
        font-size: 1rem;
        font-weight: 500;
    }}
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
    }}
    .stButton>button {{
        background-color: #0077c2;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }}
    .stButton>button:hover {{
        background-color: #005fa1;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Gemini AI CONFIGURATION ---

try:
    # This will read the environment variable from Vercel's settings
    api_key = os.getenv("GOOGLE_API_KEY") 
    if not api_key:
        # Fallback to Streamlit secrets for local development
        api_key = st.secrets.get("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found. Please set it in your Vercel project settings or local Streamlit secrets.")
        
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Error configuring AI model: {e}", icon="🚨")
    st.stop()

# --- 3. SESSION STATE INITIALIZATION ---

if "page" not in st.session_state:
    st.session_state.page = "Overview"
if "data_points" not in st.session_state:
    st.session_state.data_points = deque(maxlen=60) # Store last 60 data points
    # Pre-populate with some initial data for a better first view
    for i in range(60):
        st.session_state.data_points.append({
            "time": pd.to_datetime(time.time() - (60 - i) * 5, unit='s'),
            "depth": 50 + random.uniform(-10, 10),
            "temperature": 12 + random.uniform(-2, 2)
        })
if "mission_progress" not in st.session_state:
    st.session_state.mission_progress = 45.0
if "battery" not in st.session_state:
    st.session_state.battery = 82.0

# --- 4. AI ANALYSIS FUNCTIONS ---

def analyze_image(uploaded_image):
    prompt = """
    You are a marine biologist and expert taxonomist. Analyze the provided image of a marine creature.
    Your task is to:
    1. Identify the creature with its common and scientific name.
    2. Provide a detailed description covering "Appearance & Habitat" and "Scientific Classification".
    3. Create a "Summary Table" with the key features.
    Format your entire response using Markdown. Use headings, bullet points, and tables exactly like this example:
    ### Identification & Common Name
    * The common name for *Acanthaluteres brownii* is indeed Spiny-tailed Leatherjacket.
    ### Appearance & Habitat
    * Males typically sport a green to yellowish-green body...
    ### Scientific Classification
    * Belonging to the family Monacanthidae...
    ### Summary Table
    | Feature            | Details                               |
    |--------------------|---------------------------------------|
    | Scientific Name    | *Acanthaluteres brownii* |
    | Common Name        | Spiny-tailed Leatherjacket            |
    | Distinctive Traits | Males: greenish body; Females: muted  |
    | Habitat            | Southern Australia; reefs & seagrass  |
    """
    image_object = Image.open(uploaded_image)
    response = gemini_model.generate_content([prompt, image_object])
    return response.text

def analyze_audio(uploaded_audio):
    prompt = """
    You are an expert bioacoustics analyst and sonar operator.
    Listen to the provided audio file and identify the most likely source of the sound.
    Is it a marine creature (like a specific whale or dolphin), a man-made object (like a ship engine, submarine sonar, or propeller), or something else?
    Provide a brief, confident analysis.
    """
    with open(uploaded_audio.name, "wb") as f:
        f.write(uploaded_audio.getbuffer())
    audio_file = genai.upload_file(path=uploaded_audio.name)
    response = gemini_model.generate_content([prompt, audio_file])
    os.remove(uploaded_audio.name) # Clean up
    return response.text

# --- 5. UI: SIDEBAR NAVIGATION ---

with st.sidebar:
    st.title("🌊 AquaSentry")
    st.markdown("---")
    if st.button("Overview", use_container_width=True):
        st.session_state.page = "Overview"
        st.rerun()
    if st.button("Live Feed & Control", use_container_width=True):
        st.session_state.page = "Control"
        st.rerun()
    if st.button("AI Analysis", use_container_width=True):
        st.session_state.page = "AI"
        st.rerun()
    st.markdown("---")
    st.info("Status: All Systems Nominal")
    st.progress(st.session_state.battery / 100, text=f"Battery: {st.session_state.battery:.1f}%")


# --- 6. MAIN APP LOGIC & PAGE RENDERING ---

set_page_background_and_style()

# Wrap main content for better styling with background
with st.container():
    st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)

    st.title("AquaSentry Command Center")

    # --- OVERVIEW PAGE ---
    if st.session_state.page == "Overview":
        st.html("<meta http-equiv='refresh' content='5'>")
        
        st.header("Mission Overview")
        
        last_depth = st.session_state.data_points[-1]['depth']
        last_temp = st.session_state.data_points[-1]['temperature']
        
        new_depth = last_depth + random.uniform(-0.5, 0.5)
        new_temp = last_temp + random.uniform(-0.1, 0.1)
        st.session_state.battery = max(0, st.session_state.battery - 0.02)
        st.session_state.mission_progress = min(100, st.session_state.mission_progress + 0.05)
        
        st.session_state.data_points.append({
            "time": pd.to_datetime(time.time(), unit='s'),
            "depth": new_depth,
            "temperature": new_temp
        })

        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.markdown(f"""
            <div class="dashboard-card">
                <span class="metric-label">CURRENT DEPTH</span><br>
                <span class="metric-value">{new_depth:.1f}m</span>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[1]:
            st.markdown(f"""
            <div class="dashboard-card">
                <span class="metric-label">WATER TEMPERATURE</span><br>
                <span class="metric-value">{new_temp:.1f}°C</span>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[2]:
             st.markdown(f"""
            <div class="dashboard-card">
                <span class="metric-label">BATTERY LEVEL</span><br>
                <span class="metric-value">{st.session_state.battery:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
        with metric_cols[3]:
             st.markdown(f"""
            <div class="dashboard-card">
                <span class="metric-label">MISSION PROGRESS</span><br>
                <span class="metric-value">{st.session_state.mission_progress:.0f}%</span>
            </div>
            """, unsafe_allow_html=True)

        df = pd.DataFrame(list(st.session_state.data_points))
        base = alt.Chart(df).encode(x=alt.X('time:T', title='Time', axis=alt.Axis(format='%H:%M:%S')))
        depth_line = base.mark_line(color='#42a5f5', strokeWidth=3).encode(
            y=alt.Y('depth:Q', title='Depth (m)', scale=alt.Scale(domain=(df['depth'].min()-10, df['depth'].max()+10)))
        )
        temp_line = base.mark_line(color='#ff7043', strokeWidth=3).encode(
            y=alt.Y('temperature:Q', title='Temp (°C)', scale=alt.Scale(domain=(df['temperature'].min()-2, df['temperature'].max()+2)))
        )
        chart = alt.layer(depth_line, temp_line).resolve_scale(y='independent').interactive()
        st.altair_chart(chart, use_container_width=True)

    # --- LIVE FEED & CONTROL PAGE ---
    elif st.session_state.page == "Control":
        st.header("Live Feed & ROV Control")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("Camera Feed")
            cam_options = ["Forward Cam", "Bottom Cam", "Rear Cam"]
            selected_cam = st.selectbox("Select Camera", cam_options)
            
            # Dynamic video selection based on the dropdown
            if selected_cam == "Forward Cam":
                st.video("https://videos.pexels.com/video-files/8065383/8065383-hd_1280_720_25fps.mp4")
            elif selected_cam == "Bottom Cam":
                st.video("https://videos.pexels.com/video-files/5914159/5914159-hd_1280_720_30fps.mp4")
            else: # Rear Cam
                st.video("https://videos.pexels.com/video-files/853801/853801-hd_1280_720_25fps.mp4")

            st.caption(f"Displaying feed from: {selected_cam}")

        with col2:
            st.subheader("Manual Controls")
            if st.button("⬆️ Forward", use_container_width=True): st.toast("Moving Forward")
            c1, c2, c3 = st.columns(3)
            if c1.button("⬅️ Left", use_container_width=True): st.toast("Turning Left")
            if c2.button("⏹️ Stop", use_container_width=True): st.toast("Stopping all movement")
            if c3.button("➡️ Right", use_container_width=True): st.toast("Turning Right")
            if st.button("⬇️ Backward", use_container_width=True): st.toast("Moving Backward")
            st.markdown("---")
            c4, c5 = st.columns(2)
            if c4.button("🔼 Ascend", use_container_width=True): st.toast("Ascending")
            if c5.button("🔽 Descend", use_container_width=True): st.toast("Descending")

    # --- AI ANALYSIS PAGE ---
    elif st.session_state.page == "AI":
        st.header("AI-Powered Marine Analysis")
        
        image_tab, sound_tab = st.tabs(["🐠 Image Recognition", "🔊 Sound Recognition"])

        with image_tab:
            st.subheader("Identify a Marine Creature")
            uploaded_image = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'], key="img_uploader")
            if uploaded_image:
                st.image(uploaded_image, caption="Uploaded Image")
                if st.button("Analyze Creature", use_container_width=True):
                    with st.spinner("AquaSentry is thinking..."):
                        analysis_result = analyze_image(uploaded_image)
                        st.markdown(analysis_result)

        with sound_tab:
            st.subheader("Identify a Marine Sound")
            uploaded_audio = st.file_uploader("Choose an audio file", type=['mp3', 'wav', 'm4a'], key="audio_uploader")
            if uploaded_audio:
                st.audio(uploaded_audio)
                if st.button("Analyze Sound", use_container_width=True):
                    with st.spinner("AquaSentry is listening..."):
                        analysis_result = analyze_audio(uploaded_audio)
                        st.success(f"**Analysis Result:** {analysis_result}")

    st.markdown('</div>', unsafe_allow_html=True)

