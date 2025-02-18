import sqlite3
import csv
import sys

csv.field_size_limit(1000000000)

conn = sqlite3.connect('my_database.db')  # Функция connect создает соединение с базой данных SQLite
                                          # и возвращает объект, представляющий ее.
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS people(
   nconst INT PRIMARY KEY,
   primaryName TEXT,
   birthYear INT,
   deathYear INT,
   primaryProfession TEXT,
   knownForTitles TEXT
   );
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS movies(
   titleId INT PRIMARY KEY,
   ordering INT,
   title TEXT,
   region TEXT,
   language TEXT,
   types TEXT,
   attributes TEXT,
   isOriginalTitle INT
   );
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS ratings(
   tconst INT PRIMARY KEY,
   averageRating INT,
   numVotes TEXT
   );
""")
# Функция для заполнения таблицы people из TSV

def fill_people_table(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Пропускаем заголовок
        for row in reader:
            cursor.execute("""
            INSERT OR IGNORE INTO people (nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles)
            VALUES (?, ?, ?, ?, ?, ?)
            """, row)

# Функция для заполнения таблицы movies из TSV
def fill_movies_table(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Пропускаем заголовок
        for row in reader:
            cursor.execute("""
            INSERT OR IGNORE INTO movies (titleId, ordering, title, region, language, types, attributes, isOriginalTitle) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, row) # создаем таблицу, если она еще не была создана

# Функция для заполнения таблицы ratings из TSV
def fill_ratings_table(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Пропускаем заголовок
        for row in reader:
            cursor.execute("""
            INSERT OR IGNORE INTO ratings (tconst, averageRating, numVotes) 
            VALUES (?, ?, ?)
            """, row)


# Заполняем таблицы
fill_people_table('name.basics.tsv')
fill_movies_table('title.akas.tsv')
fill_ratings_table('title.ratings.tsv')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()



