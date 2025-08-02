# Standard library imports
import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

class ProgressTracker:
    """Handles user progress tracking and data persistence."""
    
    def __init__(self, db_path: str = "data/progress.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize the SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                language TEXT,
                lesson_type TEXT,
                difficulty TEXT,
                start_time TEXT,
                end_time TEXT,
                duration INTEGER,
                score INTEGER
            )
        ''')
        
        # Interactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                timestamp TEXT,
                user_input TEXT,
                ai_response TEXT,
                feedback_score INTEGER,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        # Progress metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                language TEXT,
                metric_type TEXT,
                metric_value REAL,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def start_session(self, user_id: str, language: str, lesson_type: str, difficulty: str) -> int:
        """Start a new learning session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sessions (user_id, language, lesson_type, difficulty, start_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, language, lesson_type, difficulty, datetime.now().isoformat()))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return session_id
    
    def end_session(self, session_id: int, score: Optional[int] = None) -> None:
        """End a learning session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get session start time to calculate duration
        cursor.execute('SELECT start_time FROM sessions WHERE id = ?', (session_id,))
        start_time_str = cursor.fetchone()[0]
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.now()
        duration = int((end_time - start_time).total_seconds())
        
        cursor.execute('''
            UPDATE sessions 
            SET end_time = ?, duration = ?, score = ?
            WHERE id = ?
        ''', (end_time.isoformat(), duration, score, session_id))
        
        conn.commit()
        conn.close()
    
    def log_interaction(self, session_id: int, user_input: str, ai_response: str, feedback_score: Optional[int] = None) -> None:
        """Log an interaction between user and AI."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interactions (session_id, timestamp, user_input, ai_response, feedback_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (session_id, datetime.now().isoformat(), user_input, ai_response, feedback_score))
        
        conn.commit()
        conn.close()
    
    def get_user_progress(self, user_id: str, language: str = None) -> Dict[str, Any]:
        """Get comprehensive progress data for a user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Base query
        query = '''
            SELECT language, lesson_type, difficulty, AVG(score) as avg_score, 
                   COUNT(*) as session_count, SUM(duration) as total_time
            FROM sessions 
            WHERE user_id = ? AND end_time IS NOT NULL
        '''
        params = [user_id]
        
        if language:
            query += ' AND language = ?'
            params.append(language)
        
        query += ' GROUP BY language, lesson_type, difficulty'
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        progress_data = {
            'sessions': [],
            'total_sessions': 0,
            'total_time': 0,
            'average_score': 0
        }
        
        total_sessions = 0
        total_time = 0
        total_score = 0
        
        for row in results:
            lang, lesson_type, difficulty, avg_score, session_count, time_spent = row
            progress_data['sessions'].append({
                'language': lang,
                'lesson_type': lesson_type,
                'difficulty': difficulty,
                'average_score': avg_score or 0,
                'session_count': session_count,
                'time_spent': time_spent or 0
            })
            
            total_sessions += session_count
            total_time += time_spent or 0
            if avg_score:
                total_score += avg_score * session_count
        
        progress_data['total_sessions'] = total_sessions
        progress_data['total_time'] = total_time
        progress_data['average_score'] = total_score / total_sessions if total_sessions > 0 else 0
        
        conn.close()
        return progress_data
