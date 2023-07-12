"""
@Author: Wenfeng Zhou
"""
import json
import os
import pathlib
from collections import deque

import cv2
import joblib
import numpy

import config
from src.models.correct.algorithm.model import Correct
from src.models.correct.utils.hash import find_template
from src.resources.video import keyframe
from src.utils.pose import get_pose


def inference(video, training_root, evaluate_root, task_type):
    """
    推理

    :param video: 视频名称
    :param training_root: 训练文件夹
    :param evaluate_root: 评价文件夹
    :param task_type: 任务类型
    :return:
    """
    video_path = os.path.join('./training', training_root, video)
    model = Correct(**joblib.load('./models/correct/correct.pkl'))
    frame_gen = keyframe(video_path)
    description = json.load(open(next(pathlib.Path(os.path.join('./templates', task_type)).glob('*.json')), 'r'))
    repeat = description['repeat']
    action_sequence = deque(description['action_sequence'] * repeat)
    status_durations = deque(description['status_durations'] * repeat)
    angle_threshold = numpy.array(description['angle_threshold'])
    threshold: numpy.ndarray = numpy.cos(angle_threshold[:, 2] / 180 * numpy.pi)
    stay_actions = description['stay_actions']
    skeleton_lines = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7), (1, 8), (8, 9), (9, 10), (10, 11),
                      (8, 12), (12, 13), (13, 14)]
    descriptions = {
        0: {
            1: '头部摆动幅度不标准'
        },
        1: {
            2: '右肩摆动幅度不标准',
            5: '左肩摆动幅度不标准',
            8: '身体摆动幅度不标准',
        },
        2: {
            3: '右臂摆动幅度不标准',
        },
        3: {
            4: '右手摆动幅度不标准',
        },
        5: {
            6: '左臂摆动幅度不标准',
        },
        6: {
            7: '左手摆动幅度不标准',
        },
        8: {
            9: '右胯摆动幅度不标准',
            12: '左胯摆动幅度不标准',
        },
        9: {
            10: '右大腿摆动幅度不标准',
        },
        10: {
            11: '右小腿摆动幅度不标准',
        },
        12: {
            13: '左大腿摆动幅度不标准',
        },
        13: {
            14: '左小腿摆动幅度不标准',
        }
    }
    fourcc = getattr(cv2, 'VideoWriter_fourcc')(*'mp4v')
    cap = getattr(cv2, 'VideoCapture')(video_path)
    fps = cap.get(getattr(cv2, 'CAP_PROP_FPS'))
    width = int(cap.get(getattr(cv2, 'CAP_PROP_FRAME_WIDTH')))
    height = int(cap.get(getattr(cv2, 'CAP_PROP_FRAME_HEIGHT')))
    output_path = os.path.join('./evaluation', evaluate_root, video)
    out = getattr(cv2, 'VideoWriter')(output_path, fourcc, fps, (width, height))
    cap.release()
    a_scores = []
    c_scores = []
    t_scores = []
    t_template = []
    evaluation = set()
    start = None
    for (pose, frame, n) in get_pose(frame_gen, config.OPENPOSE_ROOT):
        template, _, status = find_template(pose, task_type)
        if len(action_sequence) > 0:
            if start is None:
                if status == action_sequence[0]:
                    start = n
            else:
                if n < start + status_durations[0] * fps:
                    t_scores.append(status)
                    t_template.append(action_sequence[0])
                else:
                    start = n
                    action_sequence.popleft()
                    status_durations.popleft()
        correct_pose, score, _ = model.run(pose, template)
        c_scores.append(score)
        correct_angle: numpy.ndarray = model.similarity[angle_threshold[:, 0], angle_threshold[:, 1]] > threshold
        a_scores.append(numpy.mean(correct_angle))
        for j in range(correct_angle.shape[0]):
            if not correct_angle[j]:
                evaluation.add(descriptions[angle_threshold[j][0]][angle_threshold[j][1]])
        cv_correct_pose = correct_pose.copy().astype(numpy.int_)
        for t in skeleton_lines:
            getattr(cv2, 'line')(frame, tuple(cv_correct_pose[t[0]]), tuple(cv_correct_pose[t[1]]), (0, 255, 0), 2)
        out.write(frame)
    out.release()
    t_scores = numpy.array(t_scores)
    t_template = numpy.array(t_template)
    if len(action_sequence) > 1:
        evaluation.add('动作时间过短')
    for action in stay_actions:
        key_action = numpy.isin(t_template, action)
        s = numpy.mean(numpy.isin(t_scores[key_action], action))
        if s < 0.5:
            evaluation.add('关键动作停留时间过短')
    c_score = numpy.mean(c_scores)
    t_score = numpy.mean(t_scores == t_template)
    a_score = numpy.mean(a_scores)
    if len(evaluation) == 0:
        evaluation.add('动作标准，请继续保持')
    return numpy.sum(numpy.array([a_score, c_score, t_score]) * numpy.array([0.4, 0.4, 0.2])), '\n'.join(evaluation)
