import gradio as gr

vcr_dataset = [None] * 10

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            index = gr.Slider(maximum=len(vcr_dataset), step=1, label='index')
            image = gr.Image()
            #buttons = [gr.Button(value=f'person {i}', min_width=20) for i in range(2)]
        with gr.Column():
            question = gr.HighlightedText(label='question', 
                                          value=[('question', 'False')], 
                                          color_map={'False':'white'})
            answer_choices = gr.HighlightedText(label='answer_choices', 
                                               value=[('a\n', 'True'), ('b\n', 'False'), ('c\n', 'False'), ('d\n', 'False')], 
                                               color_map={'True':'green', 'False':'white'})
            rationale_choices = gr.HighlightedText(label='rationale_choices', 
                                                   value=[('a\n', 'True'), ('b\n', 'False'), ('c\n', 'False'), ('d\n', 'False')], 
                                                   color_map={'True':'green', 'False':'white'})

demo.launch()