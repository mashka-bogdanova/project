import telebot
from telebot import types
import sqlite3
from googletrans import Translator

bot = telebot.TeleBot('7746010028:AAFIIkCfTsUD13vnWLwVEb9dbpwbOa5uxOM')
myHeaders = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-KEY": 'RX4X65K-F9KMGB1-HA7F7R6-GYSF9KS'
}

TOKEN = '7746010028:AAFIIkCfTsUD13vnWLwVEb9dbpwbOa5uxOM'

user_states = {}


special_names_directors = {
    'Стивен': 'Steven',
    'Кристофер': 'Christopher',
    'Стэнли': 'Stanley',
    'Кубрик': 'Kubrick',
    'Альфред': 'Alfred',
    'Хичкок': 'Hitchcock',
    'Акира': 'Akira',
    'Куросава': 'Kurosawa',
    'Федерико': 'Federico',
    'Феллини': 'Fellini',
    'Мартин': 'Martin',
    'Скорсезе': 'Scorsese',
    'Чарли': 'Charles',
    'Чаплин': 'Chaplin',
    'Спилберг': 'Spielberg',
    'Андрей': 'Andrei',
    'Тарковский': 'Tarkovsky',
    'Дэвид': 'David',
    'Линч': 'Lynch',
    'Сергей': 'Sergei',
    'Ейзенштейн': 'Eisenstein',
    'Вуди': 'Woody',
    'Аллен': 'Allen',
    'Роман': 'Roman',
    'Полански': 'Polanski',
    'Квентин': 'Quentin',
    'Тарантино': 'Tarantino',
    'Финчер': 'Fincher',
    'Нолан': 'Nolan',
    'Спайк': 'Spike',
    'Ли': 'Lee',
    'Дуглас': 'Douglas',
    'Сирк': 'Sirk',
    'Оливер': 'Oliver',
    'Ридли': 'Ridley',
    'Скотт': 'Scott',
    'Милош': 'Milos',
    'Форман': 'Forman',
    'Хаяо': 'Hayao',
    'Миядзаки': 'Miyazaki',
    'Уэс': 'Wes',
    'Андерсон': 'Anderson',
    'Даррен': 'Darren',
    'Аронофски': 'Aronofsky',
    'Лукас': 'Lucas',
    'Джордж': 'George',
    'Клуни': 'Clooney',
    'Джеймс': 'James',
    'Кэмерон': 'Cameron',
    'Кроненберг': 'Cronenberg',
    'Вим': 'Wim',
    'Вендерс': 'Wenders',
    'Стоун': 'Stone',
    'Джоэл': 'Joel',
    'Коэн': 'Coen',
    'Джон': 'John',
    'Кассаветис': 'Cassavetes',
    'Ричард': 'Richard',
    'Бёртон': 'Burton',
    'Марлон': 'Marlon',
    'Брандо': 'Brando',
    'Кирк': 'Kirk',
    'Чарлтон': 'Charlton',
    'Хестон': 'Heston',
    'Петер': 'Peter',
    'Лорре': 'Lorre',
    'Пол': 'Paul',
    'Ньюман': 'Newman',
    'Энтони': 'Anthony',
    'Куинн': 'Quinn',
    'Стюарт': 'Stewart',
    'Памела': 'Pamela',
    'Дженнифер': 'Jennifer',
    'Энистон': 'Aniston',
    'Кевин': 'Kevin',
    'Бейкон': 'Bacon',
    'Люк': 'Luc',
    'Бессон': 'Besson',
    'Шон': 'Sean',
    'Коннери': 'Connery',
    'Крейвен': 'Craven',
    'Рассел': 'Russell',
    'Кроу': 'Crowe',
    'Том': 'Tom',
    'Круз': 'Cruise',
    'Джейми': 'Jamie',
    'Кёртис': 'Curtis',
    'Роберт': 'Robert',
    'Де': 'De',
    'Ниро': 'Niro',
    'Джони': 'Johnny',
    'Депп': 'Depp',
    'Майкл': 'Michael',
    'Клинт': 'Clint',
    'Иствуд': 'Eastwood',
    'Джоди': 'Jodie',
    'Фостер': 'Foster',
    'Мел': 'Mel',
    'Гибсон': 'Gibson',
    'Дастин': 'Dustin',
    'Хоффман': 'Hoffman',
    'Томми': 'Tommy',
    'Джонс': 'Jones',
    'Джуд': 'Jude',
    'Лоу': 'Law',
    'Мэтью': 'Matthew',
    'МакКонахи': 'McConaughey',
    'Гэри': 'Gary',
    'Олдман': 'Oldman',
    'Ву': 'Woo',
}

