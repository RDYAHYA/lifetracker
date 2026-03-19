# LifeTracker  
#### Description:  
"LifeTracker" is a modern and simple web application that helps you organize and track different parts of your daily life — your mood, productivity, expenses, notes, and tasks — all in one place.

It is built with Flask, SQLite, HTML, CSS, and JavaScript.  
This project was created as my final project for CS50x 2025, combining what I’ve learned about backend development, frontend design, and database management.

---

## Overview

I wanted to build something practical that could help me and others stay organized and aware of how each day goes.  
LifeTracker allows users to:

- Create an account and log in securely  
- Track their daily mood and productivity  
- Add and manage tasks with deadlines and priorities  
- Write and pin personal notes  
- Record expenses and visualize them on a chart  
- View all data together in the Life Stats dashboard  

Each feature is connected so users can see their progress and patterns over time.

---

## Main Features

"User Accounts"  
- Register and log in with validation and error handling  
- Secure session management using Flask-Session  

"Mood & Productivity"  
- Log daily mood on a 1–10 scale  
- Add reflection notes  
- Updates appear instantly on the dashboard  

"Tasks"  
- Add tasks with name, deadline, status, and priority  
- Edit or delete tasks anytime  
- Mark completed tasks to track progress  

"Notes"  
- Add notes and pin important ones  
- Pinned notes appear in the summary dashboard  

"Expense Tracker"  
- Add expenses with category, amount, and description  
- View spending through an interactive Chart.js graph  

"Life Stats"  
- See all your data summarized in one place:
  - Average mood
  - Task progress by priority
  - Monthly expenses chart
  - Pinned notes

---

## Design Decisions

I wanted LifeTracker to feel simple, modern, and easy to use.  
- Flask was chosen for its simplicity and flexibility.  
- SQLite was used because it is lightweight and works perfectly for small projects.  
- Bootstrap ensures a clean and responsive design.  
- Chart.js was added to create a dynamic expense chart.  
- The color palette and layout were designed to look modern and friendly.

---

## Project Structure

/lifetracker
│
├── app.py # Main Flask application with routes and logic
├── models.py # Database models
├── helpers.py # Utility functions
├── requirements.txt # Python dependencies
│
├── /instance
│ └── database.db # SQLite database
│
├── /templates # HTML files
│ ├── layout.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ └── apology.html
│
├── /static
│ ├── /css
│ │ └── styles.css
│ ├── /js
│ │ └── main.js
│ └── /images
│ ├── icon.png
│ └── background.png
│
└── README.md # Project documentation

---

## How to Run Locally
      git clone https://github.com/RDYAHYA/lifetracker.git

      cd lifetracker
      pip install -r requirements.txt
      flask run


Then open your browser and go to:  
http://127.0.0.1:5000

---

## Author

Name: RIADI Yahia  
GitHub: RDYAHYA  
Location: Morocco  
Date: October 2025  



