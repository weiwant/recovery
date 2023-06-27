import json
import os

import joblib

from config import OPENPOSE_ROOT
from src.models.keyframe import KeyFrame
from src.utils.pose import process_video

if __name__ == '__main__':
    videos_path = './datasets/KeyFrame/video'
    jsons_path = './datasets/KeyFrame/json'
    videos = os.listdir(videos_path)
    model = KeyFrame()
    for video in videos:
        video_gen = process_video(os.path.join(videos_path, video), OPENPOSE_ROOT)
        label = json.load(open(os.path.join(jsons_path, os.path.splitext(video)[0] + '.json'), 'r'))['index']
        model.retrain(video_gen, label)
    model.gen = None
    joblib.dump(model, './models/KeyFrame.pkl')