actors_special_names = {
    'Одри': 'Audrey',
    'Хепбёрн': 'Hepburn',
    'Сэмюэл': 'Samuel',
    'Л. Джексон': 'L. Jackson',
    'Аль': 'Al',
    'Пачино': 'Pacino',
    'Морган': 'Morgan',
    'Фриман': 'Freeman',
    'Клинт': 'Clint',
    'Иствуд': 'Eastwood',
    'Сильвестр': 'Sylvester',
    'Сталлоне': 'Stallone',
    'Вигго': 'Viggo',
    'Мортенсен': 'Mortensen',
    'Том': 'Tom',
    'Харди': 'Hardy',
    'Джейсон': 'Jason',
    'Стейтем': 'Statham',
    'Мэтью': 'Matthew',
    'МакКонахи': 'McConaughey',
    'Леонардо': 'Leonardo',
    'ДиКаприо': 'DiCaprio',
    'Джефф': 'Jeff',
    'Бриджес': 'Bridges',
    'Джим': 'Jim',
    'Керри': 'Carrey',
    'Иен': 'Ian',
    'Маккеллен': 'McKellen',
    'Джон': 'John',
    'Малкович': 'Malkovich',
    'Киану': 'Keanu',
    'Ривз': 'Reeves',
    'Дензел': 'Denzel',
    'Вашингтон': 'Washington',
    'Кевин': 'Kevin',
    'Костнер': 'Costner',
    'Шон': 'Sean',
    'Пенн': 'Penn',
    'Коннери': 'Connery',
    'Брэд': 'Brad',
    'Питт': 'Pitt',
    'Мэтт': 'Matt',
    'Дэймон': 'Damon',
    'Роберт': 'Robert',
    'Де Ниро': 'De Niro',
    'Уиллем': 'Willem',
    'Дефо': 'Dafoe',
    'Киллиан': 'Cillian',
    'Мёрфи': 'Murphy',
    'Рами': 'Rami',
    'Малек': 'Malek',
    'Брюс': 'Bruce',
    'Уиллис': 'Willis',
    'Арнольд': 'Arnold',
    'Шварценеггер': 'Schwarzenegger',
    'Рэй': 'Ray',
    'Лиотта': 'Liotta',
    'Бэйкон': 'Bacon',
    'Райан': 'Ryan',
    'Рейнольдс': 'Reynolds',
    'Гослинг': 'Gosling',
    'Вин': 'Vin',
    'Дизель': 'Diesel',
    'Гэри': 'Gary',
    'Олдман': 'Oldman',
    'Кристиан': 'Christian',
    'Бейл': 'Bale',
    'Тоби': 'Tobey',
    'Магуайр': 'Maguire',
    'Хэнкс': 'Hanks',
    'Николас': 'Nicolas',
    'Кейдж': 'Cage',
    'Круз': 'Cruise',
    'Траволта': 'Travolta',
    'Курт': 'Kurt',
    'Рассел': 'Russell',
    'Марк': 'Mark',
    'Уолберг': 'Wahlberg',
    'Кроу': 'Crowe',
    'Дуэйн': 'Dwayne',
    'Джонсон': 'Johnson',
    'Идрис': 'Idris',
    'Эльба': 'Elba',
    'Хоакин': 'Joaquin',
    'Феникс': 'Phoenix',
    'Мэл': 'Mel',
    'Гибсон': 'Gibson',
    'Эдвард': 'Edward',
    'Нортон': 'Norton',
    'Уилл': 'Will',
    'Смит': 'Smith',
    'Джеки': 'Jackie',
    'Чан': 'Chan',
    'Кристоф': 'Christoph',
    'Вальц': 'Waltz',
    'Вивьен': 'Vivien',
    'Ли': 'Leigh',
    'Мэрил': 'Meryl',
    'Стрип': 'Streep',
    'Мэрлин': 'Marilyn',
    'Монро': 'Monroe',
    'Джоди': 'Jodie',
    'Фостер': 'Foster',
    'Николь': 'Nicole',
    'Кидман': 'Kidman',
    'Кейт': 'Cate',
    'Бланшетт': 'Blanchett',
    'Шарлиз': 'Charlize',
    'Терон': 'Theron',
    'Софи': 'Sophia',
    'Лорен': 'Loren',
    'Сигурни': 'Sigourney',
    'Уивер': 'Weaver',
    'Сандра': 'Sandra',
    'Буллок': 'Bullock',
    'Хелена': 'Helena',
    'Бонэм': 'Bonham',
    'Картер': 'Carter',
    'Марлен': 'Marlene',
    'Дитрих': 'Dietrich',
    'Ума': 'Uma',
    'Турман': 'Thurman',
    'Анджелина': 'Angelina',
    'Джоли': 'Jolie',

}
special_names_authors = {
    'Стивен': 'Stephen',
    'Кинг': 'King',
    'Агата': 'Agatha',
    'Кристи': 'Christie',
    'Рэй': 'Raymond',
    'Брэдбери': 'Bradbury',
    'Эрих': 'Erich',
    'Мария': 'Maria',
    'Ремарк': 'Remark',
    'Джоан': 'Joanne',
    'Роулинг': 'Rowling',
    'Дэниел': 'Daniel',
    'Киз': 'Keyes',
    'Джордж': 'George',
    'Оруэлл': 'Orwell',
    'Оскар': 'Oscar',
    'Уальд': 'Wilde',
    'Антуан': 'Antoine',
    'де': 'de',
    'Сент-Экзюпери': 'Saint-Exupery',
    'Джек': 'Jack',
    'Лондон': 'London',
    'Джейн': 'Jane ',
    'Остин': 'Austen',
    'Джером': 'Jerome',
    'Сэлинджер': 'Salinger',
    'Фрэнсис': 'Francis',
    'Скотт': 'Scott',
    'Фицджеральд': 'Fitzgerald',
    'Шарлотта': 'Charlotte',
    'Бронте': 'Bronte',
    'Нил': 'Neil',
    'Гейман': 'Gaiman',
    'Харуки': 'Haruki',
    'Мураками': 'Murakami',
    'Чак': 'Chuck',
    'Паланик': 'Palahnuik',
    'Артур': 'Arthur',
    'Конан': 'Conan',
    'Дойл': 'Doyle',
    'Харпер': 'Harper',
    'Ли': 'Lee',
    'Пауло': 'Paulo',
    'Коэльо': 'Coelho',
    'Джон': 'John',
    'Толкиен': 'Tolkien',
    'Александр': 'Alexandre',
    'Дюма': 'Dumas',
    'Габриель': 'Gabriel',
    'Маркес': 'Marques',
    'Эрнест': 'Ernest',
    'Хемингуэй': 'Hemingway',
    'Олдос': 'Aldous',
    'Хаксли': 'Huxley',
    'Эмили': 'Emily',
    'Уиллиам': 'William',
    'Голдинг': 'Golding',
    'Фаулз': 'Fowles',
    'Маргарет': 'Margaret',
    'Митчелл': 'Mitchell',
    'Шекспир': 'Shakespeare',
    'Дэн': 'Dan',
    'Браун': 'Brown',
    'Сомерсет': 'Somerset',
    'Моэм': 'Maugham',
    'Виктор': 'Victor',
    'Гюго': 'Hugo',
    'Маркус': 'Markus',
    'Зусак': 'Zusak',
    'Франц': 'Franz',
    'Кафка': 'Kafka',
    'Жюль': 'Jules',
    'Верн': 'Verne',
    'Кен': 'Ken',
    'Кизи': 'Kesey',
    'Достоевский': 'Dostoevsky',
    'Фёдор': 'Fyodor',
    'Лев': 'Leo',
    'Толстой': 'Tolstoy',
    'Тургенев': 'Turgenev',
    'Иван': 'Ivan',
    'Михаил': 'Mikhail',
    'Булгаков': 'Bulgakov',
    'Пушкин': 'Pushkin',
    'Николай': 'Nikolai',
    'Гоголь': 'Gogol',
    'Стругацкий': 'Strugatsky',
    'Аркадий': 'Arkady',
    'Борис': 'Boris',
    'Лермонтов': 'Lermontov',
    'Чехов': 'Chekhov',
    'Антон': 'Anton',
    'Набоков': 'Nabokov',
    'Владимир': 'Vladimir',
    'Куприн': 'Kuprin',
}


