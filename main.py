import streamlit as st
import re
import tempfile
import os
import time
from datetime import datetime
import pandas as pd
from pydub import AudioSegment
from openai import OpenAI
import requests
import numpy as np
from io import BytesIO

# Configure AudioSegment
AudioSegment.converter = "ffmpeg"
AudioSegment.ffprobe = "ffprobe"

# Page configuration
st.set_page_config(
    page_title="VoiceCanvas",
    page_icon="🎙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #19A7CE; text-align: center; }
    .sub-header { font-size: 1.5rem; color: #146C94; margin-bottom: 2rem; }
    .stButton>button { background-color: #19A7CE; color: white; }
    .api-input { margin: 1rem 0; padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# Session state initialization
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

# Voice models
OPENAI_VOICES = {
    "Alloy (Neutral)": "alloy",
    "Echo (Male)": "echo",
    "Fable (Male)": "fable",
    "Onyx (Male)": "onyx",
    "Nova (Female)": "nova",
    "Shimmer (Female)": "shimmer"
}

MOCK_VOICES = {
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

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY") or st.session_state.api_key
    if api_key:
        try:
            client = OpenAI(api_key=api_key)
            client.models.list()
            st.session_state.openai_key_valid = True
            return client
        except Exception as e:
            st.session_state.openai_key_valid = False
            print(f"OpenAI API key validation error: {str(e)}")
    return None

def parse_text(text, from_file=False):
    if from_file:
        text = text.decode('utf-8')

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

def generate_mock_voice(text, voice_model, speed=1.0, pitch=0, emotion=None):
    time.sleep(0.5)
    audio = AudioSegment.silent(duration=len(text) * 50)

    # Create a simple tone based on the voice model
    freq = 220.0 if "female" in voice_model.lower() else 110.0
    t = np.linspace(0, len(text)/20, int(44100 * len(text)/20))
    signal = np.sin(2 * np.pi * freq * t)

    # Apply effects based on emotion
    if emotion:
        if "happy" in emotion.lower():
            signal *= 1.2
        elif "sad" in emotion.lower():
            signal *= 0.8

    # Convert to audio segment
    audio = AudioSegment(
        signal.astype(np.float32).tobytes(),
        frame_rate=44100,
        sample_width=4,
        channels=1
    )

    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio.export(temp_file.name, format="mp3")
    return temp_file.name

def generate_openai_voice(text, voice_model, speed=1.0, pitch=0, emotion=None):
    client = get_openai_client()
    if not client:
        raise ValueError("OpenAI API key not available")

    if emotion:
        text = f"[{emotion}] {text}"

    response = client.audio.speech.create(
        model="tts-1",
        voice=voice_model,
        input=text,
        speed=speed
    )

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    response.stream_to_file(temp_file.name)
    return temp_file.name

def generate_voice(text, voice_model, speed=1.0, pitch=0, emotion=None):
    if st.session_state.api_provider == "openai" and get_openai_client():
        return generate_openai_voice(text, voice_model, speed, pitch, emotion)
    return generate_mock_voice(text, voice_model, speed, pitch, emotion)

def combine_audio_files(audio_files):
    if not audio_files:
        return None

    combined = AudioSegment.empty()
    pause = AudioSegment.silent(duration=500)

    for file_path in audio_files:
        audio = AudioSegment.from_mp3(file_path)
        combined += audio + pause

    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    combined.export(output_file.name, format="mp3")
    return output_file.name

# Main app layout
st.markdown("<h1 class='main-header'>VoiceCanvas</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Transform Text into Character-Driven Audio</h2>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("API Configuration")
    api_provider = st.radio("Select API Provider", ["OpenAI", "Mock (No API)"],
                           index=0 if st.session_state.api_provider == "openai" else 1)
    st.session_state.api_provider = api_provider.lower()

    if st.session_state.api_provider == "openai":
        api_key = st.text_input("OpenAI API Key", type="password",
                               value=st.session_state.api_key)
        if api_key:
            st.session_state.api_key = api_key
            st.success("API Key set!")

    st.title("Navigation")
    step = st.radio("Process Steps",
                    ["1. Text Input", "2. Character Mapping",
                     "3. Voice Generation", "4. Audio Output"],
                    index=st.session_state.current_step - 1)
    st.session_state.current_step = int(step[0])

# Step 1: Text Input
if st.session_state.current_step == 1:
    st.header("Step 1: Upload or Enter Your Text")
    input_method = st.radio("Choose input method:", ["Upload File", "Direct Text Entry"])

    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload script file", type=['txt'])
        if uploaded_file:
            try:
                st.session_state.parsed_data = parse_text(uploaded_file.read(), True)
                st.success(f"Parsed {len(st.session_state.parsed_data)} entries!")

                for i, entry in enumerate(st.session_state.parsed_data[:5]):
                    emotion_text = f" ({entry['emotion']})" if entry['emotion'] else ""
                    st.text(f"{entry['character']}{emotion_text}: {entry['dialogue'][:50]}...")

                if st.button("Continue to Character Mapping"):
                    st.session_state.current_step = 2
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        sample_text = """Narrator: Once upon a time in a small village...
Hero (brave): I will protect this village!
Villain (angry): You cannot stop me!"""

        text_input = st.text_area("Enter your script:", value=sample_text, height=300)
        if st.button("Parse Text"):
            try:
                st.session_state.parsed_data = parse_text(text_input)
                st.success(f"Parsed {len(st.session_state.parsed_data)} entries!")

                for entry in st.session_state.parsed_data:
                    emotion_text = f" ({entry['emotion']})" if entry['emotion'] else ""
                    st.text(f"{entry['character']}{emotion_text}: {entry['dialogue'][:50]}...")

                if st.button("Continue to Character Mapping"):
                    st.session_state.current_step = 2
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Step 2: Character Mapping
elif st.session_state.current_step == 2:
    st.header("Step 2: Map Characters to Voices")

    if not st.session_state.parsed_data:
        st.warning("Please enter text first!")
        if st.button("Back to Text Input"):
            st.session_state.current_step = 1
            st.rerun()
    else:
        characters = list(set([entry['character'] for entry in st.session_state.parsed_data]))
        voice_models = OPENAI_VOICES if st.session_state.api_provider == "openai" else MOCK_VOICES

        with st.form("character_mapping"):
            for character in characters:
                col1, col2 = st.columns([3, 1])
                with col1:
                    voice = st.selectbox(f"Voice for {character}:",
                                       options=list(voice_models.keys()),
                                       key=f"voice_{character}")
                    st.session_state.character_voices[character] = voice

                with col2:
                    with st.expander("Voice Settings"):
                        settings = st.session_state.voice_settings.get(character, {"speed": 1.0})
                        settings["speed"] = st.slider("Speed:",
                                                    0.5, 2.0, settings["speed"], 0.1,
                                                    key=f"speed_{character}")
                        st.session_state.voice_settings[character] = settings

            if st.form_submit_button("Save Voices"):
                st.success("Voice mappings saved!")
                if st.button("Continue to Voice Generation"):
                    st.session_state.current_step = 3
                    st.rerun()

# Step 3: Voice Generation
elif st.session_state.current_step == 3:
    st.header("Step 3: Generate Character Voices")

    if not st.session_state.parsed_data or not st.session_state.character_voices:
        st.warning("Please map characters first!")
        if st.button("Back to Character Mapping"):
            st.session_state.current_step = 2
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            speed = st.slider("Speech Speed:", 0.5, 2.0, 1.0, 0.1)
        with col2:
            pitch = st.slider("Voice Pitch:", -20, 20, 0, 5)

        if st.button("Generate Audio"):
            st.session_state.audio_files = []
            progress = st.progress(0)
            status = st.empty()

            for i, entry in enumerate(st.session_state.parsed_data):
                status.text(f"Generating: {entry['character']}")
                try:
                    voice_name = st.session_state.character_voices[entry['character']]
                    voice_model = OPENAI_VOICES[voice_name] if st.session_state.api_provider == "openai" else voice_name

                    audio_file = generate_voice(
                        entry['dialogue'],
                        voice_model,
                        speed,
                        pitch,
                        entry.get('emotion')
                    )

                    if audio_file:
                        st.session_state.audio_files.append({
                            'character': entry['character'],
                            'dialogue': entry['dialogue'],
                            'file_path': audio_file
                        })
                except Exception as e:
                    st.error(f"Error with {entry['character']}: {str(e)}")

                progress.progress((i + 1) / len(st.session_state.parsed_data))

            if st.session_state.audio_files:
                status.text("Combining audio...")
                try:
                    final_audio = combine_audio_files([af['file_path'] for af in st.session_state.audio_files])
                    st.session_state.final_audio = final_audio
                    status.text("Done!")

                    if st.button("Continue to Audio Output"):
                        st.session_state.current_step = 4
                        st.rerun()
                except Exception as e:
                    st.error(f"Error combining audio: {str(e)}")

# Step 4: Audio Output
elif st.session_state.current_step == 4:
    st.header("Step 4: Listen to Your Audio Story")

    if not st.session_state.final_audio:
        st.warning("Please generate audio first!")
        if st.button("Back to Voice Generation"):
            st.session_state.current_step = 3
            st.rerun()
    else:
        st.audio(st.session_state.final_audio)

        with open(st.session_state.final_audio, "rb") as file:
            st.download_button(
                "Download Audio",
                file,
                "voicecanvas_story.mp3",
                "audio/mp3"
            )

        st.subheader("Individual Character Clips")
        for audio_entry in st.session_state.audio_files:
            with st.expander(f"{audio_entry['character']}: {audio_entry['dialogue'][:50]}..."):
                st.audio(audio_entry['file_path'])

        feedback = st.text_area("How was your experience?")
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")

        if st.button("Start New Project"):
            for key in ['parsed_data', 'character_voices', 'audio_files', 'final_audio']:
                st.session_state[key] = None if key == 'final_audio' else []
            st.session_state.current_step = 1
            st.rerun()

# Footer
st.markdown("---")
st.markdown("© 2025 VoiceCanvas | Made with ❤️ for KUKU FM Project K")
