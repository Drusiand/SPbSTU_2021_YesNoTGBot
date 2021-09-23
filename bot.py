from telebot import TeleBot
import requests
import os

TOKEN = os.environ["TOKEN"]
URL = os.environ["URL"]

bot = TeleBot(TOKEN)
url = URL
games = list()


def run():
    raw_data = requests.get(url).json()
    for key, value in enumerate(raw_data):
        games.append(value)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Alright!\n"
                                               "Type /next to get new game;\n"
                                               "Type /previous to return to previous one;\n")
        bot.register_next_step_handler(message, next_game, -1)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Type /start to start the session!")
    else:
        bot.send_message(message.from_user.id, "Sorry, I can't understand what you wrote!\n"
                                               "Please, type /help.")


def next_game(message, game_index):
    if message.text == "/next":
        if game_index < len(games) - 1:
            game_index += 1
            bot.send_message(message.from_user.id, process_game_token(games[game_index]))
        else:
            bot.send_message(message.from_user.id, "You reached the end of database!")
    elif message.text == "/previous":
        if game_index > 0:
            game_index -= 1
            bot.send_message(message.from_user.id, process_game_token(games[game_index]))
        else:
            bot.send_message(message.from_user.id, "You reached the beginning of the database!")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Type /next to get new game;\n"
                                               "Type /previous to return to previous one;\n"
                                               "Type /stop to stop the session;\n")
    elif message.text == "/stop":
        bot.send_message(message.from_user.id, "Session is stopped!\n"
                                               "To begin the new one type /start")
    else:
        bot.send_message(message.from_user.id, "Sorry, I can't understand what you wrote!\n"
                                               "Please, type /help.")
    if message.text != "/stop":
        bot.register_next_step_handler(message, next_game, game_index)


def process_game_token(data):
    result = ""
    for token in data:
        result += token.upper() + ": " + data[token] + "\n\n"
    return result


if __name__ == '__main__':
    run()
    bot.polling(none_stop=True, interval=0)
