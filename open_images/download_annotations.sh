#!/bin/bash
set -e

if [ ! -d "data" ]; then
  mkdir data
fi
if [ ! -d "data/all_labels" ]; then
  mkdir data/all_labels
fi

wget https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv -P data/all_labels
wget https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv -P data/all_labels
wget https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv -P data/all_labels
wget https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv -P data/all_labels