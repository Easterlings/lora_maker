IMG2IMG_PARAMETERS = {
    "default":{
        "init_images": [
          "string" #base64_img
        ],
        "clip_skip":1,
        "prompt": "",  #提示词
        "negative_prompt": "Asian, Japanese, Korean, Chinese, UnrealisticDream",
        "resize_mode": 0, #调整大小模式0:just resize
        "mask_blur": 1, #蒙版模糊度
        "inpainting_fill": 1, # 0:fill,1:original
        "inpaint_full_res": False, #Inpaint area False:whole picture,True:only masked
        "inpainting_mask_invert": 1,  #蒙版模式 0:重绘蒙版内容,1:重绘非蒙版内容
        "sampler_name": "DPM++ SDE Karras", #采样方法
        "steps": 20,
        "restore_faces": True,
        "batch_size":1,
        "n_iter": 1,
        "cfg_scale": 7,
        "denoising_strength": 0.7, #重绘强度
        "seed": -1,
        "width": 768,
        "height": 1024,
        "send_images": True, #False,
        "save_images": False, #True,
        "override_settings_restore_afterwards": False,
        "override_settings": {
            "sd_model_checkpoint": "saiwei_clothes"
            # "sd_model_checkpoint": "realisticVisionV51_v51VAE"
        },
        # "mask": "string", # base64_img
        "alwayson_scripts": {}
    }
}