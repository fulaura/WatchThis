import psycopg2
from psycopg2 import sql
from encoder import generate_embedding_local as gel
from pgvector.psycopg2 import register_vector
import numpy as np


def similar_n(conn, cur, text, n=5):
    try:
        text_embedded=gel(text)
        print(text)
        query_embedding = np.array(text_embedded, dtype=np.float32)
        
        query = """
            SELECT embeddings <-> %s::vector AS similarity, title, plot
            FROM movies 
            ORDER BY similarity
            LIMIT 10;
        """
        
        register_vector(conn)
        cur.execute(query, (query_embedding,))
        results = cur.fetchall()

        # for result in results:
        #     print(f"Title: {result}")
            
        conn.commit()
        return results
    except Exception as e:
        print("Unexpected error occured while searching:", e)
        conn.rollback()


    