# bot-connection-en leaked by @ktrjp
#
#
#  ██████╗░███████╗██╗░░░██╗██╗██╗░░░░░██╗░░░░░░██████╗
#  ██╔══██╗██╔════╝██║░░░██║██║██║░░░░░██║░░░░░██╔════╝
#  ██║░░██║█████╗░░╚██╗░██╔╝██║██║░░░░░██║░░░░░╚█████╗░
#  ██║░░██║██╔══╝░░░╚████╔╝░██║██║░░░░░██║░░░░░░╚═══██╗
#  ██████╔╝███████╗░░╚██╔╝░░██║███████╗███████╗██████╔╝
#  ╚═════╝░╚══════╝░░░╚═╝░░░╚═╝╚══════╝╚══════╝╚═════╝░
#
#     AND HERE AGAIN! YES, IT'S A BOT FOR ACCOUNT LINKING AND RECOVERY!
#
#         I ALSO HAVE A FEW IDEAS FOR THIS BOT!
#    
# version-bot: v1.0

import telebot
import socket
from telebot import types
import sqlite3
import re

bot = telebot.TeleBot('YOUR_BOT_TOKEN')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'HELLO! COME UP WITH SOMETHING SMART HERE!\n\n⛔ Commands:\n/connect - Link an account!\n/profile - View profile\n/recloud - Recover account')

@bot.message_handler(commands=['connect'])
def connect_command(message):
    try:
        player_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "❌ Incorrect usage!:\n/connect lowID\n\nYour in-game ID! For example, 1, 2, 3\nNot #2PPDEV52")
        return

    try:
        user_id = message.from_user.id

        bot_db_connection = sqlite3.connect('database/Bot/users.db')  # Bot's database
        bot_db_cursor = bot_db_connection.cursor()

        bot_db_cursor.execute('''CREATE TABLE IF NOT EXISTS accountconnect 
                                (lowID INTEGER PRIMARY KEY, trophies INTEGER, name TEXT, id_user INTEGER)''')
        bot_db_connection.commit()

        bot_db_cursor.execute("SELECT lowID, trophies, name FROM accountconnect WHERE id_user = ?", (user_id,))
        result = bot_db_cursor.fetchone()

        if result:
            bot.send_message(message.chat.id, "❌ Account already linked!")
            return

        server_db_connection = sqlite3.connect('database/Player/plr.db')
        server_db_cursor = server_db_connection.cursor()

        server_db_cursor.execute("SELECT lowID, trophies, name FROM plrs WHERE lowID = ?", (player_id,))
        result = server_db_cursor.fetchone()

        if result:
            bot_db_cursor.execute("INSERT INTO accountconnect VALUES (?, ?, ?, ?)", (*result, user_id))

            bot_db_connection.commit()
            bot_db_connection.close()
            server_db_connection.close()

            bot.send_message(message.chat.id, f"🏴 Your account {player_id} is linked!\n🙇 Nickname: {result[2]}\n🏆 Trophies: {result[1]}")
        else:
            bot_db_connection.close()
            server_db_connection.close()

            bot.send_message(message.chat.id, "❌ Account with the specified ID not found!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ {str(e)}")

@bot.message_handler(commands=['profile'])
def handle_profile(message):
    user_id = message.from_user.id

    users_conn = sqlite3.connect('users.db')
    users_cursor = users_conn.cursor()

    account_conn = sqlite3.connect('users.db')
    account_cursor = account_conn.cursor()

    try:
        account_cursor.execute(f"SELECT lowID FROM accountconnect WHERE id_user = {user_id}")
        row = account_cursor.fetchone()

        if row:
            lowID = row[0]

            plr_conn = sqlite3.connect('database/Player/plr.db')  # Replace with your path.
            plr_cursor = plr_conn.cursor()

            plr_cursor.execute(f"SELECT token, name, trophies, gems, starpoints, vip FROM plrs WHERE lowID = {lowID}")
            plr_row = plr_cursor.fetchone()

            if plr_row:
                token, name, trophies, gems, starpoints, vip = plr_row
                vip_status = f"VIP-STATUS{vip}" if vip else "VIP-NONE"

                profile_info = f"🤠 Account {name}:\n\n🆔 ID: {lowID}\n📱 Token: {token}\n🏆 Trophies: {trophies}\n💎 Gems: {gems}\n💸"
                bot.send_message(user_id, profile_info)
            else:
                bot.send_message(user_id, "❌ Error!")

            plr_conn.close()
        else:
            bot.send_message(user_id, "❌ Something went wrong! Try again!)")

    except Exception as e:
        bot.send_message(user_id, f"{str(e)}")

    finally:
        users_conn.close()
        account_conn.close()                             

@bot.message_handler(commands=['recloud'])
def lost_account(message):
    user_id = message.from_user.id

    try:
        users_conn = sqlite3.connect('users.db')
        users_cursor = users_conn.cursor()

        users_cursor.execute(f"SELECT lowID FROM accountconnect WHERE id_user = {user_id}")
        row = users_cursor.fetchone()

        if row:
            lowID = row[0]

            plr_conn = sqlite3.connect('database/Player/plr.db')  # Replace with your path
            plr_cursor = plr_conn.cursor()

            plr_cursor.execute(f"SELECT token FROM plrs WHERE lowID = {lowID}")
            plr_row = plr_cursor.fetchone()

            if plr_row:
                old_token = plr_row[0]

                bot.send_message(user_id, f"💬 Your token: {old_token}\n"
                                          "🆘 We're sorry you lost your account. Follow the steps below to recover it:\n"
                                          "1. Clear all game data\n"
                                          "2. Register again and log into the game's mail\n"
                                          "3. Take a screenshot of the notification\n"
                                          "4. Send it to the bot, and your account will be recovered (if you linked it)\n\n"
                                          "⛔ Enter /stop to cancel the procedure")

                bot.send_message(user_id, "Enter a new token to link:")

                @bot.message_handler(func=lambda m: m.from_user.id == user_id and any(char.isdigit() for char in m.text))
                def handle_token(message):
                    new_token = message.text

                    try:
                        plr_conn_local = sqlite3.connect('database/Player/plr.db')  # Replace the path
                        plr_cursor_local = plr_conn_local.cursor()

                        plr_cursor_local.execute(f"SELECT lowID FROM plrs WHERE token = ?", (new_token,))
                        row = plr_cursor_local.fetchone()

                        if row:
                            lowID_to_delete = row[0]

                            plr_cursor_local.execute(f"DELETE FROM plrs WHERE lowID = ?", (lowID_to_delete,))
                            plr_conn_local.commit()

                            plr_cursor_local.execute(f"UPDATE plrs SET token = ? WHERE lowID = ?", (new_token, lowID))
                            plr_conn_local.commit()

                            bot.send_message(user_id, "✅ Account successfully linked!")
                        else:
                            bot.send_message(user_id, "❌ Invalid token!")

                    except Exception as e:
                        bot.send_message(user_id, f"❌ {str(e)}")
                    finally:
                        plr_conn_local.close()

                bot.register_next_step_handler(message, handle_token)
            else:
                bot.send_message(user_id, "❌ ERROR")

            plr_conn.close()
        else:
            bot.send_message(user_id, "❌ Link your account or contact support.")

    except Exception as e:
        bot.send_message(user_id, f"❌ An error occurred: {str(e)}")

    finally:
        users_conn.close()

@bot.message_handler(commands=['stop'])
def stop_procedure(message):
    bot.send_message(message.chat.id, "❌ Linking canceled!")
    start(message)                      
              
bot.polling()