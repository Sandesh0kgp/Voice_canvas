import streamlit as st
import re
import tempfile
import os
import time
import json
from datetime import datetime
import pandas as pd
from pydub import AudioSegment
from openai import OpenAI
import requests
from io import BytesIO

# ==============================================
# INITIAL SETUP AND CONFIGURATION
# ==============================================

# Configure FFmpeg paths and verify installation
def configure_ffmpeg():
    try:
        # Try default paths first
        AudioSegment.converter = "ffmpeg"
        AudioSegment.ffprobe = "ffprobe"
        
        # Verify installation by creating a test file
        test_audio = AudioSegment.silent(duration=1000)
        with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp:
            test_audio.export(tmp.name, format="mp3")
        return True
    except Exception as e:
        st.warning(f"FFmpeg initialization warning: {str(e)}")
        return False

if not configure_ffmpeg():
    st.error("""
    FFmpeg not properly configured! Audio processing may not work.
    Please install FFmpeg and add it to your PATH.
    - Linux: sudo apt-get install ffmpeg
    - Mac: brew install ffmpeg
    - Windows: Download from ffmpeg.org
    """)

# Initialize all session state variables
def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.update({
            'parsed_data': [],
            'character_voices': {},
            'audio_files': [],
            'final_audio': None,
            'current_step': 1,
            'api_key': "",
            'api_provider': "openai",
            'voice_settings': {},
            'initialized': True
        })

init_session_state()

# ==============================================
# UI CONFIGURATION
# ==============================================

