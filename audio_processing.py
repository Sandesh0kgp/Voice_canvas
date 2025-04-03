import os
import time
import tempfile
import random
import io
from pydub import AudioSegment
import streamlit as st
from gtts import gTTS

# Configure pydub to use the correct ffmpeg path
if os.name == 'nt':  # Windows
    AudioSegment.converter = r"C:\path\to\ffmpeg.exe"
    AudioSegment.ffprobe = r"C:\path\to\ffprobe.exe"
else:  # Linux/MacOS
    AudioSegment.converter = "ffmpeg"
    AudioSegment.ffprobe = "ffprobe"

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

def load_xtts_model():
    """Load the XTTS model if not already loaded."""
    if not st.session_state.tts_model_loaded:
        try:
            # Display loading message
            with st.spinner("Loading XTTS model... This may take a minute."):
                try:
                    # First try to import the dependencies
                    import torch
                    from TTS.api import TTS
                except ImportError as e:
                    st.error(f"Error importing required libraries: {str(e)}")
                    st.info("The TTS package could not be imported. Using mock audio generation instead.")
                    return False
                
                try:
                    # Initialize TTS with XTTS-v2
                    # Let's use the small model for faster loading and less memory usage
                    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
                    
                    # Check if CUDA is available and create the model
                    use_gpu = torch.cuda.is_available()
                    tts = TTS(model_name, gpu=use_gpu)
                    
                    # Store the model in session state
                    st.session_state.tts_model = tts
                    st.session_state.tts_model_loaded = True
                    st.success(f"XTTS model loaded successfully. Using GPU: {use_gpu}")
                    return True
                except Exception as e:
                    st.error(f"Error initializing XTTS model: {str(e)}")
                    st.info("Using mock audio generation instead.")
                    return False
        except Exception as e:
            st.error(f"Unexpected error loading XTTS model: {str(e)}")
            st.info("Using mock audio generation instead.")
            return False
    return True

def generate_voice_xtts(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Generate voice audio from text using XTTS-v2."""
    try:
        # Check if XTTS model is loaded, if not try to load it
        if not st.session_state.tts_model_loaded:
            if not load_xtts_model():
                st.warning("XTTS model could not be loaded. Using mock audio generation instead.")
                return generate_voice_mock(text, voice_model, speed, pitch, emotion)
        
        # Get the model from session state
        tts = st.session_state.tts_model
        
        # Apply emotion through text modification if provided
        modified_text = text
        if emotion:
            modified_text = f"[{emotion}] {text}"
        
        # Directory for reference voice files
        voice_dir = "reference_voices"
        
        # Ensure the directory exists
        if not os.path.exists(voice_dir):
            os.makedirs(voice_dir)
        
        # Define path to reference voice file
        reference_wav = f"{voice_dir}/{voice_model}.wav"
        
        # Check if reference voice file exists
        use_reference = os.path.exists(reference_wav)
        
        # Create a temporary file to save the generated audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            try:
                # Generate speech with or without reference
                if use_reference:
                    tts.tts_to_file(
                        text=modified_text,
                        file_path=temp_file.name,
                        speaker_wav=reference_wav,
                        language="en",
                        speed=speed
                    )
                else:
                    # If no reference file exists, use default voice
                    tts.tts_to_file(
                        text=modified_text,
                        file_path=temp_file.name,
                        language="en",
                        speed=speed
                    )
                
                return temp_file.name
            except Exception as e:
                # If TTS fails, log the error and fall back to mock
                st.error(f"Error during TTS generation: {str(e)}")
                os.unlink(temp_file.name)  # Clean up the temporary file
                return generate_voice_mock(text, voice_model, speed, pitch, emotion)
            
    except Exception as e:
        st.error(f"Error generating audio with XTTS: {str(e)}")
        return generate_voice_mock(text, voice_model, speed, pitch, emotion)

def generate_voice_openai(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Generate voice audio from text using OpenAI TTS."""
    try:
        # Check for API key
        api_key = st.session_state.api_key
        if not api_key:
            raise ValueError("OpenAI API Key is required but not provided.")
        
        # Import OpenAI
        from openai import OpenAI
        
        # Apply emotion through text modification if provided
        if emotion:
            text = f"[{emotion}] {text}"
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Generate speech
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice_model,
                input=text,
                speed=speed
            )
            
            # Save to file
            response.stream_to_file(temp_file.name)
            return temp_file.name
            
    except Exception as e:
        st.error(f"Error generating audio with OpenAI: {str(e)}")
        return generate_voice_mock(text, voice_model, speed, pitch, emotion)

