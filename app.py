from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from models import db, train_tasks
import os
import time

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('file[]')
    timestamp = time.time()
    files_path = os.path.join(app.config['UPLOAD_FOLDER'], str(timestamp))
    if not os.path.exists(files_path):
        os.makedirs(files_path)

    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(files_path, filename))

    task = train_tasks(
        img_dir = files_path,
        lora_name = request.form['lora_name'],
        img_num = len(files),
    )

    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()