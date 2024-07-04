import base64
from PIL import Image, JpegImagePlugin
import io

def image_to_base64(image):
    if isinstance(image, bytes):
        return base64.b64encode(image).decode('utf-8')
    if isinstance(image, JpegImagePlugin.JpegImageFile):
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    if isinstance(image, Image.Image):
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    with open(image, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def base64_to_image(base64_string, output_path=None):
    # 解码 base64 数据
    image_data = base64.b64decode(base64_string)

    # 使用 BytesIO 创建一个文件对象
    image_buffer = io.BytesIO(image_data)

    # 使用 PIL 打开图像
    image = Image.open(image_buffer)

    # 如果提供了输出路径，则保存图像
    if output_path:
        image.save(output_path)

    return image