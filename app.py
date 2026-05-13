from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, get_db
from auth import signup_user, login_user
import os

app = Flask(__name__)
app.secret_key = 'imat2718_secret_key'

# Initialise the database when app starts
with app.app_context():
    init_db()

# ─── HOME PAGE ───────────────────────────────────────────
@app.route('/')
def index():
    db = get_db()
    courses = db.execute('SELECT * FROM courses').fetchall()
    db.close()
    return render_template('index.html', courses=courses)

# ─── COURSE DETAIL PAGE ──────────────────────────────────
@app.route('/course/<int:course_id>')
def course(course_id):
    db = get_db()
    course = db.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
    modules = db.execute('SELECT * FROM modules WHERE course_id = ?', (course_id,)).fetchall()
    db.close()
    return render_template('course.html', course=course, modules=modules)

# ─── MODULE DETAIL PAGE ──────────────────────────────────
@app.route('/module/<int:module_id>')
def module(module_id):
    db = get_db()
    module = db.execute('SELECT * FROM modules WHERE id = ?', (module_id,)).fetchone()
    db.close()
    return render_template('module.html', module=module)

# ─── SIGN UP ─────────────────────────────────────────────
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        result = signup_user(full_name, email, password)
        if result == 'success':
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email already registered. Try logging in.', 'error')
    return render_template('signup.html')

# ─── LOGIN ───────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = login_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            flash(f"Welcome back, {user['full_name']}!", 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html')

# ─── LOGOUT ──────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# ─── REGISTER FOR A COURSE ───────────────────────────────
@app.route('/register/<int:course_id>', methods=['GET', 'POST'])
def register(course_id):
    if 'user_id' not in session:
        flash('Please log in to register for a course.', 'error')
        return redirect(url_for('login'))
    db = get_db()
    course = db.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
    if request.method == 'POST':
        existing = db.execute(
            'SELECT * FROM enrollments WHERE user_id = ? AND course_id = ?',
            (session['user_id'], course_id)
        ).fetchone()
        if existing:
            flash('You are already enrolled in this course.', 'error')
        else:
            db.execute(
                'INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)',
                (session['user_id'], course_id)
            )
            db.commit()
            flash(f"Successfully registered for {course['name']}!", 'success')
        db.close()
        return redirect(url_for('course', course_id=course_id))
    db.close()
    return render_template('register.html', course=course)

if __name__ == '__main__':
    app.run(debug=True)