def translation(title):
    translator = Translator()
    str = "'" + title + "'"
    title_ru = translator.translate(str, dest='ru').text
    return title_ru


def translate_author(name):
    parts = name.split
    tr_parts = []
    for part in parts:
        if part in special_names_authors:
            tr_parts.append(special_names_authors[part])
        else:
            bot.send_message(name.chat.id, 'Пожалуйста, проверьте написание имени или напишите запрос на английском')
    return " ".join(tr_parts)


def translate_person(name):
    parts = name.split
    tr_parts = []
    for part in parts:
        if part in actors_special_names:
            tr_parts.append(actors_special_names[part])
        elif part in special_names_directors:
            tr_parts.append(special_names_directors[part])
        else:
            bot.send_message(name.chat.id, 'Пожалуйста, проверьте написание имени или напишите запрос на английском')
    return " ".join(tr_parts)




def find_movies_by_person(person_name, role):
    person_name_eng = translate_person(person_name)
    if not person_name_eng:
        return []
    conn = sqlite3.connect('my_database.db')
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT nconst FROM people WHERE primaryName = ?", (person_name_eng,))
        person_id = cursor.fetchone()
        if not person_id:
            return []

        cursor.execute("""
            SELECT m.primaryTitle, m.startYear, r.averageRating, m.genres, m.runtimeMinutes 
            FROM principals1 p
            JOIN movies1 m ON p.tconst = m.tconst
            LEFT JOIN ratings r ON p.tconst = r.tconst
            WHERE p.nconst = ? AND p.category = ?
            ORDER BY r.averageRating DESC
            LIMIT 15
        """, (person_id[0], role))

        results = []
        for title, year, rating, genres, runtime in cursor.fetchall():
            results.append((
                title or "Нет названия",
                year or "неизвестен",
                float(rating) if rating else 0.0,
                genres or "не указаны",
                runtime or "?"
            ))
        return results
    except sqlite3.Error as e:
        print("DB Error:", e)
        return []
    finally:
        conn.close()


