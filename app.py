from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, flash, session
import os
from main import process_image  # Assuming process_image function is defined in main.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text  # Import text function from SQLAlchemy

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/graphics_studio'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# Initialize SQLAlchemy and Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Initialize app with db and bcrypt
db.init_app(app)
bcrypt.init_app(app)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

# Routes
@app.route('/')
def index():
    return render_template('index.html', logged_in=session.get('logged_in'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename)

@app.route('/process', methods=['POST'])
def process_file():
    data = request.json
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], data['filename']) if data['filename'] in os.listdir(app.config['UPLOAD_FOLDER']) else os.path.join(app.config['PROCESSED_FOLDER'], data['filename'])
    operation = data['operation']
    value = data['value']
    
    if operation == 'detect_white':
        output_filename = process_image(filepath, operation, value, app.config['PROCESSED_FOLDER'])
    else:
        output_filename = process_image(filepath, operation, value, app.config['PROCESSED_FOLDER'])
    
    return jsonify({'processedImagePath': f"/processed/{output_filename}", 'newProcessedFilename': output_filename})

@app.route('/processed/<filename>')
def get_processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter_by(username=username).first():
        flash('Username already exists.','error')
        return redirect(url_for('index'))
    if User.query.filter_by(email=email).first():
        flash('Email already exists.','error')
        return redirect(url_for('index'))

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()  # Commit changes to the database

    flash('Registration successful. Please log in.','success')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        session['logged_in'] = True
        session['username'] = username
        flash('You have successfully logged in.','success')
        return redirect(url_for('index'))
    else:
        flash('Invalid username or password.','error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have successfully logged out.','success')
    return redirect(url_for('index'))

@app.route('/update-password', methods=['POST'])
def update_password():
    email = request.form.get('email')
    new_password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        flash('Password updated successfully.','success')
    else:
        flash('User not found.','error')

    return redirect(url_for('index'))

@app.route('/delete-account/<int:user_id>', methods=['POST'])
def delete_account(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Account deleted successfully.')
    else:
        flash('User not found.')

    return redirect(url_for('index'))

@app.route('/test-db')
def test_db_connection():
    try:
        result = db.session.execute(text('SELECT 1'))
        if result.scalar() == 1:
            return 'Database connection successful!'
        else:
            return 'Database connection failed.'
    except Exception as e:
        return f'Database connection failed: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
