import os
import jsonlines
import subprocess
import json

if not os.path.exists('checkpoint.txt'):
    with open('checkpoint.txt','w',encoding='utf-8') as f:
        f.write('0')

# 读取checkpoint，从checkpoint之后开始下载
with open('checkpoint.txt','r',encoding='utf-8') as f:
    cp = int(f.read().strip())

# 读取links.jsonl文件，获得要读取的文件的信息
with jsonlines.open('links.jsonl','r') as f:
    links = []
    for line in f:
        links.append(line)

# 存储现有的BV号
BVs = [item["video_id"] for item in links]

def check(BV):
    '''
    检查视频是单p还是多p
    返回是否是多p，以及总标题信息
    '''
    title1=json.loads(subprocess.check_output(['lux','-j',BV]))[0]['title']
    title2=json.loads(subprocess.check_output(['lux','-j','-eto',BV]))[0]['title']
    if title1==title2:
        multipart = False
        title = title1
    else:
        multipart = True
        title = title1.removesuffix(' '+title2)
    return {"multipart":multipart,"title":title}

def add_video_link(BV):
    '''
    添加视频链接
    '''
    # 首先检查是否和已有的重复
    if BV in BVs:
        print("列表中已存在，跳过中...")
        return 1
    information = check(BV)
    newitem = {"id":len(links),"video_id":BV}
    newitem["multipart"]=str(information["multipart"])
    newitem["title"]=information["title"]
    print(newitem["title"])
    links.append(newitem)
    with jsonlines.open('links.jsonl','w') as f:
        for item in links:
            f.write(item)
    BVs.append(BV)
    print("写入成功！")
    return 0

def cmd_download_BV(BV, multipart, filepath, cookie='cookie.txt', Caption=True):
    '''
    拼接出把BV下载到filepath中的命令
    '''
    # subprocess.run(['lux','-i','BV1ws4y1K7Nd'],shell=True)
    args = ['lux','-o',filepath]
    if multipart:
        args = args + ['-p','-eto']
    if cookie != None:
        args = args + ['-c',cookie]
    if Caption:
        args.append('-C')
    args.append(BV)
    return args

def cmd(commands):
    '''
    执行终端命令
    '''
    result = subprocess.run(commands,shell=True)
    return result.returncode

def download_BV(BV, multipart=False, filepath='.', cookie='cookie.txt', Caption=True):
    '''
    下载视频
    '''
    args = cmd_download_BV(BV,multipart,filepath,cookie,Caption)
    result = cmd(args)
    return result

def download(cookie=None,Caption=True):
    '''
    批量下载视频
    '''
    checkpoint = cp
    to_be_downloaded = links[checkpoint+1:] # 待下载的视频链接和相关信息
    if len(to_be_downloaded)==0:
        print("没有待下载的视频！")
        return 1
    for item in to_be_downloaded:
        BV=item["video_id"] # 读取BV号
        multpart = item["multipart"] # 读取是否有多个part
        filepath = str(checkpoint+1) # 用于存储视频的子文件夹
        if not os.path.exists(filepath):
            os.mkdir(filepath) # 若不存在则新建
        result = download_BV(BV,multpart,filepath,cookie,Caption)
        if result==0:
            checkpoint += 1
            with open('checkpoint.txt','w',encoding='utf-8') as f:
                f.write(str(checkpoint))
            print('下载成功！')
        else:
            print('下载失败！')
            break

def menu():
    '''
    简单的用户界面
    '''
    while True:
        choice = input('''
Bilibili批量下载器V1.0, 作者lixiang90
请选择你的操作：
1. 添加要下载的视频的BV号
2. 批量下载视频
3. 结束
你的选择：''')
        if choice == '1':
            q = 0
            while q == 0:
                BV = input('请输入BV号(退出请输入E):')
                if BV == 'E':
                    q = 1
                else:
                    r = add_video_link(BV)
                    if r == 1:
                        print('已存在!')
                    else:
                        print('成功!')
        elif choice == '2':
            print('准备批量下载视频...')
            if os.path.exists("cookie.txt"):
                download(cookie="cookie.txt")
            else:
                download()
        elif choice == '3':
            print('结束程序...')
            exit()
        else:
            print('错误的选项，请重新输入！')

if __name__ == '__main__':
    menu()