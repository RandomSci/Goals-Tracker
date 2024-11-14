# app/__init__.py
from flask import Flask
from .database import get_db, close_db
from .routes import index, add_task, complete_task

app = Flask(__name__)

# Register routes
app.add_url_rule('/', view_func=index)
app.add_url_rule('/add_task', view_func=add_task, methods=['POST'])
app.add_url_rule('/complete_task/<int:task_id>', view_func=complete_task, methods=['POST'])

# Teardown app context to close database connection
@app.teardown_appcontext
def teardown_db(exception):
    close_db()