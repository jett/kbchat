import os
import telebot

from loader import construct_prompt

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the QC Bot POC. What is your question?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    response = construct_prompt("Who is responsible for approving policies?")
    bot.reply_to(message, response)


bot.infinity_polling()
