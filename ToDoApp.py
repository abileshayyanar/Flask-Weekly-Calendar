from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "todo.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    day = db.Column(db.String(10), nullable=False)  # Store day of week

    def __repr__(self):
        return f"<Task {self.id}: {self.content} on {self.day}>"

@app.route("/")
def index():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    tasks_by_day = {day: Task.query.filter_by(day=day).all() for day in days}
    return render_template("index.html", tasks_by_day=tasks_by_day)

@app.route("/add", methods=["POST"])
def add():
    task_content = request.form.get("task")
    task_day = request.form.get("day")
    if task_content and task_day:
        new_task = Task(content=task_content, day=task_day)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the new "day" column if fresh DB
    app.run(debug=True)
