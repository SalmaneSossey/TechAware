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
from app.services.paper_service import PaperService

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
• Show you top relevant papers on-demand with `/papers`
• Provide AI-generated summaries and probable applications
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
/papers [n] - Show top relevant papers (default: 3, max: 5)
/unsubscribe - Stop receiving daily digests
/help - Show this help message
/status - Check your subscription status

📚 About TechAware:
TechAware helps you stay aware of emerging advances in AI, software engineering, and data science. Get AI-powered summaries of the latest research papers delivered daily.

💡 Try `/papers` to see today's most relevant research papers with summaries and probable applications!

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

async def papers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /papers command - show top relevant papers"""
    try:
        # Get the number of papers to show (default 3, max 5)
        num_papers = 3
        if context.args:
            try:
                num_papers = min(int(context.args[0]), 5)
            except (ValueError, IndexError):
                num_papers = 3
        
        # Get papers from service
        paper_service = PaperService()
        papers = await paper_service.get_daily_top(num_papers)
        
        if not papers:
            await update.message.reply_text(
                "🤖 No papers available at the moment. Please try again later!"
            )
            return
        
        # Send papers one by one for better readability
        intro_message = f"🔬 <b>Top {len(papers)} Research Papers Today</b>\n\n"
        intro_message += "Here are the most relevant papers with AI-generated summaries and potential applications:\n\n"
        
        await update.message.reply_text(intro_message, parse_mode="HTML")
        
        for i, paper in enumerate(papers, 1):
            paper_message = format_paper_message(paper, i)
            
            # Create inline keyboard for each paper
            keyboard = [
                [InlineKeyboardButton("📖 Read Full Paper", url=paper.pdf_url)]
            ]
            
            # Only add frontend button if URL is valid (not localhost)
            frontend_url = os.getenv("FRONTEND_URL", "")
            if frontend_url and not frontend_url.startswith("http://localhost"):
                keyboard.append([InlineKeyboardButton("🌐 Explore More Papers", url=frontend_url)])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                paper_message,
                reply_markup=reply_markup,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            
    except Exception as e:
        logger.error(f"Error in papers_command: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        await update.message.reply_text(
            f"❌ Sorry, I encountered an error while fetching papers. Error: {str(e)[:100]}"
        )

def escape_markdown(text: str) -> str:
    """Escape special characters for Telegram Markdown"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

def format_paper_message(paper, index: int) -> str:
    """Format a paper into a readable Telegram message"""
    # Use HTML formatting instead of Markdown for better compatibility
    message = f"<b>{index}. {paper.title}</b>\n\n"
    
    # Authors
    authors_str = ", ".join(paper.authors[:3])  # Show first 3 authors
    if len(paper.authors) > 3:
        authors_str += f" +{len(paper.authors) - 3} more"
    message += f"👥 <b>Authors:</b> {authors_str}\n"
    
    # Category and score
    message += f"📂 <b>Category:</b> {paper.category}\n"
    message += f"⭐ <b>Relevance Score:</b> {paper.score:.1f}/100\n\n"
    
    # Summary
    message += f"📝 <b>AI Summary:</b>\n{paper.summary_short}\n\n"
    
    # Impact suggestions (probable applications)
    if paper.impact_suggestions:
        message += f"🚀 <b>Probable Applications:</b>\n"
        for suggestion in paper.impact_suggestions:
            message += f"• {suggestion}\n"
        message += "\n"
    
    # Tags
    if paper.tags:
        tags_str = " ".join([f"#{tag.replace(' ', '')}" for tag in paper.tags])
        message += f"🏷️ {tags_str}\n\n"
    
    # Publication date
    message += f"📅 Published: {paper.published_at}"
    
    return message

def create_bot_application(token: str) -> Application:
    """Create and configure the bot application"""
    application = Application.builder().token(token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("papers", papers_command))
    
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
    digest_message = "🔬 <b>TechAware Daily Digest</b>\n\n"
    digest_message += f"Here are today's top {len(papers)} research papers with summaries and applications:\n\n"
    
    # Send to all subscribers
    success_count = 0
    for user_id in subscriptions.keys():
        try:
            # Send intro message
            await application.bot.send_message(
                chat_id=int(user_id),
                text=digest_message,
                parse_mode="HTML"
            )
            
            # Send each paper as a separate message for better readability
            for i, paper in enumerate(papers[:3], 1):  # Send top 3 papers in digest
                paper_message = format_paper_message(paper, i)
                
                # Create inline keyboard for each paper
                keyboard = [
                    [InlineKeyboardButton("📖 Read Full Paper", url=paper.pdf_url)]
                ]
                
                # Only add frontend button if URL is valid (not localhost)
                frontend_url = os.getenv("FRONTEND_URL", "")
                if frontend_url and not frontend_url.startswith("http://localhost"):
                    keyboard.append([InlineKeyboardButton("🌐 Explore More Papers", url=frontend_url)])
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await application.bot.send_message(
                    chat_id=int(user_id),
                    text=paper_message,
                    reply_markup=reply_markup,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
            
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to send digest to user {user_id}: {e}")
    
    logger.info(f"Daily digest sent to {success_count}/{len(subscriptions)} subscribers")
