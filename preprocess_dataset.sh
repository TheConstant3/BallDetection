#!/bin/bash
set -e

cd open_images
python preprocess_dataset.py
python download_images.py
cd ../real_data
python create_real_dataset.py
python replace_to_open_images.py
