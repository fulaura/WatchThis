# from database_create import db_connect, db_init, db_load
# from database_search import similar_n


# database initialazation
# conn, cur = db_connect()

# if conn and cur:
#     db_init(conn, cur)
#     db_load(conn, cur, './app3_fin/data/database_movies.parquet')

# print("searching for similar movies...")
# #database search
# test="Love of 2 couples"
# results = similar_n(conn, cur, test) #you can specify num of res (n=)
# for result in results:
#     print(f"Similarity: {result[0]}  Title: {result[1]}")
#     print(f"Plot: {result[2]}")
#     print("")
#check database_search.py to add more queries in order to implement window functions etc.



from app import app

if __name__ == '__main__':
    app.run(debug=True)
    
    
