#gradio 图片输入输出demo
import numpy as np
import gradio as gr
from PIL import Image
from common.sd_api import img2img_request, get_img2img_request_data
from utils import image_to_base64,base64_to_image

def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

def sd_img2img_with_lora(img, prompt, denoising_strength):
    pil_image = Image.fromarray(img)
    request_data = get_img2img_request_data()
    request_data['init_images']=[
        image_to_base64(pil_image)
    ]
    request_data["prompt"] = prompt
    request_data["denoising_strength"] = denoising_strength
    img_size = pil_image.size

    request_data["width"] = img_size[0]
    request_data["height"] = img_size[1]
    response_data = img2img_request(request_data)
    img_bs64 = response_data['images'][0]
    img = base64_to_image(img_bs64)
    return img

demo = gr.Interface(
    fn = sd_img2img_with_lora, 
    inputs=[gr.Image(), "text", gr.Slider(0, 1, step=0.01)],
    outputs= ["image"]
    )


demo.launch(server_name = "0.0.0.0", server_port=8080)