from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/videos'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

profile_sheets = []
learning_videos = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():  # Renamed from 'home' to 'index' to match base.html
    return render_template('index.html')

@app.route('/profile_sheet', methods=['GET', 'POST'])
def profile_sheet():
    if request.method == 'POST':
        question = request.form.get('question')
        if 'video' not in request.files:
            return redirect(url_for('profile_sheet'))
        file = request.files['video']
        if file.filename == '':
            return redirect(url_for('profile_sheet'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_sheets.append({'question': question, 'video': f'videos/{filename}'})
        return redirect(url_for('profile_sheet'))
    return render_template('profile_sheet.html', sheets=profile_sheets)

@app.route('/delete_profile_sheet/<int:index>')
def delete_profile_sheet(index):
    if 0 <= index < len(profile_sheets):
        video_path = profile_sheets[index]['video']
        full_path = os.path.join('static', video_path)
        if os.path.exists(full_path):
            os.remove(full_path)
        profile_sheets.pop(index)
    return redirect(url_for('profile_sheet'))

@app.route('/learning', methods=['GET', 'POST'])
def learning():
    if request.method == 'POST':
        topic = request.form.get('topic')
        if 'video' not in request.files:
            return redirect(url_for('learning'))
        file = request.files['video']
        if file.filename == '':
            return redirect(url_for('learning'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            learning_videos.append({'topic': topic, 'video': f'videos/{filename}'})
        return redirect(url_for('learning'))
    return render_template('learning.html', videos=learning_videos)

@app.route('/delete_learning/<int:index>')
def delete_learning(index):
    if 0 <= index < len(learning_videos):
        video_path = learning_videos[index]['video']
        full_path = os.path.join('static', video_path)
        if os.path.exists(full_path):
            os.remove(full_path)
        learning_videos.pop(index)
    return redirect(url_for('learning'))

@app.route('/movie_review')
def movie_review():
    return render_template('movie_review.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Received message from {name} ({email}): {message}")
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)