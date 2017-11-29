from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def main_page():
  return render_template('main_page.html')

@app.route('/login/')
def login_page():
  return render_template('login_page.html')

@app.route('/register/')
def register_page():
  return 'Register Page :)'

@app.route('/recipe/<recipe_id>')
def recipe_page(recipe_id):
  return 'Recipe page with id : {0}'.format(recipe_id)