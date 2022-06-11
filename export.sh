#!/bin/bash

if [ "$1" = "" ]; then
  echo "Please, set path to weights"
  exit 1
fi

cd yolov5 && python export.py --include onnx --weights $1