"""
@Author: Wenfeng Zhou
"""
import cv2
import torch

from src.models.keyframe.framework.model import PGL_SUM
from src.models.keyframe.utils.summary import generate_summary
from src.models.keyframe.utils.video import VideoPreprocessor


def keyframe(video_path, use_model=False, rate=0.5, fps=30):
    """
    关键帧提取

    :param use_model: 模型
    :param video_path: 视频路径
    :param rate: 采样率
    :param fps: 帧率
    :return:
    """
    if use_model:
        video_processor = VideoPreprocessor(int(fps * rate))
        n_frames, features, cps, n_fps, picks = video_processor.run(video_path)
        model = PGL_SUM(input_size=1024, output_size=1024, num_segments=4, heads=8,
                        fusion="add", pos_enc="absolute")
        model.load_state_dict(torch.load('./models/keyframe/keyframe.pt'))
        model.eval()
        with torch.no_grad():
            scores, _ = model(torch.Tensor(features).view(-1, 1024))
            scores = scores.squeeze(0).cpu().numpy().tolist()
            summary = generate_summary([cps], [scores], [n_frames], [picks])[0]
        cap = getattr(cv2, 'VideoCapture')(video_path)
        for i in range(len(summary)):
            if summary[i]:
                cap.set(getattr(cv2, 'CAP_PROP_POS_FRAMES'), i)
                _, frame = cap.read()
                yield frame, i
        cap.release()
    else:
        cap = getattr(cv2, 'VideoCapture')(video_path)
        v_fps = cap.get(getattr(cv2, 'CAP_PROP_FPS'))
        step = int(v_fps * rate)
        n = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if n % step == 0:
                yield frame, n
            n += 1
        cap.release()
