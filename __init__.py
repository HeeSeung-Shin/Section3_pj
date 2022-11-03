from flask import Flask, render_template
import pandas as pd
import sqlite3

# serve=pd.read_csv('serve.csv',index_col=0)
# genre_keywords=pd.read_csv('genre_keywords.csv',index_col=0)

# app=Flask(__name__)

# @app.route('/')
# def hoem():
#     genre_list = sorted(list(genre_keywords['genre']))
#     return render_template('home.html',genre_list =genre_list)


# @app.route(f'/search/<genre>',defaults={'keyword':''})
# @app.route(f'/search/<genre>/<keyword>')
# def movie_refer(genre,keyword):
#     genre_list = pd.read_csv('genre_keywords.csv',index_col=0)
#     keywords_list=sorted(list(genre_keywords[genre_keywords['genre']==gerne]['keywords']))
    
#     if (bool(genre) ==True) and (bool(keyword) == False):
#         result = serve[['title', 'image', 'pubDate', 'director', 'actor', 'genre', 'nation', 'pos_per', 'pos_key', 'neg_key']]
#         result[reulst['genre']==genre].sort_values('pos_per',ascending=False).iloc[:20]
        
    
#     elif (bool(genre) ==True) and (bool(keyword) == True):
#         result = serve[['title', 'image', 'pubDate', 'director', 'actor', 'genre', 'nation', 'pos_per', 'pos_key', 'neg_key']]
#         result[(reulst['genre']==genre)& (reulst['pos_key']).str.contains(keyword)].sort_values('pos_per',ascending=False).iloc[:20]

        
        
    
#     return render_template('service.html',genre_list=genre_list, keywords_list=keywords_list, genre=genre,keyword=keyword,
#         title_list=list(result['title']),image_list=list(result['image']),date_list=list(result['pubDate']),movie_genre_list=list(result['genre']),
#         director_list=list(result['director']), actor_list=list(result['actor']),nation_list=list(result['nation']),pos_list=list(100*result['pos_per'].apply(lambda x: round(x,2))),
#         posk_list=list(result['pos_key']),negk_list=list(result['neg_key']), length= len(result))

# if __name__ == '__main__':
#     app.run(debug = True)


conn = sqlite3.connect('web_service.db',check_same_thread=False)
cur = conn.cursor()



app=Flask(__name__)

@app.route('/')
def hoem():
    genre_list = sorted([genre[0] for genre in cur.execute('select genre from genre_keywords').fetchall()])
    return render_template('home.html',genre_list =genre_list)


@app.route(f'/search/<genre>',defaults={'keyword':''})
@app.route(f'/search/<genre>/<keyword>')
def movie_refer(genre,keyword):
    genre_list = sorted([genre[0] for genre in cur.execute('select genre from genre_keywords').fetchall()])
    keywords_list=sorted(cur.execute(f'''select keywords
                from genre_keywords
                where genre == "{genre}"
                    ''').fetchall()[0][0].split(','))
    
    if (bool(genre) ==True) and (bool(keyword) == False):
        query = cur.execute(f'''select title, image, pubDate,director, actor, genre, nation, pos_per, pos_key, neg_key
        from serve
        Where genre="{genre}" 
        ORDER BY pos_per Desc
        Limit 20
        ''')
        cols = [column[0] for column in query.description]
        result = pd.DataFrame(data = query.fetchall(), columns=cols)

        
    
    elif (bool(genre) ==True) and (bool(keyword) == True):
        
        query = cur.execute(f'''select title, image, pubDate,director, actor, genre, nation, pos_per, pos_key, neg_key
        from serve
        Where genre="{genre}" and pos_key LIKE "%{keyword}%"
        ORDER BY pos_per Desc
        Limit 20
        ''')
        cols = [column[0] for column in query.description]
        result = pd.DataFrame(data = query.fetchall(), columns=cols)
        
    
    return render_template('service.html',genre_list=genre_list, keywords_list=keywords_list, genre=genre,keyword=keyword,
        title_list=list(result['title']),image_list=list(result['image']),date_list=list(result['pubDate']),movie_genre_list=list(result['genre']),
        director_list=list(result['director']), actor_list=list(result['actor']),nation_list=list(result['nation']),pos_list=list(100*result['pos_per'].apply(lambda x: round(x,2))),
        posk_list=list(result['pos_key']),negk_list=list(result['neg_key']), length= len(result))


if __name__ == '__main__':
    app.run(debug = True)