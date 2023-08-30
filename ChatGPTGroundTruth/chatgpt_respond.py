import requests
import os
import time

url = "https://api.openai.com/v1/chat/completions"
key = os.environ['OPENAI_API_KEY']

headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {key}'
}

def respond(messages):
    data = {
    "model": "gpt-3.5-turbo",
    "messages": messages
    }
    repeat = 3
    code = 0
    while repeat > 0 and code != 200:
        if repeat < 3:
            time.sleep(30)
        response = requests.post(url, headers=headers, json=data)
        code = response.status_code
        repeat -= 1
    if code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return 'F'

def simple_respond(message):
    m = [{"role":"user","content":message}]
    r = respond(m)
    return r

if __name__=='__main__':
    m = [{"role":"user","content":"在动画片CLANNAD中，男主角的名字是什么？"}]
    r = respond(m)
    print(r)