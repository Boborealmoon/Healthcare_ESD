from flask import Flask, request
from flask_cors import CORS
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, Updater

import logging
# Debugger and Logger to help identify issues
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# https://api.telegram.org/bot6401686238:AAFlMPg5PcrEiPF9UDTL7nyTLSUHEzN6WME/getMe

# Initialize Flask app
app = Flask(__name__)
CORS(app)


# Telegram token (replace 'YOUR_BOT_TOKEN' with your actual bot token)
BOT_TOKEN = "6401686238:AAFlMPg5PcrEiPF9UDTL7nyTLSUHEzN6WM"

def main() -> None:
    """Start the bot."""
    logging.info('\033[1;34mInitialization bot\033[m')
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.contact, handle_message_request))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))
    updater.start_polling()
    updater.idle()

def send_message(username, chat_id, msg):
    bot_token = BOT_TOKEN
    bot_chatID = chat_id
    bot_message = f'{msg}{username}'
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.text

# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, this is the SMU Clinic Bot!")

# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)


# @app.route('/webhook', methods=['POST'])
# def webhook():
#     update = Update.de_json(request.get_json(force=True), updater.bot)
#     dispatcher.process_update(update)
#     return 'OK'


if __name__ == '__main__':
    app.run(port=5556, debug=True)
    updater.start_polling()