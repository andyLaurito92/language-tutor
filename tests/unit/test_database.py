"""
Unit tests for the database module.
"""
import pytest
import sqlite3
import tempfile
import os
from datetime import datetime
from unittest.mock import patch, MagicMock


class TestProgressTracker:
    """Test cases for the ProgressTracker class."""
    
    def test_init_creates_database(self, temp_dir):
        """Test that initializing ProgressTracker creates the database."""
        from utils.database import ProgressTracker
        
        db_path = os.path.join(temp_dir, 'test.db')
        tracker = ProgressTracker(db_path)
        
        # Check that database file was created
        assert os.path.exists(db_path)
        
        # Check that tables were created
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['sessions', 'interactions', 'progress_metrics']
        for table in expected_tables:
            assert table in tables
        
        conn.close()
    
    def test_init_creates_directory(self, temp_dir):
        """Test that init creates parent directory if it doesn't exist."""
        from utils.database import ProgressTracker
        
        # Use a nested path that doesn't exist
        db_path = os.path.join(temp_dir, 'subdir', 'test.db')
        tracker = ProgressTracker(db_path)
        
        assert os.path.exists(db_path)
        assert os.path.exists(os.path.dirname(db_path))
    
    def test_start_session(self, mock_database_path):
        """Test starting a new session."""
        from utils.database import ProgressTracker
        
        tracker = ProgressTracker(mock_database_path)
        
        session_id = tracker.start_session(
            user_id='test_user',
            language='Spanish',
            lesson_type='Conversation Practice',
            difficulty='Intermediate'
        )
        
        assert isinstance(session_id, int)
        assert session_id > 0
        
        # Verify session was inserted
        conn = sqlite3.connect(mock_database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sessions WHERE id = ?', (session_id,))
        session = cursor.fetchone()
        
        assert session is not None
        assert session[1] == 'test_user'  # user_id
        assert session[2] == 'Spanish'    # language
        assert session[3] == 'Conversation Practice'  # lesson_type
        assert session[4] == 'Intermediate'  # difficulty
        assert session[5] is not None    # start_time
        assert session[6] is None        # end_time (should be None initially)
        
        conn.close()
    
    def test_end_session(self, mock_database_path):
        """Test ending a session."""
        from utils.database import ProgressTracker
        
        tracker = ProgressTracker(mock_database_path)
        
        # Start a session first
        session_id = tracker.start_session('test_user', 'Spanish', 'Grammar Lessons', 'Beginner')
        
        # End the session
        tracker.end_session(session_id, score=85)
        
        # Verify session was updated
        conn = sqlite3.connect(mock_database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT end_time, duration, score FROM sessions WHERE id = ?', (session_id,))
        session_data = cursor.fetchone()
        
        assert session_data[0] is not None  # end_time
        assert session_data[1] is not None  # duration
        assert session_data[1] >= 0         # duration should be non-negative
        assert session_data[2] == 85        # score
        
        conn.close()
    
    def test_end_session_without_score(self, mock_database_path):
        """Test ending a session without providing a score."""
        from utils.database import ProgressTracker
        
        tracker = ProgressTracker(mock_database_path)
        session_id = tracker.start_session('test_user', 'French', 'Vocabulary Building', 'Advanced')
        
        tracker.end_session(session_id)  # No score provided
        
        conn = sqlite3.connect(mock_database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT score FROM sessions WHERE id = ?', (session_id,))
        score = cursor.fetchone()[0]
        
        assert score is None
        conn.close()
    
    def test_log_interaction(self, mock_database_path):
        """Test logging an interaction."""
        from utils.database import ProgressTracker
        
        tracker = ProgressTracker(mock_database_path)
        session_id = tracker.start_session('test_user', 'German', 'Pronunciation Practice', 'Intermediate')
        
        user_input = "Hallo, wie geht es dir?"
        ai_response = "Sehr gut! Your pronunciation is improving."
        feedback_score = 4
        
        tracker.log_interaction(session_id, user_input, ai_response, feedback_score)
        
        # Verify interaction was logged
        conn = sqlite3.connect(mock_database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM interactions WHERE session_id = ?', (session_id,))
        interaction = cursor.fetchone()
        
        assert interaction is not None
        assert interaction[1] == session_id    # session_id
        assert interaction[2] is not None     # timestamp
        assert interaction[3] == user_input   # user_input
        assert interaction[4] == ai_response  # ai_response
        assert interaction[5] == feedback_score  # feedback_score
        
        conn.close()
    
    def test_log_interaction_without_feedback(self, mock_database_path):
        """Test logging an interaction without feedback score."""
        from utils.database import ProgressTracker
        
        tracker = ProgressTracker(mock_database_path)
        session_id = tracker.start_session('test_user', 'Italian', 'Reading Comprehension', 'Beginner')
        
        tracker.log_interaction(session_id, "Ciao!", "Ciao! Come stai?")
        
        conn = sqlite3.connect(mock_database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT feedback_score FROM interactions WHERE session_id = ?', (session_id,))
        feedback_score = cursor.fetchone()[0]
        
        assert feedback_score is None
        conn.close()
    
    def test_get_user_progress_no_data(self, mock_database_path):
        """Test getting progress for user with no data."""
        from utils.database import ProgressTracker
        
        tracker = ProgressTracker(mock_database_path)
        progress = tracker.get_user_progress('nonexistent_user')
        
        expected = {
            'sessions': [],
            'total_sessions': 0,
            'total_time': 0,
            'average_score': 0
        }
        
        assert progress == expected
    
    def test_get_user_progress_with_data(self, mock_database_path):
        """Test getting progress for user with session data."""
        from utils.database import ProgressTracker
        
        tracker = ProgressTracker(mock_database_path)
        
        # Create multiple sessions for the same user
        session1 = tracker.start_session('test_user', 'Spanish', 'Conversation Practice', 'Intermediate')
        session2 = tracker.start_session('test_user', 'Spanish', 'Grammar Lessons', 'Intermediate')
        session3 = tracker.start_session('test_user', 'French', 'Vocabulary Building', 'Beginner')
        
        # End sessions with scores
        tracker.end_session(session1, score=80)
        tracker.end_session(session2, score=90)
        tracker.end_session(session3, score=70)
        
        progress = tracker.get_user_progress('test_user')
        
        assert progress['total_sessions'] == 3
        assert progress['total_time'] >= 0  # Should have some duration
        assert progress['average_score'] == 80  # (80 + 90 + 70) / 3
        assert len(progress['sessions']) == 3  # Three different session types
    
    def test_get_user_progress_filtered_by_language(self, mock_database_path):
        """Test getting progress filtered by specific language."""
        from utils.database import ProgressTracker
        
        tracker = ProgressTracker(mock_database_path)
        
        # Create sessions in different languages
        session1 = tracker.start_session('test_user', 'Spanish', 'Conversation Practice', 'Intermediate')
        session2 = tracker.start_session('test_user', 'French', 'Grammar Lessons', 'Beginner')
        
        tracker.end_session(session1, score=85)
        tracker.end_session(session2, score=75)
        
        # Get progress for Spanish only
        progress = tracker.get_user_progress('test_user', language='Spanish')
        
        assert progress['total_sessions'] == 1
        assert progress['average_score'] == 85
        assert len(progress['sessions']) == 1
        assert progress['sessions'][0]['language'] == 'Spanish'
    
    def test_get_user_progress_with_incomplete_sessions(self, mock_database_path):
        """Test that incomplete sessions (without end_time) are ignored."""
        from utils.database import ProgressTracker
        
        tracker = ProgressTracker(mock_database_path)
        
        # Create sessions - one completed, one incomplete
        session1 = tracker.start_session('test_user', 'Spanish', 'Conversation Practice', 'Intermediate')
        session2 = tracker.start_session('test_user', 'Spanish', 'Grammar Lessons', 'Intermediate')
        
        # Only end one session
        tracker.end_session(session1, score=80)
        # session2 remains incomplete
        
        progress = tracker.get_user_progress('test_user')
        
        # Should only count the completed session
        assert progress['total_sessions'] == 1
        assert progress['average_score'] == 80
    
    def test_database_schema(self, mock_database_path):
        """Test that the database schema is created correctly."""
        from utils.database import ProgressTracker
        
        tracker = ProgressTracker(mock_database_path)
        
        conn = sqlite3.connect(mock_database_path)
        cursor = conn.cursor()
        
        # Check sessions table schema
        cursor.execute("PRAGMA table_info(sessions)")
        sessions_columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        expected_sessions_columns = {
            'id': 'INTEGER',
            'user_id': 'TEXT',
            'language': 'TEXT',
            'lesson_type': 'TEXT',
            'difficulty': 'TEXT',
            'start_time': 'TEXT',
            'end_time': 'TEXT',
            'duration': 'INTEGER',
            'score': 'INTEGER'
        }
        
        assert sessions_columns == expected_sessions_columns
        
        # Check interactions table schema
        cursor.execute("PRAGMA table_info(interactions)")
        interactions_columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        expected_interactions_columns = {
            'id': 'INTEGER',
            'session_id': 'INTEGER',
            'timestamp': 'TEXT',
            'user_input': 'TEXT', 
            'ai_response': 'TEXT',
            'feedback_score': 'INTEGER'
        }
        
        assert interactions_columns == expected_interactions_columns
        
        # Check progress_metrics table schema
        cursor.execute("PRAGMA table_info(progress_metrics)")
        metrics_columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        expected_metrics_columns = {
            'id': 'INTEGER',
            'user_id': 'TEXT',
            'language': 'TEXT',
            'metric_type': 'TEXT',
            'metric_value': 'REAL',
            'timestamp': 'TEXT'
        }
        
        assert metrics_columns == expected_metrics_columns
        
        conn.close()