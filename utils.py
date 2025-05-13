import sqlite3

def get_db_connection():
    conn = sqlite3.connect("truyen/truyen.db")
    conn.row_factory = sqlite3.Row  
    return conn

def get_article(news_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT title, content, image_url FROM truyen WHERE id = ?", (news_id,))
    article = cursor.fetchone()
    
    conn.close()
    return article

def get_prev_article(news_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title FROM truyen WHERE id < ? ORDER BY id DESC LIMIT 1", (news_id,))
    prev_article = cursor.fetchone()
    
    conn.close()
    return prev_article

def get_next_article(news_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title FROM truyen WHERE id > ? ORDER BY id ASC LIMIT 1", (news_id,))
    next_article = cursor.fetchone()
    
    conn.close()
    return next_article

def get_random_stories(news_id, limit=3):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, image_url FROM truyen WHERE id != ? ORDER BY RANDOM() LIMIT ?", 
                  (news_id, limit))
    random_stories = cursor.fetchall()
    
    conn.close()
    return random_stories

def get_total_news(keyword=""):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if keyword:
        cursor.execute("SELECT COUNT(*) FROM truyen WHERE title LIKE ? OR title LIKE ?", 
                      ('%' + keyword + '%', '%' + keyword + '%'))
    else:
        cursor.execute("SELECT COUNT(*) FROM truyen")
    
    total_news = cursor.fetchone()[0]
    
    conn.close()
    return total_news

def get_total_newstl(the_loai=""):
    conn = get_db_connection()
    cursor = conn.cursor()

    if the_loai:
        cursor.execute("SELECT COUNT(*) FROM truyen WHERE the_loai = ?", (the_loai,))
    else:
        cursor.execute("SELECT COUNT(*) FROM truyen")

    total = cursor.fetchone()[0]
    conn.close()
    return total



def get_news_list(keyword="", limit=10, offset=0):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if keyword:
        cursor.execute("""SELECT id, title, content, image_url, url
                          FROM truyen
                          WHERE title LIKE ? OR title LIKE ?
                          ORDER BY id DESC
                          LIMIT ? OFFSET ?""", 
                      ('%' + keyword + '%', '%' + keyword + '%', limit, offset))
    else:
        cursor.execute("""SELECT id, title, content, image_url, url
                          FROM truyen
                          ORDER BY id DESC
                          LIMIT ? OFFSET ?""", 
                      (limit, offset))
    
    news_list = cursor.fetchall()
    
    conn.close()
    return news_list

def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT the_loai, image_url FROM truyen GROUP BY the_loai")  
    categories = cursor.fetchall() 
    
    conn.close()
    return categories


def get_news_listtl(the_loai="", limit=10, offset=0):
    conn = get_db_connection()
    cursor = conn.cursor()

    if the_loai:
        cursor.execute("""SELECT id, title, content, image_url, url 
                          FROM truyen 
                          WHERE the_loai = ? 
                          ORDER BY id DESC 
                          LIMIT ? OFFSET ?""", 
                       (the_loai, limit, offset))
    else:
        cursor.execute("""SELECT id, title, content, image_url, url 
                          FROM truyen 
                          ORDER BY id DESC 
                          LIMIT ? OFFSET ?""", 
                       (limit, offset))

    news_list = cursor.fetchall()
    conn.close()
    return news_list

def getuser(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def like(id_user, id_story):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM like WHERE id_user = ? AND id_story = ?", (id_user, id_story))
    result = cursor.fetchone()

    if result[0] == 0:
        cursor.execute("INSERT INTO like (id_user, id_story) VALUES (?, ?)", (id_user, id_story))
    else:
        cursor.execute("DELETE FROM like WHERE id_user = ? AND id_story = ?", (id_user, id_story))

    conn.commit()
    conn.close()

def is_liked(id_user, id_story):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM like WHERE id_user = ? AND id_story = ?", (id_user, id_story))
    liked = cursor.fetchone() is not None
    conn.close()
    return liked

def get_top(limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT truyen.title, truyen.image_url, COUNT(like.id_story) AS total_likes,truyen.id
    FROM truyen
    JOIN like ON truyen.id = like.id_story
    GROUP BY truyen.id
    ORDER BY total_likes DESC
    LIMIT ?;
    """
    cursor.execute(query, (limit,))
    results = cursor.fetchall()

    conn.close()

    top_like = [
        {"title": row[0], "image_url": row[1], "countlike": row[2], "id": row[3], }
        for row in results
    ]
    return top_like

def get_liked_user(id_user):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT like.idlike, like.id_user, truyen.title,truyen.image_url,truyen.the_loai,truyen.id
        FROM like
        JOIN truyen ON truyen.id = like.id_story
        WHERE like.id_user = ?
    """
    cursor.execute(query, (id_user,))
    results = cursor.fetchall()

    conn.close()

    liked_stories = [
        {"idlike": row[0], "id_user": row[1], "title": row[2], "image_url": row[3], "the_loai": row[4], "id": row[5]}
        for row in results
    ]
    
    return liked_stories







