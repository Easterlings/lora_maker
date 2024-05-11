from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped

db = SQLAlchemy()

class train_tasks(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    img_dir = db.Column(db.String(128), unique=True, nullable=True)
    trained = db.Column(db.Integer, unique=True, nullable=False)
    user = db.Column(db.Integer, unique=True, nullable=True)
    lora_name = db.Column(db.String(32), unique=True, nullable=False)
    img_num = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, img_dir, lora_name, img_num):
        self.img_dir = img_dir
        self.trained = 0
        self.lora_name = lora_name
        self.img_num = img_num