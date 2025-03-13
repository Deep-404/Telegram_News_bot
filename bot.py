import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# Constants
TELEGRAM_BOT_TOKEN = "TELGRAM BOT KEY"
NEWS_API_KEY = "NEWS API KEY"

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Helper function to fetch news
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return articles


# Command to send news on demand
async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Fetch the latest news
    articles = get_news()

    # Format the news into a readable message
    if articles:
        message = "Here are the latest news updates:\n\n"
        for article in articles[:5]:  # Limit to 5 articles
            message += f"{article['title']}\n{article['url']}\n\n"
    else:
        message = "No news available at the moment."

    # Send the news to the user
    await update.message.reply_text(message)


# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /news to get the latest news updates.")


# Main function
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", send_news))

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