def generate_voice_gtts(text, voice_model="en", speed=1.0, pitch=0, emotion=None):
    """Generate voice audio from text using Google Text-to-Speech with enhanced voice variety."""
    try:
        # Apply emotion through text modification if provided
        if emotion:
            emotion_prefixes = {
                "happy": "♪ ",
                "sad": "*sigh* ",
                "angry": "Grr! ",
                "surprised": "Oh! ",
                "frightened": "Oh no! ",
                "neutral": ""
            }
            
            # Get the appropriate prefix or default to emotion name
            prefix = emotion_prefixes.get(emotion.lower(), f"[{emotion}] ")
            text = f"{prefix}{text}"
        
        # Extract character type from voice model name to apply appropriate audio processing
        character_type = "neutral"
        if "narrator" in voice_model.lower():
            character_type = "narrator"
        elif "hero" in voice_model.lower():
            character_type = "hero"
        elif "heroine" in voice_model.lower():
            character_type = "heroine"
        elif "villain" in voice_model.lower():
            character_type = "villain"
        elif "elder" in voice_model.lower():
            character_type = "elder"
        elif "child" in voice_model.lower():
            character_type = "child"
        elif "comic" in voice_model.lower():
            character_type = "comic"
        elif "sidekick" in voice_model.lower():
            character_type = "sidekick"
        elif "mentor" in voice_model.lower():
            character_type = "mentor"
        elif "announcer" in voice_model.lower():
            character_type = "announcer"
            
        # Map voice_model to language code for gTTS
        # Default to "en" (English) if no mapping exists
        lang_mapping = {
            "en": "en",
            "en_us": "en",
            "en_uk": "en-uk",
            "es": "es",
            "fr": "fr",
            "de": "de",
            "it": "it",
            "pt": "pt",
            "ru": "ru",
            "ja": "ja",
            "ko": "ko",
            "zh": "zh-CN"
        }
        
        # Extract language from voice model string
        lang_code = "en"  # Default
        for code, lang in lang_mapping.items():
            if code in voice_model.lower():
                lang_code = lang
                break
        
        # Create a gTTS object with appropriate settings
        # Use 'slow' parameter for additional voice variation
        use_slow = False
        if character_type in ["elder", "mentor"]:
            use_slow = True
        elif speed < 0.9:
            use_slow = True
            
        # Create TTS object
        tts = gTTS(text=text, lang=lang_code, slow=use_slow)
        
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            tts.save(temp_file.name)
            
            # Apply character-specific audio modifications
            try:
                # Load the saved audio
                audio = AudioSegment.from_file(temp_file.name, format="mp3")
                
                # Apply different default pitch and speed adjustments based on character type
                # This creates more distinct voices even if user doesn't adjust settings
                character_adjustments = {
                    "narrator": {"pitch_mod": 0, "speed_mod": 0},
                    "hero": {"pitch_mod": -2, "speed_mod": 0.05},
                    "heroine": {"pitch_mod": 4, "speed_mod": 0.05},
                    "villain": {"pitch_mod": -4, "speed_mod": -0.1},
                    "elder": {"pitch_mod": -3, "speed_mod": -0.15},
                    "child": {"pitch_mod": 7, "speed_mod": 0.1},
                    "comic": {"pitch_mod": 3, "speed_mod": 0.2},
                    "sidekick": {"pitch_mod": 2, "speed_mod": 0.1},
                    "mentor": {"pitch_mod": -1, "speed_mod": -0.05},
                    "announcer": {"pitch_mod": -2, "speed_mod": 0.05}
                }
                
                # Get adjustments for this character type
                adj = character_adjustments.get(character_type, {"pitch_mod": 0, "speed_mod": 0})
                
                # Combine character-specific adjustments with user settings
                adjusted_speed = max(0.5, min(1.8, speed + adj["speed_mod"]))
                adjusted_pitch = pitch + adj["pitch_mod"]
                
                # Apply speed adjustment (by changing the frame rate)
                adjusted_audio = audio._spawn(audio.raw_data, overrides={
                    "frame_rate": int(audio.frame_rate * adjusted_speed)
                })
                
                # Apply pitch adjustment
                if adjusted_pitch != 0:
                    # Convert pitch value (from -20 to +20) to semitones (typical range of -12 to +12)
                    semitones = adjusted_pitch / 2.0
                    
                    # Apply pitch shift through sample rate adjustment
                    new_sample_rate = int(adjusted_audio.frame_rate * (2 ** (semitones / 12.0)))
                    adjusted_audio = adjusted_audio._spawn(adjusted_audio.raw_data, overrides={
                        "frame_rate": new_sample_rate
                    })
                
                # Maintain original frame rate
                adjusted_audio = adjusted_audio.set_frame_rate(audio.frame_rate)
                
                # Add character-specific sound processing effects
                if character_type == "villain":
                    # Add slight echo effect for villains
                    echo_overlay = adjusted_audio - 6  # Reduced volume for echo
                    adjusted_audio = adjusted_audio.overlay(echo_overlay, position=75)
                
                elif character_type == "announcer":
                    # Add a bit of bass boost for announcers
                    adjusted_audio = adjusted_audio + 2  # Slight volume boost
                
                # Save the adjusted audio
                adjusted_audio.export(temp_file.name, format="mp3")
                
            except Exception as e:
                # If audio processing fails, use the original audio
                print(f"Warning: Failed to apply audio adjustments: {e}")
            
            return temp_file.name
            
    except Exception as e:
        st.error(f"Error generating audio with gTTS: {str(e)}")
        return generate_voice_mock(text, voice_model, speed, pitch, emotion)

