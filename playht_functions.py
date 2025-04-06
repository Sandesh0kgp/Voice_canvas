# Function to get PlayHT voices
def get_playht_voices():
    """Get available voice models from PlayHT API."""
    if not st.session_state.playht_key or not st.session_state.playht_user_id:
        return []
        
    try:
        url = "https://api.play.ht/api/v2/voices"
        headers = {
            "Accept": "application/json",
            "AUTHORIZATION": st.session_state.playht_key,
            "X-USER-ID": st.session_state.playht_user_id
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            voices = response.json()
            # Filter to only include cloned voices
            cloned_voices = [v for v in voices if v.get('isCloned', False)]
            return cloned_voices
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
        url = "https://api.play.ht/api/v2/cloned-voices"
        headers = {
            "Accept": "application/json",
            "AUTHORIZATION": st.session_state.playht_key,
            "X-USER-ID": st.session_state.playht_user_id
        }
        
        # Read the audio file
        with open(audio_file_path, 'rb') as f:
            files = {
                'sample_file': (os.path.basename(audio_file_path), f, 'audio/mpeg')
            }
            
            data = {
                'voice_name': name,
                'description': description
            }
            
            response = requests.post(url, headers=headers, data=data, files=files)
            
            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                return result.get('id')
            else:
                st.error(f"Error creating voice clone: {response.status_code} - {response.text}")
                return None
    except Exception as e:
        st.error(f"Error connecting to PlayHT API: {str(e)}")
        return None

# Function to check voice clone status
def check_playht_voice_clone_status(voice_id):
    """Check the status of a voice clone process."""
    if not st.session_state.playht_key or not st.session_state.playht_user_id:
        return None
        
    try:
        url = f"https://api.play.ht/api/v2/cloned-voices/{voice_id}"
        headers = {
            "Accept": "application/json",
            "AUTHORIZATION": st.session_state.playht_key,
            "X-USER-ID": st.session_state.playht_user_id
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
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
        url = "https://api.play.ht/api/v2/tts"
        headers = {
            "Accept": "application/json",
            "AUTHORIZATION": st.session_state.playht_key,
            "X-USER-ID": st.session_state.playht_user_id,
            "Content-Type": "application/json"
        }
        
        # Apply emotion through text modification if provided
        if emotion:
            text = f"[{emotion}] {text}"
        
        data = {
            "text": text,
            "voice": voice_id,
            "output_format": "mp3",
            "speed": speed,
            "sample_rate": 24000
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            audio_url = result.get('url')
            
            if audio_url:
                # Download the audio file
                audio_response = requests.get(audio_url)
                
                # Save the audio to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                    temp_file.write(audio_response.content)
                    return temp_file.name
            else:
                st.error("No audio URL returned from PlayHT")
                return None
        else:
            st.error(f"Error generating audio: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None