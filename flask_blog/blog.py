from crypt import methods
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_blog.db'
db = SQLAlchemy(app)

class blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    def __repr__(self):
	    return f"{self.title}+{self.author}+{self.body}"


@app.route('/',methods= ['POST', 'GET'])
def blog():
    if request.method == "POST":
        author_info = request.form['blog_author']
        body_info = request.form['blog_body']
        title_info = request.form['blog_title']
        if author_info!="" and title_info!="":
            one_new_blog = blogs(title = title_info,author=author_info,body=body_info)
            try:
                db.session.add(one_new_blog)
                db.session.commit()
                return redirect(url_for('blog'))
            except:
                return f'<h1>There was an issue adding your task</h1>'
        else:
            return render_template('error.html')
    else:
        all_blogs = blogs.query.order_by(blogs.id).all()
        return render_template('home.html',all_blogs = all_blogs)

@app.route('/delete/<int:id>')
def delete(id):
    blogs.query.filter_by(id=id).delete()
    all_blogs = blogs.query.order_by(blogs.id).all()
    for b in all_blogs:
        if b.id > id:
            b.id = b.id-1
    db.session.commit()
    return redirect(url_for('blog'))

@app.route('/blog/<id>')
def the_id(id):
    this_blog = blogs.query.get(id)
    return render_template('blog_detail.html',blog = this_blog)

@app.route('/new-blog')
def new_blog():
    return render_template('new_blog.html')

if __name__ == "__main__":
    app.run(debug=True)
