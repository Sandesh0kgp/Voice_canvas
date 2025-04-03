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

from utils import parse_text_from_file, parse_text_from_string, export_dialogue_to_csv, extract_unique_characters
from audio_processing import (
    generate_voice,
    combine_audio_segments,
    get_background_music,
    load_xtts_model,
    generate_voice_mock
)

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

# Ensure reference_voices directory exists
voice_dir = "reference_voices"
if not os.path.exists(voice_dir):
    os.makedirs(voice_dir)

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
if 'tts_model_loaded' not in st.session_state:
    st.session_state.tts_model_loaded = False
if 'tts_model' not in st.session_state:
    st.session_state.tts_model = None
if 'api_provider' not in st.session_state:
    st.session_state.api_provider = "xtts"  # Default to XTTS
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", "")
if 'error_message' not in st.session_state:
    st.session_state.error_message = None

# Define voice models for OpenAI
openai_voice_models = {
    "Alloy": "alloy",
    "Echo": "echo",
    "Fable": "fable",
    "Onyx": "onyx",
    "Nova": "nova",
    "Shimmer": "shimmer"
}

# Define voice models for XTTS
xtts_voice_models = {
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

# Define voice models for Google TTS
gtts_voice_models = {
    # English voices with character suggestions
    "Narrator (English US)": "en_us_narrator",
    "Hero (English US)": "en_us_hero",
    "Heroine (English UK)": "en_uk_heroine",
    "Elder (English UK)": "en_uk_elder",
    "Child (English US)": "en_us_child",
    "Villain (English US)": "en_us_villain",
    "Comic Relief (English UK)": "en_uk_comic",
    "Sidekick (English US)": "en_us_sidekick",
    "Mentor (English UK)": "en_uk_mentor",
    "Announcer (English US)": "en_us_announcer",
    
    # Keep some international options
    "Spanish Character": "es",
    "French Character": "fr",
    "German Character": "de",
    "Italian Character": "it"
}

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

def clear_audio_files():
    """Clear temporary audio files."""
    for file_path in st.session_state.audio_files:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                st.warning(f"Could not remove temporary file {file_path}: {e}")
    
    st.session_state.audio_files = []

def process_dialogue():
    """Process dialogue and generate audio for each line."""
    try:
        # Clear previous audio files
        clear_audio_files()
        
        # Clear any previous errors
        st.session_state.error_message = None
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Process each dialogue line
        audio_segments = []
        
        for idx, item in enumerate(st.session_state.parsed_data):
            character = item.get('character', 'Narrator')
            dialogue = item.get('dialogue', '')
            emotion = item.get('emotion', None)
            
            status_text.text(f"Processing: {character}'s dialogue...")
            
            # Get voice settings for this character
            voice_model = st.session_state.character_voices.get(character, 'neutral_narrator')
            voice_settings = st.session_state.voice_settings.get(character, {})
            
            speed = voice_settings.get('speed', 1.0)
            pitch = voice_settings.get('pitch', 0)
            
            # Generate voice
            audio_file = generate_voice(
                text=dialogue,
                voice_model=voice_model,
                speed=speed,
                pitch=pitch,
                emotion=emotion
            )
            
            st.session_state.audio_files.append(audio_file)
            audio_segments.append(audio_file)
            
            # Update progress
            progress = (idx + 1) / len(st.session_state.parsed_data)
            progress_bar.progress(progress)
        
        # Get background track
        status_text.text("Adding background track...")
        
        # Combine all audio segments
        final_audio = combine_audio_segments(
            audio_segments,
            background_track=st.session_state.background_track,
            bg_volume=st.session_state.bg_volume
        )
        
        st.session_state.final_audio = final_audio
        st.session_state.current_step = 3  # Move to final step
        
        status_text.text("Processing complete!")
        progress_bar.progress(1.0)
        
        # Slight delay before removing progress indicators
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
    except Exception as e:
        st.session_state.error_message = str(e)
        st.error(f"Error processing dialogue: {e}")

def main():
    """Main application function."""
    st.markdown("<h1 class='main-header'>VoiceCanvas</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Transform your dialogue scripts into immersive audio productions</h2>", unsafe_allow_html=True)
    
    # Display any error messages
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        if st.button("Clear Error"):
            st.session_state.error_message = None
            st.rerun()
    
    # Step tabs
    step_tabs = st.tabs(["1. Upload Script", "2. Assign Voices", "3. Generate & Export"])
    
    # Step 1: Upload Script
    with step_tabs[0]:
        st.header("Upload Your Dialogue Script")
        st.markdown("""
        Upload a text file containing your dialogue script or paste it directly below.
        
        **Format Guidelines:**
        - For character dialogue: `Character (emotion): Dialogue text`
        - For narration: Just write the text
        
        **Example:**
        ```
        Narrator: Once upon a time in a faraway land.
        Princess (happy): I love this beautiful kingdom!
        Knight (serious): Your Highness, danger approaches from the north.
        ```
        """)
        
        # File upload option
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
        
        # Text input option
        script_text = st.text_area("Or paste your dialogue script here:", height=200)
        
        # Process button
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Process Script"):
                if uploaded_file is not None:
                    # Process uploaded file
                    st.session_state.parsed_data = parse_text_from_file(uploaded_file)
                    st.session_state.current_step = 2  # Move to step 2
                    st.rerun()
                elif script_text.strip():
                    # Process text input
                    st.session_state.parsed_data = parse_text_from_string(script_text)
                    st.session_state.current_step = 2  # Move to step 2
                    st.rerun()
                else:
                    st.error("Please upload a file or enter text to process.")
        
        # Display processed data if available
        if st.session_state.parsed_data:
            with st.expander("Preview Processed Script"):
                for idx, item in enumerate(st.session_state.parsed_data):
                    character = item.get('character', 'Narrator')
                    emotion = item.get('emotion', None)
                    dialogue = item.get('dialogue', '')
                    
                    if emotion:
                        st.markdown(f"**{character}** *(emotion: {emotion})*: {dialogue}")
                    else:
                        st.markdown(f"**{character}**: {dialogue}")
                
                # Option to export to CSV
                st.download_button(
                    label="Export as CSV",
                    data=export_dialogue_to_csv(st.session_state.parsed_data),
                    file_name=f"dialogue_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        # API Provider selection
        st.markdown("---")
        st.subheader("Voice Generation Settings")
        
        # Provider selection
        api_provider = st.radio(
            "Select Voice Provider:",
            options=["XTTS (Local)", "Google TTS (Free)", "OpenAI API (Cloud)"],
            index=0 if st.session_state.api_provider == "xtts" else 
                  1 if st.session_state.api_provider == "gtts" else 2,
            horizontal=True
        )
        
        # Update session state based on selection
        if api_provider == "OpenAI API (Cloud)":
            st.session_state.api_provider = "openai"
            
            # Show API key input if OpenAI is selected
            api_key = st.text_input(
                "OpenAI API Key (Optional, will use environment variable if empty):",
                value=st.session_state.api_key,
                type="password"
            )
            
            if api_key != st.session_state.api_key:
                st.session_state.api_key = api_key
                
            st.markdown("""
            *Note: Using OpenAI requires an API key and will use credits from your account.
            Audio quality is higher but processing takes place in the cloud.*
            """)
        elif api_provider == "Google TTS (Free)":
            st.session_state.api_provider = "gtts"
            
            st.markdown("""
            *Note: Google TTS is a free service that doesn't require authentication.
            We've enhanced it with character voice profiles that automatically adjust pitch, speed, 
            and apply audio effects to create distinct voices for different character types:
            
            - Narrator, Hero, Heroine, Villain, Elder, Child, Comic Relief, Sidekick, Mentor, and Announcer
            - Each character type has unique voice characteristics
            - Pitch and speed can be further customized for each character
            - Works with both US and UK English accents
            - No API key required!*
            """)
        else:
            st.session_state.api_provider = "xtts"
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Load XTTS Model"):
                    load_xtts_model()
                    if st.session_state.tts_model_loaded:
                        st.success("XTTS model loaded successfully!")
                    else:
                        st.warning("Failed to load XTTS model. Using mock audio generation instead.")
            
            st.markdown("""
            *Note: XTTS is a local model that doesn't require an API key.
            If the model fails to load due to dependency issues, the application will use
            mock audio generation with silent audio segments that match dialogue length.*
            """)
            
            # Show notice if model is not loaded
            if not st.session_state.tts_model_loaded:
                st.info("The XTTS model is not currently loaded. Audio will be generated using the mock implementation (silent audio tracks).")
    
    # Step 2: Assign Voices
    with step_tabs[1]:
        if not st.session_state.parsed_data:
            st.info("Please upload and process a script in Step 1 first.")
        else:
            st.header("Assign Voices to Characters")
            
            # Extract unique characters
            unique_characters = extract_unique_characters(st.session_state.parsed_data)
            
            # Create columns for better layout
            col1, col2 = st.columns([1, 1])
            
            # Available voice models based on selected provider
            if st.session_state.api_provider == "openai":
                voice_models = openai_voice_models
            elif st.session_state.api_provider == "gtts":
                voice_models = gtts_voice_models
            else:
                voice_models = xtts_voice_models
            
            with col1:
                st.subheader("Character Voices")
                
                # Assign voices to characters
                for character in unique_characters:
                    # Get current voice for this character (or default)
                    current_voice = st.session_state.character_voices.get(character, list(voice_models.values())[0])
                    
                    # Convert internal voice ID to display name
                    display_voice = current_voice
                    for name, id in voice_models.items():
                        if id == current_voice:
                            display_voice = name
                            break
                    
                    # Voice selection dropdown
                    selected_voice = st.selectbox(
                        f"Voice for {character}:",
                        options=list(voice_models.keys()),
                        index=list(voice_models.keys()).index(display_voice) if display_voice in voice_models.keys() else 0
                    )
                    
                    # Update voice in session state
                    st.session_state.character_voices[character] = voice_models[selected_voice]
            
            with col2:
                st.subheader("Voice Settings")
                
                # Add fine-tuning options for each character
                for character in unique_characters:
                    with st.expander(f"Settings for {character}"):
                        # Initialize settings in session state
                        if character not in st.session_state.voice_settings:
                            st.session_state.voice_settings[character] = {
                                'speed': 1.0,
                                'pitch': 0
                            }
                        
                        # Speed adjustment (0.5 to 1.5)
                        speed = st.slider(
                            "Speaking Speed:",
                            min_value=0.5,
                            max_value=1.5,
                            value=st.session_state.voice_settings[character].get('speed', 1.0),
                            step=0.1,
                            key=f"speed_{character}"
                        )
                        
                        # Pitch adjustment (-20 to 20, available for XTTS and Google TTS)
                        if st.session_state.api_provider in ["xtts", "gtts"]:
                            pitch = st.slider(
                                "Pitch Adjustment:",
                                min_value=-20,
                                max_value=20,
                                value=st.session_state.voice_settings[character].get('pitch', 0),
                                step=1,
                                key=f"pitch_{character}"
                            )
                        else:
                            pitch = 0
                            
                        # Update settings in session state
                        st.session_state.voice_settings[character] = {
                            'speed': speed,
                            'pitch': pitch
                        }
            
            # Background track selection
            st.markdown("---")
            st.subheader("Background Music")
            
            # Track selection dropdown
            bg_track = st.selectbox(
                "Select Background Track:",
                options=list(BACKGROUND_TRACKS.keys()),
                index=list(BACKGROUND_TRACKS.keys()).index("None")
            )
            
            # Background volume slider (only if track is not None)
            if bg_track != "None":
                bg_volume = st.slider(
                    "Background Volume:",
                    min_value=0.0,
                    max_value=1.0,
                    value=st.session_state.bg_volume,
                    step=0.1
                )
                st.session_state.bg_volume = bg_volume
            
            # Update background track in session state
            st.session_state.background_track = bg_track
            
            # Process button
            if st.button("Generate Audio"):
                process_dialogue()
                st.rerun()
    
    # Step 3: Generate & Export
    with step_tabs[2]:
        if not st.session_state.final_audio:
            st.info("Please complete Steps 1 and 2 to generate audio.")
        else:
            st.header("Your Audio Production")
            
            # Display audio playback
            st.audio(st.session_state.final_audio)
            
            # Download option
            st.download_button(
                label="Download Audio",
                data=open(st.session_state.final_audio, "rb").read(),
                file_name=f"voice_canvas_production_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                mime="audio/mp3"
            )
            
            # Option to save project
            st.markdown("---")
            st.subheader("Save Project")
            
            # Create project data
            project_data = {
                "parsed_data": st.session_state.parsed_data,
                "character_voices": st.session_state.character_voices,
                "voice_settings": st.session_state.voice_settings,
                "background_track": st.session_state.background_track,
                "bg_volume": st.session_state.bg_volume,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Serialize to JSON
            project_json = json.dumps(project_data, indent=2)
            
            # Download button for project file
            st.download_button(
                label="Save Project File",
                data=project_json,
                file_name=f"voice_canvas_project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            # Start over button
            if st.button("Start New Project"):
                # Clear session state
                st.session_state.parsed_data = []
                st.session_state.character_voices = {}
                st.session_state.audio_files = []
                st.session_state.final_audio = None
                st.session_state.current_step = 1
                
                # Clear temporary files
                clear_audio_files()
                
                # Rerun app
                st.rerun()

# Run the app
if __name__ == "__main__":
    main()
        
