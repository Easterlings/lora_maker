class Config(object):
    DEBUG = True
    PORT = 9898
    UPLOAD_FOLDER = 'images'  # 替换为你想要保存图片的路径
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@192.168.200.193/make_lora'  # 替换为你的数据库 URI