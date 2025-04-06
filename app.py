# Define enhanced CSS
enhanced_css = """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700;800&display=swap');
    
    /* Global Theme */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: linear-gradient(135deg, #f8f9ff 0%, #edf1f9 100%);
        border-radius: 1.2rem;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.06);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
    }
    
    .main-header {
        font-size: 3.4rem;
        font-weight: 800;
        background: linear-gradient(120deg, #6C63FF 0%, #FF6584 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        animation: fadeIn 1.2s ease-in-out;
    }
    
    .sub-header {
        font-size: 1.6rem;
        background: linear-gradient(120deg, #4F46E5 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2.5rem;
        text-align: center;
        font-weight: 500;
        animation: slideUp 1s ease-in-out;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(120deg, #6C63FF 0%, #8B5CF6 100%);
        color: white;
        border: none;
        border-radius: 0.6rem;
        padding: 0.7rem 1.4rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(108, 99, 255, 0.25);
        font-family: 'Montserrat', sans-serif;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 18px rgba(108, 99, 255, 0.3);
        background: linear-gradient(120deg, #7C73FF 0%, #9B6CF6 100%);
    }
    
    .stButton>button:active {
        transform: translateY(1px);
    }
    
    /* Input Fields */
    .api-input {
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
        padding: 1.5rem;
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 0.8rem;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.06);
        border-left: 5px solid #6C63FF;
        transition: all 0.3s ease;
    }
    
    .api-input:hover {
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.08);
        background-color: rgba(255, 255, 255, 0.95);
        transform: translateY(-2px);
    }
    
    /* Section Styling */
    .css-1r6slb0, .css-1inwz65 {
        border-radius: 0.9rem;
        border: 1px solid rgba(108, 99, 255, 0.15);
        background-color: rgba(255, 255, 255, 0.85);
        padding: 1.4rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .css-163ttbj {
        background: linear-gradient(180deg, #f5f7ff 0%, #e8ecff 100%);
        border-right: 1px solid rgba(108, 99, 255, 0.15);
    }
    
    /* Audio Player */
    audio {
        width: 100%;
        border-radius: 10px;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.12);
        background: linear-gradient(90deg, #6C63FF 0%, #8B5CF6 100%);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(25px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Expanders and Selectboxes */
    .streamlit-expanderHeader, .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 0.7rem;
        border: 1px solid rgba(108, 99, 255, 0.2);
        transition: all 0.3s ease;
        font-family: 'Montserrat', sans-serif;
    }
    
    .streamlit-expanderHeader:hover, .stSelectbox > div > div:hover {
        background-color: rgba(255, 255, 255, 0.95);
        border-color: rgba(108, 99, 255, 0.4);
        transform: translateY(-1px);
    }
    
    /* Text Area */
    .stTextArea > div > div {
        border-radius: 0.7rem;
        border: 1px solid rgba(108, 99, 255, 0.25);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div:focus-within {
        border-color: #6C63FF;
        box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.25);
        transform: translateY(-2px);
    }
    
    /* Dataframe/Table Styling */
    .dataframe {
        border-radius: 0.7rem;
        overflow: hidden;
        border: none !important;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.07);
        font-family: 'Poppins', sans-serif;
    }
    
    .dataframe th {
        background: linear-gradient(90deg, #6C63FF 0%, #8B5CF6 100%) !important;
        color: white !important;
        font-weight: 600;
        padding: 0.8rem 1.2rem !important;
    }
    
    .dataframe td {
        padding: 0.7rem 1.2rem !important;
        border-bottom: 1px solid #f0f2f6;
        background-color: white;
    }
    
    .dataframe tr:nth-child(even) td {
        background-color: #f9fafc;
    }
    
    /* Tooltips */
    .stTooltipIcon {
        color: #6C63FF !important;
    }
    
    /* Audio Container */
    .audio-container {
        background: linear-gradient(135deg, #f9f9ff 0%, #f0f3ff 100%);
        border-radius: 12px;
        padding: 16px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border-left: 5px solid #6C63FF;
        transition: all 0.3s ease;
    }
    
    .audio-container:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        transform: translateY(-4px);
        background: linear-gradient(135deg, #f9f9ff 0%, #f5f8ff 100%);
    }
    
    /* Progress Steps */
    .step-container {
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
        position: relative;
    }
    
    .step {
        background: #f0f3ff;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: #6C63FF;
        position: relative;
        z-index: 2;
        transition: all 0.3s ease;
        border: 2px solid #6C63FF;
    }
    
    .step.active {
        background: #6C63FF;
        color: white;
        box-shadow: 0 0 0 5px rgba(108, 99, 255, 0.2);
        animation: pulse 2s infinite;
    }
    
    .step-line {
        position: absolute;
        top: 20px;
        left: 40px;
        right: 40px;
        height: 2px;
        background: #e0e4f5;
        z-index: 1;
    }
</style>
"""
import streamlit as st
import re
import tempfile
import os
import time
import json
import random
from datetime import datetime
import pandas as pd
from pydub import AudioSegment
from openai import OpenAI
import requests
from io import BytesIO

# Configure pydub to use the correct ffmpeg path
import os
from pydub import AudioSegment

if os.name == 'nt':  # Windows
    AudioSegment.converter = r"C:\path\to\ffmpeg.exe"
    AudioSegment.ffprobe = r"C:\path\to\ffprobe.exe"
else:  # Linux/MacOS
    AudioSegment.converter = "ffmpeg"
    AudioSegment.ffprobe = "ffprobe"

# Set page configuration
st.set_page_config(
    page_title="VoiceCanvas",
    page_icon="🎙️",
    layout="wide"
)
# Apply enhanced CSS
st.markdown(enhanced_css, unsafe_allow_html=True)

# Initialize session state variables
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = []
if 'character_voices' not in st.session_state:
    st.session_state.character_voices = {}
if 'audio_files' not in st.session_state:
    st.session_state.audio_files = []
if 'final_audio' not in st.session_state:
    st.session_state.final_audio = None
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.environ.get("OPENAI_API_KEY")
if 'api_provider' not in st.session_state:
    st.session_state.api_provider = "openai"
if 'playht_key' not in st.session_state:
    st.session_state.playht_key = "e57647dcee5a4cb2883f71dc734fe8d5"
if 'playht_user_id' not in st.session_state:
    st.session_state.playht_user_id = "YvUkSVjesNQqUCunaulS9XO3xM03"
if 'playht_voice_models' not in st.session_state:
    st.session_state.playht_voice_models = []
