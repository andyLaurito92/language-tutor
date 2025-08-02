#!/usr/bin/env python3
"""
Simple command-line interface for the AI Language Tutor.
This provides a basic way to test the tutor functionality without Streamlit.
"""

import os
import sys
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Local imports
from src.tutor.ai_tutor import AITutor
from src.tutor.lessons import LessonManager
from src.utils.config import Config
from src.utils.database import ProgressTracker

class SimpleTutor:
    def __init__(self):
        self.tutor = None
        self.lesson_manager = LessonManager()
        self.progress_tracker = ProgressTracker()
        self.session_id = None
        self.user_id = "cli_user"
        
    def setup(self):
        """Initialize the tutor."""
        try:
            Config.validate_config()
            
            # Initialize AI tutor with the configured provider
            self.tutor = AITutor.from_config(Config)
            
            print(f"✅ AI Tutor initialized with {Config.MODEL_PROVIDER}")
            if Config.MODEL_PROVIDER == 'ollama':
                print(f"🦙 Using Ollama model: {Config.OLLAMA_MODEL}")
                print("💡 Make sure Ollama is running: 'ollama serve'")
            elif Config.MODEL_PROVIDER == 'openai':
                print(f"🤖 Using OpenAI model: {Config.OPENAI_MODEL}")
            
            return True
        except Exception as e:
            print(f"❌ Error initializing tutor: {e}")
            if Config.MODEL_PROVIDER == 'ollama':
                print("💡 Make sure Ollama is installed and running:")
                print("   1. Install: brew install ollama")
                print("   2. Start: ollama serve")
                print("   3. Download model: ollama pull llama3.2")
            return False
    
    def select_language(self):
        """Let user select a language."""
        languages = list(Config.SUPPORTED_LANGUAGES.keys())
        print("\nAvailable languages:")
        for i, lang in enumerate(languages, 1):
            print(f"{i}. {lang}")
        
        while True:
            try:
                choice = int(input("\nSelect a language (number): ")) - 1
                if 0 <= choice < len(languages):
                    return languages[choice]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def select_difficulty(self):
        """Let user select difficulty level."""
        levels = Config.DIFFICULTY_LEVELS
        print("\nDifficulty levels:")
        for i, level in enumerate(levels, 1):
            print(f"{i}. {level}")
        
        while True:
            try:
                choice = int(input("\nSelect difficulty (number): ")) - 1
                if 0 <= choice < len(levels):
                    return levels[choice]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def select_lesson_type(self):
        """Let user select lesson type."""
        types = Config.LESSON_TYPES
        print("\nLesson types:")
        for i, lesson_type in enumerate(types, 1):
            print(f"{i}. {lesson_type}")
        
        while True:
            try:
                choice = int(input("\nSelect lesson type (number): ")) - 1
                if 0 <= choice < len(types):
                    return types[choice]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def start_lesson(self, language, difficulty, lesson_type):
        """Start a new lesson."""
        # Get lesson content
        lessons = self.lesson_manager.get_lessons(
            lesson_type.lower().replace(' ', '_'), 
            difficulty.lower()
        )
        lesson_data = lessons[0] if lessons else {}
        
        # Set tutor context
        self.tutor.set_learning_context(language, difficulty, lesson_type, lesson_data)
        
        # Start session tracking
        self.session_id = self.progress_tracker.start_session(
            self.user_id, language, lesson_type, difficulty
        )
        
        print(f"\n🎓 Starting {difficulty} level {lesson_type} lesson for {language}")
        if lesson_data:
            print(f"Lesson: {lesson_data.get('title', 'General Practice')}")
            print(f"Description: {lesson_data.get('description', '')}")
        
        # Generate and show introduction
        intro = self.tutor.generate_lesson_introduction()
        print(f"\n🤖 Tutor: {intro}")
        
        return True
    
    def chat_loop(self):
        """Main conversation loop."""
        print("\n" + "="*50)
        print("💬 Conversation started! Type 'quit' to end the lesson.")
        print("="*50)
        
        while True:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            
            if not user_input:
                continue
            
            # Process input
            print("🤔 Thinking...")
            response_data = self.tutor.process_student_input(user_input, "text")
            
            # Show response
            print(f"\n🤖 Tutor: {response_data['response']}")
            
            # Show feedback if available
            feedback = response_data.get('feedback', {})
            if feedback:
                print("\n📊 Feedback:")
                if 'grammar_score' in feedback:
                    print(f"   Grammar Score: {feedback['grammar_score']}/10")
                if feedback.get('errors'):
                    print(f"   Areas to improve: {', '.join(feedback['errors'])}")
                if feedback.get('strengths'):
                    print(f"   Strengths: {', '.join(feedback['strengths'])}")
            
            # Log interaction
            if self.session_id:
                self.progress_tracker.log_interaction(
                    self.session_id,
                    user_input,
                    response_data['response'],
                    int(response_data.get('confidence_score', 0.8) * 10)
                )
    
    def end_lesson(self):
        """End the current lesson."""
        if self.session_id:
            # End session with average score
            score = 8  # Could be calculated from feedback
            self.progress_tracker.end_session(self.session_id, score)
            
            # Show lesson summary
            summary = self.tutor.get_lesson_summary()
            print("\n" + "="*50)
            print("📋 LESSON SUMMARY")
            print("="*50)
            print(f"Summary: {summary.get('summary', 'Great practice session!')}")
            
            if summary.get('achievements'):
                print(f"\n✅ Achievements:")
                for achievement in summary['achievements']:
                    print(f"   • {achievement}")
            
            if summary.get('areas_to_improve'):
                print(f"\n📈 Areas to improve:")
                for area in summary['areas_to_improve']:
                    print(f"   • {area}")
            
            if summary.get('next_steps'):
                print(f"\n🎯 Next steps:")
                for step in summary['next_steps']:
                    print(f"   • {step}")
            
            print("\n" + "="*50)
    
    def show_progress(self):
        """Show user progress."""
        progress = self.progress_tracker.get_user_progress(self.user_id)
        
        print("\n" + "="*50)
        print("📊 YOUR PROGRESS")
        print("="*50)
        print(f"Total Sessions: {progress['total_sessions']}")
        print(f"Total Time: {progress['total_time']//60} minutes")
        print(f"Average Score: {progress['average_score']:.1f}/10")
        
        if progress['sessions']:
            print("\nSession Details:")
            for session in progress['sessions']:
                print(f"  {session['language']} - {session['lesson_type']} ({session['difficulty']})")
                print(f"    Sessions: {session['session_count']}, Avg Score: {session['average_score']:.1f}")
        
        print("="*50)
    
    def run(self):
        """Main application loop."""
        print("🎓 Welcome to AI Language Tutor!")
        print("="*40)
        
        if not self.setup():
            return
        
        while True:
            print("\nWhat would you like to do?")
            print("1. Start a new lesson")
            print("2. View progress") 
            print("3. Quit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                language = self.select_language()
                difficulty = self.select_difficulty()
                lesson_type = self.select_lesson_type()
                
                if self.start_lesson(language, difficulty, lesson_type):
                    self.chat_loop()
                    self.end_lesson()
                    
            elif choice == '2':
                self.show_progress()
                
            elif choice == '3':
                print("\n👋 Goodbye! Keep practicing!")
                break
                
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    tutor = SimpleTutor()
    tutor.run()
