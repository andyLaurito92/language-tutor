import io
import tempfile
import wave
from typing import Optional, Tuple, Dict, Any
import speech_recognition as sr
import streamlit as st

# Try to import OpenAI for Whisper support
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class SpeechHandler:
    """Handles speech recognition and text-to-speech functionality."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize speech handler with configuration.
        
        Args:
            config: Dictionary containing speech configuration
                - openai_api_key: OpenAI API key (if using OpenAI)
                - stt_provider: 'openai', 'google', or 'offline'
                - tts_provider: 'openai' or None
        """
        self.config = config
        
        # Handle both old and new config formats
        if 'provider' in config:
            # Old format: {'provider': 'openai', 'api_key': 'key'}
            self.provider = config.get('provider', 'google')
            api_key = config.get('api_key')
        else:
            # New format: {'stt_provider': 'openai', 'openai_api_key': 'key'}
            self.provider = config.get('stt_provider', 'google')
            api_key = config.get('openai_api_key')
        
        # Initialize OpenAI client if using OpenAI Whisper
        if self.provider == 'openai' and OPENAI_AVAILABLE and api_key:
            self.client = OpenAI(api_key=api_key)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
        except Exception as e:
            st.warning(f"Microphone not available: {e}")
            self.microphone = None
    
    def transcribe_audio(self, audio_file) -> str:
        """Transcribe audio using the configured provider."""
        if self.provider == 'openai' and OPENAI_AVAILABLE:
            return self._transcribe_with_openai(audio_file)
        else:
            return self._transcribe_with_speech_recognition(audio_file)
    
    def _transcribe_with_openai(self, audio_file) -> str:
        """Transcribe audio using OpenAI Whisper."""
        try:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            return transcript
        except Exception as e:
            st.error(f"Error with OpenAI Whisper: {str(e)}")
            # Fallback to speech recognition
            return self._transcribe_with_speech_recognition(audio_file)
    
    def _transcribe_with_speech_recognition(self, audio_file) -> str:
        """Transcribe audio using SpeechRecognition library."""
        try:
            # If audio_file is a file path, read it
            if isinstance(audio_file, str):
                with sr.AudioFile(audio_file) as source:
                    audio = self.recognizer.record(source)
            elif hasattr(audio_file, 'read'):
                # If it's a file-like object (BytesIO), we need to convert it to AudioData
                # Save to temporary file and read it back
                audio_file.seek(0)  # Reset file pointer
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                    tmp_file.write(audio_file.read())
                    tmp_file_path = tmp_file.name
                
                try:
                    with sr.AudioFile(tmp_file_path) as source:
                        audio = self.recognizer.record(source)
                finally:
                    # Clean up temporary file
                    import os
                    try:
                        os.unlink(tmp_file_path)
                    except:
                        pass
            else:
                # Assume it's already AudioData
                audio = audio_file
            
            # Try Google Speech Recognition (free)
            if self.provider == 'google':
                return self.recognizer.recognize_google(audio)
            # Try offline recognition (requires additional setup)
            elif self.provider == 'offline':
                return self.recognizer.recognize_sphinx(audio)
            else:
                # Default to Google
                return self.recognizer.recognize_google(audio)
                
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            st.error(f"Error with speech recognition service: {e}")
            return "Speech recognition service error"
        except Exception as e:
            st.error(f"Error transcribing audio: {str(e)}")
            return ""
    
    def recognize_speech_from_microphone(self, timeout: int = 5, phrase_time_limit: int = 10) -> Tuple[bool, str]:
        """
        Capture speech from microphone and transcribe it.
        
        Returns:
            Tuple[bool, str]: (success, transcribed_text_or_error_message)
        """
        if not self.microphone:
            return False, "Microphone not available"
            
        try:
            with self.microphone as source:
                st.info("🎤 Listening... Speak now!")
                # Listen for audio input
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            # Check if we got audio data
            if not audio:
                return False, "No audio captured"
            
            # For OpenAI Whisper, we need to convert to a file-like object
            if self.provider == 'openai' and OPENAI_AVAILABLE:
                try:
                    # Convert audio to file-like object for Whisper
                    wav_data = audio.get_wav_data()
                    wav_file = io.BytesIO(wav_data)
                    wav_file.name = "audio.wav"
                    
                    # Transcribe using Whisper
                    transcription = self.transcribe_audio(wav_file)
                except Exception as e:
                    st.error(f"Error processing audio for OpenAI: {str(e)}")
                    # Fallback to direct audio processing
                    transcription = self._transcribe_with_speech_recognition(audio)
            else:
                # Use the audio data directly with speech_recognition
                transcription = self._transcribe_with_speech_recognition(audio)
            
            if transcription and transcription.strip():
                return True, transcription.strip()
            else:
                return False, "Could not transcribe audio"
                
        except sr.WaitTimeoutError:
            return False, "Listening timeout - no speech detected"
        except sr.UnknownValueError:
            return False, "Could not understand audio"
        except sr.RequestError as e:
            return False, f"Could not request results; {e}"
        except Exception as e:
            return False, f"Error during speech recognition: {str(e)}"
    
    def text_to_speech(self, text: str, language: str = "en") -> Optional[bytes]:
        """
        Convert text to speech using OpenAI TTS.
        
        Args:
            text: Text to convert to speech
            language: Language code for the text
            
        Returns:
            Audio bytes or None if error
        """
        if not hasattr(self, 'client') or not self.client:
            st.warning("Text-to-speech not available (OpenAI API key not configured)")
            return None
            
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",  # You can change this to nova, echo, fable, onyx, or shimmer
                input=text
            )
            
            return response.content
            
        except Exception as e:
            st.error(f"Error generating speech: {str(e)}")
            return None
    
    def play_audio_response(self, text: str, language: str = "en"):
        """Generate and play audio response."""
        audio_bytes = self.text_to_speech(text, language)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
    
    @staticmethod
    def get_supported_languages():
        """Get list of languages supported by Whisper."""
        return [
            "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh",
            "ar", "hi", "tr", "pl", "nl", "sv", "da", "no", "fi"
        ]
