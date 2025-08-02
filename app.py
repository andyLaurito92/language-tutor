import streamlit as st
import os
import sys
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.config import Config
from src.utils.database import ProgressTracker
from src.tutor.ai_tutor import AITutor
from src.tutor.speech import SpeechHandler
from src.tutor.lessons import LessonManager

# Page configuration
st.set_page_config(
    page_title="AI Language Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables."""
    if 'config_validated' not in st.session_state:
        st.session_state.config_validated = False
    
    if 'tutor' not in st.session_state:
        st.session_state.tutor = None
    
    if 'speech_handler' not in st.session_state:
        st.session_state.speech_handler = None
        
    if 'lesson_manager' not in st.session_state:
        st.session_state.lesson_manager = LessonManager()
    
    if 'progress_tracker' not in st.session_state:
        st.session_state.progress_tracker = ProgressTracker()
    
    if 'current_session_id' not in st.session_state:
        st.session_state.current_session_id = None
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = "default_user"  # In production, implement proper user auth

def validate_configuration():
    """Validate configuration for selected provider."""
    try:
        Config.validate_config()
        st.session_state.config_validated = True
        return True
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        
        # Get current provider
        provider = os.getenv('MODEL_PROVIDER', 'openai')
        
        if provider == 'openai':
            st.info("Please set your OPENAI_API_KEY in the .env file or as an environment variable.")
        elif provider == 'ollama':
            st.info("Please ensure Ollama is running locally or check your OLLAMA_BASE_URL configuration.")
        
        return False

def setup_sidebar():
    """Setup the sidebar with learning options."""
    st.sidebar.title("🎓 AI Language Tutor")
    
    # Model provider selection
    provider = st.sidebar.selectbox(
        "AI Provider",
        options=["openai", "ollama"],
        index=0 if os.getenv('MODEL_PROVIDER', 'openai') == 'openai' else 1,
        help="Choose between OpenAI (cloud) or Ollama (local) models",
        key="model_provider"
    )
    
    # Update environment variable
    os.environ['MODEL_PROVIDER'] = provider
    
    if provider == 'ollama':
        # Get available Ollama models dynamically
        available_models = ["llama3.1", "llama3.2", "qwen2", "mistral", "gemma2"]  # Default options
        
        try:
            import requests
            ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            response = requests.get(f"{ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models_data = response.json().get('models', [])
                if models_data:
                    # Extract model names and add them to the list
                    detected_models = [model['name'] for model in models_data]
                    # Combine detected models with defaults, remove duplicates
                    all_models = list(set(available_models + detected_models))
                    available_models = sorted(all_models)
        except:
            # If we can't connect to Ollama, use default list
            pass
        
        # Ollama model selection with smart defaults
        default_index = 0
        if "mistral:latest" in available_models:
            default_index = available_models.index("mistral:latest")
        elif "llama3.2:latest" in available_models:
            default_index = available_models.index("llama3.2:latest")
        elif "mistral" in available_models:
            default_index = available_models.index("mistral")
        elif "llama3.2" in available_models:
            default_index = available_models.index("llama3.2")
        
        ollama_model = st.sidebar.selectbox(
            "Ollama Model",
            options=available_models,
            index=default_index,
            help="Select the local Ollama model to use",
            key="ollama_model"
        )
        os.environ['OLLAMA_MODEL'] = ollama_model
        
        # Show Ollama status
        try:
            import requests
            ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            response = requests.get(f"{ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                st.sidebar.success("🟢 Ollama Connected")
            else:
                st.sidebar.error("🔴 Ollama Not Responding")
        except:
            st.sidebar.error("🔴 Ollama Not Available")
    
    # Language selection
    selected_language = st.sidebar.selectbox(
        "Target Language",
        options=list(Config.SUPPORTED_LANGUAGES.keys()),
        key="selected_language"
    )
    
    # Lesson type selection
    lesson_type = st.sidebar.selectbox(
        "Lesson Type",
        options=Config.LESSON_TYPES,
        key="lesson_type"
    )
    
    # Difficulty level
    difficulty = st.sidebar.selectbox(
        "Difficulty Level",
        options=Config.DIFFICULTY_LEVELS,
        key="difficulty"
    )
    
    # Voice input toggle
    use_voice = st.sidebar.checkbox("Enable Voice Input 🎤", key="use_voice")
    
    # Start new lesson button
    if st.sidebar.button("Start New Lesson", type="primary"):
        start_new_lesson(selected_language, lesson_type, difficulty)
    
    # Progress section
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Your Progress")
    
    if st.sidebar.button("View Progress"):
        show_progress()
    
    return selected_language, lesson_type, difficulty, use_voice

def start_new_lesson(language: str, lesson_type: str, difficulty: str):
    """Start a new learning lesson."""
    try:
        # Initialize tutor if not already done or if provider changed
        if not st.session_state.tutor:
            config = Config()
            model_config = config.get_model_config()
            st.session_state.tutor = AITutor.from_config(config)
        
        # Initialize speech handler if not already done
        if not st.session_state.speech_handler:
            # Create speech configuration
            openai_key = os.getenv('OPENAI_API_KEY')
            speech_config = {
                'openai_api_key': openai_key,
                'stt_provider': 'openai' if openai_key else 'google',
                'tts_provider': 'openai' if openai_key else None
            }
            st.session_state.speech_handler = SpeechHandler(speech_config)
        
        # Get lesson content
        lessons = st.session_state.lesson_manager.get_lessons(
            lesson_type.lower().replace(' ', '_'), 
            difficulty.lower()
        )
        
        lesson_data = lessons[0] if lessons else {}
        
        # Set learning context
        st.session_state.tutor.set_learning_context(language, difficulty, lesson_type, lesson_data)
        
        # Start tracking session
        session_id = st.session_state.progress_tracker.start_session(
            st.session_state.user_id, language, lesson_type, difficulty
        )
        st.session_state.current_session_id = session_id
        
        # Clear conversation history
        st.session_state.conversation_history = []
        
        # Generate lesson introduction
        intro = st.session_state.tutor.generate_lesson_introduction()
        st.session_state.conversation_history.append({
            "role": "tutor",
            "content": intro,
            "timestamp": datetime.now()
        })
        
        provider = os.getenv('MODEL_PROVIDER', 'openai')
        st.success(f"Started new {difficulty} level {lesson_type} lesson for {language} using {provider.title()}!")
        
    except ImportError as e:
        st.error(f"Model provider not available: {str(e)}")
        st.error("Check your model provider configuration and try again.")
    except ValueError as e:
        st.error(f"Configuration error: {str(e)}") 
        st.error("Check your model provider configuration and try again.")
    except Exception as e:
        st.error(f"Error starting lesson: {str(e)}")
        st.error("Check your model provider configuration and try again.")
        return
    
    # Rerun after successful lesson start
    st.rerun()

def show_progress():
    """Display user progress."""
    progress_data = st.session_state.progress_tracker.get_user_progress(st.session_state.user_id)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sessions", progress_data['total_sessions'])
    
    with col2:
        st.metric("Total Time (minutes)", f"{progress_data['total_time'] // 60}")
    
    with col3:
        st.metric("Average Score", f"{progress_data['average_score']:.1f}")
    
    if progress_data['sessions']:
        st.subheader("Session Details")
        for session in progress_data['sessions']:
            with st.expander(f"{session['language']} - {session['lesson_type']} ({session['difficulty']})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"Sessions: {session['session_count']}")
                with col2:
                    st.write(f"Avg Score: {session['average_score']:.1f}")
                with col3:
                    st.write(f"Time: {session['time_spent'] // 60} min")

def handle_voice_input():
    """Handle voice input from user."""
    if st.button("🎤 Start Recording", key="record_button"):
        with st.spinner("Listening... Please speak now!"):
            success, result = st.session_state.speech_handler.recognize_speech_from_microphone()
            
            if success:
                st.session_state.current_input = result
                st.success(f"Transcribed: {result}")
                return result
            else:
                st.error(f"Speech recognition failed: {result}")
                return None
    return None

def handle_text_input():
    """Handle text input from user."""
    # Use a unique key that changes after sending to force clearing
    if 'message_counter' not in st.session_state:
        st.session_state.message_counter = 0
    
    # Check if we're currently processing a message
    is_processing = st.session_state.get('processing_message', False)
    
    # Use a form to enable Enter key submission
    with st.form(key=f"message_form_{st.session_state.message_counter}", clear_on_submit=True):
        user_input = st.text_input(
            "Type your message:",
            key=f"text_input_{st.session_state.message_counter}",
            placeholder="Processing your message..." if is_processing else "Type your response here... (Press Enter to send)",
            disabled=is_processing
        )
        
        # Form submit button (this will be triggered by Enter key too)
        submitted = st.form_submit_button("Send", disabled=is_processing)
        
        if submitted and user_input and not is_processing:
            # Increment counter to create new form on next rerun
            st.session_state.message_counter += 1
            return user_input
    
    return None

def process_user_input(user_input: str, input_type: str):
    """Process user input and get AI response."""
    if not st.session_state.tutor:
        st.error("Please start a lesson first!")
        return
    
    # Set processing state immediately to gray out input on next render
    st.session_state.processing_message = True
    
    # Add user input to conversation history
    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now(),
        "input_type": input_type
    })
    
    # Force immediate rerun to show grayed input and user message
    st.rerun()

def continue_ai_processing():
    """Continue with AI processing after showing grayed input."""
    if not st.session_state.get('processing_message', False):
        return
    
    # Get the last user message to process
    user_messages = [msg for msg in st.session_state.conversation_history if msg["role"] == "user"]
    if not user_messages:
        st.session_state.processing_message = False
        return
        
    last_user_msg = user_messages[-1]
    
    # Get AI response
    with st.spinner("Thinking..."):
        response_data = st.session_state.tutor.process_student_input(
            last_user_msg["content"], 
            last_user_msg.get("input_type", "text")
        )
        
        # Add AI response to conversation history
        st.session_state.conversation_history.append({
            "role": "tutor",
            "content": response_data["response"],
            "timestamp": datetime.now(),
            "feedback": response_data.get("feedback", {})
        })
        
        # Log interaction with proper confidence score handling
        if st.session_state.current_session_id:
            confidence_score = response_data.get("confidence_score", 0.5)
            # Ensure confidence_score is a float and properly bounded
            try:
                confidence_float = float(confidence_score)
                confidence_float = max(0.0, min(1.0, confidence_float))  # Clamp between 0 and 1
                confidence_int = int(confidence_float * 10)
            except (ValueError, TypeError):
                confidence_int = 5  # Default fallback
                
            st.session_state.progress_tracker.log_interaction(
                st.session_state.current_session_id,
                last_user_msg["content"],
                response_data["response"],
                confidence_int
            )
    
    # Clear processing state
    st.session_state.processing_message = False
    st.rerun()

def display_conversation():
    """Display the conversation history."""
    if not st.session_state.conversation_history:
        st.info("Start a lesson to begin your conversation with the AI tutor!")
        return
    
    # Create a container for the conversation that auto-scrolls
    for idx, message in enumerate(st.session_state.conversation_history):
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
                if message.get("input_type") == "speech":
                    st.caption("🎤 Voice input")
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
                
                # Show feedback if available
                if "feedback" in message and message["feedback"]:
                    feedback = message["feedback"]
                    with st.expander("📈 Feedback", expanded=False):
                        if "grammar_score" in feedback:
                            st.metric("Grammar Score", f"{feedback['grammar_score']}/10")
                        
                        if feedback.get("errors"):
                            st.write("**Areas to improve:**")
                            for error in feedback["errors"]:
                                st.write(f"• {error}")
                        
                        if feedback.get("strengths"):
                            st.write("**Strengths:**")
                            for strength in feedback["strengths"]:
                                st.write(f"• {strength}")
                
                # Audio playback for AI response
                if st.session_state.speech_handler and st.button(f"🔊 Play Audio", key=f"play_{idx}"):
                    st.session_state.speech_handler.play_audio_response(
                        message["content"], 
                        Config.SUPPORTED_LANGUAGES.get(st.session_state.get("selected_language", "English"), "en")
                    )
    
    # Add auto-scroll behavior using a more reliable approach
    if len(st.session_state.conversation_history) > 0:
        # Create an empty element at the bottom that will force scroll
        st.empty()
        
        # Use components.html for more reliable JavaScript execution
        try:
            import streamlit.components.v1 as components
            components.html(
                """
                <script>
                // Wait for the page to fully render then scroll
                setTimeout(function() {
                    window.parent.document.querySelector('.main').scrollTop = 
                        window.parent.document.querySelector('.main').scrollHeight;
                }, 100);
                </script>
                """,
                height=0
            )
        except:
            # Fallback: use a simple markdown approach to push content down
            st.markdown("<br>" * 2, unsafe_allow_html=True)

def show_practice_exercises():
    """Show practice exercises."""
    if st.session_state.tutor:
        st.subheader("📝 Practice Exercise")
        
        if st.button("Generate New Exercise"):
            exercise = st.session_state.tutor.generate_practice_exercise()
            st.session_state.current_exercise = exercise
        
        if hasattr(st.session_state, 'current_exercise'):
            exercise = st.session_state.current_exercise
            st.write(f"**{exercise['title']}**")
            st.write(exercise['instructions'])
            st.info(exercise['content'])

def main():
    """Main application function."""
    initialize_session_state()
    
    # Validate configuration
    if not st.session_state.config_validated:
        if not validate_configuration():
            st.stop()
    
    # Setup sidebar
    language, lesson_type, difficulty, use_voice = setup_sidebar()
    
    # Main content area
    st.title("🎓 AI Language Tutor")
    st.markdown("Learn languages with AI-powered conversations, speech recognition, and personalized feedback!")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["💬 Conversation", "📝 Practice", "📊 Progress"])
    
    with tab1:
        # Display conversation
        display_conversation()
        
        # Input section
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Handle user input
            user_input = None
            
            if use_voice and st.session_state.speech_handler:
                voice_input = handle_voice_input()
                if voice_input:
                    user_input = voice_input
                    input_type = "speech"
            
            if not user_input:
                text_input = handle_text_input()
                if text_input:
                    user_input = text_input
                    input_type = "text"
            
            # Process input
            if user_input:
                process_user_input(user_input, input_type)
            
            # Continue with AI processing if we're in processing state
            if st.session_state.get('processing_message', False):
                continue_ai_processing()
        
        with col2:
            if st.button("End Lesson", type="secondary"):
                if st.session_state.current_session_id:
                    # Calculate session score based on conversation
                    avg_score = 8  # Placeholder - could be calculated from feedback
                    st.session_state.progress_tracker.end_session(
                        st.session_state.current_session_id, 
                        avg_score
                    )
                    
                    # Show lesson summary
                    if st.session_state.tutor:
                        summary = st.session_state.tutor.get_lesson_summary()
                        st.success("Lesson completed!")
                        st.write("**Summary:**", summary.get("summary", ""))
                        
                    st.session_state.current_session_id = None
    
    with tab2:
        show_practice_exercises()
    
    with tab3:
        show_progress()

if __name__ == "__main__":
    main()
