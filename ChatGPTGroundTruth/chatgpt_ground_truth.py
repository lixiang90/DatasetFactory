from chatgpt_respond import simple_respond
import os
import shutil
import jsonlines

def ground_truth(file='questions.jsonl', save='ground_truth.jsonl'):
    if not os.path.exists(save):
        shutil.copy(file, save)
    
    data = []
    with jsonlines.open(save, 'r') as reader:
        for obj in reader:
            data.append(obj)
    while True:
        for i in range(len(data)):
            if 'ground_truth' not in data[i].keys():
                prompt = f"Please answer a question about {data[i]['topic']}: {data[i]['question']}"
                print(f"Question {i+1}: {prompt}")
                gtruth = simple_respond(prompt)
                if gtruth != 'F':
                    data[i]['ground_truth'] = gtruth
                    with jsonlines.open(save, 'w') as writer:
                        for item in data:
                            writer.write(item)
                    print(f"Answer: {gtruth}")
        complete = True
        for item in data:
            if 'ground_truth' not in item.keys():
                complete = False
        if complete:
            break
            
                

if __name__ == '__main__':
    ground_truth()