import telebot
from telebot import types
import sqlite3
from googletrans import Translator
import dictionaries
from collections import defaultdict


bot = telebot.TeleBot('7746010028:AAFIIkCfTsUD13vnWLwVEb9dbpwbOa5uxOM')

TOKEN = '7746010028:AAFIIkCfTsUD13vnWLwVEb9dbpwbOa5uxOM'

user_states = {}
user_filters = {}
translator = Translator()


def translate_text(text, src='auto', dest='ru'):
    try:
        return translator.translate(text, src=src, dest=dest).text
    except:
        return text


def translate_author(name):
    parts = name.split()
    return " ".join(dictionaries.special_names_authors.get(part, part) for part in parts)


def translate_person(name):
    parts = name.split()
    tr_parts = []
    for part in parts:
        if part in dictionaries.actors_special_names:
            tr_parts.append(dictionaries.actors_special_names[part])
        elif part in dictionaries.special_names_directors:
            tr_parts.append(dictionaries.special_names_directors[part])
        else:
            tr_parts.append(part)
    return " ".join(tr_parts)


def find_movies_by_filters(filters):
    conn = sqlite3.connect('D:/maria/db/my_database1.db')
    try:
        cursor = conn.cursor()

        query = """
            SELECT DISTINCT
                m.tconst,  
                m.primaryTitle, 
                m.startYear, 
                r.averageRating,
                m.genres,
                m.runtimeMinutes
            FROM movies1 m
            LEFT JOIN ratings r ON m.tconst = r.tconst
            LEFT JOIN principals p ON m.tconst = p.tconst
            LEFT JOIN people pe ON p.nconst = pe.nconst
            WHERE 1=1
        """

        params = []

        if 'director' in filters:
            dir_eng = translate_person(filters['director'])
            query += " AND p.nconst IN (SELECT nconst FROM people WHERE primaryName LIKE ?) AND p.category = 'director'"
            params.append(f"%{dir_eng}%")

        if 'actor' in filters:
            act_eng = translate_person(filters['actor'])
            query += " AND p.nconst IN (SELECT nconst FROM people WHERE primaryName LIKE ?) AND p.category = 'actor'"
            params.append(f"%{act_eng}%")

        if 'genre' in filters:
            query += " AND m.genres LIKE ?"
            params.append(f"%{filters['genre']}%")

        if 'year' in filters:
            query += " AND m.startYear = ?"
            params.append(filters['year'])

        if 'rating' in filters:
            query += " AND r.averageRating >= ?"
            params.append(filters['rating'])

        if 'runtime' in filters:
            query += " AND m.runtimeMinutes >= ?"
            params.append(filters['runtime'])

        query += " ORDER BY r.averageRating DESC LIMIT 5"

        cursor.execute(query, params)
        results = cursor.fetchall()

        unique_movies = {}
        for row in results:
            tconst = row[0]
            if tconst not in unique_movies:
                unique_movies[tconst] = {
                    'title': row[1] or "Без названия",
                    'year': row[2] or "?",
                    'rating': float(row[3]),
                    'genres': row[4] or "Не указаны",
                    'runtime': f"{row[5]} мин" if row[5] else "?"
                }

        return list(unique_movies.values())

    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")
        return []
    finally:
        conn.close()


def find_books_by_filters(filters):
    conn = sqlite3.connect('D:/maria/db/my_database_books.db')
    try:
        cursor = conn.cursor()

        query = """
            SELECT title, authors, published_year, average_rating, description
            FROM people
            WHERE 1=1
        """

        params = []

        if 'author' in filters:
            auth_eng = translate_author(filters['author'])
            query += " AND authors LIKE ?"
            params.append(f"%{auth_eng}%")

        if 'genre' in filters:
            query += " AND categories LIKE ?"
            params.append(f"%{filters['genre']}%")

        if 'year' in filters:
            query += " AND published_year = ?"
            params.append(filters['year'])

        if 'rating' in filters:
            query += " AND average_rating >= ?"
            params.append(filters['rating'])

        if 'plot' in filters:
            query += " AND description LIKE ?"
            params.append(f"%{filters['plot']}%")

        query += " ORDER BY average_rating DESC LIMIT 5"

        cursor.execute(query, params)
        books = cursor.fetchall()

        return [(translate_text(title), authors, year, rating, description)
                for title, authors, year, rating, description in books]
    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")
        return []
    finally:
        conn.close()

