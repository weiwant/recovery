import os

import numpy


def feature_hash(feature: numpy.ndarray):
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
    return (numpy.abs(cos) > numpy.sqrt(2) / 2).astype(numpy.int32).reshape((64,))


def save_template(feature, mission_type, status):
    """
    保存模板

    :param feature: 特征
    :param mission_type: 任务类型
    :param status: 动作状态
    :return:
    """
    hash_array = feature_hash(feature)
    numpy.save(
        os.path.join('./templates', mission_type,
                     format(int(''.join(hash_array.astype(str)), 2), '0>16x') + '_' + str(status)),
        feature)


def find_template(feature, mission_type=None):
    """
    寻找模板

    :param feature: 特征
    :param mission_type: 任务类型
    :return:
    """
    hash_array = feature_hash(feature)
    names = []
    if mission_type is None:
        for t in os.listdir('./templates'):
            names.extend([os.path.join('./templates', t, f) for f in os.listdir(os.path.join('./templates', t))])
    else:
        names.extend([os.path.join('./templates', mission_type, f) for f in
                      os.listdir(os.path.join('./templates', mission_type))])
    template = max(names, key=lambda x: numpy.sum(
        hash_array == numpy.array(list(format(int(os.path.basename(x)[:16], 16), '0>64b')), dtype=numpy.int32)))
    return numpy.load(template)
