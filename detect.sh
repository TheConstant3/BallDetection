#!/bin/bash

if [ "$1" = "" ]; then
  echo "Please, set path to video!"
  exit 1
fi

video_dir="$(dirname "$1}")"
filename="$(basename "$1")"

nvidia-docker run -it -v "$video_dir":/app/videos ball_detector --video videos/$filename