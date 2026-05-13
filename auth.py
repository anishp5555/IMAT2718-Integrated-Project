import hashlib
from database import get_db

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(full_name, email, password):
    db = get_db()
    try:
        hashed = hash_password(password)
        db.execute(
            'INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)',
            (full_name, email, hashed)
        )
        db.commit()
        return 'success'
    except:
        return 'error'
    finally:
        db.close()

def login_user(email, password):
    db = get_db()
    hashed = hash_password(password)
    user = db.execute(
        'SELECT * FROM users WHERE email = ? AND password = ?',
        (email, hashed)
    ).fetchone()
    db.close()
    return user