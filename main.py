# VoiceCanvas - AI Audio Story Generator
# Last Updated: June 2024
# Version: 2.0

import streamlit as st
import re
import tempfile
import os
import time
import pandas as pd
from pydub import AudioSegment
from openai import OpenAI

# ======================
# PAGE CONFIGURATION
# ======================
# Must be the very first Streamlit command
st.set_page_config(
    page_title="VoiceCanvas",
    page_icon="🎙️",
    layout="wide"
)

# ======================
# CUSTOM CSS
# ======================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #19A7CE;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #146C94;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #19A7CE;
        color: white;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# INITIALIZATION
# ======================
# Initialize all session state variables
if 'initialized' not in st.session_state:
    st.session_state.update({
        'parsed_data': [],
        'character_voices': {},
        'audio_files': [],
        'final_audio': None,
        'current_step': 1,
        'api_key': "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",
        'api_provider': "openai",
        'background_track': "None",
        'bg_volume': 0.3,
        'initialized': True
    })

# Configure FFmpeg paths
AudioSegment.converter = "ffmpeg"
AudioSegment.ffprobe = "ffprobe"

# ======================
# CONSTANTS
# ======================
OPENAI_VOICES = {
    "Alloy (Neutral)": "alloy",
    "Echo (Male)": "echo",
    "Fable (Male)": "fable",
    "Onyx (Male)": "onyx",
    "Nova (Female)": "nova",
    "Shimmer (Female)": "shimmer"
}

BACKGROUND_TRACKS = {
    "None": None,
    "Peaceful Nature": "nature",
    "Sci-Fi Ambience": "scifi",
    "Suspenseful Mystery": "suspense",
    "Fantasy Adventure": "fantasy"
}

# ======================
# CORE FUNCTIONS
# ======================
def parse_text(text):
    """Parse script text into structured dialogue"""
    lines = text.strip().split('\n')
    parsed = []
    for line in lines:
        if not line.strip():
            continue
        match = re.match(r"(.*?)(?:\s*\((.*?)\))?\s*:\s*(.*)", line)
        if match:
            parsed.append({
                "character": match.group(1).strip(),
                "emotion": match.group(2).strip() if match.group(2) else None,
                "dialogue": match.group(3).strip()
            })
        else:
            parsed.append({
                "character": "Narrator",
                "emotion": None,
                "dialogue": line.strip()
            })
    return parsed

def generate_tts(text, voice, speed=1.0):
    """Generate TTS audio using OpenAI"""
    try:
        client = OpenAI(api_key=st.session_state.api_key)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            with client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=speed
            ) as response:
                response.stream_to_file(tmp.name)
            return tmp.name
    except Exception as e:
        st.error(f"TTS Generation Error: {str(e)}")
        return None

def create_background(duration_ms, track_type):
    """Generate background audio track"""
    if not track_type or track_type == "None":
        return AudioSegment.silent(duration=duration_ms)
    
    base = AudioSegment.silent(duration=duration_ms)
    # Add simple tone patterns based on track type
    if track_type == "nature":
        for i in range(0, duration_ms, 3000):
            tone = AudioSegment.silent(duration=500).low_pass_filter(800)
            base = base.overlay(tone, position=i)
    elif track_type == "scifi":
        for i in range(0, duration_ms, 1500):
            tone = AudioSegment.silent(duration=100).high_pass_filter(2000)
            base = base.overlay(tone, position=i)
    return base

def combine_audio(audio_files, bg_track=None, bg_volume=0.3):
    """Combine dialogue clips with optional background"""
    if not audio_files:
        return None
    
    combined = AudioSegment.empty()
    for file in audio_files:
        clip = AudioSegment.from_mp3(file)
        combined += clip + AudioSegment.silent(duration=500)
    
    if bg_track and bg_track != "None":
        bg_audio = create_background(len(combined), bg_track)
        bg_audio = bg_audio - (20 * (1 - bg_volume))  # Adjust volume
        combined = combined.overlay(bg_audio)
    
    output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    combined.export(output, format="mp3")
    return output

