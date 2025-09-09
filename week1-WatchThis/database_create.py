import psycopg2
from psycopg2 import sql
import pandas as pd
import numpy as np
from pgvector.psycopg2 import register_vector

def db_connect():
    try:
        conn = psycopg2.connect(
            dbname="***", 
            user="***", 
            password="***", 
            host="localhost",  
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SET CLIENT_ENCODING TO 'UTF8';")
        conn.commit()
        print("Database connected successfully!")
        return conn,cur
    except Exception as e:
        conn.rollback()
        print("Unexpected error occured while connecting:", e)
        return None, None

def db_init(conn,cur):
    try:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        register_vector(conn)
        conn.commit()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id SERIAL PRIMARY KEY,
                title TEXT,
                plot TEXT,
                genres TEXT,
                movie_cast TEXT,
                fullplot TEXT,
                countries TEXT,
                directors TEXT,
                rated TEXT,
                lastupdated TEXT,
                type TEXT,
                runtime TEXT,
                released BIGINT,
                awards_wins INT,
                awards_nominations INT,
                year INT,
                poster TEXT,
                languages TEXT,
                writers TEXT,
                merged_rating TEXT,
                merged_plot TEXT,
                embeddings VECTOR(384)
            );
        """)
        conn.commit()
        print("Table 'movies' created successfully!")
    except Exception as e:
        conn.rollback()
        print("Unexpected error occured while Setting Up the Database:", e)
        return None, None

def db_load(conn, cur, path):
    print('Loading data...')
    insert_query = """
        INSERT INTO movies (
            title, plot, genres, movie_cast, fullplot, countries, directors, rated, lastupdated, 
            type, runtime, released, awards_wins, awards_nominations, year, poster, languages, writers, 
            merged_rating, merged_plot, embeddings
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    df = pd.read_parquet(path)

    df['embeddings'] = (
        df['embeddings']
        .astype(str)
        .str.replace('[', '', regex=False)
        .str.replace(']', '', regex=False)
        .str.replace('\n', '', regex=False)
        .str.split()
        .apply(lambda x: [float(val) for val in x] if x else [])
    )

    df = df[df['embeddings'].apply(bool)]

    fill_defaults = {
        'title': 'Unknown Title', 'plot': 'No plot available', 'genres': 'Unknown',
        'cast': 'Unknown', 'fullplot': 'No full plot available', 'countries': 'Unknown',
        'directors': 'Unknown', 'rated': 'Unrated', 'lastupdated': 'Unknown',
        'type': 'Unknown', 'poster': 'No poster available', 'languages': 'Unknown',
        'writers': 'Unknown', 'merged_rating': 'Unknown', 'merged_plot': 'No plot available'
    }

    for col, default in fill_defaults.items():
        if col in df.columns:
            df.fillna({col: default}, inplace=True)

    int_cols = ['runtime.$numberInt', 'awards.wins.$numberInt', 'awards.nominations.$numberInt', 'year.$numberInt']
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    date_cols = ['released.$date.$numberLong']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    df.rename(columns={'cast': 'movie_cast'}, inplace=True)

    data_to_insert = [
        tuple(row) for row in df[
            ['title', 'plot', 'genres', 'movie_cast', 'fullplot', 'countries', 'directors', 
             'rated', 'lastupdated', 'type', 'runtime.$numberInt', 'released.$date.$numberLong', 
             'awards.wins.$numberInt', 'awards.nominations.$numberInt', 'year.$numberInt', 'poster', 
             'languages', 'writers', 'merged_rating', 'merged_plot', 'embeddings']
        ].values
    ]

    try:
        cur.executemany(insert_query, data_to_insert)
        conn.commit()
        print(f"{len(data_to_insert)} rows inserted successfully!")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()

    try:
        cur.execute("CREATE INDEX ON movies USING ivfflat (embeddings);")
        conn.commit()
        print("Index created successfully!")
    except Exception as e:
        print(f"Error creating index: {e}")