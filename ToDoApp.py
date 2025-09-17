from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date, timedelta

today = date.today()
sunday = today - timedelta(days=today.weekday() + 1 if today.weekday() != 6 else 0)

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
    done = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(300))

    def __repr__(self):
        return f"<Task {self.id}: {self.content} on {self.day}>"

@app.route("/")
def index():
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    tasks_by_day = {day: Task.query.filter_by(day=day).all() for day in days}
    return render_template("index.html", tasks_by_day=tasks_by_day, week_sunday=sunday)

@app.route("/add", methods=["POST"])
def add():
    task_content = request.form.get("task")
    task_days = request.form.getlist("days")
    task_description = request.form.get("description")
    if task_content and task_days:
        for day in task_days:
            new_task = Task(content=task_content, day=day, description=task_description)
            db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/mark_done/<int:task_id>")
def mark_done(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = True
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
