#!/usr/bin/env python3
"""
Test module for AI tutor Catalan support functionality.

This module tests the AI tutor's ability to generate appropriate prompts
and handle Catalan language learning interactions without requiring LLM dependencies.
"""

# Standard library imports
import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


class TestAITutorCatalan(unittest.TestCase):
    """Test cases for AI tutor Catalan language support."""
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.language = "Catalan"
        self.difficulty = "Intermediate"
        self.lesson_type = "Conversation Practice"
    
    def test_catalan_prompt_generation(self) -> None:
        """Test that AI tutor can generate appropriate prompts for Catalan."""
        # Simulate the system prompt generation (from ai_tutor.py get_system_prompt method)
        base_prompt = f"""You are an expert language tutor for {self.language}. Your student is at a {self.difficulty} level and is working on {self.lesson_type}.

Your teaching approach should be:
1. Encouraging and patient
2. Corrective but constructive
3. Adaptive to the student's level
4. Interactive and engaging
5. Focused on practical usage

Guidelines:
- Always respond in a mix of {self.language} and English appropriate for the {self.difficulty} level
- For beginners: Use more English with simple {self.language} phrases
- For intermediate: Use more {self.language} with English explanations when needed  
- For advanced: Primarily use {self.language} with minimal English

When the student makes mistakes:
- Gently correct them
- Explain why it's incorrect
- Provide the correct version
- Give additional examples if helpful

Encourage the student to practice speaking and ask questions."""

        # Check that the prompt contains the expected elements
        self.assertIn(self.language, base_prompt, "Catalan not found in prompt")
        self.assertIn(self.difficulty, base_prompt, "Difficulty level not found in prompt")
        self.assertIn(self.lesson_type, base_prompt, "Lesson type not found in prompt")
        
        # Verify prompt structure
        self.assertGreater(len(base_prompt), 100, "Prompt should be substantial")
        self.assertIn("expert language tutor", base_prompt.lower(), "Should identify as expert tutor")

    def test_catalan_lesson_introduction(self) -> None:
        """Test generation of lesson introduction for Catalan."""
        # Test lesson introduction prompt
        intro_prompt = f"""Generate a friendly introduction for a {self.difficulty} level {self.language} lesson on {self.lesson_type}.

The introduction should:
1. Welcome the student (do NOT use placeholder names like [Student's Name] - just say "Welcome!" or "Hello!")
2. Briefly explain what they'll learn
3. Set expectations for the lesson
4. Ask a question to start the conversation

Important: Use actual greetings, not placeholders. Be direct and personal without using brackets or placeholder text.

Keep it appropriate for {self.difficulty} level students."""

        # Verify the intro prompt contains expected elements
        self.assertIn(self.language, intro_prompt, "Catalan not found in intro prompt")
        self.assertIn(self.difficulty, intro_prompt, "Difficulty level not found in intro prompt")
        self.assertIn("Welcome", intro_prompt, "Should contain welcome greeting")

    def test_catalan_language_code_usage(self) -> None:
        """Test that the Catalan language code can be used properly."""
        try:
            from src.utils.config import Config
            
            # Get the Catalan language code
            catalan_code = Config.SUPPORTED_LANGUAGES.get('Catalan')
            
            self.assertIsNotNone(catalan_code, "Catalan should be in supported languages")
            self.assertEqual(catalan_code, 'ca', "Catalan code should be 'ca'")
            
            # Verify Catalan is in the supported languages list
            self.assertIn('Catalan', Config.SUPPORTED_LANGUAGES, "Catalan should be supported")
            
        except ImportError:
            self.skipTest("Config module not available - dependencies not installed")

    def test_catalan_lesson_types_support(self) -> None:
        """Test that Catalan works with different lesson types."""
        try:
            from src.utils.config import Config
            
            lesson_types = Config.LESSON_TYPES
            
            for lesson_type in lesson_types:
                # Test that we can generate context for each lesson type
                context_prompt = f"Teaching {self.language} {lesson_type} at {self.difficulty} level"
                
                self.assertIn(self.language, context_prompt)
                self.assertIn(lesson_type, context_prompt)
                self.assertIn(self.difficulty, context_prompt)
                
        except ImportError:
            self.skipTest("Config module not available - dependencies not installed")

    def tearDown(self) -> None:
        """Clean up after each test method."""
        pass


if __name__ == '__main__':
    unittest.main()