# ======================
# UI COMPONENTS
# ======================
def show_text_input():
    """Step 1: Text Input Interface"""
    st.header("Step 1: Input Your Script")
    method = st.radio("Input Method:", ["Upload File", "Direct Entry"])
    
    if method == "Upload File":
        file = st.file_uploader("Upload script", type=['txt'])
        if file:
            st.session_state.parsed_data = parse_text(file.getvalue().decode('utf-8'))
            st.success(f"Parsed {len(st.session_state.parsed_data)} lines!")
            if st.button("Continue →"):
                st.session_state.current_step = 2
                st.rerun()
    else:
        sample = """Narrator: Once upon a time...
Character (happy): Hello world!"""
        text = st.text_area("Enter script:", value=sample, height=300)
        if st.button("Parse Text"):
            st.session_state.parsed_data = parse_text(text)
            st.success(f"Parsed {len(st.session_state.parsed_data)} lines!")
            if st.button("Continue →"):
                st.session_state.current_step = 2
                st.rerun()

def show_character_mapping():
    """Step 2: Character Voice Mapping"""
    st.header("Step 2: Map Voices to Characters")
    if not st.session_state.parsed_data:
        st.warning("No script loaded!")
        if st.button("← Back"):
            st.session_state.current_step = 1
            st.rerun()
        return
    
    chars = list(set([e['character'] for e in st.session_state.parsed_data]))
    with st.form("voice_mapping"):
        for char in chars:
            voice = st.selectbox(
                f"Voice for {char}",
                options=list(OPENAI_VOICES.keys()),
                key=f"voice_{char}"
            )
            st.session_state.character_voices[char] = voice
        
        if st.form_submit_button("Save Mappings"):
            st.success("Voices mapped!")
            if st.button("Continue →"):
                st.session_state.current_step = 3
                st.rerun()

def show_voice_generation():
    """Step 3: Voice Generation"""
    st.header("Step 3: Generate Audio")
    if not st.session_state.character_voices:
        st.warning("No voices mapped!")
        if st.button("← Back"):
            st.session_state.current_step = 2
            st.rerun()
        return
    
    # Background audio settings
    st.subheader("Background Settings")
    bg_track = st.selectbox(
        "Background Track",
        options=list(BACKGROUND_TRACKS.keys()),
        index=list(BACKGROUND_TRACKS.keys()).index(st.session_state.background_track)
    )
    bg_vol = st.slider("Volume", 0.1, 0.5, st.session_state.bg_volume, 0.05)
    
    if st.button("Generate Audio"):
        with st.spinner("Generating voices..."):
            st.session_state.audio_files = []
            for entry in st.session_state.parsed_data:
                voice = OPENAI_VOICES[st.session_state.character_voices[entry['character']]]
                audio = generate_tts(entry['dialogue'], voice)
                if audio:
                    st.session_state.audio_files.append(audio)
            
            if st.session_state.audio_files:
                st.session_state.final_audio = combine_audio(
                    st.session_state.audio_files,
                    bg_track,
                    bg_vol
                )
                st.session_state.current_step = 4
                st.rerun()

def show_audio_output():
    """Step 4: Final Audio Output"""
    st.header("Step 4: Your Audio Story")
    if not st.session_state.final_audio:
        st.warning("No audio generated!")
        if st.button("← Back"):
            st.session_state.current_step = 3
            st.rerun()
        return
    
    st.audio(st.session_state.final_audio)
    with open(st.session_state.final_audio, "rb") as f:
        st.download_button(
            "Download Story",
            f,
            "voice_story.mp3",
            "audio/mp3"
        )
    
    if st.button("Create New Story"):
        # Reset everything except API settings
        st.session_state.update({
            'parsed_data': [],
            'character_voices': {},
            'audio_files': [],
            'final_audio': None,
            'current_step': 1
        })
        st.rerun()

# ======================
# MAIN APP FLOW
# ======================
st.markdown("<h1 class='main-header'>VoiceCanvas</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>AI-Powered Audio Story Creator</h2>", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    steps = ["1. Text Input", "2. Character Mapping", "3. Voice Generation", "4. Audio Output"]
    step = st.radio("Steps", steps, index=st.session_state.current_step-1)
    st.session_state.current_step = steps.index(step) + 1

# Show current step
if st.session_state.current_step == 1:
    show_text_input()
elif st.session_state.current_step == 2:
    show_character_mapping()
elif st.session_state.current_step == 3:
    show_voice_generation()
elif st.session_state.current_step == 4:
    show_audio_output()

# Footer
st.markdown("---")
st.markdown("© 2024 VoiceCanvas | v2.0 | June 2024 Update")
