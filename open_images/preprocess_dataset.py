import os.path

dataset_labels_path = 'data/dataset/labels'
os.makedirs(dataset_labels_path, exist_ok=True)

src_path = 'data/all_labels'
dst_path = 'data/need_download'
os.makedirs(dst_path, exist_ok=True)

class_id = '/m/01226z'  # Football


for file_src, split_ in [('validation-annotations-bbox.csv', 'validation'),
                         ('test-annotations-bbox.csv', 'test'),
                         ('oidv6-train-annotations-bbox.csv', 'train')]:
    new_lines = []
    labels = dict()
    with open(f'{src_path}/{file_src}') as f:
        for line in f.readlines():
            if class_id in line:
                image_id = line.split(',')[0]
                new_lines.append(f'{split_}/{image_id}\n')
                if image_id not in labels:
                    labels[image_id] = []
                XMin, XMax, YMin, YMax = map(float, line.split(',')[4:8])
                w = XMax - XMin
                h = YMax - YMin
                labels[image_id].append(f'0 {XMin + w/2} {YMin + h/2} {w} {h}\n')

    with open(f'{dst_path}/{split_}.txt', 'w+') as f:
        f.writelines(new_lines)

    path_to_labels = f'{dataset_labels_path}/{split_}'
    os.makedirs(path_to_labels, exist_ok=True)

    for image_id, label in labels.items():
        with open(f'{path_to_labels}/{image_id}.txt', 'w+') as file:
            file.writelines(label)
