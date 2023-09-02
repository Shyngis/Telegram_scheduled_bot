
import pandas as pd
import requests
import time
import os
import telebot
import sqlite3
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import datetime


bot = telebot.TeleBot('5974199732:AAHG4LqeRtXnbBh0YETIMj51IIYsxyF1ilM')

# Define the handler function for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Get the user ID from the message object
    user_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    username = message.chat.username


    conn = sqlite3.connect('users.db')
    c = conn.cursor()


    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,username TEXT,first_name TEXT,last_name TEXT)''')


    c.execute("INSERT OR IGNORE INTO users (id, username, first_name, last_name) VALUES (?,?,?,?)", (user_id, username, first_name, last_name))
    conn.commit()

    c.close()
    conn.close()

    # Send a welcome message to the user
    bot.reply_to(message, "Hello! Thanks for jor joining me;)")


bot.polling()


while True:
    sheet_id = "1BcaIHbR8gFyGiPddjxG63JMTBTfgwqut2MsnyuYMWoA"

    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

    df = pd.read_csv(url)
    df["Schedule Datetime"] = pd.to_datetime(df["Schedule Datetime"])
    df

    previous_minute = pd.datetime.now() + pd.Timedelta(minutes=-1)
    print(type(previous_minute))
    current_time = pd.datetime.now()
    print(type(current_time))
    df = df[(df["Schedule Datetime"] > previous_minute) &  (df["Schedule Datetime"]  < current_time)]
    df

    def send_message(row):
        bot_id = "5974199732:AAHG4LqeRtXnbBh0YETIMj51IIYsxyF1ilM"
        chat_id = row[2]
        message = row[0]
        url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"

        return requests.get(url).json()

    if not df.empty:
        df['status'] = df.apply(send_message, axis=1)
    time.sleep(60)
    df












































# import pandas as pd
# import requests
# import time
#
#
# while True:
#     sheet_id = "1BcaIHbR8gFyGiPddjxG63JMTBTfgwqut2MsnyuYMWoA"
#
#     url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
#
#     df = pd.read_csv(url)
#     df["Schedule Datetime"] = pd.to_datetime(df["Schedule Datetime"])
#     df
#
#     previous_minute = pd.datetime.now() + pd.Timedelta(minutes=-1)
#     print(type(previous_minute))
#     current_time = pd.datetime.now()
#     print(type(current_time))
#     df = df[(df["Schedule Datetime"] > previous_minute) &  (df["Schedule Datetime"]  < current_time)]
#     df
#
#
#     def send_message(row):
#         bot_id = "5974199732:AAHG4LqeRtXnbBh0YETIMj51IIYsxyF1ilM"
#         chat_id = '59169078'
#         message = row[0]
#         url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"
#
#         return requests.get(url).json()
#
#     if not df.empty:
#         df['status'] = df.apply(send_message, axis=1)
#     time.sleep(60)
#     df



