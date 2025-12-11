from datetime import datetime
import pytz

india = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(india)


import random
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
import sqlite3
import os
import uuid
import cv2
import handTracking.handTrackingModule as htm



app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'db/site.db'

# Initialize webcam
camera = cv2.VideoCapture(0)

# Hand Detector initialize
detector = htm.HandDetector(min_detection_confidence=0.85)

# Buffer variables for letter detection
letter_buffer = []
max_buffer_size = 20
last_sign_time = 0
previous_letter = ""
stable_start_time = None
required_hold_time = 0.5

EMAIL_ADDRESS = "rautomkar1630@gmail.com"
EMAIL_PASSWORD = "iwtjobhyvsygiyfu"
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']  # 👈 ye user input hai
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            code = random.randint(100000, 999999)
            session['reset_email'] = email
            session['reset_code'] = str(code)

            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            import smtplib

            # ✅ These should be fixed
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS                    # 👈 Always your Gmail
            msg['To'] = email                              # ✅ Should be user-entered email
            msg['Subject'] = 'Your Password Reset Code'

            body = f'Your password reset code is: {code}'
            msg.attach(MIMEText(body, 'plain'))

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
                server.quit()
                print(f"✅ Code {code} sent to {email}")
                flash("Verification code has been sent to your email.", "success")
                return redirect(url_for('verify_code'))
            except Exception as e:
                print("❌ Email sending failed:", e)
                flash("Failed to send email. Try again.", "danger")
        else:
            flash("Email not found", "danger")
    return render_template('forgot_password.html')


@app.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    if request.method == 'POST':
        input_code = request.form['code']
        if input_code == session.get('reset_code'):
            return redirect(url_for('reset_password'))
        else:
            flash("Invalid code")
    return render_template('verify_code.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['password']
        hashed = generate_password_hash(new_password)

        email = session.get('reset_email')
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
        conn.commit()
        conn.close()

        flash("Password updated successfully.")
        return redirect(url_for('login'))

    return render_template('reset_password.html')
from werkzeug.security import generate_password_hash

def migrate_plain_passwords():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users")
    users = cursor.fetchall()

    updated = 0
    for user in users:
        user_id, password = user
        if not password.startswith("pbkdf2:") and not password.startswith("scrypt:"):
            hashed = generate_password_hash(password)
            cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user_id))
            updated += 1

    conn.commit()
    conn.close()
    print(f"✅ {updated} user(s) updated to hashed passwords.")


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            full_name TEXT, 
            email TEXT, 
            username TEXT UNIQUE, 
            password TEXT
        )
    ''')
   
    # c.execute('''
    #     CREATE TABLE IF NOT EXISTS lessons (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         title TEXT NOT NULL,
    #         description TEXT,
    #         created_by TEXT,
    #         created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    #     )
    # ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS hand_gestures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER,
            letter TEXT,
            image_path TEXT,
            FOREIGN KEY (lesson_id) REFERENCES lessons(id)
        )
    ''')

    # c.execute('''
    #      CREATE TABLE IF NOT EXISTS Recognition_result (
    #          id INTEGER PRIMARY KEY AUTOINCREMENT,
    #          word TEXT,
    #          detected_at DATETIME DEFAULT CURRENT_TIMESTAMP
    #      )
    #  ''')
    c.execute('''
      CREATE TABLE IF NOT EXISTS Recognition_result_old (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          word TEXT,
          detected_at DATETIME
      )
  ''')
#     # ✅ Correct: omit the `id` so SQLite will auto-generate it
#     c.execute('''
#     INSERT INTO Recognition_result (word, detected_at)
#     SELECT word, detected_at FROM Recognition_result_old
# ''')
#     c.execute("ALTER TABLE Recognition_result ADD COLUMN user_id INTEGER")


#     c.execute("DROP TABLE Recognition_result_old")
    



