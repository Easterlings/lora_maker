from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv()

# GroundingDINO config and checkpoint path
GROUNDING_DINO_CONFIG_PATH = os.getenv('GROUNDING_DINO_CONFIG_PATH')
GROUNDING_DINO_CHECKPOINT_PATH = os.getenv('GROUNDING_DINO_CHECKPOINT_PATH')

SOURCE_IMAGE_PATH = os.getenv('SOURCE_IMAGE_PATH')
RESULT_IMAGE_PATH = os.getenv('RESULT_IMAGE_PATH')
TRAIN_RESOURCES_PATH = os.getenv('TRAIN_RESOURCES_PATH')

# GroundingDINO class and threshold parameter config
CLASSES = ["head"] 
BOX_THRESHOLD = 0.10
TEXT_THRESHOLD = 0.35
NMS_THRESHOLD = 0.5

# LORA_SCRIPT config
LORA_SCRIPT_PATH = os.getenv('LORA_SCRIPT_PATH')
LORA_SCRIPT_TRAIN_PATH = os.getenv('LORA_SCRIPT_TRAIN_PATH')

# SD_LORA_MODEL_DIR
SD_LORA_MODEL_DIR = os.getenv('SD_LORA_MODEL_DIR')