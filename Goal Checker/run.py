from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # your MySQL username
        password="",  # your MySQL password
        database="roadmap"
    )

# Route to display tasks and handle search by year
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/View_Progress', methods=['GET'])
def index():
    # Get the selected year from the dropdown (default to 2023 if no year selected)
    year = request.args.get('year', type=int)
    
    # Establish database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get all unique years from the database to populate the dropdown
    cursor.execute("SELECT DISTINCT year FROM tasks ORDER BY year ASC")
    years = cursor.fetchall()

    # If year is selected, filter tasks by the selected year
    if year:
        cursor.execute("SELECT * FROM tasks WHERE year = %s ORDER BY task_name", (year,))
    else:
        # If no year is selected, show all tasks
        cursor.execute("SELECT * FROM tasks ORDER BY year ASC, task_name")
    
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('View_Progress.html', tasks=tasks, years=years, selected_year=year)

# Route to create a new task
@app.route('/create_task', methods=['POST'])
def create_task():
    task_name = request.form['task_name']
    status = request.form['status']
    due_date = request.form['due_date']
    priority = request.form['priority']
    year = request.form['year']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO tasks (task_name, status, due_date, priority, year) VALUES (%s, %s, %s, %s, %s)', 
                   (task_name, status, due_date, priority, year))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

# Route to update task status
@app.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    status = request.form['status']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE tasks SET status = %s WHERE id = %s', (status, task_id))
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
