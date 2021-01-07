from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(1000))
    assignto = db.Column(db.String(100))
    asdate = db.Column(db.String(100))
    prior = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    desc = request.form.get("desc")
    asdate = request.form.get("asdate")
    prior = request.form.get("prior")
    assignto = request.form.get("assignto")

    new_todo = Todo(title=title, complete=False, desc=desc , asdate=asdate, prior=prior,assignto=assignto)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))    


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))       


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
