import streamlit as st
import re
import tempfile
import os
import time
import base64
from io import BytesIO
import json
from datetime import datetime
import pandas as pd
from pydub import AudioSegment

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

# Define voice models
voice_models = {
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
def generate_voice(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Generate voice audio from text (mock implementation)."""
    # In a real implementation, this would call an API like ElevenLabs
    # For now, we'll create a silent audio segment as a placeholder
    
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

# App header
st.markdown("<h1 class='main-header'>VoiceCanvas</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Transform Text into Character-Driven Audio</h2>", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
step = st.sidebar.radio(
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
                    st.experimental_rerun()
                
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
                    st.experimental_rerun()
                    
            except Exception as e:
                st.error(f"Error parsing text: {str(e)}")

# Step 2: Character Mapping
elif st.session_state.current_step == 2:
    st.header("Step 2: Map Characters to Voices")
    
    if not st.session_state.parsed_data:
        st.warning("Please upload or enter your text first!")
        if st.button("Go Back to Text Input"):
            st.session_state.current_step = 1
            st.experimental_rerun()
    else:
        # Get unique characters
        characters = list(set([entry['character'] for entry in st.session_state.parsed_data]))
        
        st.subheader("Assign voices to characters")
        
        # Create a form for character mapping
        with st.form("character_mapping_form"):
            for character in characters:
                st.session_state.character_voices[character] = st.selectbox(
                    f"Voice for {character}:",
                    options=list(voice_models.keys()),
                    key=f"voice_{character}"
                )
            
            submit_button = st.form_submit_button("Save Voice Mappings")
        
        if submit_button:
            # Update parsed data with voice models
            for entry in st.session_state.parsed_data:
                character = entry["character"]
                selected_voice = st.session_state.character_voices.get(character, "Neutral Narrator")
                entry["voice_model"] = voice_models[selected_voice]
            
            st.success("Characters mapped to voices successfully!")
            
            # Continue button
            if st.button("Continue to Voice Generation"):
                st.session_state.current_step = 3
                st.experimental_rerun()

# Step 3: Voice Generation
elif st.session_state.current_step == 3:
    st.header("Step 3: Generate Character Voices")
    
    if not st.session_state.parsed_data or not any("voice_model" in entry for entry in st.session_state.parsed_data):
        st.warning("Please map characters to voices first!")
        if st.button("Go Back to Character Mapping"):
            st.session_state.current_step = 2
            st.experimental_rerun()
    else:
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
                    # Generate audio for this dialogue
                    audio_file = generate_voice(
                        text=entry['dialogue'],
                        voice_model=entry['voice_model'],
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
                        st.experimental_rerun()
                        
                except Exception as e:
                    st.error(f"Error combining audio files: {str(e)}")

# Step 4: Audio Output
elif st.session_state.current_step == 4:
    st.header("Step 4: Listen to Your Audio Story")
    
    if not st.session_state.final_audio:
        st.warning("Please generate audio first!")
        if st.button("Go Back to Voice Generation"):
            st.session_state.current_step = 3
            st.experimental_rerun()
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
            st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("© 2025 VoiceCanvas | Developed for KUKU FM Project K")
