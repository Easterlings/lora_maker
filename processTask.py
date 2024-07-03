#从数据库读取未训练任务，获取其文件路径及其它参数，跑get_theme_only，提取训练主体，填写参数，跑训练脚本
from common.models import db, train_tasks
from app import app
from common.copy_face import get_theme_only
import os 
import subprocess
from config.system import TRAIN_RESOURCES_PATH, LORA_SCRIPT_PATH, SD_LORA_MODEL_DIR, LORA_SCRIPT_TRAIN_PATH
import shutil

os.environ['CURL_CA_BUNDLE'] = '' 

def clear_train_dir():
    assert len(TRAIN_RESOURCES_PATH.split("/")) > 2
    for root, dirs, files in os.walk(TRAIN_RESOURCES_PATH, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))


def set_config(task):
    print("setting config...")
    # 设置参数
    with open(LORA_SCRIPT_TRAIN_PATH, 'r') as file:
        script_content = file.readlines()

    # 遍历文件内容,并修改需要更改的参数
    for i, line in enumerate(script_content):
        if line.startswith('output_name='):
            script_content[i] = f'output_name="{task.lora_name}"     # output model name | 模型保存名称\n'
        elif line.startswith('network_dim='):
            script_content[i] = f'network_dim={task.network_dim}                 # network dim | 常用 4~128，不是越大越好\n'
        elif line.startswith('network_alpha='):
            script_content[i] = f'network_alpha={task.network_alpha}               # network alpha | 常用与 network_dim 相同的值或者采用较小的值，如 network_dim的一半 防止下溢。默认值为 1，使用较小的 alpha 需要提升学习率。\n'
        elif line.startswith('resolution='):
            script_content[i] = f'resolution="{task.resolution}"  # image resolution w,h. 图片分辨率，宽,高。支持非正方形，但必须是 64 倍数。\n'
        elif line.startswith('batch_size='):
            script_content[i] = f'batch_size={task.batch_size}      # batch size\n'
        elif line.startswith('max_train_epoches='):
            script_content[i] = f'max_train_epoches={task.max_train_epoches} #max train epoches | 最大训练 epoch\n'
        elif line.startswith('save_every_n_epochs='):
            script_content[i] = f'save_every_n_epochs={task.save_every_n_epochs} # save every n epochs | 每 N 个 epoch 保存一次\n'
        elif line.startswith('lr='):
            script_content[i] = f'lr="{task.lr}"\n'
        elif line.startswith('unet_lr='):
            script_content[i] = f'unet_lr="{task.unet_lr}"\n'
        elif line.startswith('text_encoder_lr='):
            script_content[i] = f'text_encoder_lr="{task.text_encoder_lr}"\n'
            break
    # 将修改后的内容写回文件
    with open(LORA_SCRIPT_TRAIN_PATH, 'w') as file:
        file.writelines(script_content)
    print("setting config finished")


def train():
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
            theme = task.theme
            for filename in os.listdir(sourceDir):
                # 检索要训练的元素，保存到两个文件夹
                edgeWidth = 0
                imagesize = (512, 512)
                get_theme_only(sourceDir, filename, edgeWidth, imagesize, theme)
            train_dir = "10_" + sourceDir.split("/")[-1]
            train_path = os.path.join(TRAIN_RESOURCES_PATH, train_dir)
            if not os.path.exists(train_path):
                return 

            set_config(task)
            result = train()
            if(result):
                task.trained = 1
                db.session.commit()
            else:
                pass

            # move_to_sd_dir(task)

    


if __name__ == '__main__':
    main()