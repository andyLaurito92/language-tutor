from typing import List, Dict, Any
import json
import os

class LessonManager:
    """Manages lesson content and structure."""
    
    def __init__(self, lessons_path: str = "data/lessons"):
        self.lessons_path = lessons_path
        os.makedirs(lessons_path, exist_ok=True)
        self.initialize_default_lessons()
    
    def initialize_default_lessons(self):
        """Create default lesson templates if they don't exist."""
        
        # Conversation lessons
        conversation_lessons = {
            "beginner": [
                {
                    "id": "conv_begin_1",
                    "title": "Basic Greetings",
                    "description": "Learn how to greet people and introduce yourself",
                    "topics": ["hello", "goodbye", "my name is", "nice to meet you"],
                    "vocabulary": ["hello", "goodbye", "name", "please", "thank you"],
                    "sample_dialogues": [
                        {
                            "scenario": "Meeting someone new",
                            "dialogue": [
                                "A: Hello! My name is Sarah. What's your name?",
                                "B: Hi Sarah! I'm Miguel. Nice to meet you!",
                                "A: Nice to meet you too, Miguel!"
                            ]
                        }
                    ]
                },
                {
                    "id": "conv_begin_2",
                    "title": "Asking for Directions",
                    "description": "Learn how to ask for and give basic directions",
                    "topics": ["where is", "how to get to", "left", "right", "straight"],
                    "vocabulary": ["where", "left", "right", "straight", "near", "far"],
                    "sample_dialogues": [
                        {
                            "scenario": "Finding a restaurant",
                            "dialogue": [
                                "A: Excuse me, where is the nearest restaurant?",
                                "B: Go straight for two blocks, then turn left.",
                                "A: Thank you very much!"
                            ]
                        }
                    ]
                }
            ],
            "intermediate": [
                {
                    "id": "conv_inter_1",
                    "title": "Making Plans",
                    "description": "Practice discussing future plans and schedules",
                    "topics": ["future tense", "time expressions", "making suggestions"],
                    "vocabulary": ["tomorrow", "next week", "maybe", "definitely", "probably"],
                    "sample_dialogues": [
                        {
                            "scenario": "Planning weekend activities",
                            "dialogue": [
                                "A: What are you doing this weekend?",
                                "B: I'm thinking about going to the movies. Would you like to come?",
                                "A: That sounds great! What time should we meet?"
                            ]
                        }
                    ]
                }
            ],
            "advanced": [
                {
                    "id": "conv_adv_1",
                    "title": "Expressing Opinions",
                    "description": "Learn to express and defend your opinions in discussions",
                    "topics": ["opinion expressions", "agreement/disagreement", "argumentation"],
                    "vocabulary": ["in my opinion", "I believe", "however", "furthermore", "on the other hand"],
                    "sample_dialogues": [
                        {
                            "scenario": "Discussing current events",
                            "dialogue": [
                                "A: What do you think about the new environmental policies?",
                                "B: In my opinion, they're a step in the right direction, but more needs to be done.",
                                "A: I agree to some extent, however, I think the implementation might be challenging."
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Grammar lessons
        grammar_lessons = {
            "beginner": [
                {
                    "id": "gram_begin_1",
                    "title": "Present Tense Verbs",
                    "description": "Learn basic present tense conjugation",
                    "rules": [
                        "Regular verbs follow standard patterns",
                        "Subject-verb agreement is important",
                        "Use present tense for current actions and habits"
                    ],
                    "examples": [
                        "I speak English",
                        "She works at a hospital",
                        "They live in New York"
                    ],
                    "exercises": [
                        {
                            "type": "fill_blank",
                            "question": "I ___ (work) at a school.",
                            "answer": "work"
                        },
                        {
                            "type": "fill_blank", 
                            "question": "She ___ (study) French.",
                            "answer": "studies"
                        }
                    ]
                }
            ]
        }
        
        # Save lesson files
        self._save_lessons("conversation", conversation_lessons)
        self._save_lessons("grammar", grammar_lessons)
    
    def _save_lessons(self, lesson_type: str, lessons: Dict):
        """Save lessons to JSON file."""
        filepath = os.path.join(self.lessons_path, f"{lesson_type}_lessons.json")
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(lessons, f, indent=2, ensure_ascii=False)
    
    def get_lessons(self, lesson_type: str, difficulty: str) -> List[Dict[str, Any]]:
        """Get lessons by type and difficulty."""
        filepath = os.path.join(self.lessons_path, f"{lesson_type.lower()}_lessons.json")
        
        if not os.path.exists(filepath):
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lessons = json.load(f)
            
            return lessons.get(difficulty.lower(), [])
        except Exception as e:
            print(f"Error loading lessons: {e}")
            return []
    
    def get_lesson_by_id(self, lesson_id: str) -> Dict[str, Any]:
        """Get a specific lesson by ID."""
        for lesson_type in ['conversation', 'grammar', 'vocabulary']:
            filepath = os.path.join(self.lessons_path, f"{lesson_type}_lessons.json")
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lessons = json.load(f)
                    
                    for difficulty in lessons:
                        for lesson in lessons[difficulty]:
                            if lesson.get('id') == lesson_id:
                                return lesson
                except Exception as e:
                    continue
        
        return {}
    
    def create_custom_lesson(self, lesson_type: str, difficulty: str, lesson_data: Dict[str, Any]):
        """Create a custom lesson."""
        filepath = os.path.join(self.lessons_path, f"{lesson_type.lower()}_lessons.json")
        
        # Load existing lessons
        lessons = {}
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                lessons = json.load(f)
        
        # Add new lesson
        if difficulty.lower() not in lessons:
            lessons[difficulty.lower()] = []
        
        lessons[difficulty.lower()].append(lesson_data)
        
        # Save updated lessons
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(lessons, f, indent=2, ensure_ascii=False)
    
    def get_lesson_topics(self, language: str) -> List[str]:
        """Get available lesson topics for a language."""
        # This could be expanded to include language-specific topics
        return [
            "Basic Conversation",
            "Travel & Tourism", 
            "Business Communication",
            "Academic Discussion",
            "Cultural Topics",
            "Daily Life",
            "Food & Dining",
            "Shopping",
            "Health & Medical",
            "Technology"
        ]
