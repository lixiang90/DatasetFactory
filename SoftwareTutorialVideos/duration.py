import cv2
import os

def get_singlefile_duration(filename):
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        rate = cap.get(5)
        frame_num = cap.get(7)
        duration = frame_num / rate
        return duration
    return -1

def get_all_video_filenames():
    if not os.path.exists('checkpoint.txt'):
        return []
    with open('checkpoint.txt','r',encoding='utf-8') as f:
        checkpoint = int(f.read())
    vname = []
    for i in range(checkpoint+1):
        vname_i = [str(i) + '/' + f for f in os.listdir(f'./{i}') if f.split('.')[-1]=='mp4']
        vname += vname_i
    return vname

def get_duration():
    vname = get_all_video_filenames()
    print(f"Totally {len(vname)} videos.")
    duration = 0
    for i,v in enumerate(vname):
        curr_duration = get_singlefile_duration(v)
        print(f'{i}. {v} : {curr_duration} s')
        duration += curr_duration
    return duration

if __name__ == '__main__':
    t = get_duration()
    print(f'Total duration: {t/3600} hours.')