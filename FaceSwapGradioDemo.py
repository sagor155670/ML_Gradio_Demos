import gradio as gr
import json
import requests
import zipfile
from zipfile import ZipFile
import io,os,glob
from PIL import Image


def Main(selected_pairs):
    return [gr.Image('/media/mlpc2/workspace/sagor/ML_Gradio/output/image_0.jpg'),gr.Video(None)]


def ExtractSource(source_image):
    images = load_images_from_folder('./output')
    return gr.Gallery(images,visible=True,interactive=True)

def ExtractTarget(target_image,prompt):
    images = load_images_from_folder('./output')
    return gr.Gallery(images,visible=True,interactive=True)



def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            images.append(img)
    return images

with gr.Blocks() as demo:
    gr.Markdown("Happy Testing!")
    with gr.Row():
        with gr.Column():

           source_image = gr.Image(label='Source Image') 
           source_extract_button = gr.Button("Extract Source")
           source_gallary = gr.Gallery("Sources",visible=False ,interactive=True)
           
        with gr.Column():
            target_image = gr.Image(label="Target Image" , visible=True)
            prompt = gr.Textbox(label="Prompt")
            target_extract_button = gr.Button("Extract Target")
            target_gallary = gr.Gallery("Sources",visible=False ,interactive=False)

        source_extract_button.click(
            ExtractSource,
            inputs= source_image,
            outputs= source_gallary
        )
        target_extract_button.click(
            ExtractTarget,
            inputs= [target_image,prompt],
            outputs= target_gallary
        )

    with gr.Row():
        selected_pairs = gr.Text(label="selected pairs")
    with gr.Row():    
        submit_button =  gr.Button("Submit")

    with gr.Row():    
        image_output = gr.Image(visible=True)
        video_output =  gr.Video(visible=True)     

        submit_button.click(
            Main,
            inputs= selected_pairs,
            outputs=[image_output,video_output]
        )


demo.launch(share=True)
