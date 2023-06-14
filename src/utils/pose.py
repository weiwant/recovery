import os

import cv2
import pyopenpose as op


def process_video(video_path, OPENPOSE_ROOT, model_type='BODY_25', max_people=1):
    """
    处理视频

    :param OPENPOSE_ROOT: openpose根目录
    :param video_path: 视频路径
    :param model_type: 模型类型
    :param max_people: 最大人数
    :return:
    """
    params = dict()
    params["model_folder"] = os.path.join(OPENPOSE_ROOT, 'models')
    params["model_pose"] = model_type
    params["number_people_max"] = max_people
    params['net_resolution'] = '256x192'
    VideoCapture = getattr(cv2, 'VideoCapture')
    cap = VideoCapture(video_path)
    frame_count = cap.get(getattr(cv2, 'CAP_PROP_FRAME_COUNT'))
    if not cap.isOpened():
        return
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    while True:
        frame_index = cap.get(getattr(cv2, 'CAP_PROP_POS_FRAMES'))
        ret, frame = cap.read()
        if not ret:
            break
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        yield datum.poseKeypoints[0, :15, :2], frame_index, frame_count
    cap.release()
