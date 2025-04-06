import streamlit as st
import re
import tempfile
import os
import time
import json
import random
import shutil
from datetime import datetime
import pandas as pd
from pydub import AudioSegment
from openai import OpenAI
import groq
import requests
from io import BytesIO
import base64

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
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
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
    
    /* Story Text Container */
    .story-text-container {
        background: linear-gradient(135deg, #f0f3ff 0%, #e8ecff 100%);
        border-radius: 10px;
        padding: 16px 20px;
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 20px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.04);
        font-family: 'Poppins', sans-serif;
    }
    
    .story-text-container p {
        border-bottom: 1px solid rgba(108, 99, 255, 0.1);
        padding-bottom: 12px;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    
    .story-text-container p:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    
    .story-text-container strong {
        color: #6C63FF;
        font-weight: 600;
    }
    
    .story-text-container em {
        color: #8B5CF6;
        font-style: italic;
        font-weight: 500;
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
    
    /* File Uploader */
    .stFileUploader > div:first-child {
        background: linear-gradient(135deg, #f9f9ff 0%, #f0f3ff 100%);
        border-radius: 12px;
        padding: 16px;
        border: 2px dashed #6C63FF;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    
    .stFileUploader > div:first-child:hover {
        background: linear-gradient(135deg, #f0f3ff 0%, #e7ecff 100%);
        transform: translateY(-2px);
        border-color: #FF6584;
    }
    
    /* Radio Buttons */
    .stRadio > div {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
    }
    
    /* Special Effects */
    .shimmer-effect {
        background: linear-gradient(90deg, 
                   rgba(255,255,255,0) 0%, 
                   rgba(255,255,255,0.8) 50%, 
                   rgba(255,255,255,0) 100%);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }
    
    .floating-element {
        animation: float 6s ease-in-out infinite;
    }
    
    /* Feature Card */
    .feature-card {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 4px solid #FF6584;
        transition: all 0.3s ease;
        margin-bottom: 15px;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        background: rgba(255, 255, 255, 0.9);
    }
</style>
"""

# Configure pydub to use the correct ffmpeg path
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
if 'elevenlabs_key' not in st.session_state:
    st.session_state.elevenlabs_key = "sk_52ac7a1f66a90f04186d0e677e526f3ddaffc3eef20cc796"
if 'elevenlabs_voice_models' not in st.session_state:
    st.session_state.elevenlabs_voice_models = {}  # Initialize as an empty dictionary
if 'elevenlabs_voice_name' not in st.session_state:
    st.session_state.elevenlabs_voice_name = "Stygian Great White Shark"
if 'openai_key' not in st.session_state:
    st.session_state.openai_key = os.environ.get("OPENAI_API_KEY")
if 'deepdub_key' not in st.session_state:
    st.session_state.deepdub_key = "dd-Rn71rk7wpT8XcrBXqvoyqoku5W6ZBMLm39a70bb4"
if 'deepdub_email' not in st.session_state:
    st.session_state.deepdub_email = "sandeshpatil0604@gmail.com"
if 'openai_voice' not in st.session_state:
    st.session_state.openai_voice = "alloy"
if 'dubbed_audio' not in st.session_state:
    st.session_state.dubbed_audio = None
if 'deepdub_voice_models' not in st.session_state:
    st.session_state.deepdub_voice_models = {}
if 'uploaded_audio' not in st.session_state:
    st.session_state.uploaded_audio = None
if 'story_text' not in st.session_state:
    st.session_state.story_text = None

# Define voice models
openai_voice_models = {
    "Alloy (Neutral)": "alloy",
    "Echo (Male)": "echo",
    "Fable (Male)": "fable",
    "Onyx (Male)": "onyx",
    "Nova (Female)": "nova",
    "Shimmer (Female)": "shimmer"
}

# Define ElevenLabs constants
ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"
DEEPDUB_API_BASE = "https://api.deepdub.ai/v1"

# Function to initialize OpenAI client
def get_openai_client():
    if 'openai_key' in st.session_state and st.session_state.openai_key:
        return OpenAI(api_key=st.session_state.openai_key)
    elif 'api_key' in st.session_state and st.session_state.api_key:
        return OpenAI(api_key=st.session_state.api_key)
    return None
    
# Function to initialize Groq client
def get_groq_client():
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if groq_api_key:
        return groq.Client(api_key=groq_api_key)
    return None
    
# Function to convert paragraph to dialogue format using Groq
def convert_paragraph_to_dialogue(text):
    """Convert paragraph text to dialogue format using Groq API."""
    try:
        client = get_groq_client()
        if not client:
            st.error("Groq API key not set. Please provide a valid API key.")
            return text
            
        # Create prompt for dialogue conversion
        prompt = f"""
        Convert the following paragraph into a dialogue format with character names, 
        emotions in parentheses, and spoken lines. Format each line as "Character (emotion): Dialogue".
        Ensure the dialogue is natural and flows well between characters.
        
        Paragraph: {text}
        
        Please return only the dialogue without any additional explanation.
        """
        
        # Generate dialogue using Groq API
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a skilled dialogue writer that converts paragraphs into natural dialogue format."},
                {"role": "user", "content": prompt}
            ]
        )
        
        dialogue_text = completion.choices[0].message.content.strip()
        return dialogue_text
        
    except Exception as e:
        st.error(f"Error converting text to dialogue format: {str(e)}")
        return text  # Return original text if conversion fails

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

# Function to parse text from uploaded file
def parse_text_from_file(file):
    """Parse text from uploaded file."""
    try:
        # Read file content based on file type
        file_content = file.getvalue().decode("utf-8")
        return parse_text_from_string(file_content)
    except Exception as e:
        st.error(f"Error parsing file: {str(e)}")
        return []

# Function to generate voice using OpenAI TTS
def generate_voice_openai(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Generate voice audio from text using OpenAI's TTS API."""
    try:
        client = get_openai_client()
        if not client:
            st.error("OpenAI API key not set. Please provide a valid API key.")
            return None
            
        # Extract text without emotion tags
        text_without_emotion = text
        
        # Create temporary file to store audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            # Generate speech using OpenAI API
            response = client.audio.speech.create(
                model="tts-1-hd",
                voice=voice_model,
                input=text_without_emotion,
                speed=speed
            )
            
            # Write response to temporary file
            response.stream_to_file(temp_file.name)
            
            return temp_file.name
            
    except Exception as e:
        st.error(f"Error generating voice with OpenAI: {str(e)}")
        return None

# Function to fetch available voice models from ElevenLabs
def fetch_elevenlabs_voices():
    """Fetch available voice models from ElevenLabs API."""
    try:
        # Check if API key is set
        if not st.session_state.elevenlabs_key:
            st.error("ElevenLabs API key not set. Please provide a valid API key.")
            return {}
            
        # Set up headers with API key
        headers = {
            "xi-api-key": st.session_state.elevenlabs_key,
            "Content-Type": "application/json"
        }
        
        # Make API request to fetch voices
        response = requests.get(f"{ELEVENLABS_API_BASE}/voices", headers=headers)
        
        if response.status_code == 200:
            voices_data = response.json()
            
            # Extract voices and their IDs and store them as a dictionary
            voices = {voice['name']: voice['voice_id'] for voice in voices_data['voices']}
            
            # Create a DataFrame with voice information for display
            voices_info = []
            for voice in voices_data['voices']:
                voices_info.append({
                    "Name": voice['name'],
                    "Voice ID": voice['voice_id'],
                    "Category": voice.get('category', 'N/A'),
                    "Labels": ", ".join([f"{k}: {v}" for k, v in voice.get('labels', {}).items()])
                })
                
            voices_df = pd.DataFrame(voices_info)
            
            # Return voices dictionary
            return voices
        else:
            st.error(f"Failed to fetch ElevenLabs voices. Status code: {response.status_code}")
            st.error(f"Response: {response.text}")
            return {}
            
    except Exception as e:
        st.error(f"Error fetching ElevenLabs voices: {str(e)}")
        return {}

# Function to generate voice using ElevenLabs
def generate_voice_elevenlabs(text, voice_id, stability=0.5, similarity_boost=0.75, emotion=None):
    """Generate voice audio from text using ElevenLabs API."""
    try:
        # Check if API key is set
        if not st.session_state.elevenlabs_key:
            st.error("ElevenLabs API key not set. Please provide a valid API key.")
            return None
            
        # Set up headers with API key
        headers = {
            "xi-api-key": st.session_state.elevenlabs_key,
            "Content-Type": "application/json"
        }
        
        # Extract text without emotion tags
        text_without_emotion = text
        
        # Prepare request data
        data = {
            "text": text_without_emotion,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }
        
        # Make API request
        response = requests.post(
            f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}/stream",
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            # Save the audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(response.content)
                return temp_file.name
        else:
            st.error(f"Failed to generate audio with ElevenLabs. Status code: {response.status_code}")
            st.error(f"Response: {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error generating voice with ElevenLabs: {str(e)}")
        return None

# Function to concatenate audio files
def concatenate_audio_files(audio_files, output_path, background_track=None, bg_volume=0.3):
    """Concatenate multiple audio files into a single audio file."""
    try:
        if not audio_files:
            return None
            
        # Load the first audio file
        combined = AudioSegment.from_file(audio_files[0])
        
        # Add a short pause between utterances
        pause = AudioSegment.silent(duration=1000)  # 1-second pause
        
        # Concatenate remaining audio files
        for audio_file in audio_files[1:]:
            next_segment = AudioSegment.from_file(audio_file)
            combined += pause + next_segment
            
        # Add background music if specified
        if background_track and background_track != "None":
            bg_audio = AudioSegment.from_file(background_track)
            
            # Loop background audio to match the length of narration
            while len(bg_audio) < len(combined):
                bg_audio += bg_audio
                
            # Trim background audio to match narration length
            bg_audio = bg_audio[:len(combined)]
            
            # Adjust volume of background audio
            bg_audio = bg_audio - (20 - (bg_volume * 20))  # Adjust volume based on bg_volume (0.1-1.0)
            
            # Mix narration with background audio
            combined = combined.overlay(bg_audio)
            
        # Export the combined audio
        combined.export(output_path, format="mp3")
        return output_path
        
    except Exception as e:
        st.error(f"Error concatenating audio files: {str(e)}")
        return None

# Function to clean up temporary files
def cleanup_temp_files(file_list):
    """Delete temporary files to clean up."""
    for file_path in file_list:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            st.warning(f"Could not remove temporary file {file_path}: {str(e)}")

# OpenAI dubbing function
def openai_dubbing(audio_file_path, target_language="en", voice="alloy"):
    """Dub audio content to a different language using OpenAI."""
    try:
        client = get_openai_client()
        if not client:
            st.error("OpenAI API key not set. Please provide a valid API key.")
            return None
        
        # First, transcribe the audio to text using Whisper
        with open(audio_file_path, "rb") as audio_file:
            transcription_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        
        transcribed_text = transcription_response
        
        # Now translate the transcribed text to the target language
        translation_prompt = f"Translate the following text to {target_language}. Maintain the tone and meaning:\n\n{transcribed_text}"
        
        translation_response = client.chat.completions.create(
            model="gpt-4o",  # Using GPT-4o for high-quality translation
            messages=[
                {"role": "system", "content": f"You are a professional translator for {target_language}."},
                {"role": "user", "content": translation_prompt}
            ]
        )
        
        translated_text = translation_response.choices[0].message.content.strip()
        
        # Finally, convert the translated text to speech in the target language
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            speech_response = client.audio.speech.create(
                model="tts-1-hd",
                voice=voice,
                input=translated_text
            )
            
            speech_response.stream_to_file(temp_file.name)
            return temp_file.name
            
    except Exception as e:
        st.error(f"Error during OpenAI dubbing: {str(e)}")
        return None

# ElevenLabs dubbing function
def elevenlabs_dubbing(audio_file_path, target_language="en", voice_id=None):
    """Dub audio content to a different language using ElevenLabs."""
    try:
        client = get_openai_client()  # For transcription and translation
        if not client or not st.session_state.elevenlabs_key:
            st.error("OpenAI and ElevenLabs API keys are required for this operation.")
            return None
        
        # First, transcribe the audio to text using Whisper
        with open(audio_file_path, "rb") as audio_file:
            transcription_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        
        transcribed_text = transcription_response
        
        # Now translate the transcribed text to the target language
        translation_prompt = f"Translate the following text to {target_language}. Maintain the tone and meaning:\n\n{transcribed_text}"
        
        translation_response = client.chat.completions.create(
            model="gpt-4o",  # Using GPT-4o for high-quality translation
            messages=[
                {"role": "system", "content": f"You are a professional translator for {target_language}."},
                {"role": "user", "content": translation_prompt}
            ]
        )
        
        translated_text = translation_response.choices[0].message.content.strip()
        
        # Finally, convert the translated text to speech using ElevenLabs
        # Set up headers with API key
        headers = {
            "xi-api-key": st.session_state.elevenlabs_key,
            "Content-Type": "application/json"
        }
        
        # Prepare request data
        data = {
            "text": translated_text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        # Make API request
        response = requests.post(
            f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}/stream",
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            # Save the audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(response.content)
                return temp_file.name
        else:
            st.error(f"Failed to generate dubbed audio with ElevenLabs. Status code: {response.status_code}")
            st.error(f"Response: {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Error during ElevenLabs dubbing: {str(e)}")
        return None

# Generate voice with DeepDub (commented out as it's not working)
def generate_voice_deepdub(text, voice_id=None, language="en"):
    """Generate voice audio from text using DeepDub API."""
    # This function is currently commented out as DeepDub API is not working properly
    pass

# DeepDub dubbing function (commented out as it's not working)
def deepdub_dubbing(audio_file_path, target_language="en", voice_id=None):
    """Dub audio content to a different language using DeepDub."""
    # This function is currently commented out as DeepDub API is not working properly
    pass

# Fetch DeepDub voices function (commented out as it's not working)
def fetch_deepdub_voices():
    """Fetch available voice models from DeepDub API."""
    # This function is currently commented out as DeepDub API is not working properly
    pass

# Helper function to get ElevenLabs voice ID by name
def get_elevenlabs_voice_id_by_name(voice_name, voices_dict):
    """Get voice ID from voice name."""
    return voices_dict.get(voice_name)

# Main function
def main():
    # App header and subheader
    st.markdown('<h1 class="main-header">🎨 VoiceCanvas</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create expressive voice narrations from your text</p>', unsafe_allow_html=True)
    
    # Tab selection with emoji-enhanced radio buttons
    tab = st.radio(
        "Choose functionality:",
        ["✨ Voice Generation", "🌍 Voice Dubbing"],
        horizontal=True,
        key="main_tab_selector"
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Voice Generation tab
    if tab == "✨ Voice Generation":
        # API Setup section
        with st.expander("🔑 API Setup", expanded=False):
            st.markdown("""
            <div class="feature-card">
                <h3 style="margin-top:0; color:#6C63FF;">🔐 API Configuration</h3>
                <p>Set up your voice provider API keys to enable voice generation.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # API provider selection
            api_provider = st.selectbox(
                "Select API Provider",
                ["OpenAI TTS", "ElevenLabs"]
            )
            
            # API key input
            if api_provider == "OpenAI TTS":
                openai_key = st.text_input(
                    "Enter your OpenAI API key",
                    value=st.session_state.openai_key if st.session_state.openai_key else "",
                    type="password"
                )
                if openai_key:
                    st.session_state.openai_key = openai_key
                    st.success("OpenAI API key set successfully!")
                
            elif api_provider == "ElevenLabs":
                elevenlabs_key = st.text_input(
                    "Enter your ElevenLabs API key",
                    value=st.session_state.elevenlabs_key if st.session_state.elevenlabs_key else "",
                    type="password"
                )
                if elevenlabs_key:
                    st.session_state.elevenlabs_key = elevenlabs_key
                    st.success("ElevenLabs API key set successfully!")
                    
                # Fetch ElevenLabs voices
                if st.button("Fetch ElevenLabs Voices"):
                    with st.spinner("Fetching voices from ElevenLabs..."):
                        voices = fetch_elevenlabs_voices()
                        if voices:
                            st.session_state.elevenlabs_voice_models = voices
                            st.success(f"Successfully fetched {len(voices)} voices from ElevenLabs!")
                        else:
                            st.error("Failed to fetch voices from ElevenLabs.")
            
        # Progress steps display
        st.markdown("""
        <div class="step-container">
            <div class="step-line"></div>
            <div class="step active">1</div>
            <div class="step">2</div>
            <div class="step">3</div>
            <div class="step">4</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 1: Enter Your Text
        st.subheader("Step 1: Enter Your Text")
        
        # Example format expander
        with st.expander("📝 Example Format", expanded=False):
            st.write("""
            Format your dialogue like this:
            ```
            Arjun (excited): I love to fold paper planes!
            Teacher (curious): Why do you enjoy it so much?
            Arjun (enthusiastic): Because they can fly so high!
            ```
            
            Character names followed by optional emotion in parentheses, then a colon, then the dialogue.
            """)
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["Enter text", "Upload file", "Use template"],
            horizontal=True
        )
        
        # Handle different input methods
        if input_method == "Enter text":
            text_input = st.text_area(
                "Enter your text:",
                height=300,
                placeholder="Enter your story or dialogue here..."
            )
            
            if text_input:
                # Check if the text is in paragraph format and offer conversion
                if ":" not in text_input:
                    is_paragraph = st.checkbox("Convert paragraph to dialogue format using Groq API")
                    
                    if is_paragraph:
                        if st.button("Convert to Dialogue"):
                            with st.spinner("Converting text to dialogue format..."):
                                dialogue_text = convert_paragraph_to_dialogue(text_input)
                                st.markdown("""
                                <div style="padding: 15px; background-color: rgba(255, 255, 255, 0.7); 
                                            border-radius: 10px; margin: 20px 0; 
                                            border-left: 5px solid #4F46E5; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                                    <h3 style="margin-top:0; color:#4F46E5;">Converted to dialogue format:</h3>
                                """, unsafe_allow_html=True)
                                
                                # Display converted dialogue
                                st.write(dialogue_text)
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                                # Save story text for later display
                                st.session_state.story_text = dialogue_text
                                
                                # Parse the dialogue text into structured data
                                parsed_data = parse_text_from_string(dialogue_text)
                                st.session_state.parsed_data = parsed_data
                                st.success(f"Successfully parsed {len(parsed_data)} lines of dialogue.")
                    else:
                        # Save story text for later display
                        st.session_state.story_text = text_input
                        
                        # Parse the text into structured data
                        parsed_data = parse_text_from_string(text_input)
                        st.session_state.parsed_data = parsed_data
                        st.success(f"Successfully parsed {len(parsed_data)} lines of dialogue.")
                else:
                    # Save story text for later display
                    st.session_state.story_text = text_input
                    
                    # Parse the text into structured data
                    parsed_data = parse_text_from_string(text_input)
                    st.session_state.parsed_data = parsed_data
                    st.success(f"Successfully parsed {len(parsed_data)} lines of dialogue.")
                
        elif input_method == "Upload file":
            uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
            
            if uploaded_file:
                # Parse the uploaded file
                parsed_data = parse_text_from_file(uploaded_file)
                
                if parsed_data:
                    st.session_state.parsed_data = parsed_data
                    st.success(f"Successfully parsed {len(parsed_data)} lines of dialogue.")
                    
                    # Save story text for later display
                    file_content = uploaded_file.getvalue().decode("utf-8")
                    st.session_state.story_text = file_content
                    
        elif input_method == "Use template":
            template_options = [
                "Children's Story",
                "Interview",
                "Drama Scene",
                "Podcast Excerpt"
            ]
            
            selected_template = st.selectbox("Select a template", template_options)
            
            # Load template based on selection
            if selected_template == "Children's Story":
                template_text = """Narrator: Once upon a time, in a magical forest, there lived a little squirrel named Sam.
Sam (excited): I'm going to collect so many acorns today!
Owl (wise): Just be careful not to wander too far, young one.
Sam (curious): But what's beyond the ancient oak tree?
Owl (cautious): The unknown can be both wonderful and dangerous.
Narrator: Sam's whiskers twitched with anticipation as he scampered towards adventure."""
                
            elif selected_template == "Interview":
                template_text = """Host (professional): Welcome to tonight's interview with renowned scientist Dr. Jane Maxwell.
Jane (confident): Thank you for having me. I'm excited to share our latest findings.
Host (curious): Your recent discovery has been called revolutionary. How did it all begin?
Jane (reflective): It started with a simple question that nobody had thought to ask before.
Host (intrigued): And what was that question?
Jane (passionate): What if everything we thought we knew about quantum physics was just the beginning?"""
                
            elif selected_template == "Drama Scene":
                template_text = """David (angry): I can't believe you would do this to me, after everything we've been through!
Sarah (defensive): You're not being fair! You never even gave me a chance to explain.
David (hurt): What is there to explain? I saw the messages, Sarah.
Sarah (tearful): It's not what you think, I promise. Please, just listen to me.
David (conflicted): I want to believe you, but how can I trust you now?
Sarah (determined): Because in fifteen years, have I ever given you a reason not to?"""
                
            elif selected_template == "Podcast Excerpt":
                template_text = """Mike (enthusiastic): Hey everyone, welcome back to Tech Talk! I'm your host Mike.
Julie (cheerful): And I'm Julie! Today we're discussing the latest smartphone releases.
Mike (inquisitive): Julie, what did you think of the new features announced this week?
Julie (thoughtful): Honestly, I'm not as impressed as I expected to be. It feels incremental rather than innovative.
Mike (agreeing): I felt the same way. It seems like companies are playing it safe these days.
Julie (optimistic): Though that new camera system might be a game-changer for mobile photography."""
                
            # Display the template
            st.text_area("Template", value=template_text, height=300, key="template_area")
            
            if st.button("Use This Template"):
                # Parse the template text
                parsed_data = parse_text_from_string(template_text)
                
                if parsed_data:
                    st.session_state.parsed_data = parsed_data
                    st.success(f"Successfully parsed {len(parsed_data)} lines of dialogue.")
                    
                    # Save story text for later display
                    st.session_state.story_text = template_text
        
        # Continue to next step
        if st.session_state.parsed_data:
            if st.button("Continue to Voice Setup ➡️"):
                st.session_state.current_step = 2
                st.rerun()
                
        # Step 2: Voice Setup
        if st.session_state.current_step >= 2:
            # Update progress steps
            st.markdown("""
            <div class="step-container">
                <div class="step-line"></div>
                <div class="step">1</div>
                <div class="step active">2</div>
                <div class="step">3</div>
                <div class="step">4</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Step 2: Voice Setup")
            
            # Extract unique characters
            characters = list(set([item["character"] for item in st.session_state.parsed_data]))
            
            # Voice model selection based on provider
            if api_provider == "OpenAI TTS":
                # OpenAI voice selection
                st.markdown("""
                <div class="feature-card">
                    <h3 style="margin-top:0; color:#6C63FF;">🗣️ Assign Voices to Characters</h3>
                    <p>Select an OpenAI voice for each character in your dialogue.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Initialize character_voices if not already set
                if not st.session_state.character_voices:
                    st.session_state.character_voices = {}
                
                # Voice settings (speed, pitch)
                col1, col2 = st.columns(2)
                with col1:
                    speed = st.slider("Speech Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
                    st.session_state.voice_settings["speed"] = speed
                    
                # Assign voices to characters
                for character in characters:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        selected_voice = st.selectbox(
                            f"Voice for {character}",
                            list(openai_voice_models.keys()),
                            key=f"voice_{character}"
                        )
                    
                    voice_id = openai_voice_models[selected_voice]
                    st.session_state.character_voices[character] = {
                        "provider": "openai",
                        "voice_id": voice_id,
                        "voice_name": selected_voice
                    }
                
            elif api_provider == "ElevenLabs":
                # ElevenLabs voice selection
                st.markdown("""
                <div class="feature-card">
                    <h3 style="margin-top:0; color:#6C63FF;">🗣️ Assign Voices to Characters</h3>
                    <p>Select an ElevenLabs voice for each character in your dialogue.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Check if voices have been fetched
                if not st.session_state.elevenlabs_voice_models:
                    st.warning("Please fetch ElevenLabs voices first using the button in the API Setup section.")
                else:
                    # Initialize character_voices if not already set
                    if not st.session_state.character_voices:
                        st.session_state.character_voices = {}
                    
                    # Voice settings (stability, similarity boost)
                    col1, col2 = st.columns(2)
                    with col1:
                        stability = st.slider("Stability", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
                        st.session_state.voice_settings["stability"] = stability
                    with col2:
                        similarity_boost = st.slider("Similarity Boost", min_value=0.0, max_value=1.0, value=0.75, step=0.1)
                        st.session_state.voice_settings["similarity_boost"] = similarity_boost
                    
                    # Assign voices to characters
                    for character in characters:
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            selected_voice = st.selectbox(
                                f"Voice for {character}",
                                list(st.session_state.elevenlabs_voice_models.keys()),
                                key=f"voice_{character}"
                            )
                        
                        voice_id = st.session_state.elevenlabs_voice_models[selected_voice]
                        st.session_state.character_voices[character] = {
                            "provider": "elevenlabs",
                            "voice_id": voice_id,
                            "voice_name": selected_voice
                        }
            
            # Background music options (future enhancement)
            st.markdown("""
            <div class="feature-card">
                <h3 style="margin-top:0; color:#FF6584;">🎵 Background Music</h3>
                <p>Add ambient music to enhance your audio narration.</p>
            </div>
            """, unsafe_allow_html=True)
            
            background_options = ["None", "Soft Piano", "Ambient", "Cinematic"]
            background_track = st.selectbox("Select background music", background_options)
            
            if background_track != "None":
                bg_volume = st.slider("Background volume", min_value=0.1, max_value=1.0, value=0.3, step=0.1)
                st.session_state.bg_volume = bg_volume
            
            st.session_state.background_track = background_track
            
            # Continue to next step
            if st.button("Continue to Audio Generation ➡️"):
                st.session_state.current_step = 3
                st.rerun()
        
        # Step 3: Generate Audio
        if st.session_state.current_step >= 3:
            # Update progress steps
            st.markdown("""
            <div class="step-container">
                <div class="step-line"></div>
                <div class="step">1</div>
                <div class="step">2</div>
                <div class="step active">3</div>
                <div class="step">4</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Step 3: Generate Audio")
            
            # Generate individual audio clips
            generate_button = st.button("🔊 Generate Voice Audio")
            
            if generate_button:
                # Clear previous audio files
                if st.session_state.audio_files:
                    cleanup_temp_files(st.session_state.audio_files)
                    st.session_state.audio_files = []
                
                # Generate audio for each dialogue line
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                total_lines = len(st.session_state.parsed_data)
                audio_files = []
                
                for i, item in enumerate(st.session_state.parsed_data):
                    character = item["character"]
                    dialogue = item["dialogue"]
                    emotion = item["emotion"]
                    
                    # Update progress
                    progress = (i + 1) / total_lines
                    progress_bar.progress(progress)
                    status_text.text(f"Generating audio for {character}: {dialogue[:50]}...")
                    
                    # Get voice settings for character
                    if character in st.session_state.character_voices:
                        voice_config = st.session_state.character_voices[character]
                        provider = voice_config["provider"]
                        voice_id = voice_config["voice_id"]
                        
                        # Generate audio based on provider
                        if provider == "openai":
                            # Generate OpenAI audio
                            audio_path = generate_voice_openai(
                                dialogue,
                                voice_id,
                                speed=st.session_state.voice_settings.get("speed", 1.0),
                                emotion=emotion
                            )
                        elif provider == "elevenlabs":
                            # Generate ElevenLabs audio
                            audio_path = generate_voice_elevenlabs(
                                dialogue,
                                voice_id,
                                stability=st.session_state.voice_settings.get("stability", 0.5),
                                similarity_boost=st.session_state.voice_settings.get("similarity_boost", 0.75),
                                emotion=emotion
                            )
                        
                        if audio_path:
                            audio_files.append(audio_path)
                    else:
                        st.warning(f"No voice assigned for character: {character}")
                
                # Store generated audio files
                st.session_state.audio_files = audio_files
                status_text.text(f"Generated audio for {len(audio_files)} dialogue lines.")
                
                # Continue to next step
                if audio_files:
                    st.session_state.current_step = 4
                    st.rerun()
        
        # Step 4: Final Export
        if st.session_state.current_step >= 4:
            # Update progress steps
            st.markdown("""
            <div class="step-container">
                <div class="step-line"></div>
                <div class="step">1</div>
                <div class="step">2</div>
                <div class="step">3</div>
                <div class="step active">4</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Step 4: Final Export")
            
            # Combine audio files if not already done
            if st.session_state.audio_files and not st.session_state.final_audio:
                with st.spinner("Combining audio files..."):
                    # Create temporary file for final audio
                    final_audio_path = tempfile.mktemp(suffix=".mp3")
                    
                    # Get background track if selected
                    bg_track = None  # Replace with actual background track path if implemented
                    
                    # Combine audio files
                    combined_path = concatenate_audio_files(
                        st.session_state.audio_files,
                        final_audio_path,
                        background_track=bg_track,
                        bg_volume=st.session_state.bg_volume
                    )
                    
                    if combined_path:
                        st.session_state.final_audio = combined_path
                        st.success("Audio files combined successfully!")
            
            # Display final audio
            if st.session_state.final_audio:
                st.markdown("""
                <div class="audio-container">
                    <h3 style="margin-top:0; color:#6C63FF;">🎧 Your Generated Voice Narration</h3>
                </div>
                """, unsafe_allow_html=True)
                
                with open(st.session_state.final_audio, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes)
            
                # Display story text if available
                if st.session_state.story_text:
                    with st.expander("📝 View Your Story Text"):
                        st.markdown("""
                        <div class="story-text-container">
                        """, unsafe_allow_html=True)
                        
                        # Format and display the story text
                        lines = st.session_state.story_text.split('\n')
                        for line in lines:
                            if line.strip():
                                st.markdown(f"<p>{line}</p>", unsafe_allow_html=True)
                                
                        st.markdown("</div>", unsafe_allow_html=True)
                
                # Download button for final audio
                with open(st.session_state.final_audio, "rb") as f:
                    b64_audio = base64.b64encode(f.read()).decode()
                    
                download_filename = f"voice_narration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                download_link = f'<a href="data:audio/mp3;base64,{b64_audio}" download="{download_filename}" style="display: inline-block; padding: 0.5rem 1rem; background: linear-gradient(120deg, #6C63FF 0%, #8B5CF6 100%); color: white; text-decoration: none; border-radius: 0.5rem; font-weight: 600; margin-top: 1rem; box-shadow: 0 4px 12px rgba(108, 99, 255, 0.25); transition: all 0.3s ease;">Download Voice Narration</a>'
                st.markdown(download_link, unsafe_allow_html=True)
                
                # Reset button
                if st.button("🔄 Start New Project"):
                    # Clean up temporary files
                    cleanup_temp_files(st.session_state.audio_files)
                    if st.session_state.final_audio:
                        cleanup_temp_files([st.session_state.final_audio])
                    
                    # Reset session state
                    st.session_state.parsed_data = []
                    st.session_state.character_voices = {}
                    st.session_state.audio_files = []
                    st.session_state.final_audio = None
                    st.session_state.current_step = 1
                    st.session_state.story_text = None
                    
                    st.rerun()
    
    # Voice Dubbing tab
    elif tab == "🌍 Voice Dubbing":
        # Show dubbing interface
        render_dubbing_interface()

# Render Voice Dubbing interface
def render_dubbing_interface():
    # API Setup section
    with st.expander("🔑 API Setup", expanded=False):
        st.markdown("""
        <div class="feature-card">
            <h3 style="margin-top:0; color:#6C63FF;">🔐 API Configuration</h3>
            <p>Set up your voice provider API keys to enable voice dubbing.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # API key inputs
        col1, col2 = st.columns(2)
        
        with col1:
            openai_key = st.text_input(
                "Enter your OpenAI API key",
                value=st.session_state.openai_key if st.session_state.openai_key else "",
                type="password",
                key="openai_key_dubbing"
            )
            if openai_key:
                st.session_state.openai_key = openai_key
                st.success("OpenAI API key set successfully!")
            
            # OpenAI voice selection
            openai_voice = st.selectbox(
                "Select OpenAI voice for dubbing",
                list(openai_voice_models.keys()),
                key="openai_voice_dubbing"
            )
            st.session_state.openai_voice = openai_voice_models[openai_voice]
        
        with col2:
            elevenlabs_key = st.text_input(
                "Enter your ElevenLabs API key",
                value=st.session_state.elevenlabs_key if st.session_state.elevenlabs_key else "",
                type="password",
                key="elevenlabs_key_dubbing"
            )
            if elevenlabs_key:
                st.session_state.elevenlabs_key = elevenlabs_key
                st.success("ElevenLabs API key set successfully!")
            
            # Fetch ElevenLabs voices
            if st.button("Fetch ElevenLabs Voices", key="fetch_elevenlabs_dubbing"):
                with st.spinner("Fetching voices from ElevenLabs..."):
                    voices = fetch_elevenlabs_voices()
                    if voices:
                        st.session_state.elevenlabs_voice_models = voices
                        st.success(f"Successfully fetched {len(voices)} voices from ElevenLabs!")
                    else:
                        st.error("Failed to fetch voices from ElevenLabs.")
    
    # Main interface section
    st.subheader("🌐 Voice Dubbing")
    
    # Dubbing provider selection with enhanced UI
    st.markdown("""
    <div class="feature-card">
        <h3 style="margin-top:0; color:#6C63FF;">🎙️ Select Dubbing Provider</h3>
        <p>Choose which service to use for dubbing your audio to another language.</p>
    </div>
    """, unsafe_allow_html=True)
    
    dubbing_provider = st.radio(
        "Dubbing Provider",
        ["OpenAI", "ElevenLabs"],
        horizontal=True
    )
    
    # Target language selection with enhanced UI
    st.markdown("""
    <div class="feature-card">
        <h3 style="margin-top:0; color:#6C63FF;">🌍 Select Target Language</h3>
        <p>Choose the language you want to dub your audio into.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two-column language selection
    col1, col2 = st.columns(2)
    
    with col1:
        target_language_group1 = st.radio(
            "European Languages",
            ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Polish", "Dutch"]
        )
    
    with col2:
        target_language_group2 = st.radio(
            "Asian & Other Languages",
            ["Hindi", "Arabic", "Chinese", "Japanese", "Korean", "Russian", "Turkish"]
        )
    
    # Determine which language was selected
    if target_language_group1 != "English":
        target_language = target_language_group1
    else:
        target_language = target_language_group2
    
    # Display the selected language with an eye-catching style
    st.markdown(f"""
    <div style="margin: 15px 0; padding: 10px 15px; background: linear-gradient(120deg, rgba(108, 99, 255, 0.1), rgba(255, 101, 132, 0.1)); 
               border-radius: 8px; border-left: 3px solid #6C63FF; font-weight: 500;">
        🎯 Selected language for dubbing: <span style="color: #6C63FF; font-weight: 700;">{target_language}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Language code mapping
    language_code_map = {
        "English": "en", "Spanish": "es", "French": "fr", "German": "de", 
        "Italian": "it", "Portuguese": "pt", "Polish": "pl", "Hindi": "hi", 
        "Arabic": "ar", "Chinese": "zh", "Japanese": "ja", "Korean": "ko", 
        "Russian": "ru", "Turkish": "tr", "Dutch": "nl"
    }
    
    # Selected language code
    lang_code = language_code_map.get(target_language, "en")
    
    # Voice selection based on provider
    voice_id = None
    if dubbing_provider == "ElevenLabs":
        if st.session_state.elevenlabs_voice_models:
            selected_voice = st.selectbox(
                "Select ElevenLabs voice for dubbing:", 
                options=list(st.session_state.elevenlabs_voice_models.keys()),
                index=0
            )
            voice_id = st.session_state.elevenlabs_voice_models[selected_voice]
        else:
            st.warning("Please fetch ElevenLabs voices first using the button in the API Setup section.")
    
    # Audio upload with enhanced UI
    st.markdown("""
    <div class="feature-card">
        <h3 style="margin-top:0; color:#6C63FF;">🎵 Upload Your Audio</h3>
        <p>Upload an audio file (MP3, WAV, or OGG format) that you'd like to dub into another language.</p>
    </div>
    """, unsafe_allow_html=True)
    uploaded_audio = st.file_uploader("", type=["mp3", "wav", "ogg"])
    
    if uploaded_audio:
        # Save uploaded audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_audio.name.split(".")[-1]) as temp_file:
            temp_file.write(uploaded_audio.getvalue())
            audio_path = temp_file.name
            
        st.session_state.uploaded_audio = audio_path
        
        # Display original audio
        st.subheader("Original Audio")
        st.audio(uploaded_audio)
    
    # Dubbing process - enhanced button style
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_dubbing = st.button("🎬 Start Dubbing Process", use_container_width=True)
    
    if st.session_state.uploaded_audio and start_dubbing:
        # Validate provider-specific requirements
        if dubbing_provider == "OpenAI":
            if not st.session_state.openai_key:
                st.error("Please enter your OpenAI API key.")
            else:
                with st.spinner(f"Dubbing audio to {target_language} with OpenAI..."):
                    dubbed_audio_path = openai_dubbing(
                        st.session_state.uploaded_audio, 
                        lang_code, 
                        st.session_state.openai_voice
                    )
                    
                    if dubbed_audio_path:
                        st.session_state.dubbed_audio = dubbed_audio_path
                        st.success(f"Audio successfully dubbed to {target_language} with OpenAI!")
                        st.rerun()
        
        elif dubbing_provider == "ElevenLabs":
            if not st.session_state.elevenlabs_key:
                st.error("Please enter your ElevenLabs API key.")
            elif not voice_id:
                st.error("Please select a voice for dubbing.")
            else:
                with st.spinner(f"Dubbing audio to {target_language} with ElevenLabs..."):
                    dubbed_audio_path = elevenlabs_dubbing(
                        st.session_state.uploaded_audio, 
                        lang_code, 
                        voice_id
                    )
                    
                    if dubbed_audio_path:
                        st.session_state.dubbed_audio = dubbed_audio_path
                        st.success(f"Audio successfully dubbed to {target_language} with ElevenLabs!")
                        st.rerun()
    
    # Display dubbed audio if available
    if st.session_state.dubbed_audio:
        st.subheader(f"Dubbed Audio ({target_language})")
        with open(st.session_state.dubbed_audio, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes)
            
        # Download button for dubbed audio
        with open(st.session_state.dubbed_audio, "rb") as f:
            b64_audio = base64.b64encode(f.read()).decode()
            
        download_filename = f"dubbed_audio_{target_language.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        download_link = f'<a href="data:audio/mp3;base64,{b64_audio}" download="{download_filename}" style="display: inline-block; padding: 0.5rem 1rem; background: linear-gradient(120deg, #6C63FF 0%, #8B5CF6 100%); color: white; text-decoration: none; border-radius: 0.5rem; font-weight: 600; margin-top: 1rem; box-shadow: 0 4px 12px rgba(108, 99, 255, 0.25); transition: all 0.3s ease;">Download Dubbed Audio</a>'
        st.markdown(download_link, unsafe_allow_html=True)
        
    # Reset button with improved styling
    st.markdown("<hr style='margin: 30px 0; border: none; height: 1px; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(108, 99, 255, 0.5), rgba(255,255,255,0));'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        reset_button = st.button("🔄 Reset Dubbing Process", use_container_width=True, type="secondary")
    
    if reset_button:
        if st.session_state.uploaded_audio:
            try:
                os.remove(st.session_state.uploaded_audio)
            except:
                pass
        if st.session_state.dubbed_audio:
            try:
                os.remove(st.session_state.dubbed_audio)
            except:
                pass
                
        st.session_state.uploaded_audio = None
        st.session_state.dubbed_audio = None
        st.rerun()

if __name__ == "__main__":
    main()
