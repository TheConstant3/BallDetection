from utils import letterbox, non_max_suppression, scale_coords
import onnxruntime
import numpy as np
import argparse
import torch
import cv2


def run(args):
    weights, path_to_video = args.weights, args.video
    cuda = torch.cuda.is_available()
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
    session = onnxruntime.InferenceSession(weights, providers=providers)

    cap = cv2.VideoCapture(path_to_video)
    count_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    imageWidth = int(cap.get(3))
    imageHeight = int(cap.get(4))

    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')

    filename = path_to_video.split('/')[-1]
    debug_filename = filename.split('.')[0] + '_debug.' + filename.split('.')[-1]
    path_to_debug_video = path_to_video[:-len(filename)] + debug_filename
    print('path_to_debug_video:', path_to_debug_video)
    out_cap = cv2.VideoWriter(path_to_debug_video, fourcc, fps, (imageWidth, imageHeight))

    i = 0
    ret, img0 = cap.read()
    while ret:
        img = letterbox(img0, [640, 640], stride=32, auto=False)[0]
        # Convert
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img).astype(dtype=np.float32)
        img /= 255
        img = img[None]
        pred = session.run([session.get_outputs()[0].name], {session.get_inputs()[0].name: img})[0]
        pred = torch.tensor(pred)
        det = non_max_suppression(pred)[0]

        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
        for *box, conf, cls in reversed(det):
            p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
            cv2.rectangle(img0, p1, p2, (0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

        i += 1
        print(f'{i}/{count_frames} frames of {path_to_video} precessed')
        out_cap.write(img0)
        ret, img0 = cap.read()

    out_cap.release()
    print('done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='configs for detecting ball')
    parser.add_argument("--weights", type=str, help="path to model weights", default='best.onnx')
    parser.add_argument("--video", type=str, help="path to video for detection", required=True)
    run(parser.parse_args())
