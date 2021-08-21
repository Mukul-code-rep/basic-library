from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    return render_template("index.html", books=db.session.query(Book).all())


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(title=request.form["title"],
                        author=request.form["author"],
                        rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit-rating", methods=['GET', 'POST'])
def edit_rating():
    if request.method == 'POST':
        try:
            to_update = Book.query.get(request.form['id'])
        except:
            pass
        else:
            to_update.rating = request.form["new-rating"]
            db.session.commit()
        finally:
            return redirect(url_for('home'))
    book = Book.query.get(request.args.get('id'))
    return render_template("edit-rating.html", book=book)


@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    to_delete = Book.query.get(book_id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, port=5002)
