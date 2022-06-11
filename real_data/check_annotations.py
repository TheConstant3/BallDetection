import os
import xml.etree.ElementTree as ET

import cv2

for f in os.listdir('data/videos'):
    print(f)
    mytree = ET.parse(f'data/annotations/{f.split(".")[0]}.xml')
    myroot = mytree.getroot()
    size = myroot.find('meta').find('task').find('original_size')
    width = size.find('width')
    height = size.find('width')
    tracks = myroot.findall('track')
    frames_boxes = dict()
    for track in tracks:
        if track.attrib['label'].lower() == 'ball':
            for i, box in enumerate(track):
                x1 = int(float(box.attrib['xtl']))
                y1 = int(float(box.attrib['ytl']))
                x2 = int(float(box.attrib['xbr']))
                y2 = int(float(box.attrib['ybr']))
                p1 = (x1, y1)
                p2 = (x2, y2)
                frame_id = int(box.attrib['frame'])
                frames_boxes[frame_id] = (p1, p2,)
    print(frames_boxes)

    cap = cv2.VideoCapture(f'data/videos/{f}')

    imageWidth = int(cap.get(3))
    imageHeight = int(cap.get(4))
    print((imageWidth, imageHeight))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    os.makedirs('data/debug_videos', exist_ok=True)
    out_cap = cv2.VideoWriter(f'data/debug_videos/{f}', fourcc, fps, (imageWidth, imageHeight))

    i = -1
    while True:
        i += 1
        ret, img = cap.read()
        if not ret:
            break

        box = frames_boxes.get(i)
        if box:
            img = cv2.resize(img, (1824, 1026))
            p1, p2 = box
            img = cv2.rectangle(img, p1, p2, (0, 0, 255))

        # cv2.imshow('', img)
        # cv2.waitKey(0)

        out_cap.write(img)

    out_cap.release()

