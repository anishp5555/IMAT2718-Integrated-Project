import sqlite3

def get_db():
    conn = sqlite3.connect('college.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            duration TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_code TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            contents TEXT,
            staff_member TEXT,
            course_id INTEGER,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT DEFAULT 'student'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO courses (name, description, duration) VALUES (?, ?, ?)", [
            ('BSc Computer Science', 'A degree covering programming, algorithms, and systems.', '3 Years'),
            ('BSc Business Information Systems', 'Combines business knowledge with IT skills.', '3 Years'),
            ('HND Computing', 'A practical computing qualification.', '2 Years'),
            
        ])
        cursor.executemany("INSERT INTO modules (module_code, title, description, contents, staff_member, course_id) VALUES (?, ?, ?, ?, ?, ?)", [
            ('IMAT1234', 'Introduction to Programming', 'Basics of Python programming.', 'Variables, loops, functions', 'Dr Smith', 1),
            ('IMAT2718', 'Integrated Project', 'Build a full system using agile methods.', 'Flask, SQLite, GitHub', 'Dr Al-Shargabi', 2),
            ('IMAT1101', 'Database Systems', 'Intro to relational databases.', 'SQL, ERDs, Normalisation', 'Dr Jones', 1),
        ])

    conn.commit()
    conn.close()
