from flask import Flask, request, redirect, url_for, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from common.models import db, train_tasks
import os
import time
from functools import wraps
from config.system import VALSUN_SSO_SYSTEM_NAME,THUMBNAIL_PATH,UPLOAD_IMAGE_PATH,SQLALCHEMY_DATABASE_URI
from common.valsun_sso import Sso
from common.image_process_api import rem_bg_request
from utils import base64_to_image
from flask_session import Session
from sqlalchemy.sql import func
import logging
from PIL import Image
import shutil

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
    files_path = os.path.join(UPLOAD_IMAGE_PATH, str(timestamp))
    thumbnail_path = os.path.join(THUMBNAIL_PATH, str(timestamp))
    if not os.path.exists(files_path):
        os.makedirs(files_path)
    if not os.path.exists(thumbnail_path):
        os.makedirs(thumbnail_path)
    for i, file in enumerate(files):
        filename = secure_filename(file.filename)
        original_full_path = os.path.join(files_path, filename)
        if file:
            if('rembg' in request.form):
                resp = rem_bg_request(file)
                no_bg_image_b64 = resp.json()["data"].get('no_bg_image')
                nobg_image = base64_to_image(no_bg_image_b64).convert('RGB')
                nobg_image.save(original_full_path)
            else:
                file.save(original_full_path)
        if i==0:
            with Image.open(original_full_path) as img:
                img.thumbnail((512, 512))  # 这里的(128, 128)是缩略图的大小，可以根据需要调整
                thumbnail_full_path = os.path.join(thumbnail_path, filename)
                img.save(thumbnail_full_path)

    task = train_tasks(
        img_dir = files_path,
        thumbnail = thumbnail_full_path,
        lora_name = request.form['lora_name'],
        network_dim = request.form['network_dim'] if request.form['network_dim'] else 32,
        network_alpha = request.form['network_alpha'] if request.form['network_alpha'] else 32,
        resolution = request.form['resolution'] if request.form['resolution'] else "512,512",
        batch_size = request.form['batch_size'] if request.form['batch_size'] else 1,
        max_train_epoches = request.form['max_train_epoches'] if request.form['max_train_epoches'] else 10,
        save_every_n_epochs = request.form['save_every_n_epochs'] if request.form['save_every_n_epochs'] else 5,
        lr = request.form['lr'] if request.form['lr'] else "1e-4",
        unet_lr = request.form['unet_lr'] if request.form['unet_lr'] else "1e-4",
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
    # 删除上传图和缩略图
    if os.path.exists(task.img_dir):
        shutil.rmtree(task.img_dir)
    if os.path.exists(os.path.dirname(task.thumbnail)):
        shutil.rmtree(os.path.dirname(task.thumbnail))

    # 删除数据库记录
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

@app.route('/images/<path:filename>')
def uploaded_file(filename):
    return send_from_directory("images", filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)