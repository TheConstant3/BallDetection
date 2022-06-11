#!/bin/bash

git clone https://github.com/ultralytics/yolov5.git

cp hyp.yaml yolov5/hyp.yaml
cp dataset.yaml yolov5/dataset.yaml
cd yolov5 && python train.py --weights yolov5m.pt --data dataset.yaml --hyp hyp.yaml --batch-size -1 --freeze 3