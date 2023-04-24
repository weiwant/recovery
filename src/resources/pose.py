import os

import cv2
import pyopenpose as op

from config import OPENPOSE_ROOT
from src.utils.logger import get_logger

logger = get_logger(__name__)


def process_video(video_path, model_type='BODY_25', max_people=1):
    """
    处理视频

    :param video_path: 视频路径
    :param model_type: 模型类型
    :param max_people: 最大人数
    :return:
    """
    logger.info(f'开始处理视频: {os.path.basename(video_path)}')
    params = dict()
    params["model_folder"] = os.path.join(OPENPOSE_ROOT, 'models')
    params["model_pose"] = model_type
    params["number_people_max"] = max_people
    params['net_resolution'] = '256x192'
    VideoCapture = getattr(cv2, 'VideoCapture')
    cap = VideoCapture(video_path)
    frame_count = cap.get(getattr(cv2, 'CAP_PROP_FRAME_COUNT'))
    if not cap.isOpened():
        logger.error(f'视频打开失败: {video_path}')
        return
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        datum = op.Datum()
        datum.cvInputData = frame
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        yield datum.poseKeypoints[0, :15, :2]
    cap.release()