def get_db_connection():
    db_path = os.path.abspath(DATABASE)  # use the DATABASE variable
    print("✅ Using database at:", db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn



def setup_admin_table():
    conn = get_db_connection()
    c = conn.cursor()

    # ✅ Create admin table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # ✅ Check if default admin exists
    c.execute('SELECT COUNT(*) as count FROM admin')
    result = c.fetchone()

    if result['count'] == 0:
        # ✅ Insert default admin
        c.execute('''
            INSERT INTO admin (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', ('Super Admin', 'admin@example.com', 'admin123', 'superadmin'))
        print("✅ Default admin user created.")

    conn.commit()
    conn.close()

# ✅ Call this at app start
setup_admin_table()

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        admin = conn.execute('SELECT admin_id, name, password FROM admin WHERE email = ?', (email,)).fetchone()
        conn.close()

        if admin is not None and admin['password'] == password:
            session['admin_id'] = admin['admin_id']
            session['admin_name'] = admin['name']
            return redirect('/admin/dashboard')
        else:
            flash('Invalid email or password')

    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    return redirect('/')  # ✅ redirects to index.html

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect('/admin/login')

    conn = get_db_connection()
    total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    total_practices = conn.execute('SELECT COUNT(*) FROM Recognition_result_old').fetchone()[0]
    # total_reports = conn.execute('SELECT COUNT(*) FROM Recognition_result').fetchone()[0]  # or another table if you have reports
    conn.close()

    return render_template('admin_dashboard.html', 
                           admin_name=session['admin_name'],
                           total_users=total_users,
                           
                           )

@app.route('/admin/view_reports', methods=['GET'])
def view_reports():
    if 'admin_id' not in session:
        return redirect('/admin/login')

    # Fetch the User List report data
    conn = get_db_connection()
    users = conn.execute('SELECT id, full_name, email, username FROM users').fetchall()

    # Fetch the Recognition Result report data
    Recognition_result = conn.execute('SELECT id, word,user_id, detected_at FROM Recognition_result_old').fetchall()

    conn.close()

    # Pass data to the template
    return render_template('view_reports.html', users=users, recognition_results=Recognition_result)





@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_user')
def user_dashboard():
    return render_template('signup.html')


from werkzeug.security import generate_password_hash  # Make sure this is imported

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check password length
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('signup.html', full_name=full_name, email=email, username=username)

        # ✅ Hash the password before saving
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (full_name, email, username, password) VALUES (?, ?, ?, ?)",
                      (full_name, email, username, hashed_password))
            conn.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Username already exists. Please try again.', 'danger')
            return render_template('signup.html', full_name=full_name, email=email, username=username)
        finally:
            conn.close()

    # If it's a GET request
    return render_template('signup.html')



from werkzeug.security import check_password_hash  # Make sure this is imported

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user:
            hashed_password = user[4]  # Assuming password column is at index 4
            is_active = user[5] if len(user) > 5 else 1  # Optional is_active check

            if check_password_hash(hashed_password, password):
                if is_active == 0:
                    flash('Your account has been deactivated. Please contact admin.', 'danger')
                    return redirect('/login')

                session['user_id'] = user[0]
                session['username'] = user[3]
                return redirect('/dashboard')
            else:
                flash('Invalid password.', 'danger')
        else:
            flash('User not found.', 'danger')

    return render_template('login.html')




@app.route('/admin/users')
def admin_users():
    if 'admin_id' not in session:
        return redirect('/admin/login')

    conn = get_db_connection()
    users = conn.execute('SELECT id AS user_id, full_name AS name, email, username, is_active FROM users').fetchall()
    conn.close()

    return render_template('admin_users.html', users=users)


@app.route('/admin/deactivate_user/<int:user_id>', methods=['POST'])
def deactivate_user(user_id):
    conn = get_db_connection()
    conn.execute('UPDATE users SET is_active = 0 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect('/admin/users')

@app.route('/admin/activate_user/<int:user_id>', methods=['POST'])
def activate_user(user_id):
    conn = get_db_connection()
    conn.execute('UPDATE users SET is_active = 1 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect('/admin/users')

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return redirect('/admin/users')
from werkzeug.security import generate_password_hash  # Make sure this is imported

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    if 'admin_id' not in session:
        return redirect('/admin/login')

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        is_active = request.form.get('is_active') == 'on'  # True if checkbox checked

        # ✅ Hash the password before saving
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('''INSERT INTO users (full_name, email, username, password, is_active) 
                            VALUES (?, ?, ?, ?, ?)''', 
                         (full_name, email, username, hashed_password, is_active))
            conn.commit()
            flash('User added successfully!', 'success')
            return redirect('/admin/users')
        except sqlite3.IntegrityError:
            flash('User with that email or username already exists!', 'danger')
        finally:
            conn.close()

    return render_template('admin_add_user.html')

@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'admin_id' not in session:
        return redirect('/admin/login')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        is_active = request.form.get('is_active') == 'on'  # True if checkbox checked

        conn.execute('''UPDATE users SET full_name = ?, email = ?, username = ?, password = ?, is_active = ? 
                        WHERE id = ?''', 
                     (full_name, email, username, password, is_active, user_id))
        conn.commit()
        conn.close()

        flash('User details updated successfully!', 'success')
        return redirect('/admin/users')

    conn.close()
    return render_template('admin_edit_user.html', user=user)

@app.route('/admin/update_profile', methods=['GET', 'POST'])
def update_admin_profile():
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    admin_id = session['admin_id']
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        if password:
            # If password is provided, update it
            conn.execute('UPDATE admin SET name = ?, email = ?, password = ? WHERE admin_id = ?',
                         (name, email, password, admin_id))
        else:
            # If no password provided, just update name/email
            conn.execute('UPDATE admin SET name = ?, email = ? WHERE admin_id = ?',
                         (name, email, admin_id))
        
        conn.commit()
        conn.close()

        # flash('Admin profile updated successfully!', 'success')
        return redirect('/admin/dashboard')
    
    conn = get_db_connection()
    admin = conn.execute('SELECT * FROM admin WHERE admin_id = ?', (admin_id,)).fetchone()
    conn.close()

    return render_template('admin_update_profile.html', admin=admin)

@app.route('/admin/add_admin', methods=['GET', 'POST'])
def add_admin():
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        try:
            conn.execute('''INSERT INTO admin (name, email, password, role)
                             VALUES (?, ?, ?, ?)''',
                         (name, email, password, role))
            conn.commit()
            flash('New admin added successfully!', 'success')
            return redirect('/admin/dashboard')
        except sqlite3.IntegrityError:
            flash('Admin with this email already exists!', 'danger')
        finally:
            conn.close()

    return render_template('admin_add_admin.html')



@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    
    username = session['username']
    
    if username.startswith('teacher'):
        return redirect('/teacher_dashboard')
    else:
        return render_template('userdash.html', name=username)

# from werkzeug.utils import secure_filename
# from werkzeug.security import generate_password_hash

# UPLOAD_FOLDER = 'static/uploads/'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# # Make sure the upload folder exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    
    # If it's a POST request, update the user's profile
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        if password:  # If a new password is provided
            c.execute('''UPDATE users SET full_name = ?, email = ?, username = ?, password = ? WHERE id = ?''',
                      (full_name, email, username, password, user_id))
        else:  # If no new password is provided, just update the other fields
            c.execute('''UPDATE users SET full_name = ?, email = ?, username = ? WHERE id = ?''',
                      (full_name, email, username, user_id))

        conn.commit()
        conn.close()
        
        flash('Profile updated successfully!', 'success')
        return redirect('/profile')  # Redirect to the profile page after update

    # If it's a GET request, fetch the user's data
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT full_name, email, username FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()

    if user:
        full_name, email, username = user
        return render_template('profile.html', full_name=full_name, email=email, username=username)
    else:
        flash('User not found.', 'danger')
        return redirect('/login')

@app.route('/history')
def user_history():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT word, detected_at FROM Recognition_result_old WHERE user_id = ? ORDER BY detected_at DESC", (user_id,))
    history = c.fetchall()
    conn.close()

    return render_template('history.html', history=history)


@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect('/login')  # Redirect to login if not authenticated

    user_id = session['user_id']

    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''UPDATE users SET full_name = ?, email = ?, username = ? WHERE id = ?''',
                  (full_name, email, username, user_id))
        conn.commit()
        conn.close()

        flash('Profile updated successfully!', 'success')
        return redirect('/profile')

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT full_name, email, username FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()

    if user:
        full_name, email, username = user
        return render_template('update_profile.html', full_name=full_name, email=email, username=username)
    else:
        flash('User not found.', 'danger')
        return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# 👉 Live camera streaming + hand tracking
def generate_frames(user_id):
    global letter_buffer, last_sign_time, previous_letter, stable_start_time
    created_word = ""  # Only store the latest word

    while True:
        success, img = camera.read()
        if not success:
            break
        else:
            img = cv2.flip(img, flipCode=1)
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)

            current_time = cv2.getTickCount() / cv2.getTickFrequency()

            if len(lmList) != 0:
                name = detector.signCondition()

                if name and name != "else":
                    if name.upper() != previous_letter:
                        stable_start_time = current_time
                        previous_letter = name.upper()
                    elif stable_start_time and (current_time - stable_start_time) >= required_hold_time:
                        letter_buffer.append(name.upper())
                        letter_buffer = letter_buffer[-max_buffer_size:]
                        stable_start_time = None
                        last_sign_time = current_time

                # Show current letter buffer on screen
                joined = "".join(letter_buffer)
                cv2.putText(img, f"Text: {joined}", (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)

            else:
                # ➤ Hand removed: store current word and replace old word
                if letter_buffer:
                    joined_word = "".join(letter_buffer)
                    created_word = joined_word  # replace old word
                    print(f"✅ Stored word on hand removal: {joined_word}")

                    # INSERT into SQLite
                    conn = sqlite3.connect(DATABASE)
                    c = conn.cursor()
                    c.execute("INSERT INTO Recognition_result_old (word, user_id) VALUES (?, ?)", (joined_word, user_id))


                    conn.commit()
                    conn.close()
                    print(f"✅ Word '{joined_word}' saved to database.")

                    letter_buffer = []
                    previous_letter = ""
                    stable_start_time = None

            # Show the latest created word
            cv2.putText(img, f"Word: {created_word}", (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 255), 2)

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/sign-detection')
def sign_detection():
    return render_template('sign_detection.html')

@app.route('/video')
def video():
    user_id = session.get('user_id')
    return Response(generate_frames(user_id), mimetype='multipart/x-mixed-replace; boundary=frame')


# 👉 New route to display lesson details
# @app.route('/lesson/<lesson_title>', methods=['GET', 'POST'])
# def view_lesson(lesson_title):
#     conn = sqlite3.connect(DATABASE)
#     c = conn.cursor()
#     c.execute("SELECT id FROM lessons WHERE lower(title) = ?", (lesson_title.lower(),))
#     row = c.fetchone()
#     if row:
#         lesson_id = row[0]
#         c.execute("SELECT letter, image_path FROM lesson_gestures WHERE lesson_id = ?", (lesson_id,))
#         letters = c.fetchall()
#         conn.close()

#         selected_letter = None
#         selected_image = None

#         if request.method == 'POST':
#             selected_letter = request.form.get('letter')
#             for ltr, img in letters:
#                 if ltr == selected_letter:
#                     selected_image = img
#                     break

#         return render_template(
#             'alphabet_lesson.html',
#             title=lesson_title,
#             letters=letters,
#             selected_letter=selected_letter,
#             selected_image=selected_image
#         )
#     else:
#         conn.close()
#         return f"Lesson '{lesson_title}' not found.", 404

@app.route('/feature/realtime-detection')
def realtime_detection():
    return render_template('feature_realtime.html')

@app.route('/feature/rule-based')
def rule_based():
    return render_template('feature_rulebased.html')

@app.route('/feature/mediapipe-opencv')
def mediapipe_opencv():
    return render_template('feature_mediapipe.html')

@app.route('/feature/expandable')
def expandable():
    return render_template('feature_expandable.html')

if __name__ == '__main__':
    if not os.path.exists('db'):
        os.makedirs('db')
    if not os.path.exists(DATABASE):
        init_db()
    else:
        # Always check tables in case of missing new tables
        init_db()
    app.run(debug=True)
