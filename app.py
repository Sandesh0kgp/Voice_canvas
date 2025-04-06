# Define enhanced CSS
enhanced_css = """
<style>
    /* Global Theme */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        border-radius: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }
    
    /* Typography */
    .main-header {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(120deg, #19A7CE 0%, #146C94 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        animation: fadeIn 1.2s ease-in-out;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #146C94;
        margin-bottom: 2.5rem;
        text-align: center;
        font-weight: 400;
        opacity: 0.9;
        animation: slideUp 1s ease-in-out;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(120deg, #19A7CE 0%, #146C94 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(25, 167, 206, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(25, 167, 206, 0.3);
    }
    
    .stButton>button:active {
        transform: translateY(1px);
    }
    
    /* Input Fields */
    .api-input {
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
        padding: 1.5rem;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 0.8rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #19A7CE;
        transition: all 0.3s ease;
    }
    
    .api-input:hover {
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        background-color: rgba(255, 255, 255, 0.95);
    }
    
    /* Section Styling */
    .css-1r6slb0, .css-1inwz65 {
        border-radius: 0.8rem;
        border: 1px solid rgba(25, 167, 206, 0.2);
        background-color: rgba(255, 255, 255, 0.8);
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .css-163ttbj {
        background-color: #f0f7fa;
        border-right: 1px solid rgba(25, 167, 206, 0.2);
    }
    
    /* Audio Player */
    audio {
        width: 100%;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        background: #146C94;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0;
            transform: translateY(20px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Expanders and Selectboxes */
    .streamlit-expanderHeader, .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 0.5rem;
        border: 1px solid rgba(25, 167, 206, 0.2);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover, .stSelectbox > div > div:hover {
        background-color: rgba(255, 255, 255, 0.9);
        border-color: rgba(25, 167, 206, 0.4);
    }
    
    /* Text Area */
    .stTextArea > div > div {
        border-radius: 0.5rem;
        border: 1px solid rgba(25, 167, 206, 0.3);
        box-shadow: 0 1px 5px rgba(0, 0, 0, 0.03);
    }
    
    .stTextArea > div > div:focus-within {
        border-color: #19A7CE;
        box-shadow: 0 0 0 1px #19A7CE;
    }
    
    /* Dataframe/Table Styling */
    .dataframe {
        border-radius: 0.5rem;
        overflow: hidden;
        border: none !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .dataframe th {
        background-color: #19A7CE !important;
        color: white !important;
        font-weight: 600;
        padding: 0.75rem 1rem !important;
    }
    
    .dataframe td {
        padding: 0.6rem 1rem !important;
        border-bottom: 1px solid #f0f2f6;
        background-color: white;
    }
    
    .dataframe tr:nth-child(even) td {
        background-color: #f9fafc;
    }
    
    /* Tooltips */
    .stTooltipIcon {
        color: #19A7CE !important;
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
    """Route to appropriate voice generation function based on API provider."""
    if st.session_state.api_provider == "openai" and st.session_state.api_key:
        return generate_voice_openai(text, voice_model, speed, pitch, emotion)
    else:
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
    
    # Export combined audio
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    combined.export(output_path, format="mp3")
    return output_path

# Function to save user preferences
def save_user_preferences(preferences):
    """Save user preferences to a file."""
    # In a real implementation, this would save to a database
    # For now, we'll just print the preferences
    print(f"Saving preferences: {preferences}")
    return True

# Function to get voice settings for a character
def get_voice_settings(character):
    """Get the voice settings for a character."""
    if character not in st.session_state.voice_settings:
        st.session_state.voice_settings[character] = {
            "speed": 1.0,
            "pitch": 0.0
        }
    return st.session_state.voice_settings[character]

# Function to get the voice model ID from name
def get_voice_model_id(voice_name):
    """Get the voice model ID from the voice name."""
    if st.session_state.api_provider == "openai":
        return openai_voice_models.get(voice_name, "alloy")
    else:
        # For mock API, just return the name
        return voice_name.lower().replace(" ", "_")

# App header
st.markdown("<h1 class='main-header'>VoiceCanvas</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Transform Text into Character-Driven Audio</h2>", unsafe_allow_html=True)

# API Key Configuration
with st.sidebar:
    st.title("API Configuration")
    
    api_provider = st.radio("Select API Provider", ["OpenAI", "Mock (No API)"], index=0 if st.session_state.api_provider == "openai" else 1)
    st.session_state.api_provider = api_provider.lower()
    
    if st.session_state.api_provider == "openai":
        api_key = st.text_input("Enter OpenAI API Key", type="password", value=st.session_state.api_key if st.session_state.api_key else "")
        if api_key:
            st.session_state.api_key = api_key
            st.success("API Key set successfully!")
        else:
            st.warning("Please enter your OpenAI API key to use voice generation.")
    
    st.markdown("---")
    st.title("Navigation")
    step = st.radio(
        "Process Steps",
        ["1. Text Input", "2. Character Mapping", "3. Voice Generation", "4. Audio Output"],
        index=st.session_state.current_step - 1
    )
    
    # Update current step based on selection
    st.session_state.current_step = int(step[0])

# Step 1: Text Input
if st.session_state.current_step == 1:
    st.header("Step 1: Upload or Enter Your Text")
    
    input_method = st.radio("Choose input method:", ["Upload File", "Direct Text Entry"])
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload your script or story file", type=['txt'])
        if uploaded_file is not None:
            try:
                st.session_state.parsed_data = parse_text_from_file(uploaded_file)
                st.success(f"Successfully parsed {len(st.session_state.parsed_data)} dialogue entries!")
                
                # Display parsed data
                st.subheader("Preview:")
                for i, entry in enumerate(st.session_state.parsed_data[:5]):
                    emotion_text = f" ({entry['emotion']})" if entry['emotion'] else ""
                    st.text(f"{entry['character']}{emotion_text}: {entry['dialogue'][:50]}...")
                
                if len(st.session_state.parsed_data) > 5:
                    st.text(f"... and {len(st.session_state.parsed_data) - 5} more entries")
                
                # Continue button
                if st.button("Continue to Character Mapping"):
                    st.session_state.current_step = 2
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error parsing file: {str(e)}")
    
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
            try:
                st.session_state.parsed_data = parse_text_from_string(text_input)
                st.success(f"Successfully parsed {len(st.session_state.parsed_data)} dialogue entries!")
                
                # Display parsed data
                st.subheader("Preview:")
                for entry in st.session_state.parsed_data:
                    emotion_text = f" ({entry['emotion']})" if entry['emotion'] else ""
                    st.text(f"{entry['character']}{emotion_text}: {entry['dialogue'][:50]}...")
                
                # Continue button
                if st.button("Continue to Character Mapping"):
                    st.session_state.current_step = 2
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error parsing text: {str(e)}")

# Step 2: Character Mapping
elif st.session_state.current_step == 2:
    st.header("Step 2: Map Characters to Voices")
    
    if not st.session_state.parsed_data:
        st.warning("Please upload or enter your text first!")
        if st.button("Go Back to Text Input"):
            st.session_state.current_step = 1
            st.rerun()
    else:
        # Get unique characters
        characters = list(set([entry['character'] for entry in st.session_state.parsed_data]))
        
        st.subheader("Assign voices to characters")
        
        # Select voice models based on API provider
        voice_models_to_use = openai_voice_models if st.session_state.api_provider == "openai" else {
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
        
        # Create a form for character mapping
        with st.form("character_mapping_form"):
            for character in characters:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    voice_selection = st.selectbox(
                        f"Voice for {character}:",
                        options=list(voice_models_to_use.keys()),
                        key=f"voice_{character}",
                        index=0
                    )
                    st.session_state.character_voices[character] = voice_selection
                
                with col2:
                    # Advanced settings expander
                    with st.expander("Voice Settings"):
                        settings = get_voice_settings(character)
                        settings["speed"] = st.slider(
                            "Speed:", 
                            min_value=0.5, 
                            max_value=2.0,
                            value=settings.get("speed", 1.0),
                            step=0.1,
                            key=f"speed_{character}"
                        )
                        
                        # Store the updated settings
                        st.session_state.voice_settings[character] = settings
            
            submit_button = st.form_submit_button("Save Voice Mappings")
        
        if submit_button:
            st.success("Voice mappings saved successfully!")
            
            # Show a preview button for testing
            if st.button("Preview a Random Line"):
                # Select a random entry
                import random
                entry = random.choice(st.session_state.parsed_data)
                
                # Get voice model for this character
                voice_name = st.session_state.character_voices.get(entry["character"], list(voice_models_to_use.keys())[0])
                voice_model = get_voice_model_id(voice_name)
                
                # Get voice settings
                settings = get_voice_settings(entry["character"])
                
                # Generate preview audio
                with st.spinner(f"Generating preview for '{entry['character']}'..."):
                    audio_file = generate_voice(
                        entry["dialogue"],
                        voice_model,
                        speed=settings["speed"],
                        emotion=entry["emotion"]
                    )
                    
                    if audio_file:
                        st.audio(audio_file)
                    else:
                        st.error("Failed to generate preview audio.")
            
            # Continue button
            if st.button("Continue to Voice Generation"):
                # Move to next step
                st.session_state.current_step = 3
                st.rerun()

# Step 3: Voice Generation
elif st.session_state.current_step == 3:
    st.header("Step 3: Generate Character Voices")
    
    if not st.session_state.parsed_data or not st.session_state.character_voices:
        st.warning("Please map characters to voices first!")
        if st.button("Go Back to Character Mapping"):
            st.session_state.current_step = 2
            st.rerun()
    else:
        # API warning if needed
        if st.session_state.api_provider == "openai" and not st.session_state.api_key:
            st.warning("⚠️ No OpenAI API key provided. Using mock audio generation instead. For real voice generation, please add your API key in the sidebar.")
        
        # Select voice models based on API provider
        voice_models_to_use = openai_voice_models if st.session_state.api_provider == "openai" else {
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
        
        # Voice customization options
        st.subheader("Voice Customization (Optional)")
        
        col1, col2 = st.columns(2)
        with col1:
            speed = st.slider("Speech Speed:", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        with col2:
            pitch = st.slider("Voice Pitch:", min_value=-20, max_value=20, value=0, step=5)
            
        # Background music selection
        st.subheader("Background Music (Optional)")
        st.markdown("🎵 Add ambient sounds or music to enhance your audio story and create an immersive atmosphere.")
        
        # Create a card-like interface for track selection
        track_container = st.container()
        with track_container:
            col1, col2 = st.columns(2)
            
            with col1:
                # Background track selection with better descriptions
                track_descriptions = {
                    "None": "No background audio",
                    "Peaceful Nature": "Gentle ambient sounds of a forest with occasional bird chirps",
                    "Sci-Fi Ambience": "Futuristic electronic tones and subtle beeps",
                    "Suspenseful Mystery": "Tense atmospheric sounds with occasional startling elements",
                    "Fantasy Adventure": "Mystical ambient sounds with magical chimes",
                    "Urban City": "City atmosphere with distant traffic and occasional street sounds",
                    "Romantic Scene": "Soft, gentle ambient tones for emotional moments",
                    "Horror Ambience": "Dark, unsettling sounds with occasional suspenseful elements",
                    "Comedy Background": "Light, playful ambient sounds for humorous scenes"
                }
                
                background_track = st.selectbox(
                    "Select Background Track:",
                    options=list(BACKGROUND_TRACKS.keys()),
                    index=list(BACKGROUND_TRACKS.keys()).index(st.session_state.background_track) if st.session_state.background_track in BACKGROUND_TRACKS else 0,
                    format_func=lambda x: x  # Just show the name in the dropdown
                )
                st.session_state.background_track = background_track
                
                # Show description of selected track
                if background_track != "None":
                    st.info(track_descriptions.get(background_track, ""))
            
            with col2:
                bg_volume = st.slider(
                    "Background Volume:", 
                    min_value=0.1, 
                    max_value=0.5, 
                    value=st.session_state.bg_volume,
                    step=0.05,
                    format="%d%%",  # Format as percentage
                    help="Higher values make background sounds louder relative to voices."
                )
                st.session_state.bg_volume = bg_volume
                
                # Show a visual indicator of the volume level
                vol_percent = int(bg_volume * 100)
                if vol_percent < 20:
                    st.caption("🔈 Subtle background (recommended for dialogue-heavy content)")
                elif vol_percent < 35:
                    st.caption("🔉 Balanced mix of speech and background")
                else:
                    st.caption("🔊 Prominent background (good for atmospheric scenes)")
                    
        # Reset button for background settings
        if st.button("Reset Background Settings"):
            st.session_state.background_track = "None"
            st.session_state.bg_volume = 0.3
            st.rerun()
        
        # Generate button
        if st.button("Generate Audio"):
            # Clear previous audio files
            st.session_state.audio_files = []
            
            # Show progress
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                character_info = st.empty()
                dialogue_preview = st.empty()
            
            # Process each dialogue entry
            for i, entry in enumerate(st.session_state.parsed_data):
                character = entry['character']
                emotion_text = f" ({entry['emotion']})" if entry['emotion'] else ""
                dialogue = entry['dialogue']
                
                # Update status display
                status_text.markdown(f"**Generating audio...** ({i+1}/{len(st.session_state.parsed_data)})")
                character_info.markdown(f"🎭 **Character:** {character}{emotion_text}")
                dialogue_preview.markdown(f"💬 \"{dialogue[:100]}{'...' if len(dialogue) > 100 else ''}\"")
                
                try:
                    # Get voice model for this character
                    voice_name = st.session_state.character_voices.get(character)
                    voice_model_id = get_voice_model_id(voice_name)
                    
                    # Generate audio for this dialogue
                    audio_file = generate_voice(
                        text=dialogue,
                        voice_model=voice_model_id,
                        speed=speed,
                        pitch=pitch,
                        emotion=entry.get('emotion', None)
                    )
                    
                    if audio_file:
                        st.session_state.audio_files.append({
                            'character': character,
                            'dialogue': dialogue,
                            'file_path': audio_file
                        })
                except Exception as e:
                    st.error(f"Error generating audio for {character}: {str(e)}")
                
                # Update progress
                progress_bar.progress((i + 1) / len(st.session_state.parsed_data))
            
            # Combine all audio files
            if st.session_state.audio_files:
                status_text.text("Combining audio files...")
                try:
                    file_paths = [af['file_path'] for af in st.session_state.audio_files]
                    
                    # Get background track and volume settings
                    background_track = BACKGROUND_TRACKS.get(st.session_state.background_track)
                    bg_volume = st.session_state.bg_volume
                    
                    # If background track is selected, add an info message
                    if background_track and background_track != "None":
                        status_text.text(f"Adding '{st.session_state.background_track}' background track...")
                    
                    # Combine audio with background music if selected
                    final_audio = combine_audio_files(
                        file_paths, 
                        background_track=background_track, 
                        bg_volume=bg_volume
                    )
                    
                    st.session_state.final_audio = final_audio
                    status_text.text("Audio generation complete!")
                    
                    # Continue button
                    if st.button("Continue to Audio Output"):
                        st.session_state.current_step = 4
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Error combining audio files: {str(e)}")

# Step 4: Audio Output
elif st.session_state.current_step == 4:
    st.header("Step 4: Listen to Your Audio Story")
    
    if not st.session_state.final_audio:
        st.warning("Please generate audio first!")
        if st.button("Go Back to Voice Generation"):
            st.session_state.current_step = 3
            st.rerun()
    else:
        st.subheader("Final Audio")
        
        # Show background track info if used
        if st.session_state.background_track != "None":
            st.info(f"Background Track: {st.session_state.background_track} (Volume: {int(st.session_state.bg_volume * 100)}%)")
        
        # Display audio player
        st.audio(st.session_state.final_audio)
        
        # Download button
        with open(st.session_state.final_audio, "rb") as file:
            btn = st.download_button(
                label="Download Audio",
                data=file,
                file_name="voicecanvas_story.mp3",
                mime="audio/mp3"
            )
        
        # Individual character audio clips
        st.subheader("Individual Character Clips")
        for audio_entry in st.session_state.audio_files:
            with st.expander(f"{audio_entry['character']}: {audio_entry['dialogue'][:50]}..."):
                st.audio(audio_entry['file_path'])
        
        # Feedback section
        st.subheader("Provide Feedback")
        feedback = st.text_area("How was your experience? Any suggestions for improvement?")
        if st.button("Submit Feedback"):
            # Here you would typically save the feedback to a database
            st.success("Thank you for your feedback!")
            
        # Start over button
        if st.button("Start New Project"):
            # Reset session state
            st.session_state.parsed_data = []
            st.session_state.character_voices = {}
            st.session_state.audio_files = []
            st.session_state.final_audio = None
            st.session_state.background_track = "None"
            st.session_state.bg_volume = 0.3
            st.session_state.current_step = 1
            st.rerun()

# Footer
st.markdown("---")
st.markdown("© 2025 VoiceCanvas | Developed for KUKU FM Project K")
