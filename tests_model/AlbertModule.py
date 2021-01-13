import aicmder as cmder
from aicmder.module.module import serving, moduleinfo
from transformers import *
import torch
import json
import numpy as np
# from tests_model.ChatbotModule import Chatbot
@moduleinfo(name='albert')
class Albert(cmder.Module):
    
    def __init__(self, **kwargs):
        # self.dummpy_params = dummpy_params
        self.pretrained = '/home/faith/ALBERT'
        # self.pretrained = '/smb/AI_models/transformer/ALBERT/'
        self.device = int(kwargs['device_id'])
        self.device = "cuda:{}".format(self.device) if self.device >= 0 else "cpu"

        print('Albert', self.device)
        self.bert = AlbertModel.from_pretrained(self.pretrained, output_attentions=False, output_hidden_states=True)
        self.bert.to(self.device)
        self.bert.eval()
        self.tokenizer = BertTokenizer.from_pretrained(self.pretrained)
        
    def evaluate(self, inputtext):
        encoding = self.tokenizer(inputtext, return_tensors='pt', padding=True, return_length=True)

        with torch.no_grad():
            input_ids = encoding['input_ids']
            # input_len = encoding['length'].to(self.device)
            mask = encoding['attention_mask']
            if self.device != 'cpu':
                mask = mask.to(self.device)
                input_ids = input_ids.to(self.device)
            outputs = self.bert(input_ids, attention_mask=mask)
            ret = outputs[0] # outputs.last_hidden_state 等价

            if self.device != 'cpu':
                cpu_ret = ret.cpu().detach().numpy()
                cpu_mask = mask.cpu().detach().numpy()
            else:
                cpu_ret = ret
                cpu_mask = mask
            result = np.dot(cpu_mask, cpu_ret.squeeze(0))

            return torch.tensor(result).numpy().tolist()
    
    @serving
    def predict(self, str):
        print('begin predict', str)
        result = self.evaluate(str)
        return json.dumps(result)
        
        
        
class Foo:
    
    def test():
        pass