def generate_voice_mock(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Generate voice audio from text (mock implementation).
    
    This creates a very simple audio pattern based on the text length
    to simulate different speaking durations.
    """
    try:
        # Simulate processing time
        time.sleep(0.5)
        
        # Calculate duration based on word count
        word_count = len(text.split())
        duration = max(1000, word_count * 200)  # at least 1 second
        
        # Adjust duration based on speed
        duration = int(duration / speed)
        
        # Create a silent audio segment of appropriate length
        audio = AudioSegment.silent(duration=duration)
        
        # Add a very simple beep at the beginning to indicate start of speech
        # This is a minimal approach to avoid filter errors
        beep = AudioSegment.silent(duration=100)
        beep = beep - 10  # Make it a bit louder
        
        # Add the beep to the beginning
        audio = audio.overlay(beep, position=0)
        
        # Add a second beep at the end
        audio = audio.overlay(beep, position=duration-100)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            audio.export(temp_file.name, format="mp3")
            return temp_file.name
            
    except Exception as e:
        # Fallback to completely silent audio if there's any error
        print(f"Error in mock audio generation: {e}")
        try:
            # Create a completely silent audio segment as absolute fallback
            audio = AudioSegment.silent(duration=2000)  # 2 seconds of silence
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                audio.export(temp_file.name, format="mp3")
                return temp_file.name
        except Exception as e2:
            # If even that fails, create an empty file
            print(f"Critical error in mock audio fallback: {e2}")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(b'')
                return temp_file.name

def generate_voice(text, voice_model, speed=1.0, pitch=0, emotion=None):
    """Route to appropriate voice generation function."""
    if st.session_state.api_provider == "openai":
        return generate_voice_openai(text, voice_model, speed, pitch, emotion)
    elif st.session_state.api_provider == "gtts":
        return generate_voice_gtts(text, voice_model, speed, pitch, emotion)
    else:
        return generate_voice_xtts(text, voice_model, speed, pitch, emotion)

def get_background_music(track_name, duration_ms):
    """Get background music track or create silent audio if track not available.
    
    This is a simplified implementation that creates silent audio with occasional
    beep patterns based on the track name.
    """
    try:
        if track_name == "None" or not track_name:
            # Return silent audio of appropriate length
            return AudioSegment.silent(duration=duration_ms)
        
        # Create a base silent audio segment
        base_audio = AudioSegment.silent(duration=duration_ms)
        
        # Add a simple pattern of beeps every few seconds
        # to indicate something is happening
        beep_interval = 5000  # 5 seconds between beeps
        for i in range(0, duration_ms, beep_interval):
            # Add a brief sound
            beep = AudioSegment.silent(duration=100)
            
            # Make it audible but not intrusive
            beep = beep - 20  # Volume adjustment
            
            # Add to base audio
            if i + 100 <= duration_ms:
                base_audio = base_audio.overlay(beep, position=i)
        
        return base_audio
        
    except Exception as e:
        # Fallback to completely silent audio
        print(f"Error generating background music: {e}")
        return AudioSegment.silent(duration=duration_ms)

def combine_audio_segments(audio_files, background_track="None", bg_volume=0.3):
    """Combine audio segments into a single continuous audio, with background track."""
    try:
        if not audio_files:
            print("Warning: No audio files provided to combine.")
            # Create a placeholder 1-second audio file
            placeholder = AudioSegment.silent(duration=1000)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                placeholder.export(temp_file.name, format="mp3")
                return temp_file.name
        
        combined = AudioSegment.empty()
        
        # Track if we've successfully added any segments
        added_segments = False
        
        # Load and join all voice segments
        for audio_path in audio_files:
            try:
                segment = AudioSegment.from_file(audio_path)
                combined += segment + AudioSegment.silent(duration=500)  # Add half-second pause between segments
                added_segments = True
            except Exception as e:
                print(f"Could not load audio file {audio_path}: {e}")
                # Add a silent segment as a placeholder
                combined += AudioSegment.silent(duration=1000)
        
        # If we couldn't add any segments, create a default one
        if not added_segments or len(combined) == 0:
            print("Warning: Could not add any audio segments. Creating placeholder.")
            combined = AudioSegment.silent(duration=3000)  # 3 seconds of silence
        
        # If we have a background track, add it
        if background_track and background_track != "None":
            try:
                # Determine total duration needed
                total_duration = len(combined)
                
                # Get background track of appropriate length
                bg_audio = get_background_music(background_track, total_duration)
                
                # Adjust background volume (bg_volume is from 0.0 to 1.0)
                # Use a safer calculation to avoid extreme values
                bg_gain_db = max(-20, min(10, 20 * (bg_volume - 0.5)))  # Limit to -20dB to +10dB
                bg_audio = bg_audio + bg_gain_db
                
                # Overlay background (ensure it's the same length)
                if len(bg_audio) > len(combined):
                    bg_audio = bg_audio[:len(combined)]
                combined = bg_audio.overlay(combined)
            except Exception as e:
                print(f"Error adding background track: {e}")
                # Continue without background if there's an error
        
        # Save combined audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            combined.export(temp_file.name, format="mp3")
            return temp_file.name
            
    except Exception as e:
        print(f"Critical error in combine_audio_segments: {e}")
        # Create an emergency fallback file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            try:
                # Try to create a minimal valid MP3
                AudioSegment.silent(duration=500).export(temp_file.name, format="mp3")
            except:
                # If even that fails, just write a small amount of data
                temp_file.write(b'\x00' * 1000)
            return temp_file.name
