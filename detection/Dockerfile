FROM nvidia/cuda:11.0.3-cudnn8-runtime-ubuntu18.04

RUN apt-get update && apt-get install python3.7-dev python3-pip ffmpeg libsm6 libxext6 -y && python3.7 -m pip install --upgrade pip

WORKDIR /app

COPY model/ .
COPY src/ .
COPY requirements.txt .

RUN mkdir videos

RUN python3.7 -m pip install -r requirements.txt

ENTRYPOINT ["python3.7", "detect.py"]