if 'custom_voice_id' not in st.session_state:
    st.session_state.custom_voice_id = None
if 'voice_clone_status' not in st.session_state:
    st.session_state.voice_clone_status = ""
if 'voice_settings' not in st.session_state:
    st.session_state.voice_settings = {}
if 'background_track' not in st.session_state:
    st.session_state.background_track = "None"
if 'bg_volume' not in st.session_state:
    st.session_state.bg_volume = 0.3

# Define voice models
openai_voice_models = {
    "Alloy (Neutral)": "alloy",
    "Echo (Male)": "echo",
    "Fable (Male)": "fable",
    "Onyx (Male)": "onyx",
    "Nova (Female)": "nova",
    "Shimmer (Female)": "shimmer"
}

# Function to initialize OpenAI client
def get_openai_client():
    if st.session_state.api_key:
        return OpenAI(api_key=st.session_state.api_key)
    return None

# Function to parse text from string
def parse_text_from_string(text):
    """Parse text into structured dialogue data."""
    lines = text.strip().split('\n')
    parsed_data = []
    
    for line in lines:
        if not line.strip():
            continue
            
        # Check if line follows the format "Character (emotion): Dialogue"
        match = re.match(r"(.*?)(?:\s*\((.*?)\))?\s*:\s*(.*)", line)
        
        if match:
            character = match.group(1).strip()
            emotion = match.group(2).strip() if match.group(2) else None
            dialogue = match.group(3).strip()
            
            parsed_data.append({
                "character": character,
                "emotion": emotion,
                "dialogue": dialogue
            })
        else:
            # If line doesn't match the format, treat it as narration
            parsed_data.append({
                "character": "Narrator",
                "emotion": None,
                "dialogue": line.strip()
            })
    
    return parsed_data

# Function to parse text from file
def parse_text_from_file(file):
    """Parse text from uploaded file."""
    text = file.getvalue().decode('utf-8')
    return parse_text_from_string(text)

# Function to generate voice using OpenAI
def generate_voice_openai(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Generate voice audio from text using OpenAI's TTS API."""
    try:
        client = get_openai_client()
        if not client:
            st.error("OpenAI API key not set. Please enter your API key.")
            return None
            
        # Apply emotion through text modification if provided
        if emotion:
            text = f"[{emotion}] {text}"
        
        # We no longer need this code since we're using streaming approach below
        # response = client.audio.speech.create(
        #     model="tts-1",
        #     voice=voice_model,
        #     input=text,
        #     speed=speed
        # )
        
        # Save the audio to a temporary file using proper streaming approach
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            with client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice=voice_model,
                input=text,
                speed=speed
            ) as streaming_response:
                streaming_response.stream_to_file(temp_file.name)
            return temp_file.name
            
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

