#!/usr/bin/env python3
"""
Launcher script for AI Language Tutor macOS app.
This script handles the application startup and launches the Streamlit interface.
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def get_app_directory():
    """Get the directory where the app is located."""
    if getattr(sys, 'frozen', False):
        # Running as a bundled executable
        return Path(sys.executable).parent
    else:
        # Running as a script
        return Path(__file__).parent

def find_available_port(start_port=8501):
    """Find an available port starting from the given port."""
    import socket
    
    for port in range(start_port, start_port + 100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    raise RuntimeError("No available ports found")

def wait_for_server(port, timeout=30):
    """Wait for the Streamlit server to start."""
    import socket
    import time
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex(('localhost', port))
                if result == 0:
                    return True
        except Exception:
            pass
        time.sleep(0.5)
    
    return False

def launch_streamlit(app_dir, port):
    """Launch the Streamlit application."""
    app_path = app_dir / "app.py"
    
    if not app_path.exists():
        raise FileNotFoundError(f"App file not found: {app_path}")
    
    # Set up environment
    env = os.environ.copy()
    env['PYTHONPATH'] = str(app_dir)
    
    # Launch Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", str(app_path),
        "--server.port", str(port),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--server.fileWatcherType", "none"
    ]
    
    return subprocess.Popen(cmd, env=env, cwd=str(app_dir))

def open_browser(port):
    """Open the default browser to the app URL."""
    url = f"http://localhost:{port}"
    webbrowser.open(url)

def main():
    """Main launcher function."""
    try:
        # Get app directory
        app_dir = get_app_directory()
        
        # Find available port
        port = find_available_port()
        
        print(f"🎓 Starting AI Language Tutor...")
        print(f"📁 App directory: {app_dir}")
        print(f"🌐 Port: {port}")
        
        # Launch Streamlit process
        process = launch_streamlit(app_dir, port)
        
        # Wait for server to start
        print("⏳ Starting server...")
        if wait_for_server(port):
            print("✅ Server started successfully!")
            
            # Open browser
            print("🌐 Opening browser...")
            open_browser(port)
            
            # Keep the launcher running
            print("🚀 AI Language Tutor is now running!")
            print(f"🔗 Access at: http://localhost:{port}")
            print("❌ Close this window to stop the application")
            
            try:
                # Wait for process to finish
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                process.terminate()
                process.wait()
        else:
            print("❌ Failed to start server")
            process.terminate()
            return 1
            
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())