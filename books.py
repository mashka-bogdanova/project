import pandas as pd
import sqlite3

df = pd.read_csv('data.csv', sep=',', header=None)


df.columns = ['isbn13', 'isbn10', 'title', 'subtitle', 'authors', 'categories', 'thumbnail', 'description', 'published_year', 'average_rating', 'num_pages', 'ratings_count']
df = df.fillna('Unknown')

df = df[df['published_year'].apply(lambda x: str(x).isdigit())] #оставляем строки только с интовым годом выхода


df['isbn13'] = df['isbn13'].astype(str)
df['isbn10'] = df['isbn10'].astype(str)
df['published_year'] = df['published_year'].astype(int)

df['average_rating'] = df['average_rating'].replace('Unknown', None)
df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce')
df['average_rating'] = df['average_rating'].fillna(0)

df['num_pages'] = df['num_pages'].replace('Unknown', None)
df['num_pages'] = pd.to_numeric(df['num_pages'], errors='coerce')
df['num_pages'] = df['num_pages'].fillna(0)

df['ratings_count'] = df['ratings_count'].replace('Unknown', None)
df['ratings_count'] = pd.to_numeric(df['ratings_count'], errors='coerce')
df['ratings_count'] = df['ratings_count'].fillna(0)


conn = sqlite3.connect('my_database_books.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS people (
    isbn13 TEXT PRIMARY KEY,
    isbn10 TEXT,
    title TEXT,
    subtitle TEXT,
    authors TEXT,
    categories TEXT,
    thumbnail TEXT,
    description TEXT,
    published_year INT,
    average_rating REAL,
    num_pages INT,
    ratings_count INT
)
''')

data_to_insert = df.to_records(index=False).tolist()
cursor.executemany('''
INSERT INTO people (isbn13, isbn10, title, subtitle, authors, categories, thumbnail, description, published_year, average_rating, num_pages, ratings_count)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', data_to_insert)

conn.commit()
conn.close()