def find_movies(filters):
    conn = sqlite3.connect('my_database.db')
    try:
        cursor = conn.cursor()
        query = """
        SELECT m.primaryTitle, m.startYear, r.averageRating, m.genres, m.runtimeMinutes
        FROM movies1 m
        LEFT JOIN ratings r ON m.tconst = r.tconst
        WHERE 1=1
        """
        params = []

        if "genre" in filters:
            query += " AND m.genres LIKE ?"
            params.append(f'%{filters["genre"]}%')
        if "year" in filters:
            query += " AND m.startYear = ?"
            params.append(int(filters["year"]))
        if "runtime" in filters:
            query += " AND m.runtimeMinutes >= ?"
            params.append(int(filters["runtime"]))
        if "rating" in filters:
            query += " AND r.averageRating >= ?"
            params.append(float(filters["rating"]))

        query += " ORDER BY r.averageRating DESC LIMIT 15"
        cursor.execute(query, params)

        results = []
        for title, year, rating, genres, runtime in cursor.fetchall():
            results.append((
                title or "Нет названия",
                year or "неизвестен",
                float(rating) if rating else 0.0,
                genres or "не указаны",
                runtime or "?"
            ))
        return results
    except sqlite3.Error as e:
        print("DB Error:", e)
        return []
    finally:
        conn.close()


