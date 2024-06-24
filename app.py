from flask import Flask, request, render_template, send_from_directory, jsonify
import os
from main import process_image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)
