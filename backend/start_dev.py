#!/usr/bin/env python3
"""
Development startup script for TechAware backend
This script starts the FastAPI server with minimal dependencies for testing
"""

import os
import sys
import uvicorn
from pathlib import Path

# Load environment variables from .env file in root directory
try:
    from dotenv import load_dotenv
    # Load from parent directory (root)
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Loaded .env from {env_path}")
except ImportError:
    print("⚠️  python-dotenv not installed, skipping .env file loading")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")

# Set environment variables for development (fallbacks)
os.environ.setdefault("MODEL_NAME", "facebook/bart-large-cnn")
os.environ.setdefault("PYTHONUNBUFFERED", "1")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

if __name__ == "__main__":
    print("🚀 Starting TechAware Backend (Development Mode)")
    print("📱 Telegram Bot Status: ", end="")
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if bot_token:
        print("✅ Enabled (Token found)")
    else:
        print("⚠️  Disabled (No TELEGRAM_BOT_TOKEN found)")
        print("   Set TELEGRAM_BOT_TOKEN in your .env file to enable the bot")
    
    print("\n🌐 Starting server on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
