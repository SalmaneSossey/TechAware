from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import papers, tags, health, telegram
from app.services.telegram_bot import create_bot_application
import os
from contextlib import asynccontextmanager

# Global bot application instance
bot_application = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - start/stop bot"""
    global bot_application
    
    # Start Telegram bot if token is provided
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if bot_token:
        try:
            bot_application = create_bot_application(bot_token)
            await bot_application.initialize()
            await bot_application.start()
            # Start polling for updates
            await bot_application.updater.start_polling()
            print("✅ Telegram bot started successfully")
        except Exception as e:
            print(f"⚠️  Failed to start Telegram bot: {e}")
    else:
        print("⚠️  TELEGRAM_BOT_TOKEN not set - bot disabled")
    
    yield
    
    # Shutdown bot
    if bot_application:
        await bot_application.updater.stop()
        await bot_application.stop()
        await bot_application.shutdown()

app = FastAPI(
    title="TechAware API",
    description="AI-powered research paper discovery and summarization",
    version="1.0.0",
    lifespan=lifespan  # Added lifespan manager
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(papers.router, prefix="/papers", tags=["papers"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(telegram.router, prefix="/telegram", tags=["telegram"])  # Added Telegram router

@app.get("/")
async def root():
    return {
        "message": "TechAware API",
        "version": "1.0.0",
        "docs": "/docs"
    }
