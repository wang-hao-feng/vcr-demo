import gradio as gr

vcr_dataset = [None] * 10

#css = "#button0 {--button-secondary-background-fill: rgba(255, 0, 0, 0.78); --button-secondary-background-fill-hover: rgba(255, 0, 0, 0.5);}"
button_css = [f"button{i}" + "{--button-secondary-background-fill: linear-gradient(to bottom right, var(--neutral-600), var(--neutral-700));\
               --button-secondary-background-fill-hover: linear-gradient(to bottom right, var(--neutral-600), var(--neutral-600));}" for i in range(64)]
css = "\n".join(button_css)

with gr.Blocks(css=css) as demo:
    with gr.Row():
        with gr.Column():
            index = gr.Slider(maximum=len(vcr_dataset), step=1, label='index')
            random_idx = gr.Button('Random')
            image_board = gr.Image()
            buttons = {}
            for j in range(8):
                with gr.Row():
                    for i in range(8):
                        buttons[i+j*8] = gr.Button(f'button {i+j*8}', size='sm', min_width=64, elem_id=f'button{i+j*8}')
            """ with gr.Row():
                for i in range(8):
                    with gr.Column():
                        for j in range(8):
                            buttons[i + j * 8] = gr.Button(f'button {i + j * 8}', size='sm') """
            #buttons = [gr.Button(value=f'person {i}', min_width=20) for i in range(2)]
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