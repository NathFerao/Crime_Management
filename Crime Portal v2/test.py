from flask import Flask, render_template, request, redirect, url_for,session,request
from flask import redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Hardcoded login credentials
LOGIN_USERNAME = 'admin'
LOGIN_PASSWORD = 'password'

# SQLite database connection
conn = sqlite3.connect('attendance.db', check_same_thread=False)
c = conn.cursor()

@app.route('/')
def home():
    if 'username' not in session:
        # User is not logged in, redirect to login
        return redirect(url_for('login'))
    return render_template('index.html', subject_data=subject_data)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        # User is already logged in, redirect to home
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
            # Authentication successful, store username in session
            session['username'] = username
            return redirect(url_for('home'))
        else:
            # Invalid credentials, show error message
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the user's session
    session.clear()
    return redirect(url_for('login'))



@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']

        # Insert the student into the database
        c.execute("INSERT INTO students (name, roll_no) VALUES (?, ?)", (name, roll_no))
        conn.commit()

        return redirect(url_for('students_list'))
    
    return render_template('add_student.html')

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    if request.method == 'POST':
        subject = request.form['subject']
        date = request.form['date']
        students = request.form.getlist('students')

        for student_id in students:
            status = request.form.get(f'status_{student_id}')
            c.execute("INSERT INTO attendance (student_id, subject, date, status) VALUES (?, ?, ?, ?)",
                      (student_id, subject, date, status))

        conn.commit()
        return redirect(url_for('students_list'))

    # Get all students
    c.execute("SELECT * FROM students")
    students = c.fetchall()

    return render_template('mark_attendance.html', students=students)



@app.route('/students_list')
def students_list():
    # Get all students
    c.execute("SELECT * FROM students")
    students = c.fetchall()

    # Get all subjects
    c.execute("SELECT DISTINCT subject FROM attendance")
    subjects = c.fetchall()

    page_size = 5  # Number of students per page
    num_students = len(students)
    num_pages = num_students // page_size + (num_students % page_size > 0)

    students_data = []
    for student in students:
        student_id = student[0]
        name = student[1]
        roll_no = student[2]

        attendance_data = []
        for subject in subjects:
            subject_name = subject[0]

            # Calculate attendance for each subject
            c.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND subject=? AND status='Present'",
                      (student_id, subject_name))
            present_attendance = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND subject=?",
                      (student_id, subject_name))
            total_attendance = c.fetchone()[0]

            # Calculate attendance percentage
            attendance_percentage = (present_attendance / total_attendance) * 100 if total_attendance != 0 else 0

            attendance_data.append({
                'subject': subject_name,
                'present_attendance': present_attendance,
                'total_attendance': total_attendance,
                'attendance_percentage': round(attendance_percentage, 2)  # Round to 2 decimal places
            })

        students_data.append({
            'name': name,
            'roll_no': roll_no,
            'attendance_data': attendance_data
        })

    return render_template('students_list.html', students=students_data, num_pages=num_pages)



if __name__ == '__main__':
    app.run(debug=True)
