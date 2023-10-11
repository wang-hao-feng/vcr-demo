from typing import Any
from PIL import Image, ImageDraw, ImageFont
import os
import jsonlines
import json

from torch.utils.data import Dataset

class VCRDataset(Dataset):
    def __init__(self, path, split='train'):
        assert split in ['train', 'val']
        self.image_root = os.path.join(path, 'vcr_images/vcr1image')
        with jsonlines.open(os.path.join(path, f'vcr_annotation/{split}_prepare.jsonl'), 'r') as reader:
            self.datas = [self.__parse(data) for data in reader.iter()]
    
    def __parse(self, data:dict):
        #image
        objects = data['objects']
        image_path = os.path.join(self.image_root, data['img_fn'])
        metadata_path = os.path.join(self.image_root, data['metadata_fn'])
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        bboxes = [bbox[:-1] for bbox in metadata['boxes']]
        segms = [[(x, y) for x, y in segm] if segm is not None else [] for segm in data['segms']]
        
        #test
        question = data['question_orig']
        answer_choices = [' '.join([word if isinstance(word, str) else str(word)[1:-1] for word in choice]) for choice in data['answer_choices']]
        answer_label = data['asnwer_label']
        rationale_choices = [' '.join([word if isinstance(word, str) else str(word)[1:-1] for word in choice]) for choice in data['rationale_choices']]
        rationale_label = data['rationale_label']
        
        return {'objects': objects, 
                'image_path': image_path, 
                'bboxes': bboxes, 
                'semgs': segms, 
                'question': question, 
                'answer_choices': answer_choices, 
                'answer_label': answer_label, 
                'rationale_choices': rationale_choices, 
                'rationale_label': rationale_label}
        
    def __getitem__(self, index) -> Any:
        data = self.datas[index]
        image = Image.open(data['image_path'])
        return {'objects': data['objects'], 
                'image': image, 
                'bboxes': data['bboxes'], 
                'semgs': data['segms'], 
                'question': data['question'], 
                'answer_choices': data['answer_choices'], 
                'answer_label': data['answer_label'], 
                'rationale_choices': data['rationale_choices'], 
                'rationale_label': data['rationale_label']}
    
    def __len__(self):
        return len(self.datas)

if __name__ == '__main__':
    vcr = None
    # read test
    from tqdm import tqdm
    for split in ['train', 'val']:
        vcr = VCRDataset('', split=split)
        for data in tqdm(vcr, desc=split):
            pass
    
    #draw test
    data = vcr[0]
    image_orig, objects, bboxes, segms = data['image'], data['objects'], data['bboxes'], data['segms']
    image = image_orig.copy()
    draw = ImageDraw.Draw(image, 'RGBA')
    font = ImageFont('arial.ttf', 20)
    import random
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(objects))]
    for idx, o in enumerate(objects):
        draw.rectangle(bboxes[idx], outline=colors[idx], width=2)
        draw.polygon(segms[idx], outline=colors[idx], width=2) if len(segms[idx] > 0) else None
        text = f'{o} {idx}'
        text_bbox = draw.textbbox((0, 0), text, font, align='center')
        text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        w, h = image.size
        draw.text((w - text_w, h - text_h), text, font=font)
    image.show()
        