import gradio as gr
import json,cv2
import requests
import zipfile
from zipfile import ZipFile
import io,os,glob
from PIL import Image
from io import BytesIO

URL = "https://kn5y0rt1cds8dk-8000.proxy.runpod.net/"
access_token = 'c8aca83933b177312 2ba65ed6429f6f13c6 1yu8aacecdfff0bfa9b b714f01de6'

photoEnhanceType = ["Color-balance","Colorize","Deblur","Denoise",
                    "Face-enhance","Face-restore","Light-balance",
                    "Remove-artifacts","Repair-scratch","Upscale","White-balance"]

def convertImageToBytes(image):
    isSuccess , buffer = cv2.imencode("jpeg",image)
    print(f"buffer success->> {isSuccess}")
    return BytesIO(buffer).getvalue()

def showScaleSlider(enhance_type,scale_factor):
    if enhance_type == "Upscale":
        scale_factor = gr.Slider(minimum=1,maximum=6,step=1,interactive=True,value=2,visible=True)
    else:
        scale_factor = gr.Slider(minimum=1,maximum=6,step=1,interactive=True,value=2,visible=False)    
    return scale_factor

def request(input_image,enhance_type,scale_factor):
    if enhance_type == "Upscale":
        url =  f"{URL}{enhance_type.lower()}/{scale_factor}"
    else:
        url =  f"{URL}{enhance_type.lower()}"   
    print(f"url>> {url}")

    image_bytes = convertImageToBytes(input_image)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    files = {
        'image': ('image.jpeg', image_bytes, 'image/jpeg')
    }

    response = requests.post(url, headers=headers, files=files)
    print(response.content)
    print(f"status code {response.status_code}")

    if response.status_code == 200:
        print("Request Successfull")
        with io.BytesIO(response.content) as zip_file:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall('output')
        print("ZIP file extracted successfully!")         
    else:
        print('Request failed.')
    return gr.Image('./output/image_0.jpg')

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():

           input_image = gr.Image(label='Input Image') 
           enhance_type = gr.Dropdown(photoEnhanceType,interactive=True)
           scale_factor = gr.Slider(minimum=1,maximum=6,step=1,interactive=True,value=2,visible=False)
           
           enhance_type.change(
               showScaleSlider,
               inputs= [enhance_type,scale_factor],
               outputs=scale_factor
           )
           
        with gr.Column():
            image_output = gr.Image()
            
             

            submit = gr.Button("Submit")
            submit.click(
                request,
                inputs = [input_image,enhance_type,scale_factor],
                outputs= image_output
            )
demo.launch(share=False)              