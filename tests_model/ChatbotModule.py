from AlbertModule import Albert
from aicmder.module.module import serving, moduleinfo
from aicmder.common import read_yaml_file
import random
import os
import numpy as np
import torch
import sqlite3

class QA:
    question_type = ''
    question = ''
    answer = ''

    def __repr__(self) -> str:
        return "{} {} {}".format(self.question_type, self.question, self.answer)

    def __hash__(self):
        return self.question

    def __eq__(self, other):
        return self.question == other.question


class QASet:

    def __init__(self, default_answers) -> None:
        self.questions = []
        self.qa_object = {}
        self.questions_embeds = []
        default_answers = ['不知道'] if default_answers is None or len(
            default_answers) == 0 else default_answers
        self.default_answers = default_answers

    def add_question(self, question: QA):
        self.questions.append(question.question)
        self.qa_object[question.question] = question

    def choose_default_ans(self):
        count = len(self.default_answers)
        index = random.randint(0, count - 1)
        return self.default_answers[index]

    def get_answer(self, question: str):
        qa = self.qa_object.get(question, None)
        if qa.question_type in ['查学校', '查小区', '学校评价']:
            conn = sqlite3.connect('/Users/faith/wechat_admin/db.sqlite3')
            c = conn.cursor()
            c.execute(qa.answer)
            ret = c.fetchall()
            conn.close()
            # print(ret)
            result = ""
            for r in ret:
                result += ','.join(r) + ' '
            result = result.strip()
            return self.choose_default_ans() if result == '' else result
            
        return qa.answer if qa is not None else self.choose_default_ans()

    def add_embedding(self, embed):
        self.questions_embeds.append(embed)

@moduleinfo(name='chatbot')
class Chatbot(Albert):
    
    _threadhold = 0.5

    def load_config(self, file_path):
        d = read_yaml_file(file_path)
        # print(d)
        self.qa_set = QASet(d.get('default'))
        for qa_type in d['chatbot'].items():
            question_type = qa_type[0]
            for ans in qa_type[1].items():
                answer = ans[0]
                for question in ans[1]:
                    qa = QA()
                    qa.answer = answer
                    qa.question = question
                    qa.question_type = question_type
                    self.qa_set.add_question(qa)

        # print(self.qa_set.get_answer('你在干什么'))
        # print(self.qa_set.get_answer('你在干什么a'))

    def __init__(self, file_path, **kwargs) -> None:
        super(Chatbot, self).__init__(**kwargs)
        assert os.path.exists(file_path)
        self.load_config(file_path)
        self.is_init = False

    def init_embedding(self):
        if self.is_init == False:
            if os.path.exists('embeds.pt'):
                self.all_embed_tensor = torch.load('embeds.pt')
            else:
                for q in self.qa_set.questions:
                    self.qa_set.add_embedding(self.evaluate(q))
                self.all_embed_tensor = torch.squeeze(torch.tensor(self.qa_set.questions_embeds))
                torch.save(self.all_embed_tensor, 'embeds.pt')
            self.is_init = True
            print('init emdbeding success!')
            
    @serving
    def chat(self, question):
        self.init_embedding()
        embed = self.evaluate(question)
        embed_tensor = torch.tensor(embed)

        similarity = torch.nn.functional.cosine_similarity(embed_tensor, self.all_embed_tensor, dim=1, eps=1e-8) 
        # print(self.qa_set.questions) 
        # print(question, similarity)
        if torch.max(similarity) > self._threadhold:
            # question = self.qa_set.questions[torch.argmax(similarity)]
            k = 3
            questions = np.array(self.qa_set.questions)[torch.topk(similarity, k)[1]]
            ret = ''
            for q in questions:
                ret += self.qa_set.get_answer(q) + ' '
            return ret
        else:
            return self.qa_set.choose_default_ans()
    


if __name__ == "__main__":

    file_path = '/Users/faith/AI_Commander/tests_model/config.yaml'
    config = {'device_id': -1}
    bot = Chatbot(file_path=file_path, **config)
    print(bot.predict('你在干嘛'))
    print(bot.predict('你去那里啦'))