from os import PathLike
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from numpy import linalg
from torch import nn
from torchvision import transforms, models


class FeatureExtractor(object):
    def __init__(self):
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.model = models.googlenet(pretrained=True)
        self.model = nn.Sequential(*list(self.model.children())[:-2])
        self.model = self.model.cuda().eval()

    def run(self, img: np.ndarray) -> np.ndarray:
        img = Image.fromarray(img)
        img = self.preprocess(img)
        batch = img.unsqueeze(0)
        with torch.no_grad():
            feat = self.model(batch.cuda())
            feat = feat.squeeze().cpu().numpy()

        assert feat.shape == (1024,), f'Invalid feature shape {feat.shape}: expected 1024'
        # normalize frame features
        feat /= linalg.norm(feat) + 1e-10
        return feat


class VideoPreprocessor(object):
    def __init__(self, sample_rate: int) -> None:
        self.model = FeatureExtractor()
        self.sample_rate = sample_rate

    def get_features(self, video_path: PathLike):
        video_path = Path(video_path)
        cap = getattr(cv2, 'VideoCapture')(str(video_path))
        assert cap is not None, f'Cannot open video: {video_path}'

        features = []
        n_frames = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if n_frames % self.sample_rate == 0:
                frame = getattr(cv2, 'cvtColor')(frame, getattr(cv2, 'COLOR_BGR2RGB'))
                feat = self.model.run(frame)
                features.append(feat)

            n_frames += 1

        cap.release()

        features = np.array(features)
        return n_frames, features

    def kts(self, n_frames, features):
        seq_len = len(features)
        picks = np.arange(0, seq_len) * self.sample_rate

        # compute change points using KTS
        kernel = np.matmul(features, features.T)
        change_points, _ = KTS.cpd_auto(kernel, seq_len - 1, 1, verbose=False)
        change_points *= self.sample_rate
        change_points = np.hstack((0, change_points, n_frames))
        begin_frames = change_points[:-1]
        end_frames = change_points[1:]
        change_points = np.vstack((begin_frames, end_frames - 1)).T

        n_frame_per_seg = end_frames - begin_frames
        return change_points, n_frame_per_seg, picks

    def run(self, video_path: PathLike):
        n_frames, features = self.get_features(video_path)
        cps, nfps, picks = self.kts(n_frames, features)
        return n_frames, features, cps, nfps, picks


class KTS:
    @classmethod
    def cpd_auto(cls, K, ncp, vmax, desc_rate=1, **kwargs):
        """Detect change points automatically selecting their number

        :param K: Kernel between each pair of frames in video
        :param ncp: Maximum number of change points
        :param vmax: Special parameter
        :param desc_rate: Rate of descriptor sampling, vmax always corresponds to 1x
        :param kwargs: Extra parameters for ``cpd_nonlin``
        :return: Tuple (cps, costs)
            - cps - best selected change-points
            - costs - costs for 0,1,2,...,m change-points
        """
        m = ncp
        _, scores = cls.cpd_nonlin(K, m, backtrack=False, **kwargs)

        N = K.shape[0]
        N2 = N * desc_rate  # length of the video before down-sampling

        penalties = np.zeros(m + 1)
        # Prevent division by zero (in case of 0 changes)
        ncp = np.arange(1, m + 1)
        penalties[1:] = (vmax * ncp / (2.0 * N2)) * (np.log(float(N2) / ncp) + 1)

        costs = scores / float(N) + penalties
        m_best = np.argmin(costs)
        cps, scores2 = cls.cpd_nonlin(K, m_best, **kwargs)

        return cps, scores2

    @classmethod
    def calc_scatters(cls, K):
        """Calculate scatter matrix: scatters[i,j] = {scatter of the sequence with
        starting frame i and ending frame j}
        """
        n = K.shape[0]
        K1 = np.cumsum([0] + list(np.diag(K)))
        K2 = np.zeros((n + 1, n + 1))
        # TODO: use the fact that K - symmetric
        K2[1:, 1:] = np.cumsum(np.cumsum(K, 0), 1)

        diagK2 = np.diag(K2)

        i = np.arange(n).reshape((-1, 1))
        j = np.arange(n).reshape((1, -1))
        scatters = (
                K1[1:].reshape((1, -1)) - K1[:-1].reshape((-1, 1)) -
                (diagK2[1:].reshape((1, -1)) + diagK2[:-1].reshape((-1, 1)) -
                 K2[1:, :-1].T - K2[:-1, 1:]) /
                ((j - i + 1).astype(np.float32) + (j == i - 1).astype(np.float32))
        )
        scatters[j < i] = 0

        return scatters

    @classmethod
    def cpd_nonlin(cls, K, ncp, lmin=1, lmax=100000, backtrack=True, verbose=True,
                   out_scatters=None):
        """Change point detection with dynamic programming

        :param K: Square kernel matrix
        :param ncp: Number of change points to detect (ncp >= 0)
        :param lmin: Minimal length of a segment
        :param lmax: Maximal length of a segment
        :param backtrack: If False - only evaluate objective scores (to save memory)
        :param verbose: If true, print verbose message
        :param out_scatters: Output scatters
        :return: Tuple (cps, obj_vals)
            - cps - detected array of change points: mean is thought to be constant
                on [ cps[i], cps[i+1] )
            - obj_vals - values of the objective function for 0..m changepoints
        """
        m = int(ncp)  # prevent numpy.int64

        n, n1 = K.shape
        assert n == n1, 'Kernel matrix awaited.'
        assert (m + 1) * lmin <= n <= (m + 1) * lmax
        assert 1 <= lmin <= lmax

        if verbose:
            print('Precomputing scatters...')
        J = cls.calc_scatters(K)

        if out_scatters is not None:
            out_scatters[0] = J

        if verbose:
            print('Inferring best change points...')
        # I[k, l] - value of the objective for k change-points and l first frames
        I: np.ndarray = 1e101 * np.ones((m + 1, n + 1))
        I[0, lmin:lmax] = J[0, lmin - 1:lmax - 1]

        if backtrack:
            # p[k, i] --- 'previous change' --- best t[k] when t[k+1] equals i
            p = np.zeros((m + 1, n + 1), dtype=int)
        else:
            p = np.zeros((1, 1), dtype=int)

        for k in range(1, m + 1):
            for i in range((k + 1) * lmin, n + 1):
                tmin = max(k * lmin, i - lmax)
                tmax = i - lmin + 1
                c = J[tmin:tmax, i - 1].reshape(-1) + \
                    I[k - 1, tmin:tmax].reshape(-1)
                I[k, i] = np.min(c)
                if backtrack:
                    p[k, i] = np.argmin(c) + tmin

        # Collect change points
        cps = np.zeros(m, dtype=int)

        if backtrack:
            cur = n
            for k in range(m, 0, -1):
                cps[k - 1] = p[k, cur]
                cur = cps[k - 1]

        scores = I[:, n].copy()
        scores[scores > 1e99] = np.inf
        return cps, scores
