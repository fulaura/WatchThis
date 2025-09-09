from flask import render_template, request
from app import app

import sys
sys.path.append("..")  # Go one level up to access files outside `app/`

from database_search import similar_n
from database_create import db_connect, db_init, db_load
conn, cur = db_connect()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
@app.route('/search', methods=['POST'])
def search():
    user_description = request.form.get('description')
    
    try:
        results = similar_n(conn, cur, user_description)
        res=[]
        for i in results:
            k=round(i[0] * 100, 2)
            result = {
                'title': i[1],
                'description': i[2],
                'similarity': k if k < 100 else 100,
                'query': user_description
            }
            # print(result)
            res.append(result)
        
        return render_template('result.html', movie=res)
        
    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', error="Server error occurred")