from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timezone

#Initialize the database 
db = SQLAlchemy()

# USERS class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Password methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Relationships
    moods = db.relationship('MoodProductivity', backref='user', lazy=True)
    expenses = db.relationship('Expense', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)
    notes = db.relationship('Note', backref='user', lazy=True)


# MOOD & PRODUCTIVITY class
class MoodProductivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=date.today)
    mood_score = db.Column(db.Integer) 
    productivity_score = db.Column(db.Integer)  
    notes = db.Column(db.Text)


# FINANCE class
class Expense(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=lambda: date.today()) 
    description = db.Column(db.Text)

# TASKS class
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_name = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default="pending")  
    priority = db.Column(db.String(10), default="medium")  
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

# NOTES class 
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    pinned = db.Column(db.Boolean, default=False)  
    date = db.Column(db.Date, default=date.today)
