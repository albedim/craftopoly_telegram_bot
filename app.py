from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

from commands.commands import startCommand, connectCommand, ticketCommand

TOKEN = '6633082584:AAGlVNcJeNG3Pr40eWOTQFBqXa4k-bUnczI'

"""
def handleResponse(response):
    response = response.lower()
    if 'hello' in response:
        return "Hey"
    return "command not found"


async def handleRequest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    response = handleResponse(text)

    await update.message.reply_text(response)
"""


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("error", context.error)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', startCommand))
    app.add_handler(CommandHandler('ticket', ticketCommand))
    app.add_handler(CommandHandler('connect', connectCommand))

    # app.add_handler(MessageHandler(filters.TEXT, handleRequest))
    app.add_error_handler(error)

    print("running")
    app.run_polling(poll_interval=3)

main()