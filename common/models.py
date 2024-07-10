from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped
from datetime import datetime
db = SQLAlchemy()

class train_tasks(db.Model):
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    img_dir: Mapped[str] = db.Column(db.String(128), unique=True, nullable=True)
    thumbnail: Mapped[str] = db.Column(db.String(100), unique=True, nullable=True)
    trained: Mapped[int] = db.Column(db.Integer, unique=True, nullable=False)
    job_no: Mapped[int] = db.Column(db.Integer, unique=True, nullable=True)
    lora_name: Mapped[str] = db.Column(db.String(32), unique=True, nullable=False)
    network_dim: Mapped[int] = db.Column(db.Integer, unique=True, nullable=True)
    network_alpha: Mapped[int] = db.Column(db.Integer, unique=True, nullable=True)
    resolution: Mapped[str] = db.Column(db.String(32), unique=True, nullable=True)
    batch_size: Mapped[int] = db.Column(db.Integer, unique=True, nullable=True)
    max_train_epoches: Mapped[int] = db.Column(db.Integer, unique=True, nullable=True)
    save_every_n_epochs: Mapped[int] = db.Column(db.Integer, unique=True, nullable=True)
    lr: Mapped[str] = db.Column(db.String(32), unique=True, nullable=True)
    unet_lr: Mapped[str] = db.Column(db.String(32), unique=True, nullable=True)
    text_encoder_lr: Mapped[str] = db.Column(db.String(32), unique=True, nullable=True)
    theme: Mapped[str] = db.Column(db.String(100), unique=True, nullable=True)
    img_num: Mapped[int] = db.Column(db.Integer, unique=True, nullable=False)
    created_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at: Mapped[datetime] = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, img_dir, thumbnail, job_no, lora_name, network_dim, network_alpha, resolution, batch_size, 
                 max_train_epoches, save_every_n_epochs, lr, unet_lr, text_encoder_lr, theme, img_num, created_at, updated_at):
        self.img_dir = img_dir
        self.thumbnail = thumbnail
        self.trained = 0
        self.job_no = job_no
        self.lora_name = lora_name
        self.network_dim = network_dim
        self.network_alpha = network_alpha
        self.resolution = resolution
        self.batch_size = batch_size
        self.max_train_epoches = max_train_epoches
        self.save_every_n_epochs = save_every_n_epochs
        self.lr = lr
        self.unet_lr = unet_lr
        self.text_encoder_lr = text_encoder_lr
        self.theme = theme
        self.img_num = img_num
        self.created_at = created_at
        self.updated_at = updated_at