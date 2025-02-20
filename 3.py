import telebot
import requests
import json
from telebot import types
from imdb_api import IMDb
import sqlite3

bot = telebot.TeleBot('7746010028:AAFIIkCfTsUD13vnWLwVEb9dbpwbOa5uxOM')
myHeaders = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-KEY": 'RX4X65K-F9KMGB1-HA7F7R6-GYSF9KS'
}

TOKEN = '7746010028:AAFIIkCfTsUD13vnWLwVEb9dbpwbOa5uxOM'
chat_id = "1731612820"

user_states = {} #словарь состояний нашего пользователя
def find_movies_by_person(person_name):
    conn = sqlite3.connect('my_database.db')  # Подключаемся к нашей базе данных
    cursor = conn.cursor()
    cursor.execute("""
    SELECT nconst FROM people WHERE primaryName = ?
    """, (person_name,))
    person = cursor.fetchone()
    if not person:
        return None  # если не нашли человека
    person_id = person[0]
    # Ищем фильмы, связанные с этим человеком
    cursor.execute("""
    SELECT movies.titleId, movies.title, movies.year, ratings.averageRating
    FROM movies
    JOIN movie_people ON movies.titleId = movie_people.movie_id
    JOIN ratings ON movies.titleId = ratings.tconst
    WHERE movie_people.person_id = ? AND movie_people.role = 'director'
    """, (person_id,))
    movies = cursor.fetchall()
    conn.close()
    return movies

@bot.message_handler(commands=['start'])  # старт бота
def get_start(message):  # функция, помогающая получить боту корректный запрос от пользователя
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем переменную, которая будет определять размер кнопок меню команд
    book = types.KeyboardButton('Ищу книгу')
    movie = types.KeyboardButton('Ищу фильм')
    markup.add(book, movie)  # создали кнопки меню
    bot.send_message(message.chat.id, 'Привет, {0.first_name}, что ты хочешь найти?'.format(message.from_user), reply_markup=markup)  # приветствие бота


@bot.message_handler(content_types=['text'])  # обработчик на получение сообщений от пользователя
def get_message(message):
    if message.chat.type == 'private':
        if message.text == 'Ищу книгу':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем переменную, которая будет определять размер кнопок нового меню команд
            plot = types.KeyboardButton('Сюжет')
            author = types.KeyboardButton('Автор')
            main_characters = types.KeyboardButton('Главные герои')
            scene_of_action = types.KeyboardButton('Место действия')
            time_of_action = types.KeyboardButton('Время действия')
            back = types.KeyboardButton('Назад')

            markup.add(plot, author, main_characters, scene_of_action, time_of_action, back)  # создали кнопки нового меню для книг
            bot.send_message(message.chat.id, 'По какому критерию хочешь найти книгу?'.format(message.from_user), reply_markup=markup)

        elif message.text == 'Ищу фильм':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создаем переменную, которая будет определять размер кнопок нового меню команд
            plot = types.KeyboardButton('Сюжет')
            director = types.KeyboardButton('Режиссёр')
            main_characters = types.KeyboardButton('Главные актёры')
            scene_of_action = types.KeyboardButton('Страна')
            time_of_action = types.KeyboardButton('Год выхода')
            back = types.KeyboardButton('Назад')

            markup.add(plot, director, main_characters, scene_of_action, time_of_action, back)  # создали кнопки нового меню для фильмов
            bot.send_message(message.chat.id, 'По какому критерию хочешь найти фильм?'.format(message.from_user), reply_markup=markup)


        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            book = types.KeyboardButton('Ищу книгу')
            movie = types.KeyboardButton('Ищу фильм')
            markup.add(book, movie)
            bot.send_message(message.chat.id, 'Что ты хочешь найти?'.format(message.from_user), reply_markup=markup)


        elif message.text == 'Режиссёр':
            bot.send_message(chat_id, 'Как зовут этого режиссера (имя, фамилия)?')
            user_states[chat_id] = 'waiting_for_director_name'  # Устанавливаем состояние пользователя


        elif user_states.get(chat_id) == 'waiting_for_director_name':
            director_name = message.text
            movies = find_movies_by_person(director_name)
            if not movies:
                bot.send_message(chat_id, 'Ничего не найдено. Проверьте имя и попробуйте еще раз.')
            else:
                response = "Вот что я нашел:\n\n"
                for movie in movies:
                    title_id, title, year, rating = movie
                    response += f" {title} ({year})\n Рейтинг: {rating}\n\n"
                bot.send_message(chat_id, response)
            user_states[chat_id] = None # cбрасываем состояние пользователя

        else:
            bot.send_message(chat_id, 'Я не понимаю, что ты хочешь')


bot.polling(none_stop=True, interval=0)  # так бот будет постоянно кидать запрос от сервера на получение вопросов от пользователя, т.е. он всегда будет "готов" к работе
