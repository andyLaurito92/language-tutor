# Standard library imports
import json
from typing import Any, Dict, List, Optional

# Third-party imports
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Import model providers
try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from langchain_ollama import ChatOllama
    OLLAMA_AVAILABLE = True
except ImportError:
    try:
        from langchain_community.chat_models import ChatOllama
        from langchain_community.llms import Ollama
        OLLAMA_AVAILABLE = True
    except ImportError:
        OLLAMA_AVAILABLE = False

class AITutor:
    """Core AI tutor class that manages conversations and learning interactions."""
    
    def __init__(self, model_config: Dict[str, Any]):
        """
        Initialize the AI tutor with model configuration.
        
        Args:
            model_config: Dictionary containing model provider configuration
                For OpenAI: {'provider': 'openai', 'model': 'gpt-4', 'api_key': 'key'}
                For Ollama: {'provider': 'ollama', 'model': 'llama3.1', 'base_url': 'http://localhost:11434'}
        """
        self.model_config = model_config
        self.llm = self._initialize_llm()
        
        # Memory to maintain conversation context
        self.memory = ConversationBufferWindowMemory(
            k=10,  # Keep last 10 exchanges
            return_messages=True
        )
        
        self.current_language = None
        self.current_difficulty = None
        self.current_lesson_type = None
        self.lesson_context = {}
    
    def _initialize_llm(self) -> Any:
        """Initialize the appropriate LLM based on configuration."""
        provider = self.model_config.get('provider', 'ollama')
        
        if provider == 'openai':
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI not available. Install with: pip install langchain-openai")
            
            return ChatOpenAI(
                openai_api_key=self.model_config['api_key'],
                model=self.model_config['model'],
                temperature=0.7
            )
        
        elif provider == 'ollama':
            if not OLLAMA_AVAILABLE:
                raise ImportError("Ollama not available. Install with: pip install langchain-ollama")
            
            return ChatOllama(
                model=self.model_config['model'],
                base_url=self.model_config.get('base_url', 'http://localhost:11434'),
                temperature=0.7
            )
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    @classmethod
    @classmethod
    def from_config(cls, config_class: Any) -> 'AITutor':
        """Create AITutor instance from Config class."""
        model_config = config_class.get_model_config()
        return cls(model_config)
    
    def set_learning_context(self, language: str, difficulty: str, lesson_type: str, lesson_data: Optional[Dict[str, Any]] = None) -> None:
        """Set the current learning context for the tutor."""
        self.current_language = language
        self.current_difficulty = difficulty
        self.current_lesson_type = lesson_type
        self.lesson_context = lesson_data or {}
        
        # Clear previous memory when starting new context
        self.memory.clear()
    
    def get_system_prompt(self) -> str:
        """Generate system prompt based on current learning context."""
        base_prompt = f"""You are an expert language tutor for {self.current_language}. Your student is at a {self.current_difficulty} level and is working on {self.current_lesson_type}.

Your teaching approach should be:
1. Encouraging and patient
2. Corrective but constructive
3. Adaptive to the student's level
4. Interactive and engaging
5. Focused on practical usage

Guidelines:
- Always respond in a mix of {self.current_language} and English appropriate for the {self.current_difficulty} level
- For beginners: Use more English with simple {self.current_language} phrases
- For intermediate: Use more {self.current_language} with English explanations when needed  
- For advanced: Primarily use {self.current_language} with minimal English

When the student makes mistakes:
- Gently correct them
- Explain why it's incorrect
- Provide the correct version
- Give additional examples if helpful

Encourage the student to practice speaking and ask questions."""

        # Add lesson-specific context
        if self.lesson_context:
            if 'topics' in self.lesson_context:
                base_prompt += f"\n\nCurrent lesson topics: {', '.join(self.lesson_context['topics'])}"
            
            if 'vocabulary' in self.lesson_context:
                base_prompt += f"\n\nKey vocabulary to practice: {', '.join(self.lesson_context['vocabulary'])}"
            
            if 'sample_dialogues' in self.lesson_context:
                base_prompt += f"\n\nYou can reference these sample dialogues for context and practice."
        
        return base_prompt
    
    def generate_lesson_introduction(self) -> str:
        """Generate an introduction for the current lesson."""
        prompt = f"""Generate a friendly introduction for a {self.current_difficulty} level {self.current_language} lesson on {self.current_lesson_type}.

The introduction should:
1. Welcome the student (do NOT use placeholder names like [Student's Name] - just say "Welcome!" or "Hello!")
2. Briefly explain what they'll learn
3. Set expectations for the lesson
4. Ask a question to start the conversation

Important: Use actual greetings, not placeholders. Be direct and personal without using brackets or placeholder text.

Keep it appropriate for {self.current_difficulty} level students."""

        if self.lesson_context and 'title' in self.lesson_context:
            prompt += f"\n\nSpecific lesson: {self.lesson_context['title']}"
            if 'description' in self.lesson_context:
                prompt += f"\nDescription: {self.lesson_context['description']}"

        response = self.llm.invoke([SystemMessage(content=self.get_system_prompt()),
                                   HumanMessage(content=prompt)])
        
        return response.content
    
    def process_student_input(self, student_input: str, input_type: str = "text") -> Dict[str, Any]:
        """
        Process student input and generate appropriate response.
        
        Args:
            student_input: The student's input (text or transcribed speech)
            input_type: "text" or "speech" to indicate input method
            
        Returns:
            Dict containing response, feedback, and metadata
        """
        # Get conversation history from memory
        chat_history = self.memory.chat_memory.messages
        
        # Create the full prompt with system message and history
        messages = [
            SystemMessage(content=self.get_system_prompt())
        ]
        
        # Add chat history
        messages.extend(chat_history)
        
        # Add current human message
        messages.append(HumanMessage(content=student_input))
        
        # Generate response using the LLM directly
        try:
            response = self.llm.invoke(messages)
            response_text = response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            # Fallback for different LLM response formats
            response_text = f"I apologize, but I'm having trouble processing your message right now. Let's continue with the lesson. Can you try rephrasing that?"
        
        # Store the conversation in memory
        self.memory.chat_memory.add_user_message(student_input)
        self.memory.chat_memory.add_ai_message(response_text)
        
        # Analyze the input for feedback
        feedback = self._analyze_student_input(student_input)
        
        return {
            "response": response_text,
            "feedback": feedback,
            "input_type": input_type,
            "confidence_score": feedback.get("confidence", 0.8)
        }
    
    def _analyze_student_input(self, input_text: str) -> Dict[str, Any]:
        """Analyze student input for grammar, vocabulary, and other metrics."""
        analysis_prompt = f"""Analyze this {self.current_language} text from a {self.current_difficulty} level student: "{input_text}"

Provide analysis in JSON format:
{{
    "grammar_score": 0-10,
    "vocabulary_level": "beginner/intermediate/advanced", 
    "errors": ["list of specific errors if any"],
    "strengths": ["list of things done well"],
    "suggestions": ["specific improvement suggestions"],
    "confidence": 0.0-1.0
}}

Focus on constructive feedback appropriate for their level."""

        try:
            analysis_response = self.llm.invoke([
                SystemMessage(content="You are a language analysis expert. Respond only with valid JSON."),
                HumanMessage(content=analysis_prompt)
            ])
            
            # Try to parse JSON response
            feedback = json.loads(analysis_response.content)
            return feedback
            
        except (json.JSONDecodeError, Exception):
            # Fallback if JSON parsing fails
            return {
                "grammar_score": 7,
                "vocabulary_level": self.current_difficulty.lower(),
                "errors": [],
                "strengths": ["Participated in the conversation"],
                "suggestions": ["Keep practicing!"],
                "confidence": 0.7
            }
    
    def generate_practice_exercise(self) -> Dict[str, Any]:
        """Generate a practice exercise based on current lesson."""
        exercise_prompt = f"""Create a practice exercise for a {self.current_difficulty} level {self.current_language} student studying {self.current_lesson_type}.

The exercise should be:
1. Appropriate for their level
2. Interactive and engaging
3. Related to the current lesson topic
4. Include clear instructions

Format as JSON:
{{
    "type": "conversation/fill_blank/translation/role_play",
    "title": "Exercise title",
    "instructions": "Clear instructions for the student", 
    "content": "Exercise content",
    "expected_response": "What kind of response you expect"
}}"""

        if self.lesson_context:
            if 'topics' in self.lesson_context:
                exercise_prompt += f"\n\nFocus on these topics: {', '.join(self.lesson_context['topics'])}"

        try:
            response = self.llm.invoke([
                SystemMessage(content=self.get_system_prompt()),
                HumanMessage(content=exercise_prompt)
            ])
            
            exercise = json.loads(response.content)
            return exercise
            
        except (json.JSONDecodeError, Exception):
            # Fallback exercise
            return {
                "type": "conversation",
                "title": "Free Practice",
                "instructions": f"Let's have a conversation in {self.current_language}. Try to use what we've learned today!",
                "content": "Tell me about your day or ask me a question.",
                "expected_response": "Natural conversation"
            }
    
    def provide_pronunciation_feedback(self, text: str, audio_confidence: float) -> str:
        """Provide feedback on pronunciation based on transcription confidence."""
        if audio_confidence > 0.9:
            return "Excellent pronunciation! Very clear and understandable."
        elif audio_confidence > 0.7:
            return "Good pronunciation! Try to speak a bit more clearly for some words."
        elif audio_confidence > 0.5:
            return "Your pronunciation needs some work. Try to speak more slowly and clearly."
        else:
            return "I had difficulty understanding. Let's practice pronunciation of key words together."
    
    def get_lesson_summary(self) -> Dict[str, Any]:
        """Generate a summary of the current lesson session."""
        if not self.memory.chat_memory.messages:
            return {"summary": "No conversation yet", "achievements": [], "areas_to_improve": []}
        
        summary_prompt = """Based on our conversation, provide a lesson summary in JSON format:
{
    "summary": "Brief summary of what we covered",
    "achievements": ["List of things the student did well"],
    "areas_to_improve": ["Areas where the student can improve"],
    "next_steps": ["Suggestions for continued learning"]
}"""

        try:
            response = self.llm.invoke([
                SystemMessage(content=self.get_system_prompt()),
                HumanMessage(content=summary_prompt)
            ])
            
            return json.loads(response.content)
            
        except (json.JSONDecodeError, Exception):
            return {
                "summary": "We had a good practice session today!",
                "achievements": ["Participated actively in the lesson"],
                "areas_to_improve": ["Continue practicing regularly"],
                "next_steps": ["Try the next lesson when ready"]
            }