def find_books_by_author(author_name):
    author_name_eng = translate_author(author_name)
    if not author_name_eng:
        return []

    conn = sqlite3.connect('my_database_books.db')
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title, authors, published_year, average_rating 
            FROM books 
            WHERE authors LIKE ?
            ORDER BY average_rating DESC
            LIMIT 10
        """, (f"%{author_name_eng}%",))

        results = []
        for title, authors, year, rating in cursor.fetchall():
            results.append((
                translation(title) if title else "Нет названия",
                authors or "неизвестен",
                year or "неизвестен",
                float(rating) if rating else 0.0
            ))
        return results
    except sqlite3.Error as e:
        print("DB Error:", e)
        return []
    finally:
        conn.close()


def find_books_by_genre(genre):
    conn = sqlite3.connect('my_database_books.db')
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title, authors, published_year, average_rating 
            FROM books 
            WHERE categories LIKE ?
            ORDER BY average_rating DESC
            LIMIT 10
        """, (f"%{genre}%",))

        results = []
        for title, authors, year, rating in cursor.fetchall():
            results.append((
                translation(title) if title else "Нет названия",
                authors or "неизвестен",
                year or "неизвестен",
                float(rating) if rating else 0.0
            ))
        return results
    except sqlite3.Error as e:
        print("DB Error:", e)
        return []
    finally:
        conn.close()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('🎬 Искать фильм'), types.KeyboardButton('📚 Искать книгу'))
    bot.send_message(message.chat.id, "Что вы хотите найти?", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == '🎬 Искать фильм')
def search_movie(message):
    chat_id = message.chat.id
    user_states[chat_id] = {
        'mode': 'movie',
        'filters': {},
        'current_step': None
    }
    show_movie_filters(chat_id)


def show_movie_filters(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('По жанру'), types.KeyboardButton('По году'))
    markup.row(types.KeyboardButton('По рейтингу'), types.KeyboardButton('По длительности'))
    markup.row(types.KeyboardButton('По режиссеру'), types.KeyboardButton('По актеру'))
    markup.row(types.KeyboardButton('Найти!'), types.KeyboardButton('↩️ Назад'))
    bot.send_message(chat_id, "Выберите критерий поиска:", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == '📚 Искать книгу')
def search_book(message):
    chat_id = message.chat.id
    user_states[chat_id] = {
        'mode': 'book',
        'filters': {},
        'current_step': None
    }
    show_book_filters(chat_id)


def show_book_filters(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('По жанру'), types.KeyboardButton('По автору'))
    markup.row(types.KeyboardButton('Найти!'), types.KeyboardButton('Назад'))
    bot.send_message(chat_id, "Выберите критерий поиска:", reply_markup=markup)


@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get('mode') == 'movie')
def handle_movie_filter(message):
    chat_id = message.chat.id
    state = user_states[chat_id]
    if message.text == '↩️ Назад':
        user_states.pop(chat_id, None)
        start(message)
        return

    if message.text == 'По жанру':
        state['current_step'] = 'genre'
        markup = types.InlineKeyboardMarkup(row_width=2)
        for genre in ['Комедия', 'Драма', 'Фантастика', 'Боевик', 'Ужасы', 'Мелодрама']:
            markup.add(types.InlineKeyboardButton(genre, callback_data=f"filter_genre_{genre}"))
        bot.send_message(chat_id, "Выберите жанр:", reply_markup=markup)

    elif message.text == 'По году':
        state['current_step'] = 'year'
        bot.send_message(chat_id, "Введите год выпуска (например, 2020):")

    elif message.text == 'По рейтингу':
        state['current_step'] = 'rating'
        bot.send_message(chat_id, "Введите минимальный рейтинг (от 0 до 10):")

    elif message.text == 'По длительности':
        state['current_step'] = 'runtime'
        bot.send_message(chat_id, "Введите минимальную длительность в минутах:")

    elif message.text == 'По режиссеру':
        state['current_step'] = 'director'
        bot.send_message(chat_id, "Введите имя режиссера (например, Квентин Тарантино):")

    elif message.text == 'По актеру':
        state['current_step'] = 'actor'
        bot.send_message(chat_id, "Введите имя актера (например, Леонардо ДиКаприо):")

    elif message.text == 'Найти!':
        if not state['filters']:
            bot.send_message(chat_id, "Сначала выберите хотя бы один критерий поиска!")
            return

        results = []
        if 'director' in state['filters']:
            results = find_movies_by_person(state['filters']['director'], 'director')
        elif 'actor' in state['filters']:
            results = find_movies_by_person(state['filters']['actor'], 'actor')
        else:
            results = find_movies(state['filters'])

        if not results:
            bot.send_message(chat_id, "По вашему запросу ничего не найдено, попробуйте еще раз")
        else:
            response = "Найденные фильмы:\n\n"
            for item in results:
                try:
                    title, year, rating, genres, runtime = item
                    response += f"<b>{title}</b> ({year})\n {rating} |  {runtime} мин\nЖанры: {genres}\n\n"
                except (ValueError, TypeError) as e:
                    print(f"Ошибка обработки элемента: {item}. Ошибка: {e}")
                    continue

            bot.send_message(chat_id, response, parse_mode="HTML")

        user_states.pop(chat_id, None)
        start(message)


