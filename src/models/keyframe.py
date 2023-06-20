import numpy
from scipy.signal import find_peaks, peak_widths
from sklearn.ensemble import RandomForestClassifier


class KeyFrame:
    """
    关键帧提取模型
    """

    def __init__(self, frame_gen=None, labels=None, **kwargs):
        """
        初始化

        :param frame_gen: 帧生成器
        :param labels: 标签
        :param kwargs: 随机森林参数
        """
        if frame_gen is not None:
            self.gen = frame_gen
            result = next(frame_gen)
            frame_num = result[2]
            skeleton = result[0]
            self.difference = numpy.zeros((int(frame_num), 8), dtype=numpy.float32)
            self.weight = numpy.zeros((int(frame_num),), dtype=numpy.float32)
            self.distance = numpy.zeros((int(frame_num),), dtype=numpy.float32)
            self.last_frame_feature = self.get_feature(skeleton)
            self.last_frame_angle = self.get_angle(self.last_frame_feature)
            self.frame_num = int(frame_num)
        if labels is not None:
            self.labels = labels
        self.model = RandomForestClassifier(**kwargs)

    def predict(self, frame_gen):
        """
        预测

        :param frame_gen: 帧生成器
        :return:
        """
        result = next(frame_gen)
        self.reset(result[2], result[0])
        result = next(frame_gen, None)
        while result is not None:
            self.next_frame(result[0], result[1])
            result = next(frame_gen, None)
        X = numpy.concatenate((self.difference, numpy.expand_dims(self.distance, axis=1),
                               numpy.expand_dims(self.weight, axis=1)), axis=1)
        return self.model.predict(X)

    def train(self):
        """
        训练模型

        :return:
        """
        if self.labels is None:
            raise ValueError('No labels')
        if self.gen is None:
            raise ValueError('No frame generator')
        result = next(self.gen, None)
        while result is not None:
            self.next_frame(result[0], result[1])
            result = next(self.gen, None)
        X = numpy.concatenate((self.difference, numpy.expand_dims(self.distance, axis=1),
                               numpy.expand_dims(self.weight, axis=1)), axis=1)
        self.model.fit(X, self.labels)

    def retrain(self, frame_gen, labels):
        """
        重新训练

        :param frame_gen:
        :param labels:
        :return:
        """
        self.labels = labels
        self.gen = frame_gen
        result = next(frame_gen)
        self.reset(result[2], result[0])
        self.train()

    def reset(self, frame_num, skeleton, labels=None):
        """
        重置

        :param frame_num: 帧数
        :param skeleton: 骨架
        :param labels: 标签
        :return:
        """
        self.difference = numpy.zeros((int(frame_num), 8), dtype=numpy.float32)
        self.weight = numpy.zeros((int(frame_num),), dtype=numpy.float32)
        self.distance = numpy.zeros((int(frame_num),), dtype=numpy.float32)
        self.last_frame_feature = self.get_feature(skeleton)
        self.last_frame_angle = self.get_angle(self.last_frame_feature)
        self.frame_num = int(frame_num)
        self.labels = labels

    @classmethod
    def get_angle(cls, feature):
        """
        获取角度

        :param feature: 特征
        :return: 角度
        """
        angle = numpy.zeros((8,), dtype=numpy.float32)
        for i in range(8):
            v1 = feature[6, i, :]
            v2 = feature[8, i, :]
            mod_v1 = numpy.linalg.norm(v1)
            mod_v2 = numpy.linalg.norm(v2)
            if not (mod_v1 == 0 or mod_v2 == 0):
                angle[i] = numpy.arccos(numpy.dot(v1, v2) / (mod_v1 * mod_v2))
        return angle

    @classmethod
    def get_feature(cls, skeleton):
        """
        获取特征

        :param skeleton: 骨架
        :return:
        """
        feature = numpy.zeros((9, 8, 2), dtype=numpy.float32)
        joints = [2, 3, 5, 6, 9, 10, 12, 13]
        ends = [0, 1, 4, 7, 11, 14]
        v1 = [(1, 2), (2, 3), (1, 5), (5, 6), (8, 9), (9, 10), (8, 12), (12, 13)]
        v2 = [(3, 2), (4, 3), (6, 5), (7, 6), (10, 9), (11, 10), (13, 12), (14, 13)]
        v3 = [(4, 2), (3, 1), (7, 5), (6, 1), (11, 9), (10, 8), (14, 12), (13, 8)]
        for i in range(6):
            for j in range(8):
                feature[i, j, :] = skeleton[joints[j]] - skeleton[ends[i]]
        for i in range(8):
            feature[6, i, :] = skeleton[v1[i][0]] - skeleton[v1[i][1]]
            feature[7, i, :] = skeleton[v3[i][0]] - skeleton[v3[i][1]]
            feature[8, i, :] = skeleton[v2[i][0]] - skeleton[v2[i][1]]
        return feature

    @classmethod
    def diff_hash(cls, feature):
        """
        获取hash值

        :param feature:
        :return:
        """
        hash_code = numpy.ones((8, 8), dtype=numpy.float32)
        for i in range(1, 9):
            for j in range(8):
                p1 = feature[i - 1, j, :]
                p2 = feature[i, j, :]
                mod_p1 = numpy.linalg.norm(p1)
                mod_p2 = numpy.linalg.norm(p2)
                if not (mod_p1 == 0 or mod_p2 == 0):
                    hash_code[i - 1, j] = numpy.dot(p1, p2) / (mod_p1 * mod_p2)
        return (hash_code > 0).astype(numpy.int32).reshape((64,))

    @classmethod
    def get_distance(cls, feature1, feature2):
        """
        获取距离

        :param feature1: 特征1
        :param feature2: 特征2
        :return:
        """
        a = cls.diff_hash(feature1)
        b = cls.diff_hash(feature2)
        difference = numpy.sum(a != b) / 64
        min_distance = numpy.min(difference)
        max_distance = numpy.max(difference)
        if max_distance - min_distance > 0:
            return (difference - min_distance) / (max_distance - min_distance)
        else:
            return difference

    def get_weight(self):
        """
        获取权重

        :return:
        """
        for i in range(8):
            angle = self.difference[:, i]
            peaks, _ = find_peaks(angle)
            window = numpy.diff(peaks)
            result = peak_widths(angle, peaks, wlen=numpy.median(window).item())
            left = numpy.floor(result[2]).astype(numpy.int32)
            right = numpy.ceil(result[3]).astype(numpy.int32)
            w = (right - left) / self.frame_num
            for j in range(len(peaks)):
                self.weight[left[j]:right[j] + 1] += w[j]
            min_weight = numpy.min(self.weight)
            max_weight = numpy.max(self.weight)
            if max_weight - min_weight > 0:
                self.weight = (self.weight - min_weight) / (max_weight - min_weight)

    def next_frame(self, skeleton, frame_index):
        """
        下一帧

        :param skeleton: 骨架
        :param frame_index: 帧索引
        :return:
        """
        feature = self.get_feature(skeleton)
        angle = self.get_angle(feature)
        frame_index = int(frame_index)
        self.difference[frame_index, :] = angle - self.last_frame_angle
        self.distance[frame_index] = self.get_distance(feature, self.last_frame_feature)
        self.last_frame_feature = feature
        self.last_frame_angle = angle
        if frame_index == self.frame_num - 1:
            self.get_weight()
