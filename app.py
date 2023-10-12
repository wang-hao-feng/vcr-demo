import gradio as gr
import json
from dataset import VCRDataset
import random

dataset_path = None
vcr_dataset = None
image, objects, bboxes, segms = None, None, None, None
mask_buttons, mask_button_state = [], dict([(f'object {i}', 0) for i in range(63)])

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
    dataset_path_text = gr.Textbox(label='vcr dataset path', info='press enter to input', interactive=True)
    split_chooser = gr.Dropdown(choices=['train', 'val'], multiselect=False, filterable=True, label='VCR dataset split')
    with gr.Row():
        with gr.Column():
            index_slider = gr.Slider(step=1, label='index', interactive=True)
            random_idx = gr.Button('Random')
            image_board = gr.Image()
            for j in range(8):
                with gr.Row():
                    for i in range(8):
                        mask_buttons.append(gr.Button(f'object {i+j*8-1}' if i+j*8 != 0 else 'hidden_all', 
                                            size='sm', min_width=16, elem_id=f'button{i+j*8}', 
                                            visible=True if i+j*8 == 0 else False))
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
    ## input dataset path
    def input_dataset_path(path):
        global dataset_path
        dataset_path = path
    dataset_path_text.submit(fn=input_dataset_path, inputs=dataset_path_text)

    ## change vcr split
    def change_dataset_split(split):
        global dataset_path
        global vcr_dataset
        if dataset_path is None:
            raise gr.Error('Please input vcr dataset path first.')
        if vcr_dataset is not None:
            del vcr_dataset
        vcr_dataset = VCRDataset(dataset_path, split=split)
        #vcr_dataset = [None] * (50 if split == 'train' else 25)
        return gr.Slider(maximum=len(vcr_dataset), interactive=True, value=0)
    split_chooser.select(fn=change_dataset_split, inputs=split_chooser, outputs=index_slider)

    ## random sample data
    def random_sample_data():
        global vcr_dataset
        if vcr_dataset is None:
            raise gr.Error('Please choose vcr split.')
        index = random.randint(0, len(vcr_dataset) - 1)
        return gr.Slider(value=index, interactive=True)
    random_idx.click(fn=random_sample_data, outputs=index_slider)

    ## show data
    def show_data(index):
        global vcr_dataset
        global image, objects, bboxes, segms
        global mask_buttons, mask_button_state
        data = vcr_dataset[index]
        objects = data['objects']
        image = data['image']
        bboxes = data['bboxes']
        segms = data['segms']
        question = data['question']
        answer_choices = data['answer_choices']
        answer_label = data['answer_label']
        rationale_choices = data['rationale_choices']
        rationale_label = data['rationale_label']
        
        a_ascii = ord('a')
        # image and text
        image_board_ = gr.Image(image, type='pil')
        question_text_ = gr.HighlightedText([(question, None)])
        answer_choices_text_ = gr.HighlightedText([(f'({chr(a_ascii + idx)}) {choice}\n', 'True' if idx == answer_label else None) 
                                                   for idx, choice in enumerate(answer_choices)])
        rationale_choices_text_ = gr.HighlightedText([(f'({chr(a_ascii + idx)}) {choice}\n', 'True' if idx == rationale_label else None) 
                                                   for idx, choice in enumerate(rationale_choices)])
        
        print([idx == answer_label for idx, _ in enumerate(answer_choices)])
        
        # mask button
        object_num = len(objects)
        new_mask_button = [gr.Button(f'{objects[i]} {i}' if i < object_num else f'object {i}', 
                                     visible=i < object_num) for i in range(63)]
        mask_button_state = dict([(f'{objects[i]} {i}' if i < object_num else f'object {i}', 0) for i in range(63)])
        
        return image_board_, question_text_, answer_choices_text_, rationale_choices_text_, *new_mask_button
    index_slider.change(fn=show_data, inputs=index_slider, 
                        outputs=[image_board, question_text, answer_choices_text, rationale_choices_text] + mask_buttons[1:])

    ## hidden all bbox or segm
    def hidden_all():
        pass

    ## change bbox or segm
    ### states = {0:none, 1:bbox, 2:segm, 3:both}
    def add_mask():
        pass

demo.launch()