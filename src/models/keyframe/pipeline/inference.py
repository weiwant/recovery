# -*- coding: utf-8 -*-

import cv2
import torch

from src.models.keyframe.framework.model import PGL_SUM
from src.models.keyframe.utils.config import get_config
from src.models.keyframe.utils.summary import generate_summary
from src.models.keyframe.utils.video import VideoPreprocessor


def main(args):
    models_path = args["model"]
    video_path = args["video_path"]
    output_path = args["output_path"]
    sample_rate = args["sample_rate"]
    video_processor = VideoPreprocessor(sample_rate)
    n_frames, features, cps, nfps, picks = video_processor.run(video_path)
    trained_model = PGL_SUM(input_size=1024, output_size=1024, num_segments=4, heads=8,
                            fusion="add", pos_enc="absolute")
    trained_model.load_state_dict(torch.load(models_path))
    trained_model.eval()
    with torch.no_grad():
        scores, _ = trained_model(torch.Tensor(features).view(-1, 1024))
        scores = scores.squeeze(0).cpu().numpy().tolist()
        summary = generate_summary([cps], [scores], [n_frames], [picks])[0]
    cap = getattr(cv2, "VideoCapture")(video_path)
    width = int(cap.get(getattr(cv2, "CAP_PROP_FRAME_WIDTH")))
    height = int(cap.get(getattr(cv2, "CAP_PROP_FRAME_HEIGHT")))
    fps = cap.get(getattr(cv2, "CAP_PROP_FPS"))

    # create summary video writer
    fourcc = getattr(cv2, "VideoWriter_fourcc")(*"mp4v")
    out = getattr(cv2, "VideoWriter")(output_path, fourcc, fps, (width, height))

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if summary[frame_idx]:
            out.write(frame)

        frame_idx += 1

    out.release()
    cap.release()


if __name__ == "__main__":
    config = get_config(config_mode='infer')
    main(config)
