import os
from flask import Flask, render_template, request, redirect, session, url_for,jsonify, flash
from utils import get_article, get_prev_article, get_next_article, get_random_stories, get_news_list, get_total_news,get_total_newstl, get_news_listtl,get_categories,getuser,like,is_liked,get_top,get_liked_user
app = Flask(__name__)
app.secret_key = os.urandom(24)
NEWS_PER_PAGE = 5  


@app.route("/read/<int:news_id>", methods=['GET', 'POST'])
def read(news_id):
    try:
        article = get_article(news_id)
            
        if not article:
            return render_template("error.html", message=" Bài viết không tồn tại.")
            
        title, content, image_url = article
        paragraphs = content.split('\n')
        prev_article = get_prev_article(news_id)
        next_article = get_next_article(news_id)
        random_stories = get_random_stories(news_id)

        id_user = session.get('iduser')
        liked = False
        if request.method == 'POST':
            if id_user:
                like(id_user, news_id)  
                liked = is_liked(id_user, news_id)  
        if id_user:
            liked = is_liked(id_user, news_id)

        return render_template(
            "read.html", 
            title=title, 
            content=content, 
            image_url=image_url,
            paragraphs=paragraphs, 
            prev_article=prev_article, 
            next_article=next_article,
            random_stories=random_stories, 
            session=session,
            liked=liked
        )

    except Exception as e:
        return render_template("error.html", message=f"❌ Lỗi truy vấn CSDL: {str(e)}")

@app.route("/")
def index():
    keyword = request.args.get("q", "")
    page = int(request.args.get("page", 1))

    try:
        total_news = get_total_news(keyword)
        total_pages = (total_news + NEWS_PER_PAGE - 1) // NEWS_PER_PAGE
        offset = (page - 1) * NEWS_PER_PAGE
    
        news_list = get_news_list(keyword, NEWS_PER_PAGE, offset)

        categories = get_categories() 
        top_like = get_top(5) 
        return render_template(
            "index.html", 
            news_list=news_list, 
            keyword=keyword, 
            page=page, 
            total_pages=total_pages,
            total_results=total_news,
            categories=categories,
            top_like=top_like, 
        )
        
    except Exception as e:
        return render_template("error.html", message=f"Lỗi truy vấn CSDL: {str(e)}")

@app.route("/theloai")
def theloai():
    the_loai = request.args.get("the_loai", "")
    page = int(request.args.get("page", 1))

    try:
        total_news = get_total_newstl(the_loai)
        total_pages = (total_news + NEWS_PER_PAGE - 1) // NEWS_PER_PAGE
        offset = (page - 1) * NEWS_PER_PAGE

        news_list = get_news_listtl(the_loai, NEWS_PER_PAGE, offset)
        categories = get_categories()

        return render_template(
            "theloai.html", 
            news_list=news_list,
            the_loai=the_loai,  
            page=page,
            total_pages=total_pages,
            total_results=total_news,
            categories=categories
        )
    
    except Exception as e:
        return render_template("error.html", message=f"Lỗi truy vấn CSDL: {str(e)}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'iduser' in session:
        return redirect(url_for("index"))
    next_link = request.args.get("next", "")
    error_message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = getuser(username, password)
        if user:
            session['iduser'] = user['iduser'] 
            session['username'] = user['username'] 
            return redirect(next_link or url_for("index"))
        else:
            error_message = "Sai tài khoản hoặc mật khẩu."

    return render_template("login.html", error=error_message)
@app.route("/logout")
def logout():
    session.clear()  
    return redirect(url_for("index"))
    

@app.route("/likedstories", methods=["GET", "POST"])
def liked_stories():
    id_user = session.get("iduser")
    if not id_user:
        return render_template("error.html", message="Bạn chưa đăng nhập")

    try:
        if request.method == "POST":
            id_story = request.form.get("id_story")
            if id_story:
                like(id_user, id_story)  

        liked = get_liked_user(id_user) 
        return render_template("liked_stories.html", liked_stories=liked)
    except Exception as e:
        return render_template("error.html", message=str(e))
    
@app.route("/introduce")
def introduce():
    return render_template("introduce.html")

if __name__ == "__main__":  
    app.run(debug=True)       


    


