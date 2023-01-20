from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request,redirect


# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

#dbオブジェクトのModelというクラスを継承する
class Post(db.Model):
    #多分dbオブジェクトのColumnクラスに引数を渡してそれぞれインスタンス化している
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    
@app.route("/",methods = ["GET","POST"])
def index():
    if request.method == "GET":
        #Postクラスのデータをすべて取ってくる
        posts = Post.query.all()
        #新たに追加された情報を含むpostsという変数をindex.htmlに渡す
        return render_template("index.html", posts = posts)

@app.route("/form", methods=["GET", "POST"])
def create():
    #requestオブジェクトのmethodという属性がPOSTだったら、
    #form.htmlのページから送られてきた情報の名前の属性が"title"と"body"という
    #ものをtitle,bodyにそれぞれ代入する
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        
        #postとしてインスタンス化する
        post = Post(title = title, body = body)
        
        #db.session.addでdbオブジェクトに追加して、
        #db.session.commitで保存する
        db.session.add(post)
        db.session.commit()
        #元のページに戻る
        return redirect("/")
        
    elif request.method == "GET":
        return render_template("form.html")

@app.route("/<int:id>/update", methods=["GET", "POST"])
def update(id):
    post = Post.query.get(id)
    if request.method == "GET":
        return render_template("update.html",post = post)
    
    elif request.method == "POST":
        post.title = request.form.get("title")
        post.body = request.form.get("body")
    
        db.session.commit()
        return redirect("/")

@app.route("/<int:id>/delete", methods=["GET"])
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")