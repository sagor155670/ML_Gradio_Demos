import gradio as gr
import json
import requests
import zipfile
from zipfile import ZipFile
import io,os,glob
from PIL import Image


isVideoOutput =  False

def request(source_image,target_image,tenor_link):
    return gr.Video(visible=True) if isVideoOutput else gr.Image(visible=True)

with gr.Blocks() as demo:
    gr.Markdown("Happy Testing!")
    with gr.Row():
        with gr.Column():

           source_image = gr.Image(label='Source') 
           target_image = gr.Image(label='Target')
           tenor_link = gr.Text(label="Tenor Link")
           
        with gr.Column():
            image_output = gr.Image(visible=False)
            video_output =  gr.Video(visible=False)
             

            submit = gr.Button("Submit")
            submit.click(
                request,
                inputs = [source_image,target_image,tenor_link],
                outputs= video_output if isVideoOutput else image_output
            )



    


demo.launch(share=True)