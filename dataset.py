from typing import Any
from PIL import Image, ImageDraw, ImageFont
import os
import jsonlines
import json
from tqdm import tqdm

from torch.utils.data import Dataset

class VCRDataset(Dataset):
    def __init__(self, path, split='train'):
        assert split in ['train', 'val']
        self.image_root = os.path.join(path, 'vcr_images/vcr1images')
        with jsonlines.open(os.path.join(path, f'vcr_annotation/{split}.jsonl'), 'r') as reader:
            self.datas = [self.__parse(data) for data in reader.iter()]
    
    def __parse(self, data:dict):
        #image
        objects = data['objects']
        image_path = os.path.join(self.image_root, data['img_fn'].replace('...', ''))
        metadata_path = os.path.join(self.image_root, data['metadata_fn'].replace('...', ''))
        """ with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        bboxes = [bbox[:-1] for bbox in metadata['boxes']]
        segms = [[(x, y) for x, y in segm[0]] if len(segm) > 0 else [] for segm in metadata['segms']] """
        
        #test
        question = data['question_orig']
        answer_choices = [' '.join([word if isinstance(word, str) else str(word)[1:-1] for word in choice]) for choice in data['answer_choices']]
        answer_label = data['answer_label']
        rationale_choices = [' '.join([word if isinstance(word, str) else str(word)[1:-1] for word in choice]) for choice in data['rationale_choices']]
        rationale_label = data['rationale_label']
        
        return {'objects': objects, 
                'image_path': image_path, 
                #'bboxes': bboxes, 
                #'semgs': segms, 
                'metadata_path': metadata_path, 
                'question': question, 
                'answer_choices': answer_choices, 
                'answer_label': answer_label, 
                'rationale_choices': rationale_choices, 
                'rationale_label': rationale_label}
        
    def __getitem__(self, index) -> Any:
        data = self.datas[index]
        image = Image.open(data['image_path'])
        with open(data['metadata_path'], 'r') as f:
            metadata = json.load(f)
        bboxes = [bbox[:-1] for bbox in metadata['boxes']]
        segms = [[(x, y) for x, y in segm[0]] if len(segm) > 0 else [] for segm in metadata['segms']]
        return {'objects': data['objects'], 
                'image': image, 
                'bboxes': bboxes, 
                'segms': segms, 
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
    vcr = VCRDataset('G:/vcr', split='val')
    max_num = 0
    for data in tqdm(vcr):
        max_num = max(max_num, len(data['objects']))
    print(max_num)
    
    #draw test
    data = vcr[0]
    image_orig, objects, bboxes, segms = data['image'], data['objects'], data['bboxes'], data['segms']
    image = image_orig.copy()
    draw = ImageDraw.Draw(image, 'RGBA')
    font = ImageFont.truetype('arial.ttf', 20)
    import random
    colors = [tuple([random.randint(0, 255) for _ in range(3)]) for _ in range(len(objects))]
    for idx, o in enumerate(objects):
        draw.rectangle(bboxes[idx], outline=colors[idx]+(200, ), width=3)
        draw.polygon(segms[idx], outline=colors[idx]+(200, ), width=3) if len(segms[idx]) > 0 else None
        text = f'{o} {idx}'
        w, h = bboxes[idx][:2]
        text_bbox = draw.textbbox((w, h), text, font, align='center', spacing=2)
        text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        draw.rectangle(text_bbox, fill=colors[idx]+(200, ))
        draw.text((w + 3, h), text, font=font, fill=(0, 0, 0), align='center', spacing=2)
    image.show()
        