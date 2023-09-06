import requests
from telegram import Update
from telegram.ext import ContextTypes

from labels.labels import *
from utils.utils import BASE_URL


async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(start_message(update.message.from_user.username))


async def connectCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 1:
        getUser = requests.put(BASE_URL + "/users/telegram/create", json={
            'telegram_user_id': str(update.message.from_user.id),
            'code': context.args[0]
        })
        if getUser.status_code == 404:
            await update.message.reply_text(user_code_not_found())
        elif getUser.status_code == 409:
            await update.message.reply_text(user_already_connected())
        elif getUser.status_code != 200:
            await update.message.reply_text(error())
        elif getUser.status_code == 200:
            await update.message.reply_text(connect_message_success(getUser.json()['param']))
    else:
        await update.message.reply_text(wrong_command_use())


async def ticketCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) > 0:
        if context.args[0] == 'create':
            if len(context.args) > 1:
                createTicket = requests.post(BASE_URL + "/tickets/?platform=telegram", json={
                    'message': " ".join(context.args[1:])
                }, headers={ "Authorization": "Bearer " + str(update.message.from_user.id) })
                if createTicket.status_code == 404:
                    await update.message.reply_text(user_code_not_found())
                elif createTicket.status_code == 409:
                    await update.message.reply_text(ticket_already_open())
                elif createTicket.status_code != 200:
                    await update.message.reply_text(error())
                elif createTicket.status_code == 200:
                    await update.message.reply_text(ticket_successfully_created())
            else:
                await update.message.reply_text(wrong_command_use())
        elif context.args[0] == 'close':
            if len(context.args) == 2:
                ticket = requests.put(BASE_URL + "/tickets/"+context.args[1]+"?platform=telegram",
                                            headers={ "Authorization": "Bearer " + str(update.message.from_user.id) })
                if ticket.status_code == 403:
                    await update.message.reply_text(no_enough_permissions())
                elif ticket.status_code == 404:
                    await update.message.reply_text(ticket_not_found())
                elif ticket.status_code == 409:
                    await update.message.reply_text(ticket_already_closed())
                elif ticket.status_code != 200:
                    await update.message.reply_text(error())
                elif ticket.status_code == 200:
                    await update.message.reply_text(ticket_successfully_closed())
            else:
                await update.message.reply_text(wrong_command_use())
        elif context.args[0] == 'info':
            if len(context.args) == 3 or len(context.args) == 2:
                page = context.args[2] if len(context.args) == 3 else "1"
                ticket = requests.get(BASE_URL + "/tickets/"+context.args[1]+"?page="+page+"&platform=telegram",
                                            headers={ "Authorization": "Bearer " + str(update.message.from_user.id) })
                if ticket.status_code == 403:
                    await update.message.reply_text(no_enough_permissions())
                elif ticket.status_code == 404:
                    await update.message.reply_text(ticket_not_found())
                elif ticket.status_code == 409:
                    await update.message.reply_text(ticket_already_closed())
                elif ticket.status_code != 200:
                    await update.message.reply_text(error())
                elif ticket.status_code == 200:
                    await update.message.reply_text(ticket_info(ticket.json()['param']))
            else:
                await update.message.reply_text(wrong_command_use())
        elif context.args[0] == 'comment':
            if len(context.args) > 2:
                ticket = requests.post(BASE_URL + "/tickets/messages?platform=telegram", json={
                    'message': " ".join(context.args[2:]),
                    'ticket_id': int(context.args[1])
                }, headers={ "Authorization": "Bearer " + str(update.message.from_user.id) })
                if ticket.status_code == 403:
                    await update.message.reply_text(no_enough_permissions())
                elif ticket.status_code == 404:
                    await update.message.reply_text(ticket_not_found())
                elif ticket.status_code == 422:
                    await update.message.reply_text(ticket_closed())
                elif ticket.status_code != 200:
                    await update.message.reply_text(error())
                elif ticket.status_code == 200:
                    await update.message.reply_text(ticket_successfully_commented())
            else:
                await update.message.reply_text(wrong_command_use())
    else:
        await update.message.reply_text(help_message())