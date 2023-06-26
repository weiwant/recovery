import os
from typing import Union

import numpy


class Correct:
    """
    矫正模型
    """

    def __init__(self, skeleton_gen=None, k=0.1, mission_type=None, labels=None, iterations=10, step=0.1):
        """
        初始化

        :param skeleton_gen: 骨架生成器
        :param k: k值
        :param mission_type: 任务类型
        :param labels: 标签
        :param iterations: 迭代次数
        :param step: 步长
        """
        self.gen = skeleton_gen
        self.feature = numpy.zeros((15, 15, 2), dtype=numpy.float32)
        self.similarity = numpy.ones((15, 15), dtype=numpy.float32)
        self.template = numpy.zeros((15, 15, 2), dtype=numpy.float32)
        self.skeleton = None
        self.e1 = None
        self.e2 = None
        self.e = None
        self.k = k
        self.labels = labels
        self.iterations = iterations
        self.step = step
        self.tp = numpy.zeros((2 * iterations,), dtype=numpy.int32)
        self.fp = numpy.zeros((2 * iterations,), dtype=numpy.int32)
        self.tn = numpy.zeros((2 * iterations,), dtype=numpy.int32)
        self.fn = numpy.zeros((2 * iterations,), dtype=numpy.int32)
        self.f1 = numpy.zeros((2 * iterations,), dtype=numpy.float32)
        self.mission_type: Union[str, None] = mission_type

    def get_feature(self):
        """
        获取特征

        :return:
        """
        result = next(self.gen, None)
        if result is None:
            return None
        else:
            self.skeleton = result
            feature = numpy.zeros(self.feature.shape, dtype=numpy.float32)
            for i in range(self.skeleton.shape[0]):
                for j in range(self.skeleton.shape[0]):
                    feature[i, j] = self.skeleton[j] - self.skeleton[i]
            return feature

    @classmethod
    def feature_hash(cls, feature: numpy.ndarray):
        """
        特征哈希

        :param feature: 特征
        :return:
        """
        joints = [2, 3, 5, 6, 9, 10, 12, 13]
        ends = [0, 1, 4, 7, 11, 14, 8]
        joint_end = feature[joints][:, ends]
        angle = feature[joints][numpy.repeat(numpy.arange(8), 2), [1, 3, 2, 4, 1, 6, 5, 7, 8, 10, 9, 11, 8, 13, 12, 14]]
        angle = angle.reshape((8, 2, 2))
        vectors = numpy.concatenate((joint_end, angle), axis=1)
        a = vectors[:, :8]
        b = vectors[:, -8:]
        cos = numpy.sum(a * b, axis=2) / (numpy.linalg.norm(a, axis=2) * numpy.linalg.norm(b, axis=2))
        return (cos > 0).astype(numpy.int32).reshape((64,))

    @classmethod
    def save_template(cls, feature, mission_type):
        """
        保存模板

        :param feature:
        :param mission_type:
        :return:
        """
        feature_hash = cls.feature_hash(feature)
        numpy.save(
            os.path.join('./templates', mission_type, format(int(''.join(feature_hash.astype(str)), 2), '0>16x')),
            feature)

    def find_template(self):
        """
        寻找模板

        :return:
        """
        feature_hash = self.feature_hash(self.feature)
        names = []
        if self.mission_type is None:
            for t in os.listdir('./templates'):
                names.extend(os.listdir(os.path.join('./templates', t)))
        else:
            names.extend(os.listdir(os.path.join('./templates', self.mission_type)))
        template = max(names, key=lambda x: numpy.sum(
            feature_hash == numpy.array(list(format(int(x[:16], 16), '0>64b')), dtype=numpy.int32)))
        return numpy.load(os.path.join('./templates', self.mission_type, template))

    def get_similarity(self):
        """
        获取相似度

        :return:
        """
        self.template = self.find_template()
        for i in range(self.feature.shape[0]):
            for j in range(self.feature.shape[0]):
                mod_feature = numpy.linalg.norm(self.feature[i, j])
                mod_template = numpy.linalg.norm(self.template[i, j])
                if not (mod_feature == 0 or mod_template == 0):
                    self.similarity[i, j] = numpy.dot(self.feature[i, j], self.template[i, j]) / (
                            mod_feature * mod_template)

    def get_e1(self):
        """
        获取e1

        :return:
        """
        n = self.similarity.shape[0]
        temp = numpy.copy(self.similarity)
        temp[numpy.eye(n, dtype=numpy.bool_)] = 0
        a = numpy.sum(self.similarity, axis=1) / (n - 1)
        A = numpy.sum(a) / n
        S = numpy.sqrt(numpy.sum((a - A) ** 2) / n)
        t = A - S
        self.e1 = numpy.sum(numpy.abs((t - self.similarity) / t), axis=1)

    def get_e2(self):
        """
        获取e2

        :return:
        """
        n = self.similarity.shape[0]
        p3_4 = int(3 * (n + 1) / 4) - 1
        p1_4 = int((n + 1) / 4) - 1
        IQR = self.similarity[:, p3_4] - self.similarity[:, p1_4]
        outlier = self.similarity[:, p1_4] - 1.5 * IQR
        self.e2 = numpy.sum(numpy.abs((outlier - self.similarity) / outlier), axis=0)

    def predict(self, gen, mission_type):
        """
        预测

        :param gen: 骨架生成器
        :param mission_type: 任务id
        :return:
        """
        self.gen = gen
        self.mission_type = mission_type
        self.feature = self.get_feature()
        while self.feature is not None:
            self.get_similarity()
            self.get_e1()
            self.get_e2()
            self.e = self.e1 + self.e2
            correct = self.e < self.k
            m = numpy.sum(correct)
            n = self.skeleton.shape[0]
            yield numpy.sum(
                numpy.repeat(numpy.expand_dims(self.skeleton[correct], axis=1), n, axis=1) + self.template[correct],
                axis=0) / m, m / n
            self.feature = self.get_feature()

    def train(self):
        """
        训练

        :return:
        """
        if self.labels is None:
            raise Exception('Labels is None')
        self.feature = self.get_feature()
        label_gen = iter(self.labels)
        step = self.k / self.iterations
        while self.feature is not None:
            self.get_similarity()
            self.get_e1()
            self.get_e2()
            self.e = self.e1 + self.e2
            k = 0
            k_right = self.k
            labels = next(label_gen)
            for i in range(self.iterations):
                correct = self.e < k
                self.tp[i] += numpy.sum(correct & labels)
                self.fp[i] += numpy.sum(correct & ~labels)
                self.tn[i] += numpy.sum(~correct & ~labels)
                self.fn[i] += numpy.sum(~correct & labels)
                self.f1[i] = 2 * self.tp[i] / (2 * self.tp[i] + self.fp[i] + self.fn[i])
                k += step
                correct = self.e < k_right
                self.tp[i + self.iterations] += numpy.sum(correct & labels)
                self.fp[i + self.iterations] += numpy.sum(correct & ~labels)
                self.tn[i + self.iterations] += numpy.sum(~correct & ~labels)
                self.fn[i + self.iterations] += numpy.sum(~correct & labels)
                self.f1[i + self.iterations] = 2 * self.tp[i + self.iterations] / (
                        2 * self.tp[i + self.iterations] + self.fp[i + self.iterations] + self.fn[i + self.iterations])
                k_right += self.step
            self.feature = self.get_feature()
        best = self.f1.argmax()
        self.k = numpy.min(best, self.iterations) * step + numpy.max(0, best - self.iterations) * self.step

    def retrain(self, gen, mission_type, labels):
        """
        重新训练

        :param gen: 骨架生成器
        :param mission_type: 任务类型
        :param labels: 标签
        :return:
        """
        self.gen = gen
        self.mission_type = mission_type
        self.tp = numpy.zeros((2 * self.iterations,), dtype=numpy.int32)
        self.fp = numpy.zeros((2 * self.iterations,), dtype=numpy.int32)
        self.tn = numpy.zeros((2 * self.iterations,), dtype=numpy.int32)
        self.fn = numpy.zeros((2 * self.iterations,), dtype=numpy.int32)
        self.labels = labels
        self.train()
