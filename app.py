import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

from commands.commands import startCommand, connectCommand, ticketCommand


load_dotenv()

TOKEN = os.environ.get("TOKEN")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("error", context.error)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', startCommand))
    app.add_handler(CommandHandler('ticket', ticketCommand))
    app.add_handler(CommandHandler('connect', connectCommand))

    # app.add_handler(MessageHandler(filters.TEXT, handleRequest))
    app.add_error_handler(error)

    print("[BOT] - status: running")
    app.run_polling(poll_interval=3)


main()
