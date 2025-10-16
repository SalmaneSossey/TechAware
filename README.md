# TechAware - Technology Awareness Engine

Your AI-powered research companion—summarizing the latest breakthroughs in AI and software engineering.

## 🚀 Features

- **AI-Powered Summaries**: Get 1-2 sentence summaries of complex research papers
- **Impact Analysis**: Understand where research applies in real-world scenarios
- **Smart Search**: Filter by categories, tags, and keywords
- **Telegram Integration**: Daily digests delivered to your Telegram
- **Modern UI**: Clean, light-themed interface inspired by leading tech platforms

## 🛠️ Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS v4
- shadcn/ui components
- Geist font family

**Backend:**
- FastAPI
- HuggingFace Transformers (BART for summarization)
- arXiv API integration
- python-telegram-bot for Telegram integration
- SQLite (development) / PostgreSQL (production ready)

## 📦 Installation

### Local Development

**Frontend:**
```bash
npm install
npm run dev
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker Compose

```bash
# Copy environment variables
cp .env.example .env

# Edit .env and add your Telegram bot token
# TELEGRAM_BOT_TOKEN=your_bot_token_here

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
\\\

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# Backend
MODEL_NAME=facebook/bart-large-cnn

# Telegram Bot
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_BOT_URL=https://t.me/your_bot_name?start=web

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### Changing the Summarization Model

Edit `backend/app/services/summarizer.py`:

```python
class Summarizer:
    def __init__(self, model_name: str = "your-model-name"):
        # Your custom model
```

Or set via environment variable:
```env
MODEL_NAME=facebook/bart-large-cnn
```

## 📡 API Endpoints

### Papers

- `GET /papers` - List papers with filters
  - Query params: `search`, `tags`, `category`, `since`, `sort`, `page`, `limit`
- `GET /papers/{id}` - Get single paper
- `GET /papers/daily/top?n=3` - Get top N papers for the day

### Tags

- `GET /tags` - Get all available tags

### Telegram

- `POST /telegram/webhook` - Telegram webhook endpoint
- `GET /telegram/subscribers/count` - Get subscriber count
- `GET /telegram/health` - Check bot configuration status

### Health

- `GET /health` - Health check

### Example Response

```json
{
  "papers": [
    {
      "id": "1",
      "arxiv_id": "2401.12345",
      "title": "Efficient Attention Mechanisms for Large Language Models",
      "authors": ["Smith, J.", "Johnson, A."],
      "abstract": "We propose a novel attention mechanism...",
      "category": "Machine Learning",
      "published_at": "2024-01-15",
      "pdf_url": "https://arxiv.org/pdf/2401.12345",
      "summary_short": "Novel attention mechanism reduces LLM training time by 40%.",
      "impact_suggestions": [
        "MLOps: Faster model training cycles",
        "Research: New baseline for transformers"
      ],
      "tags": ["LLM", "Attention", "Efficiency"],
      "score": 95.0
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

## 🤖 Telegram Bot Setup

### Step 1: Create Your Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the prompts to name your bot
4. Copy the bot token (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Configure Environment Variables

Add your bot token to `.env`:

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_BOT_URL=https://t.me/techaware_bot?start=web
```

### Step 3: Start the Backend

```bash
# With Docker
docker-compose up -d backend

# Or locally
cd backend
uvicorn app.main:app --reload
```

You should see: `✅ Telegram bot started successfully`

### Step 4: Test Your Bot

1. Open Telegram and search for your bot
2. Send `/start` command
3. The bot should respond with a welcome message
4. Click "Subscribe to Daily Digests" to subscribe

### Bot Commands

- `/start` - Subscribe to daily research digests
- `/unsubscribe` - Stop receiving daily digests
- `/help` - Show help message
- `/status` - Check your subscription status
- `/papers [n]` - Get the top `n` most relevant papers (default: 3, max: 5)

### Troubleshooting

**Bot doesn't respond:**
- Check that `TELEGRAM_BOT_TOKEN` is set correctly in `.env`
- Verify the backend is running: `docker-compose logs backend`
- Look for "Telegram bot started successfully" in logs
- Make sure there are no typos in the bot token

**Can't find the bot:**
- Verify the bot username in BotFather
- Update `TELEGRAM_BOT_URL` with the correct bot username

**Subscription not working:**
- Check backend logs for errors
- Ensure the `backend/data` directory has write permissions
- Verify subscriptions are saved in `backend/data/subscriptions.json`

## 🎨 Customization

### Theme Colors

Edit `app/globals.css` to customize the color scheme:

```css
@theme inline {
  --background: oklch(1 0 0);  /* White background */
  --primary: oklch(0.70 0.20 210);  /* Electric blue */
  /* ... other colors */
}
```

### Adding New Categories

Edit `backend/app/services/scraper.py`:

```python
categories = ["cs.AI", "cs.LG", "cs.CV", "cs.NE"]  # Add more
```

## 📝 Development Notes

- The frontend uses mock data by default for demo purposes
- The backend includes a placeholder scraper that can be connected to arXiv
- Summarization model downloads on first use (~1.6GB for BART)
- For production, replace SQLite with PostgreSQL
- Add authentication for the `/ingest/run` endpoint
- Telegram bot uses polling mode (suitable for development)
- For production, consider using webhooks instead of polling

## 🚢 Deployment


### Railway/Render (Backend)

1. Connect your GitHub repository
2. Set environment variables (including `TELEGRAM_BOT_TOKEN`)
3. Deploy from `backend/` directory
4. For production, configure webhook mode for better performance

### Telegram Bot in Production

For production deployments, use webhook mode instead of polling:

```python
# In backend/app/main.py
# Replace polling with webhook
await bot_application.bot.set_webhook(
    url=f"{YOUR_BACKEND_URL}/telegram/webhook"
)
```

## 📄 License

MIT License - feel free to use this project for your own research tools!

## 🙏 Acknowledgments

- Built by Eng. Sossey Salmane
- Powered by [HuggingFace Transformers](https://huggingface.co/transformers/)
- Data from [arXiv](https://arxiv.org/)
- Telegram integration via [python-telegram-bot](https://python-telegram-bot.org/)

---

**TechAware** - Stay Aware. Stay Ahead.
