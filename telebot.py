from typing import Final
from textblob import TextBlob
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# === Bot Configuration ===
TOKEN: Final = '7264049682:AAF3I95o4OKoHopPI-tSYxvTstT3xAF7QSk'  # Replace with your token
BOT_USERNAME: Final = '@may_chan_bot'


# === Command Handlers ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Well well, here you are again. How is your day? Tell me everything—I would love to know!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
       "Now I'm gonna tell you how i operate i am a bot well i'm one but you see i want you to forget that i am a bot i want you to think of me as your friend and i will be your friend and we will have conversations together and yeah i live in the present not like these humans who either does live in the past or in the furture escaping from the present my friend i want you to be like one who live in present and to the present so i dont rember about whats in the past nor think about the furture i just live in the present and i want you to do the same"
    )

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command.")


# === Sentiment-based Response ===
def handle_response(text: str) -> str:
    text = text.lower()
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity

    if "hello" in text or "hi" in text:
        return "Hey you! 😊 How are you today?"
    elif "sad" in text or sentiment < 0:
        return "Aww 😢 I’m here for you. Want to talk about it?"
    elif "happy" in text or sentiment > 0:
        return "That makes me so happy too! 😄 Tell me more!"
    elif "bored" in text:
        return "Let’s find something fun to talk about! 🥳"
    else:
        return "Hmm... interesting 🤔. Tell me more."


# === Message Handler ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    message_type = update.message.chat.type

    print(f'User({update.message.chat.id}) in {message_type}: {text}')

    if message_type == "group":
        if BOT_USERNAME in text:
            text = text.replace(BOT_USERNAME, "").strip()
        else:
            return

    response = handle_response(text)
    await update.message.reply_text(response)


# === Error Handler ===
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


# === Main Application ===
if __name__ == "__main__":
    print("Bot is starting...")

    app = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Text message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    app.add_error_handler(error_handler)

    print("Polling started")
    app.run_polling()
