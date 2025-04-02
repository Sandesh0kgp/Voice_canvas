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
import numpy as np
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
</style>
""", unsafe_allow_html=True)

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
    st.session_state.api_key = os.environ.get("OPENAI_API_KEY", "")
if 'api_provider' not in st.session_state:
    st.session_state.api_provider = "openai"
if 'voice_settings' not in st.session_state:
    st.session_state.voice_settings = {}

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
    # First try to use the environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    
    # If not found, try to use the one from session state
    if not api_key and st.session_state.api_key:
        api_key = st.session_state.api_key
        
    if api_key:
        return OpenAI(api_key=api_key)
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
    client = get_openai_client()
    if not client:
        st.error("OpenAI API key not set. Please enter your API key.")
        raise ValueError("OpenAI API key is not available")
        
    # Apply emotion through text modification if provided
    if emotion:
        text = f"[{emotion}] {text}"
    
    # Call OpenAI TTS API
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice_model,
        input=text,
        speed=speed
    )
    
    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        response.stream_to_file(temp_file.name)
        return temp_file.name

# Function to generate voice (mock implementation as fallback)
def generate_voice_mock(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Generate voice audio from text (mock implementation)."""
    # Simulate processing time
    time.sleep(0.5)
    
    # Create a proper mock audio file with audible tones
    word_count = len(text.split())
    duration = max(1000, word_count * 200)  # at least 1 second
    
    # Generate a simple tone sequence based on voice_model and text content
    # This creates different audio patterns for different characters/voices
    audio = AudioSegment.silent(duration=0)
    
    # Create a simple hash of the text and voice model to generate unique tone sequences
    tone_seed = sum(ord(c) for c in text) + sum(ord(c) for c in voice_model)
    
    # Generate simple tones based on the text content
    segment_duration = 150  # ms per tone
    num_segments = min(20, max(3, word_count))
    
    for i in range(num_segments):
        # Create a tone with frequency based on the character and position in text
        freq = 300 + ((tone_seed + i * 33) % 700)  # frequency between 300-1000 Hz
        volume = -20  # dB
        
        # Generate sine wave tone
        sample_rate = 44100
        t = np.linspace(0, segment_duration/1000, int(segment_duration * sample_rate / 1000))
        tone = np.sin(2 * np.pi * freq * t) * (10 ** (volume / 20))
        
        # Convert to audio segment
        tone_segment = AudioSegment(
            tone.astype(np.float32).tobytes(),
            frame_rate=sample_rate,
            sample_width=4,
            channels=1
        )
        
        # Add short silence between tones
        audio += tone_segment + AudioSegment.silent(duration=50)
    
    # Apply speed adjustment by modifying the audio speed
    if speed != 1.0:
        # This is a crude approximation of speed change
        audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * speed)
        }).set_frame_rate(44100)
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        audio.export(temp_file.name, format="mp3")
        return temp_file.name

# Function to generate voice (router)
def generate_voice(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Route to appropriate voice generation function based on API provider."""
    # Check if we have an API key in environment or session state
    has_api_key = bool(os.environ.get("OPENAI_API_KEY") or st.session_state.api_key)
    
    if st.session_state.api_provider == "openai" and has_api_key:
        try:
            # Try to use OpenAI, but fall back to mock if there's any error
            return generate_voice_openai(text, voice_model, speed, pitch, emotion)
        except Exception as e:
            st.warning(f"OpenAI API error: {str(e)}. Falling back to mock provider.")
            return generate_voice_mock(text, voice_model, speed, pitch, emotion)
    else:
        return generate_voice_mock(text, voice_model, speed, pitch, emotion)

# Function to combine audio files
def combine_audio_files(audio_files):
    """Combine multiple audio files with a short pause between them."""
    if not audio_files:
        return None
        
    combined = AudioSegment.empty()
    pause = AudioSegment.silent(duration=500)  # 500ms pause
    
    for file_path in audio_files:
        audio = AudioSegment.from_mp3(file_path)
        combined += audio + pause
    
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
        sample_text = """Narrator: Once upon a time, in a small village, there lived a boy named Arjun.
Arjun (happy): I want to explore the world beyond these mountains!
Narrator: But Arjun's parents were worried about his safety.
Parents (worried): Arjun, it's dangerous out there. Please stay home."""
        
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
        has_api_key = bool(os.environ.get("OPENAI_API_KEY") or st.session_state.api_key)
        if st.session_state.api_provider == "openai" and not has_api_key:
            st.warning("⚠️ No OpenAI API key found. Using mock audio generation instead. For real voice generation, please add your API key in the sidebar.")
        
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
        
        # Generate button
        if st.button("Generate Audio"):
            # Clear previous audio files
            st.session_state.audio_files = []
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Process each dialogue entry
            for i, entry in enumerate(st.session_state.parsed_data):
                status_text.text(f"Generating audio for: {entry['character']}")
                
                try:
                    # Get voice model for this character
                    character = entry['character']
                    voice_name = st.session_state.character_voices.get(character)
                    voice_model_id = get_voice_model_id(voice_name)
                    
                    # Generate audio for this dialogue
                    audio_file = generate_voice(
                        text=entry['dialogue'],
                        voice_model=voice_model_id,
                        speed=speed,
                        pitch=pitch,
                        emotion=entry.get('emotion', None)
                    )
                    
                    if audio_file:
                        st.session_state.audio_files.append({
                            'character': entry['character'],
                            'dialogue': entry['dialogue'],
                            'file_path': audio_file
                        })
                except Exception as e:
                    st.error(f"Error generating audio for {entry['character']}: {str(e)}")
                
                # Update progress
                progress_bar.progress((i + 1) / len(st.session_state.parsed_data))
            
            # Combine all audio files
            if st.session_state.audio_files:
                status_text.text("Combining audio files...")
                try:
                    file_paths = [af['file_path'] for af in st.session_state.audio_files]
                    final_audio = combine_audio_files(file_paths)
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
            st.session_state.current_step = 1
            st.rerun()

# Footer
st.markdown("---")
st.markdown("© 2025 VoiceCanvas | Developed for KUKU FM Project K")
