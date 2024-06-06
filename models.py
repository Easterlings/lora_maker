from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped
from datetime import datetime
db = SQLAlchemy()

class train_tasks(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    img_dir: Mapped[str] = db.Column(db.String(128), unique=True, nullable=True)
    trained: Mapped[int] = db.Column(db.Integer, unique=True, nullable=False)
    job_no: Mapped[int] = db.Column(db.Integer, unique=True, nullable=True)
    lora_name: Mapped[str] = db.Column(db.String(32), unique=True, nullable=False)
    theme: Mapped[str] = db.Column(db.String(100), unique=True, nullable=True)
    img_num: Mapped[int] = db.Column(db.Integer, unique=True, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, img_dir, job_no, lora_name, theme, img_num, created_at, updated_at):
        self.img_dir = img_dir
        self.trained = 0
        self.job_no = job_no
        self.lora_name = lora_name
        self.theme = theme
        self.img_num = img_num
        self.created_at = created_at
        self.updated_at = updated_at