user_data = {}

USER_STATES = {
    'SELECTING_TYPE': 0,
    'REQUESTING_FILM': 1,
    'REQUESTING_BOOK': 2,
    'WAITING_FILTER_VALUE': 3,
    'ASKING_ADD_MORE': 4,
    'SEARCHING': 5
}

def reset_user_state(chat_id):
    user_data[chat_id] = {
        'state': USER_STATES['SELECTING_TYPE'],
        'search_type': None,
        'filters': {},
        'current_filter': None
    }


FILM_FILTERS = {
    'Режиссёр': 'director',
    'Актёр': 'actor',
    'Жанр': 'genre',
    'Год выхода': 'year',
    'Продолжительность': 'runtime',
    'Рейтинг': 'rating'
}

BOOK_FILTERS = {
    'Автор': 'author',
    'Жанр': 'genre',
    'Год публикации': 'year',
    'Рейтинг': 'rating',
    'Сюжет': 'plot'
}


@bot.message_handler(commands=['start'])
def start(message):
    reset_user_state(message.chat.id)
    show_main_menu(message.chat.id)


def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Ищу фильм')
    btn2 = types.KeyboardButton('Ищу книгу')
    markup.add(btn1, btn2)

    user_data[chat_id]['state'] = USER_STATES['SELECTING_TYPE']
    bot.send_message(chat_id, 'Что вы хотите найти?', reply_markup=markup)


@bot.message_handler(func=lambda message: user_data[message.chat.id]['state'] == USER_STATES['SELECTING_TYPE'])
def handle_search_type(message):
    chat_id = message.chat.id

    if message.text == 'Ищу фильм':
        user_data[chat_id]['search_type'] = 'film'
        user_data[chat_id]['state'] = USER_STATES['REQUESTING_FILM']
        show_film_filters(chat_id)
    elif message.text == 'Ищу книгу':
        user_data[chat_id]['search_type'] = 'book'
        user_data[chat_id]['state'] = USER_STATES['REQUESTING_BOOK']
        show_book_filters(chat_id)
    else:
        bot.send_message(chat_id, 'Пожалуйста, выберите тип поиска')


