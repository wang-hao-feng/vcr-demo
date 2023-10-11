import gradio as gr
import json
from dataset import VCRDataset
import random

vcr_dataset = None
image, question, answer_choices, answer_label, rationale_choices, rationale_label = [None] * 6

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
    # blocks structures
    split_chooser = gr.Dropdown(choices=['train', 'val'], multiselect=False, filterable=True, label='VCR dataset split')
    with gr.Row():
        with gr.Column():
            index_slider = gr.Slider(step=1, label='index')
            random_idx = gr.Button('Random')
            image_board = gr.Image()
            buttons = {}
            for j in range(8):
                with gr.Row():
                    for i in range(8):
                        buttons[i+j*8] = gr.Button(f'object {i+j*8}' if i+j*8 != 0 else 'hidden_all', 
                                                   size='sm', min_width=16, elem_id=f'button{i+j*8}')
        with gr.Column():
            question_text = gr.HighlightedText(label='question', 
                                          value=[('question', None)], 
                                          color_map={'False':'white'})
            answer_choices_text = gr.HighlightedText(label='answer choices', 
                                               value=[('a\n', 'True'), ('b\n', None), ('c\n', None), ('d\n', None)], 
                                               color_map={'True':'green'})
            rationale_choices_text = gr.HighlightedText(label='rationale choices', 
                                                   value=[('a\n', 'True'), ('b\n', None), ('c\n', None), ('d\n', None)], 
                                                   color_map={'True':'green'})

    # functions
    ## change vcr split
    def change_dataset_split(split):
        global vcr_dataset
        if vcr_dataset is not None:
            del vcr_dataset
        #vcr_dataset = VCRDataset('G:/vcr', split=split)
        vcr_dataset = [None] * (50 if split == 'train' else 25)
        return gr.Slider(maximum=len(vcr_dataset), interactive=True)
    split_chooser.select(fn=change_dataset_split, inputs=split_chooser, outputs=index_slider)

demo.launch()