# Function to get PlayHT voices
def get_playht_voices():
    """Get available voice models from PlayHT API."""
    if not st.session_state.playht_key or not st.session_state.playht_user_id:
        return []
        
    try:
        # Updated endpoint to match PlayHT's documentation
        url = "https://api.play.ht/api/v1/voices?cloned=true"
        headers = {
            "Accept": "application/json",
            "Authorization": st.session_state.playht_key,
            "X-User-ID": st.session_state.playht_user_id
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # The API response might be an array directly, or nested under a key
            result = response.json()
            voices = result if isinstance(result, list) else result.get('voices', [])
            
            # Format the voices to have consistent structure with our app
            formatted_voices = []
            for voice in voices:
                formatted_voice = {
                    'id': voice.get('id'),
                    'name': voice.get('name'),
                    'isCloned': True,
                    'created_at': voice.get('created_at', 'Unknown date')
                }
                formatted_voices.append(formatted_voice)
            
            return formatted_voices
        else:
            st.error(f"Error getting PlayHT voices: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to PlayHT API: {str(e)}")
        return []

# Function to create voice clone with PlayHT
def create_playht_voice_clone(name, audio_file_path, description="My cloned voice"):
    """Create a new voice clone using PlayHT API."""
    if not st.session_state.playht_key or not st.session_state.playht_user_id:
        return None
        
    try:
        # Correct endpoint for voice cloning with PlayHT v1 API
        url = "https://api.play.ht/api/v1/voices/clone/instant" 
        headers = {
            "Accept": "application/json",
            "Authorization": st.session_state.playht_key,
            "X-User-ID": st.session_state.playht_user_id

        }
        
        # Read the audio file
        with open(audio_file_path, 'rb') as f:
            # Simplify filename to avoid issues with special characters
            simple_filename = "voice_sample.mp3"
            
            files = {
                'sample_file': (simple_filename, f, 'audio/mpeg')
            }
            
            data = {
                'voice_name': name,
                'description': description
            }
            
            # Add more detailed logging
            st.write("Attempting voice clone with:", url)
            st.write("File being uploaded:", os.path.basename(audio_file_path))
            
            # Make the API request with additional debugging
            try:
                response = requests.post(url, headers=headers, data=data, files=files)
                st.write(f"Response status code: {response.status_code}")
                st.write(f"Response headers: {response.headers}")
                if response.text:
                    st.write(f"Response content (preview): {response.text[:200]}")
            except Exception as e:
                st.error(f"Request error: {str(e)}")
                return None
            
            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                voice_id = result.get('id') or result.get('voice_id')
                
                if voice_id:
                    st.success(f"Voice clone created successfully with ID: {voice_id}")
                    return voice_id
                else:
                    st.warning("Voice clone request accepted but no ID returned. Refreshing voices may show your new voice.")
                    return "pending"
            else:
                st.error(f"Error creating voice clone: {response.status_code} - {response.text}")
                return None
    except Exception as e:
        st.error(f"Error connecting to PlayHT API: {str(e)}")
        st.error(f"Details: {str(e)}")
        return None

# Function to check voice clone status
def check_playht_voice_clone_status(voice_id):
    """Check the status of a voice clone process."""
    if not st.session_state.playht_key or not st.session_state.playht_user_id:
        return None
    
    # If voice_id is "pending", we just need to refresh voices
    if voice_id == "pending":
        # Get the updated voice list to see if the new voice appears
        voices = get_playht_voices()
        if voices:
            return {"status": "completed", "id": "refresh_needed"}
        else:
            return {"status": "processing", "id": "pending"}
    
    try:
        # First check if the voice exists in the current voice list
        voices = get_playht_voices()
        for voice in voices:
            if voice.get('id') == voice_id:
                return {"status": "completed", "id": voice_id}
        
        # If not found in the list, check directly with API
        url = f"https://api.play.ht/api/v1/voice/{voice_id}"
        headers = {
            "Accept": "application/json",
            "Authorization": st.session_state.playht_key,
            "X-User-ID": st.session_state.playht_user_id
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            # Check if the voice exists and is usable
            status = "completed" if result.get("status") == "CREATION_SUCCEEDED" else "processing"
            return {"status": status, "id": voice_id}
        elif response.status_code == 404:
            # Voice ID not found, but cloning might still be in progress
            return {"status": "processing", "id": voice_id}
        else:
            st.error(f"Error checking voice clone status: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to PlayHT API: {str(e)}")
        return None

# Function to generate voice using PlayHT
def generate_voice_playht(text, voice_id, speed=1.0, pitch=0, emotion=None):
    """Generate voice audio from text using PlayHT API."""
    if not st.session_state.playht_key or not st.session_state.playht_user_id:
        st.error("PlayHT API key or User ID not set. Please enter your credentials.")
        return None
        
    try:
        # Updated API endpoint to match PlayHT's current API
        url = "https://api.play.ht/api/v1/convert"
        headers = {
            "Accept": "application/json",
            "Authorization": st.session_state.playht_key,
            "X-User-ID": st.session_state.playht_user_id,
            "Content-Type": "application/json"
        }
        
        # Apply emotion through text modification if provided
        if emotion:
            text = f"[{emotion}] {text}"
        
        # Format data according to PlayHT v1 API
        data = {
            "content": [text],
            "voice": voice_id,
            "output_format": "mp3",
            "speed": speed,
            "sample_rate": 24000
        }
        
        # Submit conversion request
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            transcription_id = result.get('transcriptionId')
            
            if not transcription_id:
                st.error("No transcription ID returned from PlayHT")
                return None
                
            # Poll status endpoint until conversion is complete (with timeout)
            status_url = f"https://api.play.ht/api/v1/articleStatus?transcriptionId={transcription_id}"
            
            # Poll with timeout
            max_attempts = 15
            for attempt in range(max_attempts):
                time.sleep(1)  # Wait between polls
                
                status_response = requests.get(status_url, headers=headers)
                if status_response.status_code != 200:
                    continue
                    
                status = status_response.json()
                
                if status.get("converted", False):
                    # Conversion complete
                    audio_url = status.get("audioUrl")
                    
                    if audio_url:
                        # Download the audio file
                        audio_response = requests.get(audio_url)
                        
                        # Save the audio to a temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                            temp_file.write(audio_response.content)
                            return temp_file.name
                    else:
                        st.error("No audio URL in the conversion result")
                        return None
            
            st.error("Timed out waiting for PlayHT conversion")
            return None
        else:
            st.error(f"Error generating audio: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

# Function to generate voice (mock implementation as fallback)
def generate_voice_mock(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Generate voice audio from text (mock implementation)."""
    # Simulate processing time
    time.sleep(0.5)
    
    # Create a silent audio segment (1 second per 5 words)
    word_count = len(text.split())
    duration = max(1000, word_count * 200)  # at least 1 second
    
    audio = AudioSegment.silent(duration=duration)
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        audio.export(temp_file.name, format="mp3")
        return temp_file.name

# Function to generate voice (router)
def generate_voice(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Route to appropriate voice generation function based on the voice model."""
    # Check if API keys exist
    has_openai_key = bool(st.session_state.api_key)
    has_playht_keys = bool(st.session_state.playht_key and st.session_state.playht_user_id)
    
    # Determine if the voice is an OpenAI voice or PlayHT voice
    is_openai_voice = voice_model in openai_voice_models.values()
    is_playht_voice = False
    
    if not is_openai_voice and has_playht_keys and st.session_state.playht_voice_models:
        # Check if the ID exists in PlayHT voices
        is_playht_voice = any(v.get('id') == voice_model for v in st.session_state.playht_voice_models)
    
    # Route to appropriate API
    if is_openai_voice and has_openai_key:
        return generate_voice_openai(text, voice_model, speed, pitch, emotion)
    elif is_playht_voice and has_playht_keys:
        return generate_voice_playht(text, voice_model, speed, pitch, emotion)
    elif has_openai_key:
        # Fallback to OpenAI if keys exist but voice is unknown
        return generate_voice_openai(text, "alloy", speed, pitch, emotion)
    else:
        # Last resort is mock when all else fails
        return generate_voice_mock(text, voice_model, speed, pitch, emotion)

# Dictionary of built-in background tracks
BACKGROUND_TRACKS = {
    "None": None,
    "Peaceful Nature": "peaceful_nature",
    "Sci-Fi Ambience": "scifi_ambience",
    "Suspenseful Mystery": "suspenseful_mystery",
    "Fantasy Adventure": "fantasy_adventure",
    "Urban City": "urban_city",
    "Romantic Scene": "romantic_scene",
    "Horror Ambience": "horror_ambience",
    "Comedy Background": "comedy_background"
}

# Function to get background music from local storage or create silent audio
def get_background_music(track_name, duration_ms):
    """Get background music track or create silent audio if track not available."""
    if track_name == "None" or not track_name:
        # Return silent audio of appropriate length
        return AudioSegment.silent(duration=duration_ms)
        
    # Create simulated ambient sounds based on the name
    # In a real implementation, these would be real audio files
    base_audio = AudioSegment.silent(duration=duration_ms)
    
    # Generate some ambient sounds based on the track name
    # This is a simplified mock implementation using noise and filters
    if "nature" in track_name.lower():
        # Nature sounds: soft wind and occasional bird chirps
        base = AudioSegment.silent(duration=5000)
        
        # Generate wind-like white noise
        for i in range(0, 5000, 500):
            # Vary the volume to simulate wind gusts
            vol_factor = random.uniform(0.2, 0.4)
            wind = AudioSegment.silent(duration=300)
            wind = wind.low_pass_filter(500)
            wind = wind - int(30 * (1 - vol_factor))  # Adjust volume
            base = base.overlay(wind, position=i)
            
        # Add occasional bird chirps
        for i in range(0, 5000, 1500):
            if random.random() > 0.5:  # 50% chance of a chirp
                # Bird chirp: short high-pitched sound
                chirp_len = random.randint(50, 150)
                chirp = AudioSegment.silent(duration=chirp_len)
                chirp = chirp.high_pass_filter(3000)
                base = base.overlay(chirp, position=i)
        
        # Loop this segment to fill the duration
        repeats = (duration_ms // 5000) + 1
        ambient = base * repeats
        ambient = ambient[:duration_ms]  # Trim to exact length
        
    elif "sci-fi" in track_name.lower():
        # Sci-fi sounds: electronic beeps and background hum
        base = AudioSegment.silent(duration=8000)
        
        # Background electronic hum
        hum = AudioSegment.silent(duration=8000)
        hum = hum.low_pass_filter(200)
        base = base.overlay(hum)
        
        # Random electronic beeps
        for i in range(0, 8000, 800):
            if random.random() > 0.6:  # 40% chance of a beep
                beep_len = random.randint(20, 100)
                beep = AudioSegment.silent(duration=beep_len)
                
                # Randomize filter to get different tones
                if random.random() > 0.5:
                    beep = beep.high_pass_filter(random.randint(2000, 4000))
                else:
                    beep = beep.low_pass_filter(random.randint(500, 1500))
                    
                base = base.overlay(beep, position=i)
                
        # Loop this segment to fill the duration
        repeats = (duration_ms // 8000) + 1
        ambient = base * repeats
        ambient = ambient[:duration_ms]  # Trim to exact length
        
    elif "suspense" in track_name.lower() or "horror" in track_name.lower():
        # Suspenseful/horror sounds: low rumble with occasional string hits
        base = AudioSegment.silent(duration=10000)
        
        # Add low rumble throughout
        rumble = AudioSegment.silent(duration=10000)
        rumble = rumble.low_pass_filter(100)
        base = base.overlay(rumble)
        
        # Add occasional string hits or sudden noises
        for i in range(0, 10000, 2500):
            if random.random() > 0.7:  # 30% chance
                hit_len = random.randint(200, 500)
                hit = AudioSegment.silent(duration=hit_len)
                hit = hit.high_pass_filter(1000)
                hit = hit - 10  # Make it louder
                base = base.overlay(hit, position=i)
                
        # Loop this segment to fill the duration
        repeats = (duration_ms // 10000) + 1
        ambient = base * repeats
        ambient = ambient[:duration_ms]  # Trim to exact length
        
    elif "fantasy" in track_name.lower():
        # Fantasy adventure: mystical atmosphere with occasional chimes
        base = AudioSegment.silent(duration=12000)
        
        # Base atmospheric sound
        atmos = AudioSegment.silent(duration=12000)
        atmos = atmos.low_pass_filter(800)
        base = base.overlay(atmos)
        
        # Add occasional chimes or harp-like sounds
        for i in range(0, 12000, 1200):
            if random.random() > 0.7:  # 30% chance
                chime_len = random.randint(50, 150)
                chime = AudioSegment.silent(duration=chime_len)
                chime = chime.high_pass_filter(3000)
                chime = chime - 15  # Volume adjustment
                base = base.overlay(chime, position=i)
                
        # Loop this segment to fill the duration
        repeats = (duration_ms // 12000) + 1
        ambient = base * repeats
        ambient = ambient[:duration_ms]  # Trim to exact length
        
    elif "urban" in track_name.lower() or "city" in track_name.lower():
        # Urban city: distant traffic and occasional horns
        base = AudioSegment.silent(duration=15000)
        
        # Traffic noise
        traffic = AudioSegment.silent(duration=15000)
        traffic = traffic.low_pass_filter(1000)
        base = base.overlay(traffic)
        
        # Occasional car horns or city sounds
        for i in range(0, 15000, 3000):
            if random.random() > 0.6:  # 40% chance
                horn_len = random.randint(100, 300)
                horn = AudioSegment.silent(duration=horn_len)
                
                # Randomize filter for different horn sounds
                filter_freq = random.randint(500, 2000)
                horn = horn.low_pass_filter(filter_freq)
                horn = horn - 20  # Volume adjustment
                base = base.overlay(horn, position=i)
                
        # Loop this segment to fill the duration
        repeats = (duration_ms // 15000) + 1
        ambient = base * repeats
        ambient = ambient[:duration_ms]  # Trim to exact length
        
    elif "comedy" in track_name.lower():
        # Comedy background: light and upbeat sounds
        base = AudioSegment.silent(duration=6000)
        
        # Light background sounds
        for i in range(0, 6000, 600):
            if random.random() > 0.7:  # 30% chance
                sound_len = random.randint(50, 200)
                sound = AudioSegment.silent(duration=sound_len)
                sound = sound.high_pass_filter(random.randint(1000, 2000))
                sound = sound - 15  # Volume adjustment
                base = base.overlay(sound, position=i)
                
        # Loop this segment to fill the duration
        repeats = (duration_ms // 6000) + 1
        ambient = base * repeats
        ambient = ambient[:duration_ms]  # Trim to exact length
        
    elif "romantic" in track_name.lower():
        # Romantic scene: soft and gentle atmosphere
        base = AudioSegment.silent(duration=10000)
        
        # Soft background sounds
        atmos = AudioSegment.silent(duration=10000)
        atmos = atmos.low_pass_filter(600)
        base = base.overlay(atmos)
        
        # Occasional gentle notes
        for i in range(0, 10000, 2000):
            if random.random() > 0.6:  # 40% chance
                note_len = random.randint(100, 300)
                note = AudioSegment.silent(duration=note_len)
                note = note.low_pass_filter(random.randint(800, 1200))
                note = note - 20  # Volume adjustment
                base = base.overlay(note, position=i)
                
        # Loop this segment to fill the duration
        repeats = (duration_ms // 10000) + 1
        ambient = base * repeats
        ambient = ambient[:duration_ms]  # Trim to exact length
        
    else:
        # Generic ambient sound for other track types
        base = AudioSegment.silent(duration=5000)
        
        # Add some subtle background noise
        noise = AudioSegment.silent(duration=5000)
        noise = noise.low_pass_filter(800)
        base = base.overlay(noise)
        
        # Loop this segment to fill the duration
        repeats = (duration_ms // 5000) + 1
        ambient = base * repeats
        ambient = ambient[:duration_ms]  # Trim to exact length
    
    return ambient

# Function to combine audio files
def combine_audio_files(audio_files, background_track=None, bg_volume=0.3):
    """Combine multiple audio files with a short pause between them and optional background music."""
    if not audio_files:
        return None
        
    combined = AudioSegment.empty()
    pause = AudioSegment.silent(duration=500)  # 500ms pause
    
    # First pass: combine all dialogue audio and calculate total length
    for file_path in audio_files:
        audio = AudioSegment.from_mp3(file_path)
        combined += audio + pause
    
    # If background track is specified, mix it with the combined audio
    if background_track and background_track != "None":
        # Get the total duration of the combined dialogue
        total_duration = len(combined)
        
        # Get the background music of appropriate length
        bg_audio = get_background_music(background_track, total_duration)
        
        # Adjust the volume of background music (0.3 = 30% of original volume)
        bg_audio = bg_audio - (1 - bg_volume) * 20  # Adjust volume (in dB)
        
        # Mix the background audio with the combined dialogue
        # Make sure bg_audio is at least as long as combined
        if len(bg_audio) < len(combined):
            # Loop the background audio if needed
            repeat_count = (len(combined) // len(bg_audio)) + 1
            bg_audio = bg_audio * repeat_count
            
        # Trim to match the dialogue length
        bg_audio = bg_audio[:len(combined)]
        
        # Mix the audio streams
        combined = combined.overlay(bg_audio, loop=False)
    
    # Export combined audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        combined.export(temp_file.name, format="mp3")
        return temp_file.name

# Function to save user preferences
def save_user_preferences(preferences):
    """Save user preferences to a file."""
    try:
        with open("user_preferences.json", "w") as f:
            json.dump(preferences, f)
        return True
    except Exception as e:
        st.error(f"Error saving preferences: {str(e)}")
        return False

# Function to get voice settings
def get_voice_settings(character):
    """Get the voice settings for a character."""
    return st.session_state.voice_settings.get(character, {
        "voice": list(openai_voice_models.keys())[0],
        "speed": 1.0,
        "pitch": 0
    })

# Function to get voice model ID
def get_voice_model_id(voice_name):
    """Get the voice model ID from the voice name."""
    # Check if it's a separator, if so return a default voice
    if voice_name == "--- PlayHT Cloned Voices ---":
        return "alloy"  # Default OpenAI voice as fallback
        
    # For OpenAI voices, return directly from the dictionary
    if voice_name in openai_voice_models:
        return openai_voice_models.get(voice_name, "alloy")
        
    # For PlayHT voices, search by name to find the ID
    if st.session_state.playht_voice_models:
        for voice in st.session_state.playht_voice_models:
            if voice.get('name') == voice_name:
                return voice.get('id')
                
    # If we can't identify it as either, return default
    return "alloy"  # Default fallback

# Main App Function
def main():
    # Application header
    st.markdown("<h1 class='main-header'>VoiceCanvas</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Transform your scripts into immersive voice experiences</p>", unsafe_allow_html=True)
    
    # Create tabs for different sections
    tabs = st.tabs(["Script to Voice", "Voice Clone Studio", "Settings", "About"])
    
    # Script to Voice Tab
    with tabs[0]:
        st.header("Script to Voice Converter")
        st.write("Enter your script text or upload a file to generate voice audio with different characters.")
        
        # Steps indicator for visual progress tracking
        col1, col2, col3 = st.columns(3)
        
        with col1:
            step1_class = "active" if st.session_state.current_step == 1 else ""
            st.markdown(f"<div class='step {step1_class}'>1</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;'>Input Text</p>", unsafe_allow_html=True)
            
        with col2:
            step2_class = "active" if st.session_state.current_step == 2 else ""
            st.markdown(f"<div class='step {step2_class}'>2</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;'>Assign Voices</p>", unsafe_allow_html=True)
            
        with col3:
            step3_class = "active" if st.session_state.current_step == 3 else ""
            st.markdown(f"<div class='step {step3_class}'>3</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center;'>Generate Audio</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='step-line'></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # STEP 1: Input Text
        if st.session_state.current_step == 1:
            # Input method selection
            input_method = st.radio("Select input method:", ["Direct Text Entry", "Upload File"], horizontal=True)
            
            if input_method == "Upload File":
                # File uploader
                uploaded_file = st.file_uploader("Upload script file:", type=["txt", "md"])
                
                if uploaded_file:
                    try:
                        st.session_state.parsed_data = parse_text_from_file(uploaded_file)
                        
                        # Display parsed data
                        st.subheader("Preview:")
                        for item in st.session_state.parsed_data[:5]:  # Preview first 5 lines
                            emotion_text = f" ({item['emotion']})" if item['emotion'] else ""
                            st.write(f"**{item['character']}{emotion_text}:** {item['dialogue']}")
                        
                        if len(st.session_state.parsed_data) > 5:
                            st.write(f"... and {len(st.session_state.parsed_data) - 5} more lines")
                            
                        # Add message about continuing
                        st.write("")  # Spacing
                        st.write("When you're ready to assign voices to characters:")
                    except Exception as e:
                        st.error(f"Error parsing file: {str(e)}")
                
                # Continue button always shown when data is parsed from file
                if st.session_state.parsed_data and input_method == "Upload File":
                    if st.button("Continue to Voice Assignment", key="continue_file_upload"):
                        st.session_state.current_step = 2
                        st.rerun()
            
            else:  # Direct Text Entry
                sample_text = """Narrator: In a small town nestled between rolling hills, lived Maya, a young artist with big dreams but little confidence.
Maya (unsure): I don't know if my paintings are good enough for the art exhibition.
Friend (encouraging): Maya, your work is incredible! You've captured emotions that speak to people.
Narrator: Maya stared at her canvas, brushstrokes of vibrant colors depicting a sunrise over mountains.
Maya (worried): But what if everyone laughs? What if I'm not ready?
Mentor (wise): The greatest masterpieces weren't created by artists who felt ready, but by those brave enough to try anyway.
Narrator: The day of the exhibition arrived, and Maya's hands trembled as she hung her painting.
Visitor (amazed): This painting... it's extraordinary! It makes me feel like anything is possible.
Maya (surprised): Really? That's exactly what I wanted to convey!
Narrator: As more people gathered around her work, Maya felt something shift inside her.
Maya (confident): Maybe I don't need to be fearless. I just need to create despite the fear.
Mentor (proud): That, my dear, is the secret to all achievement.
Narrator: That night, with the town's applause still echoing in her ears, Maya began her next painting with newfound purpose.
Maya (determined): Every brushstroke is a step forward. I don't need to see the whole staircase to take the first step."""
                text_input = st.text_area("Enter your script:", value=sample_text, height=300,
                                 help="Format: Character (emotion): Dialogue")
                
                if st.button("Parse Text"):
                    if text_input.strip():
                        st.session_state.parsed_data = parse_text_from_string(text_input)
                        
                        # Display parsed data
                        st.subheader("Parsed Result:")
                        for item in st.session_state.parsed_data[:5]:  # Preview first 5 lines
                            emotion_text = f" ({item['emotion']})" if item['emotion'] else ""
                            st.write(f"**{item['character']}{emotion_text}:** {item['dialogue']}")
                        
                        if len(st.session_state.parsed_data) > 5:
                            st.write(f"... and {len(st.session_state.parsed_data) - 5} more lines")
                        
                        # Add a "Continue" button outside of the if statement
                        st.write("") # Add some spacing
                        st.write("When you're ready to assign voices to characters:")
                    else:
                        st.error("Please enter some text before parsing.")
                
                # Continue button always shown when data is parsed, with unique key
                if st.session_state.parsed_data:
                    if st.button("Continue to Voice Assignment", key="continue_text_input"):
                        st.session_state.current_step = 2
                        st.rerun()
        
        # STEP 2: Voice Assignment
        elif st.session_state.current_step == 2:
            st.subheader("Assign Voices to Characters")
            
            # Get unique characters
            unique_characters = set(item["character"] for item in st.session_state.parsed_data)
            
            # Initialize voice settings if not already set
            for character in unique_characters:
                if character not in st.session_state.voice_settings:
                    st.session_state.voice_settings[character] = {
                        "voice": list(openai_voice_models.keys())[0],
                        "speed": 1.0,
                        "pitch": 0
                    }
            
            # Display voice settings for each character
            st.write("Customize voice settings for each character:")
            
            # Voice assignment widgets
            for character in unique_characters:
                with st.expander(f"**{character}**", expanded=(character == list(unique_characters)[0])):
                    col1, col2 = st.columns(2)
                    
                    # Get current settings for this character
                    current_settings = st.session_state.voice_settings.get(character, {
                        "voice": list(openai_voice_models.keys())[0],
                        "speed": 1.0,
                        "pitch": 0
                    })
                    
                    # Voice selection based on API provider
                    voice_options = []
                    
                    # Always include OpenAI voices
                    voice_options = list(openai_voice_models.keys())
                    
                    # Add PlayHT voices if available
                    if st.session_state.playht_voice_models:
                        # Add a separator
                        if voice_options:
                            voice_options.append("--- PlayHT Cloned Voices ---")
                        
                        # Add all PlayHT voices
                        for v in st.session_state.playht_voice_models:
                            voice_name = v.get('name', v.get('id', 'Unknown'))
                            if voice_name not in voice_options:
                                voice_options.append(voice_name)
                    
                    with col1:
                        voice = st.selectbox(
                            f"Voice for {character}:",
                            options=voice_options,
                            index=voice_options.index(current_settings["voice"]) if current_settings["voice"] in voice_options else 0,
                            key=f"voice_{character}"
                        )
                    
                    with col2:
                        speed = st.slider(
                            f"Speed for {character}:",
                            min_value=0.5,
                            max_value=1.5,
                            value=current_settings["speed"],
                            step=0.1,
                            key=f"speed_{character}"
                        )
                    
                    # Update settings in session state
                    st.session_state.voice_settings[character] = {
                        "voice": voice,
                        "speed": speed,
                        "pitch": 0  # Pitch is not directly supported in OpenAI TTS, kept for future compatibility
                    }
                    
                    # Test button for this character
                    test_text = next((item["dialogue"] for item in st.session_state.parsed_data 
                                    if item["character"] == character), "Testing voice.")
                    
                    if st.button(f"Test Voice for {character}", key=f"test_{character}"):
                        if st.session_state.api_provider == "openai" and not st.session_state.api_key:
                            st.error("Please set your OpenAI API key in the Settings tab.")
                        elif st.session_state.api_provider == "playht" and (not st.session_state.playht_key or not st.session_state.playht_user_id):
                            st.error("Please set your PlayHT API credentials in the Settings tab.")
                        else:
                            # Get the first dialogue for this character to test
                            emotion = next((item["emotion"] for item in st.session_state.parsed_data 
                                        if item["character"] == character and item["emotion"]), None)
                            
                            voice_model = get_voice_model_id(voice)
                            
                            with st.spinner(f"Generating test audio for {character}..."):
                                audio_file = generate_voice(
                                    test_text,
                                    voice_model,
                                    speed,
                                    0,
                                    emotion
                                )
                                
                                if audio_file:
                                    st.audio(audio_file)
                                else:
                                    st.error("Failed to generate test audio.")
            
            # Background music selection
            st.subheader("Background Music")
            col1, col2 = st.columns(2)
            
            with col1:
                background_track = st.selectbox(
                    "Select background music:",
                    options=list(BACKGROUND_TRACKS.keys()),
                    index=list(BACKGROUND_TRACKS.keys()).index(st.session_state.background_track) if st.session_state.background_track in BACKGROUND_TRACKS else 0
                )
                st.session_state.background_track = background_track
                
            with col2:
                if background_track != "None":
                    bg_volume = st.slider(
                        "Background volume:",
                        min_value=0.1,
                        max_value=0.9,
                        value=st.session_state.bg_volume,
                        step=0.1
                    )
                    st.session_state.bg_volume = bg_volume
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Back to Text Input"):
                    st.session_state.current_step = 1
                    st.rerun()
                    
            with col2:
                if st.button("Continue to Audio Generation"):
                    st.session_state.current_step = 3
                    st.rerun()
        
        # STEP 3: Generate Audio
        elif st.session_state.current_step == 3:
            st.subheader("Generate Audio")
            
            # Summary of settings
            st.write("Here's a summary of your settings:")
            
            # Display unique characters and their voice settings
            unique_characters = set(item["character"] for item in st.session_state.parsed_data)
            
            for character in unique_characters:
                settings = st.session_state.voice_settings.get(character, {
                    "voice": list(openai_voice_models.keys())[0],
                    "speed": 1.0,
                    "pitch": 0
                })
                
                st.write(f"- **{character}**: {settings['voice']} (Speed: {settings['speed']})")
            
            st.write(f"- **Background Music**: {st.session_state.background_track}")
            if st.session_state.background_track != "None":
                st.write(f"- **Background Volume**: {int(st.session_state.bg_volume * 100)}%")
            
            # Generate button
            if st.button("Generate Full Audio"):
                if st.session_state.api_provider == "openai" and not st.session_state.api_key:
                    st.error("Please set your OpenAI API key in the Settings tab.")
                elif st.session_state.api_provider == "playht" and (not st.session_state.playht_key or not st.session_state.playht_user_id):
                    st.error("Please set your PlayHT API credentials in the Settings tab.")
                else:
                    # Clear previous audio files
                    st.session_state.audio_files = []
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Generate audio for each dialogue item
                    total_items = len(st.session_state.parsed_data)
                    
                    for i, item in enumerate(st.session_state.parsed_data):
                        character = item["character"]
                        dialogue = item["dialogue"]
                        emotion = item["emotion"]
                        
                        # Update progress
                        progress = (i / total_items)
                        progress_bar.progress(progress)
                        status_text.text(f"Generating audio for {character}: {dialogue[:30]}...")
                        
                        # Get voice settings for this character
                        settings = st.session_state.voice_settings.get(character, {
                            "voice": list(openai_voice_models.keys())[0],
                            "speed": 1.0,
                            "pitch": 0
                        })
                        
                        voice_model = get_voice_model_id(settings["voice"])
                        
                        # Generate voice audio
                        audio_file = generate_voice(
                            dialogue,
                            voice_model,
                            settings["speed"],
                            settings["pitch"],
                            emotion
                        )
                        
                        if audio_file:
                            st.session_state.audio_files.append(audio_file)
                    
                    # Combine all audio files with background music
                    progress_bar.progress(0.95)
                    status_text.text("Combining audio files...")
                    
                    bg_track = BACKGROUND_TRACKS.get(st.session_state.background_track)
                    
                    final_audio = combine_audio_files(
                        st.session_state.audio_files,
                        bg_track,
                        st.session_state.bg_volume
                    )
                    
                    # Complete!
                    progress_bar.progress(1.0)
                    status_text.text("Audio generation complete!")
                    
                    if final_audio:
                        st.session_state.final_audio = final_audio
                        
                        # Display success message
                        st.success("Your script has been converted to audio successfully!")
                        
                        # Play the combined audio
                        st.subheader("Combined Audio")
                        st.markdown("<div class='audio-container'>", unsafe_allow_html=True)
                        st.audio(final_audio)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Download button for the final audio
                        with open(final_audio, "rb") as f:
                            st.download_button(
                                label="Download Full Audio",
                                data=f,
                                file_name=f"voicecanvas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                                mime="audio/mp3"
                            )
                    else:
                        st.error("Failed to generate combined audio.")
            
            # Display previously generated audio if available
            if st.session_state.final_audio:
                st.subheader("Previously Generated Audio")
                st.markdown("<div class='audio-container'>", unsafe_allow_html=True)
                st.audio(st.session_state.final_audio)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Download button for the final audio
                with open(st.session_state.final_audio, "rb") as f:
                    st.download_button(
                        label="Download Full Audio",
                        data=f,
                        file_name=f"voicecanvas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                        mime="audio/mp3"
                    )
            
            # Navigation button
            if st.button("Back to Voice Assignment"):
                st.session_state.current_step = 2
                st.rerun()
                
    # Voice Clone Studio Tab
    with tabs[1]:
        st.header("Voice Clone Studio")
        st.write("Create your own custom voice clone with PlayHT technology.")
        
        # Display a simple explanation
        st.markdown("""
        ### Create Your Own Voice
        Upload a voice sample and create a digital copy of any voice in seconds.
        Your custom voices can be used in the Script to Voice tab for any character.
        """)
        
        # API settings are already set
        
        # Simple interface for voice list
        if st.button("Refresh My Voices", key="refresh_voices"):
            with st.spinner("Loading your voices..."):
                st.session_state.playht_voice_models = get_playht_voices()
        
        # Display voices in a clean way
        if st.session_state.playht_voice_models:
            st.subheader("Your Voices")
            
            # Create columns for the voices
            cols = st.columns(2)
            
            for i, voice in enumerate(st.session_state.playht_voice_models):
                voice_id = voice.get('id')
                voice_name = voice.get('name', 'Unknown')
                
                # Alternate between columns
                with cols[i % 2]:
                    with st.container():
                        st.markdown(f"### {voice_name}")
                        
                        # Test button
                        if st.button(f"🔊 Test", key=f"test_{voice_id}"):
                            with st.spinner("Generating sample..."):
                                test_text = "This is my voice. How does it sound?"
                                
                                audio_file = generate_voice_playht(
                                    test_text,
                                    voice_id,
                                    1.0,
                                    0,
                                    None
                                )
                                
                                if audio_file:
                                    st.audio(audio_file)
                        
                        st.write("---")
        else:
            st.info("No custom voices found. Create one below!")
        
        # Simplified voice creation
        st.subheader("Create New Voice")
        
        # Single column layout
        voice_name = st.text_input("Voice Name:", value="My Voice")
        
        # Audio upload with clear instruction
        st.write("Upload a clear voice recording (MP3 format, 30+ seconds of speaking)")
        uploaded_audio = st.file_uploader("Choose audio file", type=["mp3"], key="voice_upload")
        
        if uploaded_audio:
            st.write("Preview your sample:")
            st.audio(uploaded_audio)
            
            if st.button("Create Voice", key="create_voice_btn"):
                with st.spinner("Processing your voice... This takes about 2-3 minutes."):
                    # Save uploaded audio to temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                        temp_file.write(uploaded_audio.getvalue())
                        audio_path = temp_file.name
                    
                    # Create voice clone with minimal parameters
                    voice_id = create_playht_voice_clone(
                        voice_name,
                        audio_path,
                        f"Voice clone created on {datetime.now().strftime('%Y-%m-%d')}"
                    )
                    
                    if voice_id:
                        st.session_state.custom_voice_id = voice_id
                        st.session_state.voice_clone_status = "processing"
                        st.success("✅ Voice creation started!")
                        st.info("Your voice will be ready in a few minutes. Click 'Check Status' to see if it's ready.")
                    else:
                        st.error("Voice creation failed. Please try again.")
        
        # Simple status check
        if st.session_state.custom_voice_id and st.session_state.voice_clone_status == "processing":
            if st.button("Check Status", key="check_status_btn"):
                with st.spinner("Checking voice status..."):
                    status = check_playht_voice_clone_status(st.session_state.custom_voice_id)
                    
                    if status:
                        clone_status = status.get('status', 'unknown')
                        
                        if clone_status == "completed":
                            st.success("🎉 Your voice is ready!")
                            st.session_state.voice_clone_status = "completed"
                            
                            # Refresh voice list
                            st.session_state.playht_voice_models = get_playht_voices()
                            
                            # Test audio
                            test_text = "Congratulations! Your voice clone is ready to use."
                            audio_file = generate_voice_playht(
                                test_text,
                                st.session_state.custom_voice_id,
                                1.0, 0, None
                            )
                            
                            if audio_file:
                                st.audio(audio_file)
                                
                        elif clone_status == "processing":
                            st.info("⏳ Still processing... Check back in a minute.")
                        else:
                            st.warning(f"Status: {clone_status}")
                    else:
                        st.error("Could not check status. Try refreshing the page.")
    
    # Settings Tab
    with tabs[2]:
        st.header("Settings")
        
        # API Provider selection
        st.subheader("API Provider")
        api_provider = st.radio(
            "Select Voice API Provider:",
            options=["OpenAI", "PlayHT"],
            index=0 if st.session_state.api_provider == "openai" else 1,
            horizontal=True
        )
        
        # Update API provider in session state (converted to lowercase)
        st.session_state.api_provider = api_provider.lower()
        
        # OpenAI API settings
        if api_provider == "OpenAI":
            st.subheader("OpenAI API Settings")
            
            st.markdown("<div class='api-input'>", unsafe_allow_html=True)
            api_key = st.text_input(
                "OpenAI API Key:",
                value=st.session_state.api_key or "",
                type="password",
                help="Enter your OpenAI API key. It will be stored only for this session."
            )
            
            if api_key:
                st.session_state.api_key = api_key
            
            # Test connection button
            if st.button("Test OpenAI Connection"):
                if not st.session_state.api_key:
                    st.error("Please enter your OpenAI API key.")
                else:
                    with st.spinner("Testing connection to OpenAI API..."):
                        client = get_openai_client()
                        if client:
                            try:
                                # Test with a simple model call
                                with client.audio.speech.with_streaming_response.create(
                                    model="tts-1",
                                    voice="alloy",
                                    input="Connection test successful."
                                ) as response:
                                    # If we get here without exception, the API key is valid
                                    pass
                                st.success("Connection to OpenAI API successful!")
                            except Exception as e:
                                st.error(f"Connection failed: {str(e)}")
                        else:
                            st.error("Failed to initialize OpenAI client.")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Link to OpenAI API docs
            st.markdown("""
            To get an OpenAI API key:
            1. Visit [OpenAI's platform](https://platform.openai.com/signup)
            2. Create an account or sign in
            3. Navigate to the API keys section
            4. Create a new API key
            """)
        
        # PlayHT API settings
        elif api_provider == "PlayHT":
            st.subheader("PlayHT API Settings")
            
            st.markdown("<div class='api-input'>", unsafe_allow_html=True)
            playht_key = st.text_input(
                "PlayHT API Key:",
                value=st.session_state.playht_key,
                type="password",
                help="Enter your PlayHT API key."
            )
            
            playht_user_id = st.text_input(
                "PlayHT User ID:",
                value=st.session_state.playht_user_id,
                type="password",
                help="Enter your PlayHT User ID."
            )
            
            if playht_key:
                st.session_state.playht_key = playht_key
            
            if playht_user_id:
                st.session_state.playht_user_id = playht_user_id
            
            # Test connection button
            if st.button("Test PlayHT Connection"):
                if not st.session_state.playht_key or not st.session_state.playht_user_id:
                    st.error("Please enter both your PlayHT API key and User ID.")
                else:
                    with st.spinner("Testing connection to PlayHT API..."):
                        try:
                            # Make a simple API call to check credentials using the v1 API
                            url = "https://api.play.ht/api/v1/voices"
                            headers = {
                                "Accept": "application/json",
                                "Authorization": st.session_state.playht_key,
                                "X-User-ID": st.session_state.playht_user_id
                            }
                            
                            response = requests.get(url, headers=headers)
                            
                            if response.status_code == 200:
                                # Store voice models in session state
                                result = response.json()
                                voices = result.get('voices', [])
                                
                                # Format the voices to match our app structure
                                cloned_voices = []
                                for voice in voices:
                                    if voice.get('voice_engine') == 'PlayHT Cloned':
                                        formatted_voice = {
                                            'id': voice.get('id'),
                                            'name': voice.get('name'),
                                            'isCloned': True,
                                            'created_at': voice.get('created_at', 'Unknown date')
                                        }
                                        cloned_voices.append(formatted_voice)
                                
                                st.session_state.playht_voice_models = cloned_voices
                                
                                st.success("Connection to PlayHT API successful!")
                                
                                if cloned_voices:
                                    st.info(f"Found {len(cloned_voices)} cloned voices in your account.")
                                else:
                                    st.info("No cloned voices found in your account yet. Create one in the Voice Clone Studio tab.")
                            else:
                                st.error(f"Connection failed: {response.status_code} - {response.text}")
                        except Exception as e:
                            st.error(f"Connection failed: {str(e)}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Link to PlayHT API docs
            st.markdown("""
            To get PlayHT API credentials:
            1. Visit [PlayHT](https://play.ht/sign-up) to create an account
            2. Once logged in, navigate to the dashboard
            3. Go to API Access to find your API Key and User ID
            4. Copy these credentials and paste them here
            """)
        
        # Reset settings button
        if st.button("Reset All Settings"):
            for key in ['character_voices', 'audio_files', 'final_audio', 'current_step', 
                       'voice_settings', 'background_track', 'bg_volume']:
                if key in st.session_state:
                    del st.session_state[key]
            
            # Reinitialize with defaults
            st.session_state.parsed_data = []
            st.session_state.character_voices = {}
            st.session_state.audio_files = []
            st.session_state.final_audio = None
            st.session_state.current_step = 1
            st.session_state.voice_settings = {}
            st.session_state.background_track = "None"
            st.session_state.bg_volume = 0.3
            
            st.success("All settings have been reset to defaults.")
            st.rerun()
    
    # About Tab
    with tabs[3]:
        st.header("About VoiceCanvas")
        
        st.write("""
        **VoiceCanvas** is a powerful tool for transforming written scripts into expressive voice audio.
        
        ### Key Features:
        
        - **Multi-character Voice Generation**: Convert dialogues between multiple characters, each with their own voice.
        - **Emotion Support**: Add emotional context to the voices by specifying emotions in your script.
        - **Background Music**: Add ambient music to enhance the atmosphere of your audio.
        - **Voice Cloning**: Create custom voice clones with PlayHT technology.
        - **Simple Format**: Use an intuitive format for your scripts: `Character (emotion): Dialogue`
        
        ### Use Cases:
        
        - Creating audiobooks with multiple characters
        - Developing voice content for games and animations
        - Prototyping podcast scripts
        - Creating educational content with different voices
        - Accessibility tools for converting text to speech
        
        ### Credits:
        
        - Voice synthesis powered by OpenAI's TTS API and PlayHT
        - Audio processing with Pydub
        - UI built with Streamlit
        """)
        
        # Version info
        st.info("Version 1.0.0")

# Run the app
if __name__ == "__main__":
    main()