# Set page configuration
st.set_page_config(
    page_title="VoiceCanvas",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS
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
    .api-input {
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 0.5rem;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================
# CORE FUNCTIONALITY
# ==============================================

# Define voice models
VOICE_MODELS = {
    "openai": {
        "Alloy (Neutral)": "alloy",
        "Echo (Male)": "echo",
        "Fable (Male)": "fable",
        "Onyx (Male)": "onyx",
        "Nova (Female)": "nova",
        "Shimmer (Female)": "shimmer"
    },
    "mock": {
        "Neutral Narrator": "neutral_narrator",
        "Young Male": "young_male",
        "Young Female": "young_female",
        "Elder Male": "elder_male",
        "Elder Female": "elder_female",
        "Child": "child",
        "Villain": "villain",
        "Hero": "hero",
        "Comic Relief": "comic_relief"
    }
}

def get_openai_client():
    """Initialize OpenAI client with API key"""
    if st.session_state.api_key:
        return OpenAI(api_key=st.session_state.api_key)
    return None

def parse_text_from_string(text):
    """Parse text into structured dialogue data"""
    lines = text.strip().split('\n')
    parsed_data = []
    
    for line in lines:
        if not line.strip():
            continue
            
        match = re.match(r"(.*?)(?:\s*\((.*?)\))?\s*:\s*(.*)", line)
        
        if match:
            parsed_data.append({
                "character": match.group(1).strip(),
                "emotion": match.group(2).strip() if match.group(2) else None,
                "dialogue": match.group(3).strip()
            })
        else:
            parsed_data.append({
                "character": "Narrator",
                "emotion": None,
                "dialogue": line.strip()
            })
    
    return parsed_data

def parse_text_from_file(file):
    """Parse text from uploaded file"""
    text = file.getvalue().decode('utf-8')
    return parse_text_from_string(text)

def generate_voice_openai(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Generate voice using OpenAI TTS API"""
    try:
        client = get_openai_client()
        if not client:
            raise ValueError("OpenAI client not initialized")
            
        if emotion:
            text = f"[{emotion}] {text}]"
        
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice_model,
            input=text,
            speed=max(0.5, min(2.0, float(speed))))
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            response.stream_to_file(tmp.name)
            return tmp.name
            
    except Exception as e:
        st.error(f"OpenAI TTS Error: {str(e)}")
        return None

def generate_voice_mock(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Mock voice generation for testing"""
    try:
        time.sleep(0.2)  # Simulate processing delay
        word_count = len(text.split())
        duration = max(1000, word_count * 200)
        audio = AudioSegment.silent(duration=duration)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio.export(tmp.name, format="mp3")
            return tmp.name
    except Exception as e:
        st.error(f"Mock generation error: {str(e)}")
        return None

def generate_voice(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Route to appropriate voice generator"""
    if st.session_state.api_provider == "openai" and st.session_state.api_key:
        return generate_voice_openai(text, voice_model, speed, pitch, emotion)
    return generate_voice_mock(text, voice_model, speed, pitch, emotion)

def combine_audio_files(audio_files):
    """Safely combine audio files with error handling"""
    if not audio_files:
        return None
        
    try:
        combined = AudioSegment.empty()
        pause = AudioSegment.silent(duration=500)
        
        for file_path in audio_files:
            if not os.path.exists(file_path):
                st.error(f"Missing audio file: {file_path}")
                continue
                
            try:
                audio = AudioSegment.from_mp3(file_path)
                combined += audio + pause
            except Exception as e:
                st.error(f"Error loading {file_path}: {str(e)}")
                continue
        
        if len(combined) == 0:
            return None
            
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        combined.export(output_path, format="mp3")
        return output_path
        
    except Exception as e:
        st.error(f"Audio combining failed: {str(e)}")
        return None

def get_voice_settings(character):
    """Get or initialize voice settings for a character"""
    if character not in st.session_state.voice_settings:
        st.session_state.voice_settings[character] = {
            "speed": 1.0,
            "pitch": 0.0
        }
    return st.session_state.voice_settings[character]

# ==============================================
# APPLICATION PAGES
# ==============================================

# App header
st.markdown("<h1 class='main-header'>VoiceCanvas</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Transform Text into Character-Driven Audio</h2>", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.title("Configuration")
    
    # API provider selection
    provider = st.radio(
        "Select API Provider",
        ["OpenAI", "Mock (No API)"],
        index=0 if st.session_state.api_provider == "openai" else 1
    )
    st.session_state.api_provider = provider.lower()
    
    # API key input
    if st.session_state.api_provider == "openai":
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.api_key,
            help="Get your key from platform.openai.com"
        )
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            if api_key:
                st.success("API key updated")
    
    st.markdown("---")
    st.title("Navigation")
    step = st.radio(
        "Process Steps",
        ["1. Text Input", "2. Character Mapping", "3. Voice Generation", "4. Audio Output"],
        index=st.session_state.current_step - 1
    )
    st.session_state.current_step = int(step[0])

# Step 1: Text Input
if st.session_state.current_step == 1:
    st.header("Step 1: Input Your Script")
    
    input_method = st.radio("Input Method:", ["Upload File", "Direct Text Entry"])
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Choose a text file", type=['txt'])
        if uploaded_file:
            try:
                st.session_state.parsed_data = parse_text_from_file(uploaded_file)
                st.success(f"Parsed {len(st.session_state.parsed_data)} lines")
                
                st.subheader("Preview:")
                for entry in st.session_state.parsed_data[:5]:
                    emo = f" ({entry['emotion']})" if entry['emotion'] else ""
                    st.text(f"{entry['character']}{emo}: {entry['dialogue'][:50]}...")
                
                if st.button("Continue to Character Mapping"):
                    st.session_state.current_step = 2
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        sample_text = """Narrator: Once upon a time in a small village...
Arjun (happy): I want to explore the world!
Parents (worried): It's dangerous out there."""
        
        text_input = st.text_area("Enter your script:", value=sample_text, height=300)
        
        if st.button("Parse Text"):
            try:
                st.session_state.parsed_data = parse_text_from_string(text_input)
                st.success(f"Parsed {len(st.session_state.parsed_data)} lines")
                
                if st.button("Continue to Mapping"):
                    st.session_state.current_step = 2
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Step 2: Character Mapping
elif st.session_state.current_step == 2:
    st.header("Step 2: Character Voice Mapping")
    
    if not st.session_state.parsed_data:
        st.warning("No parsed data found!")
        if st.button("Back to Text Input"):
            st.session_state.current_step = 1
            st.rerun()
    else:
        characters = list(set([e['character'] for e in st.session_state.parsed_data]))
        
        with st.form("voice_mapping"):
            for char in characters:
                col1, col2 = st.columns([3, 1])
                with col1:
                    voice = st.selectbox(
                        f"Voice for {char}",
                        options=list(VOICE_MODELS[st.session_state.api_provider].keys()),
                        key=f"voice_{char}"
                    )
                    st.session_state.character_voices[char] = voice
                
                with col2:
                    with st.expander("Settings"):
                        settings = get_voice_settings(char)
                        settings["speed"] = st.slider(
                            "Speed", 0.5, 2.0, 1.0, 0.1,
                            key=f"speed_{char}"
                        )
            
            if st.form_submit_button("Save Mappings"):
                st.success("Voice mappings saved!")
                
                if st.button("Continue to Generation"):
                    st.session_state.current_step = 3
                    st.rerun()

# Step 3: Voice Generation
elif st.session_state.current_step == 3:
    st.header("Step 3: Generate Audio")
    
    if not st.session_state.character_voices:
        st.warning("Complete character mapping first!")
        if st.button("Back to Mapping"):
            st.session_state.current_step = 2
            st.rerun()
    else:
        if st.button("Generate All Voices"):
            st.session_state.audio_files = []
            progress_bar = st.progress(0)
            status = st.empty()
            
            for i, entry in enumerate(st.session_state.parsed_data):
                progress = (i + 1) / len(st.session_state.parsed_data)
                progress_bar.progress(progress)
                status.text(f"Processing {entry['character']}...")
                
                voice_name = st.session_state.character_voices[entry['character']]
                voice_model = VOICE_MODELS[st.session_state.api_provider][voice_name]
                settings = get_voice_settings(entry['character'])
                
                audio_file = generate_voice(
                    entry['dialogue'],
                    voice_model,
                    speed=settings['speed'],
                    emotion=entry['emotion']
                )
                
                if audio_file:
                    st.session_state.audio_files.append(audio_file)
            
            progress_bar.empty()
            status.success("Generation complete!")
            
            if st.session_state.audio_files:
                st.session_state.final_audio = combine_audio_files(st.session_state.audio_files)
                
                if st.button("Continue to Output"):
                    st.session_state.current_step = 4
                    st.rerun()

# Step 4: Audio Output
elif st.session_state.current_step == 4:
    st.header("Step 4: Audio Output")
    
    if not st.session_state.final_audio:
        st.warning("Generate audio first!")
        if st.button("Back to Generation"):
            st.session_state.current_step = 3
            st.rerun()
    else:
        st.audio(st.session_state.final_audio)
        
        with open(st.session_state.final_audio, "rb") as f:
            st.download_button(
                "Download Audio",
                f,
                "voicecanvas_output.mp3",
                "audio/mp3"
            )
        
        if st.button("Start New Project"):
            st.session_state.update({
                'parsed_data': [],
                'character_voices': {},
                'audio_files': [],
                'final_audio': None,
                'current_step': 1
            })
            st.rerun()

# Footer
st.markdown("---")
st.markdown("© 2023 VoiceCanvas | Text-to-Speech Story Creator")
