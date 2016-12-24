import numpy as np


class Node:
    def __init__(self, i):
        self.i = i
        self.children = {}
        self.is_leaf = False
        self.value = None

    def __call__(self, x):
        if self.is_leaf:
            return self.value
        else:
            label = x[self.i]
            return self.children[self._classify_value(self.children.keys(), label)].value

    def find_child_by_threshold(self, label):
        labels = sorted(list(self.children.keys()))
        # print("length = " + repr(len(labels)))
        intervals = {}
        for i in range(0, len(labels) - 1, 1):
            i = int(i)
            if i is 0:
                d = (labels[i + 1] - labels[i]) / 2
                intervals[labels[i]] = (int(labels[i] - d / 2), int(labels[i] + d / 2))
            else:

                if i is (len(labels) - 1):
                    d = int(labels[i] - (intervals[i - 1][1]))
                    intervals[labels[i]] = (int(intervals[labels[i - 1][1]]), int(labels[i] + d))
                else:
                    midpoint = int((labels[i]) + ((labels[i + 1] - labels[i]) / 2))
                    intervals[labels[i]] = (intervals[labels[i - 1]][1], midpoint)
        for v, (inf, sup) in intervals.items():
            if (label >= inf) and (label <= sup):
                return v

    def find_child_by_threshold3(self, label):
        labels = sorted(list(self.children.keys()))
        for i in range(0, len(labels), 1):
            i = int(i)

    def find_child_by_threshold2(self, label):
        variance = np.variance(self.children.keys())
        for v in self.children.keys():
            if (label >= v - variance) and (label <= v + variance):
                return v
            else:
                return self.largest_child()

    def largest_child(self):
        ret = None
        for v, (xv, yv) in self.children.items():
            if ret is None:
                ret = v
            else:
                if len(xv) > len(self.children[ret]):
                    ret = v
        return ret

    def assign_child(self, i_value, childNode):
        self.children[i_value] = childNode

    def assign_value(self, value):
        self.value = value
        self.is_leaf = True

    def has_label(self, v):
        if v in self.children.keys():
            return True
        return False

    @staticmethod
    def _classify_value(values, v):
        if v <= values[0]:
            return values[0]
        if v >= values[len(values) - 1]:
            return values[len(values) - 1]
        for i in range(1, len(values), 1):
            if (v <= values[i]) and (v >= values[i - 1]):
                return values[i]
