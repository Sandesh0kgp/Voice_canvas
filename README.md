# 🎨 VoiceCanvas

VoiceCanvas is a powerful text-to-speech platform built with Streamlit that transforms written stories, dialogues, and scripts into expressive voice narrations. It leverages multiple voice providers and background audio options to create professional audio content.

## 🚀 Features

### ✨ Voice Generation
- Convert text to natural-sounding speech
- Auto-parse dialogue with character detection
- Convert paragraphs to dialogue with AI
- Assign unique voices to each character
- Add expression and emotion to narration

### 🌍 Voice Dubbing
- Translate audio between languages
- Maintain original voice characteristics
- Preserve emotional tone and inflection
- Support for multiple target languages
- Option to use different voices for dubbing

### 🎵 Enhanced Audio
- Add background music tracks
- Include ambient sound effects
- Dynamic volume automation
- Multiple track layering
- Audio fine-tuning controls

### 📂 Project Management
- Save and load projects
- Export audio in multiple formats
- Create project templates
- Batch process multiple files
- Version control for projects

## 🛠️ Technical Requirements

- Python 3.11 or higher
- Dependencies:
  - groq>=0.22.0
  - openai>=1.70.0
  - pandas>=2.2.3
  - pydub>=0.25.1
  - requests>=2.32.3
  - streamlit>=1.44.1

## 🚀 Getting Started

1. Clone this project on Replit
2. Set up your API keys:
   - OpenAI API key
   - ElevenLabs API key
   - Groq API key (optional)

3. Run the application using the "Run" button

The app will be available at the provided Replit URL.

## 💡 Usage

1. **Voice Generation**
   - Enter your text or upload a file
   - Assign voices to characters
   - Add background music
   - Generate and export audio

2. **Voice Dubbing**
   - Upload audio file
   - Select target language
   - Choose dubbing provider
   - Generate dubbed version

## 📊 Analytics

- Track project engagement
- Perform A/B testing on voices
- Compare audio variants
- Monitor audience feedback
- Get quality improvement insights

## 🎯 Project Structure

```
├── app.py              # Main application file
├── pyproject.toml      # Project dependencies└── README.md          # Project documentation
```

## 🔑 API Integration

VoiceCanvas integrates with multiple external services:
- OpenAI API for text-to-speech
- ElevenLabs API for realistic voice generation
- Groq API for paragraph-to-dialogue conversion

## 📝 License

This project is MIT licensed.
