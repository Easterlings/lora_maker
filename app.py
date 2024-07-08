from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from common.models import db, train_tasks
import os
import time
from functools import wraps
from config.system import VALSUN_SSO_SYSTEM_NAME,UPLOAD_FOLDER,SQLALCHEMY_DATABASE_URI
from common.valsun_sso import Sso
from flask_session import Session
from sqlalchemy.sql import func
import logging

# 设置日志级别和格式
logging.basicConfig(filename='logging.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
app.secret_key = ""
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def response(code:int,data={},msg=""):
    res = {
        "code":code,
        "data":data,
        "message":msg
    }
    return jsonify(res), code

def check_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        sso = Sso(VALSUN_SSO_SYSTEM_NAME)
        sso_login = sso.check_login()
        if not sso_login:
            if "/api/" in request.url:
                return response(403,{"login_url":sso.get_sso_url()},"请登录")
            else:
                return redirect(sso.get_sso_url())
        return f(*args, **kwargs)
    return decorated_function

@app.route('/upload', methods=['POST'])
@check_login
def upload_file():
    user_info = Sso.get_user_info()
    files = request.files.getlist('file[]')
    timestamp = time.time()
    files_path = os.path.join(UPLOAD_FOLDER, str(timestamp))
    if not os.path.exists(files_path):
        os.makedirs(files_path)

    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(files_path, filename))

    task = train_tasks(
        img_dir = files_path,
        lora_name = request.form['lora_name'],
        network_dim = request.form['network_dim'] if request.form['network_dim'] else 128,
        network_alpha = request.form['network_alpha'] if request.form['network_alpha'] else 64,
        resolution = request.form['resolution'] if request.form['resolution'] else "512,512",
        batch_size = request.form['batch_size'] if request.form['batch_size'] else 2,
        max_train_epoches = request.form['max_train_epoches'] if request.form['max_train_epoches'] else 20,
        save_every_n_epochs = request.form['save_every_n_epochs'] if request.form['save_every_n_epochs'] else 2,
        lr = request.form['lr'] if request.form['lr'] else "5e-5",
        unet_lr = request.form['unet_lr'] if request.form['unet_lr'] else "5e-5",
        text_encoder_lr = request.form['text_encoder_lr'] if request.form['text_encoder_lr'] else "1e-5",
        job_no = user_info['job_no'],
        theme = request.form['theme'],
        img_num = len(files),
        created_at = func.now(),
        updated_at = func.now()
    )

    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
@check_login
def delete_task():
    user_info = Sso.get_user_info()
    job_no = user_info['job_no']
    id = request.form['id']
    task = db.session.execute(db.select(train_tasks)
                              .filter(train_tasks.job_no == job_no)
                              .filter(train_tasks.id == id)).scalar_one()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/')
@check_login
def home():
    user_info = Sso.get_user_info()
    job_no = user_info['job_no']
    tasks = db.session.query(train_tasks).filter(train_tasks.job_no == job_no).all()
    return render_template('index.html', tasks = tasks)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)