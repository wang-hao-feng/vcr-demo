import gradio as gr
import json
from dataset import VCRDataset

vcr_dataset = None

with open('colors.json', 'r') as f:
    button_colors = json.load(f)

button_css = [f"#button{i} " + \
              "{--button-secondary-background-fill: rgba" + \
              str(tuple(button_colors[str(i)]) + (0.78,)) + \
              "; --button-secondary-background-fill-hover: rgba" + \
              str(tuple(button_colors[str(i)]) + (0.5,)) + \
              ";}" for i in range(1, 64)]
css = "\n".join(button_css)

with gr.Blocks(css=css) as demo:
    split_chooser = gr.Dropdown(choices=['train', 'val'], multiselect=False, filterable=True, label='VCR dataset split')
    with gr.Row():
        with gr.Column():
            index = gr.Slider(maximum=10, step=1, label='index')
            random_idx = gr.Button('Random')
            image_board = gr.Image()
            buttons = {}
            for j in range(8):
                with gr.Row():
                    for i in range(8):
                        buttons[i+j*8] = gr.Button(f'object {i+j*8}' if i+j*8 != 0 else 'hidden_all', 
                                                   size='sm', min_width=16, elem_id=f'button{i+j*8}')
        with gr.Column():
            question = gr.HighlightedText(label='question', 
                                          value=[('question', None)], 
                                          color_map={'False':'white'})
            answer_choices = gr.HighlightedText(label='answer choices', 
                                               value=[('a\n', 'True'), ('b\n', None), ('c\n', None), ('d\n', None)], 
                                               color_map={'True':'green'})
            rationale_choices = gr.HighlightedText(label='rationale choices', 
                                                   value=[('a\n', 'True'), ('b\n', None), ('c\n', None), ('d\n', None)], 
                                                   color_map={'True':'green'})

demo.launch()