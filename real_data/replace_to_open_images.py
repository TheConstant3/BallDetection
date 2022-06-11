import shutil
import os

source_dir = 'data/dataset'
target_dir = '../open_images/data/dataset'

for data_type in ['images', 'labels']:
    path_from = f'{source_dir}/{data_type}'
    path_to = f'{target_dir}/{data_type}/train'
    file_names = os.listdir(path_from)
    for file_name in file_names:
        try:
            shutil.move(os.path.join(path_from, file_name), path_to)
        except:
            os.remove(os.path.join(path_to, file_name))
            shutil.move(os.path.join(path_from, file_name), path_to)
