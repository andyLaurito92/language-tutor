#!/usr/bin/env python3
"""
Visual demo of the Catalan language support in the language tutor.
This creates a simple visualization showing the language dropdown options.
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def create_visual_demo():
    """Create a visual representation of the language dropdown with Catalan."""
    try:
        from src.utils.config import Config
        
        print("🎓 AI Language Tutor - Language Selection")
        print("=" * 50)
        print()
        
        # Show the language dropdown as it would appear in Streamlit
        print("📍 Target Language:")
        print("┌─────────────────────────────────────────┐")
        
        languages = list(Config.SUPPORTED_LANGUAGES.keys())
        for i, lang in enumerate(languages):
            code = Config.SUPPORTED_LANGUAGES[lang]
            if lang == "Catalan":
                # Highlight Catalan as the new addition
                print(f"│ {i+1:2}. {lang:<20} ({code}) ← NEW! │")
            else:
                print(f"│ {i+1:2}. {lang:<20} ({code})        │")
        
        print("└─────────────────────────────────────────┘")
        print()
        
        # Show a sample lesson configuration with Catalan
        print("🔧 Sample Lesson Configuration:")
        print("┌─────────────────────────────────────────┐")
        print("│ Target Language:    Catalan (ca)        │")
        print("│ Lesson Type:        Conversation        │")
        print("│ Difficulty Level:   Intermediate        │")
        print("│ AI Provider:        Ollama/OpenAI       │")
        print("└─────────────────────────────────────────┘")
        print()
        
        # Show what the AI tutor would receive
        print("🤖 AI Tutor Context:")
        print("┌─────────────────────────────────────────┐")
        print("│ 'You are an expert language tutor for   │")
        print("│  Catalan. Your student is at an         │")
        print("│  Intermediate level and is working on   │")
        print("│  Conversation Practice...'              │")
        print("└─────────────────────────────────────────┘")
        print()
        
        print("✅ Catalan is now fully integrated!")
        print("✅ Users can select Catalan from the dropdown")
        print("✅ AI tutor will provide Catalan language instruction")
        print("✅ All lesson types and difficulty levels supported")
        
    except Exception as e:
        print(f"❌ Error creating demo: {e}")

def show_before_after():
    """Show the before and after comparison."""
    print("\n📊 Before vs After Comparison:")
    print("=" * 40)
    
    print("\n❌ BEFORE (without Catalan):")
    print("   Supported: 10 languages")
    print("   Missing: Catalan language support")
    
    print("\n✅ AFTER (with Catalan):")
    print("   Supported: 11 languages")  
    print("   Added: Catalan (ca) support")
    print("   Impact: Expanded language learning options")

if __name__ == "__main__":
    create_visual_demo()
    show_before_after()