import numpy as np
import random
from ..decisiontree.Node import Node
from ..dataset.Dataset import highest_information_gain
from ..dataset.Dataset import partition_by_attribute
from ..dataset.Dataset import most_common_label


class RandomForest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.d = x.shape[1]
        self.k = int(np.log2(self.d))

    def ensemble(self, n):
        return [self.construct_tree() for i in range(0, n)]

    def remove_features(self, to_remove, available_features):
        available_features_copy = available_features.copy()
        for x in to_remove:
            available_features_copy.remove(x)
        return available_features_copy

    def select_random_features(self, k, available_features):
        k_features = set()
        if len(available_features) <= k:
            return available_features
        for i in range(0, k):
            # try:
                k_features.add(random.sample(available_features, 1)[0])
            # except statistics.StatisticsError:
        return k_features

    def construct_tree(self):
        x, y = self.bag_set(self.x, self.y)
        available_features = set()
        for i in range(0, self.d, 1):
            available_features.add(i)
        k_attributes = self.select_random_features(self.k, available_features)
        available_features = self.remove_features(k_attributes, available_features)
        return self._id3(x, y, k_attributes, available_features)

    def bag_set(self, x, y):
        m = int(self.d * 0.38)
        sx = []
        sy = []
        sample_indices = random.sample(range(0, len(x)), m)
        for i in sample_indices:
            sx.append(x[i])
            sy.append(y[i])
        return sx, sy

    def construct_sets(self, t):
        sets = []
        for i in range(0, t):
            available_features = range(0, self.d)
            I = []
            for j in range(0, self.k):
                random.shuffle(available_features)
                I.append(available_features.pop())
            sets.append(I)
        return sets

    def _id3(self, x, y, k_attributes, available_features):
        if len(set(y)) is 1:
            node = Node(None)
            node.assign_value(y[0])
            return node
        else:
            A = highest_information_gain(x, y, k_attributes)
            root = Node(A)
            partitions = partition_by_attribute(x, y, A)
            for (v, (xv, yv)) in partitions.items():
                node = Node(v)
                if len(xv) is 0:
                    node.assign_value(most_common_label(y))
                    root.assign_child(v, node)
                else:
                    k_attributes = self.select_random_features(self.k, available_features)
                    available_features = self.remove_features(k_attributes, available_features)
                    node = self._id3(xv, yv, k_attributes, available_features)
                    root.assign_child(v, node)
            return root




