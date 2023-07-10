"""
@Author: Wenfeng Zhou
"""
import numpy


class Correct:
    """
    矫正模型
    """

    def __init__(self, k=0.1):
        """
        初始化

        :param k: k值
        """
        self.e = None
        self.e2 = None
        self.e1 = None
        self.similarity = None
        self.feature = None
        self.template = None
        self.skeleton = None
        self.k = k

    def get_feature(self):
        """
        获取特征

        :return:
        """
        n = self.skeleton.shape[0]
        feature = numpy.zeros((n, n, 2), dtype=numpy.float32)
        for i in range(n):
            for j in range(n):
                feature[i, j] = self.skeleton[j] - self.skeleton[i]
        return feature

    def get_similarity(self):
        """
        获取相似度

        :return:
        """
        n = self.skeleton.shape[0]
        similarity = numpy.ones((n, n), dtype=numpy.float32)
        for i in range(n):
            for j in range(n):
                mod_feature = numpy.linalg.norm(self.feature[i, j])
                mod_template = numpy.linalg.norm(self.template[i, j])
                if not (mod_feature == 0 or mod_template == 0):
                    similarity[i, j] = numpy.dot(self.feature[i, j], self.template[i, j]) / (
                            mod_feature * mod_template)
        return similarity

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
        return numpy.sum(numpy.abs((t - self.similarity) / t), axis=1)

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
        return numpy.sum(numpy.abs((outlier - self.similarity) / outlier), axis=0)

    def run(self, skeleton, template):
        """
        运行

        :param skeleton: 骨骼
        :param template: 模板
        :return:
        """
        self.skeleton = skeleton
        self.template = template
        self.feature = self.get_feature()
        self.similarity = self.get_similarity()
        self.e1 = self.get_e1()
        self.e2 = self.get_e2()
        self.e = self.e1 + self.e2
        correct = self.e < self.k
        m = numpy.sum(correct)
        n = self.skeleton.shape[0]
        if not m == 0:
            return numpy.sum(
                numpy.repeat(numpy.expand_dims(self.skeleton[correct], axis=1), n, axis=1) + self.template[correct],
                axis=0) / m, m / n, self.e
        else:
            return (numpy.repeat(numpy.expand_dims(self.skeleton[[0]], axis=1), n, axis=1) + self.template[0]).reshape(
                n, 2), 0, self.e
