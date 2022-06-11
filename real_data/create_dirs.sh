#!/bin/bash

if [ ! -d "data" ]; then
  mkdir data
fi

if [ ! -d "data/annotations" ]; then
  mkdir data/annotations
fi

if [ ! -d "data/videos" ]; then
  mkdir data/videos
fi