@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get('mode') == 'book')
def handle_book_filter(message):
    chat_id = message.chat.id
    state = user_states[chat_id]

    if message.text == '↩️ Назад':
        user_states.pop(chat_id, None)
        start(message)
        return

    if message.text == 'По жанру':
        state['current_step'] = 'genre'
        markup = types.InlineKeyboardMarkup(row_width=2)
        for genre in ['Фантастика', 'Фэнтези', 'Детектив', 'Роман', 'Научная литература']:
            markup.add(types.InlineKeyboardButton(genre, callback_data=f"filter_genre_{genre}"))
        bot.send_message(chat_id, "Выберите жанр:", reply_markup=markup)

    elif message.text == 'По автору':
        state['current_step'] = 'author'
        bot.send_message(chat_id, "Введите имя автора (например, Стивен Кинг):")

    elif message.text == 'Найти!':
        if not state['filters']:
            bot.send_message(chat_id, "Сначала выберите хотя бы один критерий поиска!")
            return

        results = []
        if 'author' in state['filters']:
            results = find_books_by_author(state['filters']['author'])
        else:
            results = find_books_by_genre(state['filters']['genre'])

        if not results:
            bot.send_message(chat_id, "По вашему запросу ничего не найдено, попробуйте еще раз")
        else:
            response = "Найденные книги:\n\n"
            for title, author, year, rating in results:
                response += f"<b>{title}</b>\n"
                response += f" {author} |  {year}\n"
                response += f" {rating}\n\n"

            bot.send_message(chat_id, response, parse_mode="HTML")

        user_states.pop(chat_id, None)
        start(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('filter_'))
def handle_callback(call):
    chat_id = call.message.chat.id
    if chat_id not in user_states:
        return

    _, filter_type, value = call.data.split('_', 2)
    user_states[chat_id]['filters'][filter_type] = value

    bot.edit_message_text(
        f"Вы выбрали: {value}",
        chat_id=chat_id,
        message_id=call.message.message_id
    )

    if user_states[chat_id]['mode'] == 'movie':
        show_movie_filters(chat_id)
    else:
        show_book_filters(chat_id)


@bot.message_handler(func=lambda m: True)
def handle_text(message):
    chat_id = message.chat.id
    if chat_id not in user_states:
        bot.send_message(chat_id, "Пожалуйста, начните с команды /start")
        return

    state = user_states[chat_id]
    if not state.get('current_step'):
        return

    if state['current_step'] in ['year', 'rating', 'runtime']:
        try:
            if state['current_step'] == 'year':
                value = int(message.text)
                if value < 1888 or value > 2100:
                    raise ValueError
            elif state['current_step'] == 'rating':
                value = float(message.text)
                if value < 0 or value > 10:
                    raise ValueError
            elif state['current_step'] == 'runtime':
                value = int(message.text)

            state['filters'][state['current_step']] = value
            state['current_step'] = None

            if state['mode'] == 'movie':
                show_movie_filters(chat_id)
            else:
                show_book_filters(chat_id)

        except ValueError:
            bot.send_message(chat_id, "Пожалуйста, введите корректное значение!")

    elif state['current_step'] in ['director', 'actor', 'author']:
        state['filters'][state['current_step']] = message.text
        state['current_step'] = None


        if state['mode'] == 'movie':
            show_movie_filters(chat_id)
        else:
            show_book_filters(chat_id)

bot.polling(none_stop=True)