#!/usr/bin/env python3
"""
Development startup script for TechAware backend with Telegram bot
"""

import os
import sys
import uvicorn

# Set environment variables for development
os.environ["MODEL_NAME"] = "facebook/bart-large-cnn"
os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["FRONTEND_URL"] = "http://localhost:3000"
os.environ["TELEGRAM_BOT_TOKEN"] = "8242501803:AAELk_92H1qoTeWi760tXfnt-5Orni9EUlg"

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

if __name__ == "__main__":
    print("🚀 Starting TechAware Backend with Telegram Bot")
    print("🤖 Bot Name: techaware_bot")
    print("📱 Telegram Bot Status: ✅ Enabled")
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
