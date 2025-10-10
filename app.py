from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from functools import wraps
from datetime import date, datetime
from collections import defaultdict
from helpers import apology,login_required, is_strong_password

from models import db,User,MoodProductivity,Expense,Task,Note


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "replace_this_with_a_secure_random_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    Session(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()


    # Mood/Productivity Maps
    MOOD_MAP = {
        1: "Very Bad", 2: "Bad", 3: "Poor", 4: "Below Average", 5: "Neutral",
        6: "Slightly Good", 7: "Good", 8: "Very Good", 9: "Excellent", 10: "Amazing"
    }

    PRODUCTIVITY_MAP = {
        1: "Lazy", 2: "Unfocused", 3: "Distracted", 4: "Below Average", 5: "Average",
        6: "Productive", 7: "Focused", 8: "Very Focused", 9: "Super Productive", 10: "Extremely Productive"
    }

    # Registre&Login routes
    @app.route("/register", methods=["GET", "POST"])
    def register():
        session.clear()
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")

            if not username or not password: 
                return apology("Username and password are required.", 400)
                
            if password != confirmation:
                return apology("Password confirmation does not match.", 400)
            
            if not is_strong_password(password):
                return apology("password must be 8+ chars, include upper/lower, number & special char")

            if User.query.filter_by(username=username).first():
                return apology("Username already taken.", 400)

            user = User(username=username)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            return redirect("/")
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        session.clear()
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session["user_id"] = user.id
                return redirect("/")
            return apology("Invalid username or password.", 400)
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")

    # dashboard route
    @app.route("/")
    @login_required
    def index():
        user_id = session["user_id"]

        # -------------- Tasks ---------------
        tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
        tasks_total = len(tasks)

        # Sort tasks by priority: high/medium/low
        priority_order = {"high": 1, "medium": 2, "low": 3}
        tasks_sorted = sorted(tasks, key=lambda t: priority_order.get(t.priority, 99))

        # ---------------- Expenses ----------------
        expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()
        expenses_total = len(expenses)

        # Group expenses by month for chart
        month_totals = defaultdict(float)
        for expense in expenses:
            month = expense.date.replace(day=1)
            month_totals[month] += float(expense.amount)

        # Prepare chart labels and values
        sorted_months = sorted(month_totals.keys())
        expense_labels = []
        expense_values = []

        if sorted_months:
            for m in sorted_months:
                expense_labels.append(m.strftime("%b %Y"))
                expense_values.append(month_totals[m])
        else:
            expense_labels = ["No Data"]
            expense_values = [0]


        # ---------------- Mood & Productivity ----------------
        mood_today = MoodProductivity.query.filter_by(user_id=user_id, date=date.today()).first()
        if mood_today:
            mood_text = MOOD_MAP.get(mood_today.mood_score)
            productivity_text = PRODUCTIVITY_MAP.get(mood_today.productivity_score)
        else:
            mood_text = "No Data"
            productivity_text = "No Data"

        # ---------------- Notes ----------------
        notes = Note.query.filter_by(user_id=user_id).order_by(Note.date.desc()).all()
        pinned_notes = Note.query.filter_by(user_id=user_id, pinned=True).order_by(Note.date.desc()).all()

        return render_template(
            "index.html",
            tasks_total=tasks_total,
            expenses_total=expenses_total,
            tasks=tasks_sorted,
            expenses=expenses,
            mood_text=mood_text,
            productivity_text=productivity_text,
            notes=notes,
            pinned_notes=pinned_notes,
            expense_labels=expense_labels,
            expense_values=expense_values
        )


    @app.route("/finance/add", methods=["POST"])
    @login_required
    def add_expense():
        user_id = session["user_id"]
        category = request.form.get("category")
        amount = request.form.get("amount")
        description = request.form.get("description")

        if not category or not amount:
            return apology("Category and amount are required.", 400)

        amount_value = float(amount)
        exp = Expense(user_id=user_id, category=category, amount=amount_value, description=description, date=date.today())
        db.session.add(exp)
        db.session.commit()
        return redirect("/")

    @app.route("/mood/add", methods=["POST"])
    @login_required
    def add_mood():
        user_id = session["user_id"]
        mood_score = request.form.get("mood_score")
        productivity_score = request.form.get("productivity_score")
        notes_text = request.form.get("notes")

        mp = MoodProductivity(user_id=user_id,date=date.today(),mood_score=int(mood_score),productivity_score=int(productivity_score),notes=notes_text)
        db.session.add(mp)
        db.session.commit()
        return redirect("/")

    @app.route("/task/add", methods=["POST"])
    @login_required
    def add_task():
        user_id = session["user_id"]
        task_name = request.form.get("task_name")
        deadline_string = request.form.get("deadline")
        status = request.form.get("status") or "pending"
        priority = request.form.get("priority") or "medium"
        deadline = datetime.strptime(deadline_string, "%Y-%m-%d").date()

        task = Task(user_id=user_id,task_name=task_name,deadline=deadline,status=status,priority=priority,created_at=datetime.now())
        db.session.add(task)
        db.session.commit()
        return redirect("/")
    
    @app.route("/task/delete/<int:task_id>", methods=["POST"])
    @login_required
    def delete_task(task_id):
        task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first()

        db.session.delete(task)
        db.session.commit()

        return redirect("/")


    @app.route("/notes/add", methods=["POST"])
    @login_required
    def add_note():
        user_id = session["user_id"]
        category = request.form.get("category")
        content = request.form.get("content")
        pinned = request.form.get("pinned") == "on"

        note = Note(user_id=user_id,category=category,content=content,pinned=pinned,date=date.today())
        db.session.add(note)
        db.session.commit()
        return redirect("/")

    @app.route("/note/delete/<int:note_id>", methods=["POST"])
    @login_required
    def delete_note(note_id):
        note = Note.query.filter_by(id=note_id, user_id=session["user_id"]).first()
        db.session.delete(note)
        db.session.commit()
        return redirect("/")

    # ---------------- Checkbox task Completed ----------------
    @app.route("/task/check/<int:task_id>")
    @login_required
    def check_task(task_id):
        task = Task.query.get(task_id)
        if task and task.user_id == session["user_id"]:
            if task.status != "done" : 
                task.status = "done" 
            else :
                task.status ="pending"
            db.session.commit()
        return redirect("/")
    
    

    return app
