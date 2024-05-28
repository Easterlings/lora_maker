#TODO 从数据库读取未训练任务，获取其文件路径及其它参数，跑face_only
from models import db, train_tasks
from app import app
from copy_face import face_only
import os 
import subprocess
from config.system import TRAIN_RESOURCES_PATH, LORA_SCRIPT_PATH, SD_LORA_MODEL_DIR, LORA_SCRIPT_TRAIN_PATH
import shutil


def clear_train_dir():
    assert len(TRAIN_RESOURCES_PATH.split("/")) > 2
    for root, dirs, files in os.walk(TRAIN_RESOURCES_PATH, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))


def set_config(lora_name):
    print("setting config...")
    # 设置参数
    with open(LORA_SCRIPT_TRAIN_PATH, 'r') as file:
        script_content = file.readlines()

    # 遍历文件内容,并修改需要更改的参数
    for i, line in enumerate(script_content):
        if line.startswith('output_name='):
            script_content[i] = f'output_name="{lora_name}"     # output model name | 模型保存名称\n'
            break
    # 将修改后的内容写回文件
    with open(LORA_SCRIPT_TRAIN_PATH, 'w') as file:
        file.writelines(script_content)
    print("setting config finished")


def train(task):
    set_config(task.lora_name)
    run_script_cmd = f'bash {LORA_SCRIPT_TRAIN_PATH}'
    subprocess.run(run_script_cmd, shell=True, check=True)
    return True

def move_to_sd_dir(task):
    name = task.lora_name
    source_file = os.path.join(LORA_SCRIPT_PATH, f"output/{name}.safetensors")
    print("source_file:",source_file)
    os.makedirs(SD_LORA_MODEL_DIR, exist_ok=True)

    shutil.move(source_file, SD_LORA_MODEL_DIR)


def main():
    #取任务，训练每一个任务对应的lora
    with app.app_context():
        tasks = db.session.query(train_tasks).filter(train_tasks.trained == 0).all()
        for task in tasks:
            print("==============================")
            clear_train_dir()
            sourceDir = task.img_dir
            for filename in os.listdir(sourceDir):
                # 检索要训练的元素，保存到两个文件夹
                edgeWidth = 0
                imagesize = (512, 512)
                face_only(sourceDir, filename, edgeWidth, imagesize)
            train_dir = "10_" + sourceDir.split("/")[-1]
            train_path = os.path.join(TRAIN_RESOURCES_PATH, train_dir)
            if not os.path.exists(train_path):
                return 

            result = train(task)
            if(result):
                task.trained = 1
                db.session.commit()
            else:
                pass

            move_to_sd_dir(task)

    


if __name__ == '__main__':
    main()