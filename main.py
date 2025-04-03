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
from io import BytesIO

# Configure FFmpeg path for Streamlit Cloud
os.environ["PATH"] += os.pathsep + '/usr/bin/ffmpeg'

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
if 'voice_settings' not in st.session_state:
    st.session_state.voice_settings = {}
if 'background_track' not in st.session_state:
    st.session_state.background_track = "None"
if 'bg_volume' not in st.session_state:
    st.session_state.bg_volume = 0.3
if 'api_provider' not in st.session_state:
    st.session_state.api_provider = "openai"
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

# Define voice models for OpenAI
openai_voice_models = {
    "Alloy": "alloy",
    "Echo": "echo",
    "Fable": "fable",
    "Onyx": "onyx",
    "Nova": "nova",
    "Shimmer": "shimmer"
}

# Define voice models for Mock API
mock_voice_models = {
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

# Function to generate voice (mock implementation)
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
        return AudioSegment.silent(duration=duration_ms)
        
    # Create simulated ambient sounds
    base_audio = AudioSegment.silent(duration=duration_ms)
    
    # Generate some ambient sounds based on the track name
    if "nature" in track_name.lower():
        base = AudioSegment.silent(duration=5000)
        for i in range(0, 5000, 500):
            vol_factor = random.uniform(0.2, 0.4)
            wind = AudioSegment.silent(duration=300)
            wind = wind.low_pass_filter(500)
            wind = wind - int(30 * (1 - vol_factor))
            base = base.overlay(wind, position=i)
            
        for i in range(0, 5000, 1500):
            if random.random() > 0.5:
                chirp_len = random.randint(50, 150)
                chirp = AudioSegment.silent(duration=chirp_len)
                chirp = chirp.high_pass_filter(3000)
                base = base.overlay(chirp, position=i)
        
        repeats = (duration_ms // 5000) + 1
        ambient = base * repeats
        ambient = ambient[:duration_ms]
    else:
        # Generic ambient sound
        base = AudioSegment.silent(duration=5000)
        noise = AudioSegment.silent(duration=5000)
        noise = noise.low_pass_filter(800)
        base = base.overlay(noise)
        repeats = (duration_ms // 5000) + 1
        ambient = base * repeats
        ambient = ambient[:duration_ms]
    
    return ambient

# Function to combine audio files
def combine_audio_files(audio_files, background_track=None, bg_volume=0.3):
    """Combine multiple audio files with optional background music."""
    if not audio_files:
        return None
        
    combined = AudioSegment.empty()
    pause = AudioSegment.silent(duration=500)
    
    for file_path in audio_files:
        audio = AudioSegment.from_mp3(file_path)
        combined += audio + pause
    
    if background_track and background_track != "None":
        total_duration = len(combined)
        bg_audio = get_background_music(background_track, total_duration)
        bg_audio = bg_audio - (1 - bg_volume) * 20
        
        if len(bg_audio) < len(combined):
            repeat_count = (len(combined) // len(bg_audio)) + 1
            bg_audio = bg_audio * repeat_count
            
        bg_audio = bg_audio[:len(combined)]
        combined = combined.overlay(bg_audio, loop=False)
    
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    combined.export(output_path, format="mp3")
    return output_path

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
                
                st.subheader("Preview:")
                for i, entry in enumerate(st.session_state.parsed_data[:5]):
                    emotion_text = f" ({entry['emotion']})" if entry['emotion'] else ""
                    st.text(f"{entry['character']}{emotion_text}: {entry['dialogue'][:50]}...")
                
                if len(st.session_state.parsed_data) > 5:
                    st.text(f"... and {len(st.session_state.parsed_data) - 5} more entries")
                
                if st.button("Continue to Character Mapping"):
                    st.session_state.current_step = 2
                    st.rerun()
                
            except Exception as e:
                st.error(f"Error parsing file: {str(e)}")
    
    else:
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
                
                st.subheader("Preview:")
                for entry in st.session_state.parsed_data:
                    emotion_text = f" ({entry['emotion']})" if entry['emotion'] else ""
                    st.text(f"{entry['character']}{emotion_text}: {entry['dialogue'][:50]}...")
                
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
        characters = list(set([entry['character'] for entry in st.session_state.parsed_data]))
        st.subheader("Assign voices to characters")
        
        voice_models_to_use = openai_voice_models if st.session_state.api_provider == "openai" else mock_voice_models
        
        # Character mapping form
        form = st.form("character_mapping_form")
        with form:
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
                        st.session_state.voice_settings[character] = settings
            
            submitted = form.form_submit_button("Save Voice Mappings")
        
        if submitted:
            st.success("Voice mappings saved successfully!")
            
            # Preview section outside the form
            if st.button("Preview a Random Line"):
                entry = random.choice(st.session_state.parsed_data)
                voice_name = st.session_state.character_voices.get(entry["character"], list(voice_models_to_use.keys())[0])
                voice_model = get_voice_model_id(voice_name)
                settings = get_voice_settings(entry["character"])
                
                with st.spinner(f"Generating preview for '{entry['character']}'..."):
                    audio_file = generate_voice_mock(
                        entry["dialogue"],
                        voice_model,
                        speed=settings["speed"],
                        emotion=entry["emotion"]
                    )
                    
                    if audio_file:
                        st.audio(audio_file)
                    else:
                        st.error("Failed to generate preview audio.")
            
            # Continue button outside the form
            if st.button("Continue to Voice Generation"):
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
        if st.session_state.api_provider == "openai" and not st.session_state.api_key:
            st.warning("⚠️ No OpenAI API key provided. Using mock audio generation instead.")
        
        voice_models_to_use = openai_voice_models if st.session_state.api_provider == "openai" else mock_voice_models
        
        st.subheader("Voice Customization (Optional)")
        col1, col2 = st.columns(2)
        with col1:
            speed = st.slider("Speech Speed:", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        with col2:
            pitch = st.slider("Voice Pitch:", min_value=-20, max_value=20, value=0, step=5)
            
        st.subheader("Background Music (Optional)")
        st.markdown("🎵 Add ambient sounds or music to enhance your audio story.")
        
        track_container = st.container()
        with track_container:
            col1, col2 = st.columns(2)
            
            with col1:
                track_descriptions = {
                    "None": "No background audio",
                    "Peaceful Nature": "Gentle ambient sounds of a forest",
                    "Sci-Fi Ambience": "Futuristic electronic tones",
                    "Suspenseful Mystery": "Tense atmospheric sounds",
                    "Fantasy Adventure": "Mystical ambient sounds",
                    "Urban City": "City atmosphere with distant traffic",
                    "Romantic Scene": "Soft, gentle ambient tones",
                    "Horror Ambience": "Dark, unsettling sounds",
                    "Comedy Background": "Light, playful ambient sounds"
                }
                
                background_track = st.selectbox(
                    "Select Background Track:",
                    options=list(BACKGROUND_TRACKS.keys()),
                    index=list(BACKGROUND_TRACKS.keys()).index(st.session_state.background_track) if st.session_state.background_track in BACKGROUND_TRACKS else 0
                )
                st.session_state.background_track = background_track
                
                if background_track != "None":
                    st.info(track_descriptions.get(background_track, ""))
            
            with col2:
                bg_volume = st.slider(
                    "Background Volume:", 
                    min_value=0.1, 
                    max_value=0.5, 
                    value=st.session_state.bg_volume,
                    step=0.05,
                    format="%d%%"
                )
                st.session_state.bg_volume = bg_volume
                
                vol_percent = int(bg_volume * 100)
                if vol_percent < 20:
                    st.caption("🔈 Subtle background")
                elif vol_percent < 35:
                    st.caption("🔉 Balanced mix")
                else:
                    st.caption("🔊 Prominent background")
                    
        if st.button("Reset Background Settings"):
            st.session_state.background_track = "None"
            st.session_state.bg_volume = 0.3
            st.rerun()
        
        if st.button("Generate Audio"):
            st.session_state.audio_files = []
            
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                character_info = st.empty()
                dialogue_preview = st.empty()
            
            for i, entry in enumerate(st.session_state.parsed_data):
                character = entry['character']
                emotion_text = f" ({entry['emotion']})" if entry['emotion'] else ""
                dialogue = entry['dialogue']
                
                status_text.markdown(f"**Generating audio...** ({i+1}/{len(st.session_state.parsed_data)})")
                character_info.markdown(f"🎭 **Character:** {character}{emotion_text}")
                dialogue_preview.markdown(f"💬 \"{dialogue[:100]}{'...' if len(dialogue) > 100 else ''}\"")
                
                try:
                    voice_name = st.session_state.character_voices.get(character)
                    voice_model_id = get_voice_model_id(voice_name)
                    
                    audio_file = generate_voice_mock(
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
                
                progress_bar.progress((i + 1) / len(st.session_state.parsed_data))
            
            if st.session_state.audio_files:
                status_text.text("Combining audio files...")
                try:
                    file_paths = [af['file_path'] for af in st.session_state.audio_files]
                    background_track = BACKGROUND_TRACKS.get(st.session_state.background_track)
                    bg_volume = st.session_state.bg_volume
                    
                    if background_track and background_track != "None":
                        status_text.text(f"Adding '{st.session_state.background_track}' background track...")
                    
                    final_audio = combine_audio_files(
                        file_paths, 
                        background_track=background_track, 
                        bg_volume=bg_volume
                    )
                    
                    st.session_state.final_audio = final_audio
                    status_text.text("Audio generation complete!")
                    
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
        
        if st.session_state.background_track != "None":
            st.info(f"Background Track: {st.session_state.background_track} (Volume: {int(st.session_state.bg_volume * 100)}%)")
        
        st.audio(st.session_state.final_audio)
        
        with open(st.session_state.final_audio, "rb") as file:
            btn = st.download_button(
                label="Download Audio",
                data=file,
                file_name="voicecanvas_story.mp3",
                mime="audio/mp3"
            )
        
        st.subheader("Individual Character Clips")
        for audio_entry in st.session_state.audio_files:
            with st.expander(f"{audio_entry['character']}: {audio_entry['dialogue'][:50]}..."):
                st.audio(audio_entry['file_path'])
        
        st.subheader("Provide Feedback")
        feedback = st.text_area("How was your experience? Any suggestions for improvement?")
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")
            
        if st.button("Start New Project"):
            st.session_state.parsed_data = []
            st.session_state.character_voices = {}
            st.session_state.audio_files = []
            st.session_state.final_audio = None
            st.session_state.voice_settings = {}
            st.session_state.background_track = "None"
            st.session_state.bg_volume = 0.3
            st.session_state.current_step = 1
            st.rerun()

# Footer
st.markdown("---")
st.markdown("© 2025 VoiceCanvas | Developed for KUKU FM Project K")
