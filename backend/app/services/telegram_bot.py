import os
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import json
from pathlib import Path

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store subscriptions in a JSON file
SUBSCRIPTIONS_FILE = Path("data/subscriptions.json")
SUBSCRIPTIONS_FILE.parent.mkdir(exist_ok=True)

def load_subscriptions():
    """Load user subscriptions from file"""
    if SUBSCRIPTIONS_FILE.exists():
        with open(SUBSCRIPTIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_subscriptions(subscriptions):
    """Save user subscriptions to file"""
    with open(SUBSCRIPTIONS_FILE, 'w') as f:
        json.dump(subscriptions, f, indent=2)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("📬 Subscribe to Daily Digests", callback_data="subscribe")],
        [InlineKeyboardButton("🌐 Visit TechAware", url=os.getenv("FRONTEND_URL", "http://localhost:3000"))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
👋 Welcome to TechAware, {user.first_name}!

I'm your AI-powered research companion, helping you stay ahead of the latest breakthroughs in AI, software engineering, and data science.

🔬 What I can do:
• Send you daily digests of the most impactful research papers
• Provide AI-generated summaries so you can quickly understand key findings
• Help you discover papers that matter to your work

Ready to stay informed effortlessly?
"""
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup
    )

async def subscribe_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle subscription button press"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    subscriptions = load_subscriptions()
    
    if user_id in subscriptions:
        await query.edit_message_text(
            "✅ You're already subscribed to daily digests!\n\n"
            "You'll receive curated research papers every day at 9:00 AM UTC.\n\n"
            "Use /unsubscribe to stop receiving digests."
        )
    else:
        subscriptions[user_id] = {
            "user_id": user_id,
            "username": query.from_user.username,
            "first_name": query.from_user.first_name,
            "subscribed_at": str(update.effective_message.date)
        }
        save_subscriptions(subscriptions)
        
        await query.edit_message_text(
            "🎉 Successfully subscribed!\n\n"
            "You'll now receive daily digests of breakthrough research papers at 9:00 AM UTC.\n\n"
            "Each digest includes:\n"
            "• AI-generated summaries\n"
            "• Key findings and impact\n"
            "• Direct links to papers\n\n"
            "Use /unsubscribe anytime to stop receiving digests."
        )

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unsubscribe command"""
    user_id = str(update.effective_user.id)
    subscriptions = load_subscriptions()
    
    if user_id in subscriptions:
        del subscriptions[user_id]
        save_subscriptions(subscriptions)
        await update.message.reply_text(
            "😢 You've been unsubscribed from daily digests.\n\n"
            "We're sorry to see you go! You can resubscribe anytime with /start."
        )
    else:
        await update.message.reply_text(
            "You're not currently subscribed to daily digests.\n\n"
            "Use /start to subscribe and stay informed!"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🤖 TechAware Bot Commands:

/start - Subscribe to daily research digests
/unsubscribe - Stop receiving daily digests
/help - Show this help message
/status - Check your subscription status

📚 About TechAware:
TechAware helps you stay aware of emerging advances in AI, software engineering, and data science. Get AI-powered summaries of the latest research papers delivered daily.

Visit our website: {website}
""".format(website=os.getenv("FRONTEND_URL", "http://localhost:3000"))
    
    await update.message.reply_text(help_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    user_id = str(update.effective_user.id)
    subscriptions = load_subscriptions()
    
    if user_id in subscriptions:
        sub_info = subscriptions[user_id]
        await update.message.reply_text(
            f"✅ Subscription Status: Active\n\n"
            f"Subscribed since: {sub_info['subscribed_at']}\n"
            f"Daily digests: Enabled\n"
            f"Delivery time: 9:00 AM UTC\n\n"
            f"Use /unsubscribe to stop receiving digests."
        )
    else:
        await update.message.reply_text(
            "❌ Subscription Status: Not subscribed\n\n"
            "Use /start to subscribe to daily research digests!"
        )

def create_bot_application(token: str) -> Application:
    """Create and configure the bot application"""
    application = Application.builder().token(token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(subscribe_callback, pattern="^subscribe$"))
    
    return application

async def send_daily_digest(application: Application, papers: list):
    """Send daily digest to all subscribed users"""
    subscriptions = load_subscriptions()
    
    if not papers:
        logger.info("No papers to send in daily digest")
        return
    
    # Format the digest message
    digest_message = "🔬 *TechAware Daily Digest*\n\n"
    digest_message += f"Here are today's top {len(papers)} research papers:\n\n"
    
    for i, paper in enumerate(papers[:5], 1):  # Send top 5 papers
        digest_message += f"*{i}. {paper['title']}*\n"
        digest_message += f"📝 {paper['summary']}\n"
        digest_message += f"🔗 [Read Paper]({paper['url']})\n\n"
    
    digest_message += f"\n🌐 [Explore more papers](http://localhost:3000/explore)"
    
    # Send to all subscribers
    success_count = 0
    for user_id in subscriptions.keys():
        try:
            await application.bot.send_message(
                chat_id=int(user_id),
                text=digest_message,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to send digest to user {user_id}: {e}")
    
    logger.info(f"Daily digest sent to {success_count}/{len(subscriptions)} subscribers")
