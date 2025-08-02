@echo off
REM AI Language Tutor Setup Script for Windows

echo 🎓 Setting up AI Language Tutor...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Create data directory
echo 📁 Creating data directories...
if not exist "data\lessons" mkdir data\lessons
if not exist "data" mkdir data

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 🔑 Creating .env file...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please edit the .env file and add your OpenAI API key:
    echo    OPENAI_API_KEY=your_actual_api_key_here
    echo.
)

echo ✅ Setup complete!
echo.
echo To run the application:
echo   1. Activate the virtual environment: venv\Scripts\activate.bat
echo   2. Set your OpenAI API key in the .env file
echo   3. Run the app: streamlit run app.py
echo.
echo 🚀 Happy learning!
pause
