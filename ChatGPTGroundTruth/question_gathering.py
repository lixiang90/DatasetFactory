import requests
import os
import jsonlines
import time
import random

key = os.getenv('OPENAI_API_KEY')
u = 'https://api.openai.com/v1/completions'
h = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + key
}
N = 500
M = 20

def gen_prompt(topic, examples):
    prompt = f"Generate {M} factual questions about {topic}:"
    for i,item in enumerate(examples):
        prompt += f"\n{i+1}. {item}"
    prompt += f'\n{len(examples)+1}.'
    return prompt

def gather(topic):
    result = []
    examples = []
    while len(result) < N:
        time.sleep(30)
        prompt = gen_prompt(topic, examples)
        d = {
            "model": "text-davinci-003",
            "prompt": prompt,
            "max_tokens": 3900,
            "temperature": 1.0
        }
        r = requests.post(url=u, headers=h, json=d, verify=False)
        if r.status_code == 200:
            res = r.json()
            text = prompt + res['choices'][0]['text']
            if '\n' in text and '. ' in text:
                qs = text.split('\n')[1:]
                new_questions = []
                for q in qs:
                    if '. ' in q:
                        if len(q.split('. ')) >= 2:
                            new_questions.append(q.split('. ',1)[1])
                for q in new_questions[len(examples):]:
                    if q not in result and len(result)<N:
                        print(f"{len(result)+1}: {q}")
                        result.append(q)
                examples = random.sample(result,3)
        else:
            return -1
    return result

def auto_gather():
    if not os.path.exists('checkpoint.txt'):
        with open('checkpoint.txt','w',encoding='utf-8') as f:
            f.write('0')
    with open('checkpoint.txt','r',encoding='utf-8') as f:
        checkpoint = int(f.read())
    with open('topic.txt','r',encoding='utf-8') as f:
        lines = f.readlines()
        topics = [t.replace('\n','') for t in lines]
    
    curr_data = []
    if os.path.exists('questions.jsonl'):
        with jsonlines.open('questions.jsonl') as reader:
            for item in reader:
                curr_data.append(item)
    
    remaining_topics = topics[checkpoint:]

    for topic in remaining_topics:
        print(f'Gathering question about {topic}:')
        new_questions = gather(topic)
        if new_questions==-1:
            print(f'Error when gathering questions of topic {topic}.')
            break
        else:
            print(f'{len(new_questions)} questions generated.')
            new_data = [{'topic':topic,'question':question} for question in new_questions]
            curr_data = curr_data + new_data
            with jsonlines.open('questions.jsonl',mode='w') as writer:
                for item in curr_data:
                    writer.write(item)
            checkpoint += 1
            with open('checkpoint.txt','w',encoding='utf-8') as f:
                f.write(str(checkpoint))
            time.sleep(1)

    if checkpoint==len(topics):
        print('Finished gathering questions.')
    else:
        print(f'Questions gathering stopped at {checkpoint}')

if __name__=='__main__':
    auto_gather()