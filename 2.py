import telebot
import requests
from telebot import types
import sqlite3
from googletrans import Translator
from transliterate import translit

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

def translation(title):
    translator = Translator()
    str = "'" + title + "'"
    title_ru = translator.translate(str, dest='ru').text
    return title_ru

def translate_person(name):
    parts = name.split()
    tr_parts = []
    for part in parts:
        if part in special_names_directors:
            tr_parts.append(special_names_directors[part])
        elif part in actors_special_names:
            tr_parts.append(actors_special_names[part])
        else:
            tr_parts.append(part)
    return " ".join(tr_parts)


def find_movies_by_person_other(person_name):
    person_name_eng = translate_person(person_name)
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT nconst FROM people WHERE primaryName = ?
        """, (person_name_eng,))
        person_id = cursor.fetchone()
        if not person_id:
            return []
        person_id = person_id[0]

        cursor.execute("""
                SELECT movies.title, ratings.averageRating, principals1.category
                FROM principals1
                LEFT JOIN movies ON principals1.tconst = movies.titleId
                LEFT JOIN ratings ON principals1.tconst = ratings.tconst
                WHERE principals1.nconst = ?
               """, (person_id,))
        results = cursor.fetchall()

        results1 = []
        for title, rating, category in results:
            if title is None:
                title = "Нет названия"
            if rating is None:
                rating = 0.0

            results1.append((title, rating, category))

        #        sorted_results = sorted(results1, key=lambda x: x[2], reverse=True)

        return results1[:15]

    except sqlite3.Error:
        return []

    finally:
        conn.close()


def find_books_by_authors_name(person_name):
    conn = sqlite3.connect('my_database_books.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT title, published_year, average_rating FROM people WHERE authors = ?
            """, (person_name,))
        books = cursor.fetchall()
        result = []
        for title, published_year, average_rating in books:
            title1 = translation(title)
            result.append((title1, published_year, average_rating))

        sorted_results = sorted(result, key=lambda x: x[2], reverse=True)

        return sorted_results[:10]
    except sqlite3.Error:
        return []

    finally:
        conn.close()


def find_books_by_genre(genre):
    conn = sqlite3.connect('my_database_books.db')
    cursor = conn.cursor()
    str = f"%{genre}%"
    try:
        query = "SELECT title, authors, published_year, average_rating  FROM people WHERE categories LIKE ?"
        cursor.execute(query, (str,))
        books = cursor.fetchall()
        result = []
        for title, authors, published_year, average_rating in books:
            title1 = translation(title)
            result.append((title1, authors, published_year, average_rating))

        sorted_results = sorted(result, key=lambda x: x[3], reverse=True)

        return sorted_results[:10]
    except sqlite3.Error:
        return []

    finally:
        conn.close()


def get_books_by_genre(genre):
    books = find_books_by_genre(genre)
    if not books:
        response = 'Ничего не найдено. Проверьте название жанра и попробуйте еще раз.'
    else:
        response = "Вот, что я нашел:\n\n"
        for book in books:
            title, authors, published_year, average_rating = book
            response += f" {title} \n Автор: {authors} \n Год выпуска книги: {published_year} \n Рейтинг: {average_rating}\n\n"

    return response


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
            main_characters = types.KeyboardButton('Жанр')
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
            bot.send_message(chat_id, 'Как зовут актера (имя, фамилия)?')
            user_states[message.chat.id] = 'waiting_for_actors_name'


        elif message.text == 'Автор':
            bot.send_message(chat_id, 'Как зовут автора книги (имя, фамилия)?')
            user_states[message.chat.id] = 'waiting_for_authors_name'

        elif message.text == 'Жанр':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            novel = types.KeyboardButton('Роман')
            fiction = types.KeyboardButton('Беллетристика')
            fantasy = types.KeyboardButton('Фантастика/фентези')
            horror = types.KeyboardButton('Ужасы')
            biography = types.KeyboardButton('Биография')
            poetry = types.KeyboardButton('Поэзия')
            political = types.KeyboardButton('Политическая литература')
            back = types.KeyboardButton('Назад')

            markup.add(novel, fiction, fantasy, horror, biography, poetry, political, back)
            bot.send_message(message.chat.id, 'Какой жанр у искомой книги?'.format(message.from_user), reply_markup=markup)


        elif message.text == 'Беллетристика':
            response = get_books_by_genre('Fiction')
            bot.send_message(message.chat.id, response)

        elif message.text == 'Роман':
            response = get_books_by_genre('A Novel')
            bot.send_message(message.chat.id, response)

        elif message.text == 'Биография':
            response = get_books_by_genre('Biography & Autobiography')
            bot.send_message(message.chat.id, response)

        elif message.text == 'Фантастика/фентези':
            response = get_books_by_genre('Fantasy')
            bot.send_message(message.chat.id, response)

        elif message.text == 'Ужасы':
            response = get_books_by_genre('Horror')
            bot.send_message(message.chat.id, response)

        elif message.text == 'Поэзия':
            response = get_books_by_genre('Poetry')
            bot.send_message(message.chat.id, response)

        elif message.text == 'Политическая литература':
            response = get_books_by_genre('Political Science')
            bot.send_message(message.chat.id, response)


        elif user_states.get(message.chat.id) == 'waiting_for_authors_name':
            authors_name = message.text.strip()
            books = find_books_by_authors_name(authors_name)
            response = "Вот, что я нашел:\n\n"
            for book in books:
                title, published_year, average_rating = book
                response += f" {title} \n Автор: {authors_name} \n Год выпуска книги: {published_year} \n Рейтинг: {average_rating}\n\n"

            bot.send_message(message.chat.id, response)
            user_states[message.chat.id] = None



        elif user_states.get(message.chat.id) == 'waiting_for_director_name':
            director_name = message.text
            movies = find_movies_by_person_other(director_name)
            if not movies:
                bot.send_message(message.chat.id, 'Ничего не найдено. Проверьте имя и попробуйте еще раз.')
            else:
                response = "Вот, что я нашел:\n\n"
                for movie in movies:
                    title, rating, category = movie

                    if category == 'director':
                        response += f" Режиссёр: \n {title} \n Рейтинг: {rating}\n\n"
                    if category == 'producer':
                        response += f" Продюссер: \n {title} \n Рейтинг: {rating}\n\n"

                bot.send_message(message.chat.id, response)
            user_states[message.chat.id] = None

        elif user_states.get(message.chat.id) == 'waiting_for_actors_name':
            actors_name = message.text.strip()
            movies = find_movies_by_person_other(actors_name)
            if not movies:
                bot.send_message(message.chat.id, 'Ничего не найдено. Проверьте имя и попробуйте еще раз.')
            else:
                response1 = "Вот, что я нашел:\n\n"
                for movie in movies:
                    title, rating, category = movie
                    if category == 'actor' or category == 'actress':
                        response1 += f" {title} \n Рейтинг: {rating}\n\n"

                bot.send_message(message.chat.id, response1)
            user_states[message.chat.id] = None


        else:
            bot.send_message(message.chat.id, 'Я не понимаю, что ты хочешь')


bot.polling(none_stop=True, interval=0)