def show_film_filters(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for filter_name in FILM_FILTERS:
        markup.add(types.KeyboardButton(filter_name))
    markup.add(types.KeyboardButton('Найти!'))
    markup.add(types.KeyboardButton('Назад'))

    bot.send_message(chat_id, 'Выберите критерий поиска фильма:', reply_markup=markup)


def show_book_filters(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for filter_name in BOOK_FILTERS:
        markup.add(types.KeyboardButton(filter_name))
    markup.add(types.KeyboardButton('Найти!'))
    markup.add(types.KeyboardButton('Назад'))

    bot.send_message(chat_id, 'Выберите критерий поиска книги:', reply_markup=markup)


@bot.message_handler(func=lambda message:
user_data[message.chat.id]['state'] in [USER_STATES['REQUESTING_FILM'], USER_STATES['REQUESTING_BOOK']] and
message.text in list(FILM_FILTERS.keys()) + list(BOOK_FILTERS.keys()))
def handle_filter_selection(message):
    chat_id = message.chat.id
    user = user_data[chat_id]

    if user['search_type'] == 'film':
        filter_key = FILM_FILTERS.get(message.text)
    else:
        filter_key = BOOK_FILTERS.get(message.text)

    if filter_key:
        user['current_filter'] = filter_key
        user['state'] = USER_STATES['WAITING_FILTER_VALUE']
        bot.send_message(chat_id, f'Введите значение для "{message.text}":')


@bot.message_handler(func=lambda message: user_data[message.chat.id]['state'] == USER_STATES['WAITING_FILTER_VALUE'])
def handle_filter_value(message):
    chat_id = message.chat.id
    user = user_data[chat_id]

    user['filters'][user['current_filter']] = message.text
    user['current_filter'] = None
    user['state'] = USER_STATES['ASKING_ADD_MORE']

    ask_to_add_more(chat_id)


def ask_to_add_more(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Да'), types.KeyboardButton('Нет'))
    bot.send_message(chat_id, 'Добавить ещё критерий поиска?', reply_markup=markup)


@bot.message_handler(func=lambda message: user_data[message.chat.id]['state'] == USER_STATES['ASKING_ADD_MORE'])
def handle_add_more_choice(message):
    chat_id = message.chat.id
    user = user_data[chat_id]

    if message.text == 'Да':
        user['state'] = USER_STATES['REQUESTING_FILM'] if user['search_type'] == 'film' else USER_STATES['REQUESTING_BOOK']
        if user['search_type'] == 'film':
            show_film_filters(chat_id)
        else:
            show_book_filters(chat_id)
    elif message.text == 'Нет':
        user['state'] = USER_STATES['SEARCHING']
        #massive(chat_id)
        perform_search(chat_id)
    else:
        bot.send_message(chat_id, 'Пожалуйста, выберите "Да" или "Нет"')


def massive(chat_id):
    result = user_data[chat_id]['search_type']
    filters = user_data[chat_id]['filters']
    query = """
                SELECT DISTINCT
                    m.tconst,  
                    m.primaryTitle, 
                    m.startYear, 
                    COALESCE(r.averageRating, 0) as rating,
                    m.genres,
                    m.runtimeMinutes
                FROM movies1 m
                LEFT JOIN ratings r ON m.tconst = r.tconst
                LEFT JOIN principals1 p ON m.tconst = p.tconst
                LEFT JOIN people pe ON p.nconst = pe.nconst
                WHERE 1=1
            """

    params = []

    if 'director' in filters:
        query += " AND p.nconst IN (SELECT nconst FROM people WHERE primaryName LIKE ?) AND p.category = 'director'"
        params.append(f"%{filters['director']}%")

    if 'actor' in filters:
        query += " AND p.nconst IN (SELECT nconst FROM people WHERE primaryName LIKE ?) AND p.category = 'actor'"
        params.append(f"%{filters['actor']}%")

    if 'genre' in filters:
        query += " AND m.genres LIKE ?"
        params.append({filters['genre']})

    if 'year' in filters:
        query += " AND m.startYear = ?"
        params.append(filters['year'])

    if 'rating' in filters:
        query += " AND r.averageRating >= ?"
        params.append(filters['rating'])

    if 'runtime' in filters:
        query += " AND m.runtimeMinutes >= ?"
        params.append(filters['runtime'])

    query += " ORDER BY r.averageRating DESC LIMIT 5"
    bot.send_message(chat_id, query)
    for par in params:
        bot.send_message(chat_id, str(par))




@bot.message_handler(func=lambda message: message.text == 'Найти!')
def handle_search_now(message):
    chat_id = message.chat.id
    user = user_data[chat_id]

    if user['state'] in [USER_STATES['REQUESTING_FILM'], USER_STATES['REQUESTING_BOOK']]:
        user['state'] = USER_STATES['SEARCHING']
        perform_search(chat_id)


@bot.message_handler(func=lambda message: message.text == 'Назад')
def handle_back(message):
    start(message.chat.id)


def perform_search(chat_id):
    try:
        if chat_id not in user_data:
            bot.send_message(chat_id, "Что-то пошло не так. Пожалуйста, начните заново с /start")
            return

        user = user_data[chat_id]
        results = []

        if user['search_type'] == 'film':
            results = find_movies_by_filters(user['filters'])
            if not results:
                bot.send_message(chat_id, "🚫 Фильмы по вашим критериям не найдены")
            else:
                response = "🎬 Найденные фильмы:\n\n"
                for movie in results:
                    response += (
                        f"📌 {movie['title']} ({movie['year']})\n"
                        f"⭐ Рейтинг: {movie['rating']}\n"
                        f"⏱ Длительность: {movie['runtime']}\n"
                        f"🎭 Жанры: {movie['genres']}\n\n"
                    )
                bot.send_message(chat_id, response)
        else:
            results = find_books_by_filters(user['filters'])
            if not results:
                bot.send_message(chat_id, "🚫 Книги по вашим критериям не найдены")
            else:
                response = "📚 Найденные книги:\n\n"
                for book in results:
                    title, authors, year, rating, _ = book
                    response += (
                        f"📖 {title}\n"
                        f"✍️ Автор: {authors}\n"
                        f"📅 Год: {year}\n"
                        f"⭐ Рейтинг: {rating}\n\n"
                    )
                bot.send_message(chat_id, response)
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        bot.send_message(chat_id, "⚠️ Произошла ошибка при поиске. Попробуйте ещё раз.")
    finally:
        reset_user_state(chat_id)
        show_main_menu(chat_id)



bot.polling(none_stop=True)


