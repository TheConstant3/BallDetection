import os
import xml.etree.ElementTree as ET

import cv2


os.makedirs('data/dataset/images', exist_ok=True)
os.makedirs('data/dataset/labels', exist_ok=True)

for f in ['video2.mp4', 'video3.mp4']:
    # if f != 'video1.webm':
    #     continue
    print(f)
    mytree = ET.parse(f'data/annotations/{f.split(".")[0]}.xml')
    myroot = mytree.getroot()
    size = myroot.find('meta').find('task').find('original_size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    tracks = myroot.findall('track')
    frames_boxes = dict()
    for track in tracks:
        if track.attrib['label'].lower() == 'ball':
            for i, box in enumerate(track):
                x1 = int(float(box.attrib['xtl']))
                y1 = int(float(box.attrib['ytl']))
                x2 = int(float(box.attrib['xbr']))
                y2 = int(float(box.attrib['ybr']))

                w_obj = x2 - x1
                h_obj = y2 - y1

                cx = x1 + w_obj / 2
                cy = y1 + h_obj / 2

                cx /= width
                cy /= height
                w_obj /= width
                h_obj /= height

                frame_id = int(box.attrib['frame'])
                if f == 'video2.mp4':
                    frames_boxes[frame_id] = f'0 {cx} {cy} {w_obj} {h_obj}\n0 0.936 0.579 0.016 0.03'
                else:
                    frames_boxes[frame_id] = f'0 {cx} {cy} {w_obj} {h_obj}'

    cap = cv2.VideoCapture(f'data/videos/{f}')

    base_name = f.split('.')[0]

    i = -1
    while True:
        i += 1
        ret, img = cap.read()
        if not ret:
            break
        if i % 30 == 0:
            cv2.imwrite(f'data/dataset/images/{base_name}_{i}.jpg', img)
            with open(f'data/dataset/labels/{base_name}_{i}.txt', 'w+') as file:
                file.write(frames_boxes[i])
