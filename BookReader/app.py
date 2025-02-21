import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
import requests
from PIL import Image
import io
import base64
import numpy as np

def process_image(input_img):
    # Convert Gradio image to bytes
    pil_image = Image.fromarray(input_img.astype('uint8'), 'RGB')
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    # Send request to local endpoint
    response = requests.post(
        "http://localhost:7860/",
        files={"image": ("input.jpg", img_bytes)},
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        
        # get the image
        output_img = Image.open(result['image_path'])
        
        # return results
        return np.array(output_img), result['summary']
    else:
        raise gr.Error(f"Error processing image: {response.text}")

# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Book Reader")
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Input Image")
            submit_btn = gr.Button("Process")
        with gr.Column():
            output_image = gr.Image(label="Imagined")
            subtitle = gr.Text(label="Summary")

    submit_btn.click(
        fn=process_image,
        inputs=input_image,
        outputs=[output_image, subtitle]
    )

if __name__ == "__main__":
    demo.launch(server_port=7864, share=False)  # Using different port to avoid conflict