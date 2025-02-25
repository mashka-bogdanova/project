import telebot
import requests
from telebot import types
import sqlite3

bot = telebot.TeleBot('7746010028:AAFIIkCfTsUD13vnWLwVEb9dbpwbOa5uxOM')
myHeaders = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-KEY": 'RX4X65K-F9KMGB1-HA7F7R6-GYSF9KS'
}

TOKEN = '7746010028:AAFIIkCfTsUD13vnWLwVEb9dbpwbOa5uxOM'

user_states = {}
def find_movies_by_person(person_name):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT nconst, knownForTitles FROM people WHERE primaryName = ?
        """, (person_name,))
        person = cursor.fetchone()
        if not person:
            return None
        person_id, known_for_titles = person
        movie_ids = known_for_titles.split(',')
        movies = []
        for movie_id in movie_ids:
            cursor.execute("""
            SELECT titleId, title FROM movies WHERE titleId = ?
            """, (movie_id,))
            movie = cursor.fetchone()
            if movie:
                movies.append(movie)
        results = []
        for movie in movies:
            title_id, title = movie
            cursor.execute("""
            SELECT averageRating FROM ratings WHERE tconst = ?
            """, (title_id,))
            rating = cursor.fetchone()
            if rating:
                results.append((title, rating[0]))
            else:
                results.append((title, "Рейтинг не найден"))
        return results
    finally:
        conn.close()



def find_movies_by_person_other(person_name):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT nconst FROM people WHERE primaryName = ?
        """, (person_name,))
        person_id = cursor.fetchone()
        if not person_id:
            return None
        movies = []
        cursor.execute("""
                SELECT tconst FROM principals1 WHERE nconst = ?
                """, (person_id,))
        movie_id = cursor.fetchone()
        if movie_id:
            movies.append(movie_id)

        results = []

        for movie_id in movies:
            cursor.execute("""
            SELECT averageRating FROM ratings WHERE tconst = ?
            """, (movie_id,))
            rating = cursor.fetchone()
            cursor.execute("""
            SELECT title FROM movies WHERE titleId = ?
            """, (movie_id,))
            title = cursor.fetchone()
            if rating:
                results.append((title, rating[0]))
            else:
                results.append((title, "Рейтинг не найден"))

        return results
    finally:
        conn.close()

@bot.message_handler(commands=['start'])
def get_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    book = types.KeyboardButton('Ищу книгу')
    movie = types.KeyboardButton('Ищу фильм')
    markup.add(book, movie)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}, что ты хочешь найти?'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_message(message):
    chat_id = message.chat.id
    if message.chat.type == 'private':
        if message.text == 'Ищу книгу':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            plot = types.KeyboardButton('Сюжет')
            author = types.KeyboardButton('Автор')
            main_characters = types.KeyboardButton('Главные герои')
            scene_of_action = types.KeyboardButton('Место действия')
            time_of_action = types.KeyboardButton('Время действия')
            back = types.KeyboardButton('Назад')

            markup.add(plot, author, main_characters, scene_of_action, time_of_action, back)
            bot.send_message(message.chat.id, 'По какому критерию хочешь найти книгу?'.format(message.from_user), reply_markup=markup)

        elif message.text == 'Ищу фильм':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            plot = types.KeyboardButton('Сюжет')
            director = types.KeyboardButton('Режиссёр')
            main_characters = types.KeyboardButton('Главные актёры')
            scene_of_action = types.KeyboardButton('Страна')
            time_of_action = types.KeyboardButton('Год выхода')
            back = types.KeyboardButton('Назад')

            markup.add(plot, director, main_characters, scene_of_action, time_of_action, back)
            bot.send_message(message.chat.id, 'По какому критерию хочешь найти фильм?'.format(message.from_user), reply_markup=markup)


        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            book = types.KeyboardButton('Ищу книгу')
            movie = types.KeyboardButton('Ищу фильм')
            markup.add(book, movie)
            bot.send_message(message.chat.id, 'Что ты хочешь найти?'.format(message.from_user), reply_markup=markup)


        elif message.text == 'Режиссёр':
            bot.send_message(chat_id, 'Как зовут этого режиссера (имя, фамилия)?')
            user_states[message.chat.id] = 'waiting_for_director_name'


        elif message.text == 'Главные актёры':
            bot.send_message(chat_id, 'Как зовут актера/актеров (имя, фамилия)?')
            user_states[message.chat.id] = 'waiting_for_actors_name'


        elif user_states.get(message.chat.id) == 'waiting_for_director_name':
            director_name = message.text
            movies = find_movies_by_person(director_name)
            if not movies:
                bot.send_message(message.chat.id, 'Ничего не найдено. Проверьте имя и попробуйте еще раз.')
            else:
                response = "Вот что я нашел:\n\n"
                for movie in movies:
                    title, rating = movie
                    response += f" {title} \n Рейтинг: {rating}\n\n"
                bot.send_message(message.chat.id, response)
            user_states[message.chat.id] = None

        elif user_states.get(message.chat.id) == 'waiting_for_actors_name':
            actors_name = message.text
            movies = find_movies_by_person(actors_name)
            if not movies:
                bot.send_message(message.chat.id, 'Ничего не найдено. Проверьте имя и попробуйте еще раз.')
            else:
                response = "Вот что я нашел:\n\n"
                for movie in movies:
                    title, rating = movie
                    response += f" {title} \n Рейтинг: {rating}\n\n"
                bot.send_message(message.chat.id, response)
            user_states[message.chat.id] = None


        else:
            bot.send_message(message.chat.id, 'Я не понимаю, что ты хочешь')


bot.polling(none_stop=True, interval=0)