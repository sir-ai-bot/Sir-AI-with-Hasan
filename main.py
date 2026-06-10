import os
import threading
from flask import Flask
from telegram.ext import Updater, CommandHandler

TOKEN = os.environ.get('BOT_TOKEN')

app = Flask(__name__)

@app.route('/')
def home():
    return "Sir AI Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

def start(update, context):
    user = update.effective_user
    update.message.reply_text(f"Hello {user.first_name}! Sir AI Bot is live on Render ❤️‍🔥")

def main():
    keep_alive()
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    print("Bot is starting polling...")
    updater.idle()

if __name__ == '__main__':
    main()
