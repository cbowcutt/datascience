import numpy as np
import statistics

class Dataset:

    def __init__(self):
        pass

def partition_by_attribute(x, y, i):
    attribute_values = set()
    [attribute_values.add(xi[i]) for xi in x]
    vs = np.linspace(min(attribute_values), max(attribute_values), 3)
    partitions = {}
    for example, label in zip(x, y):
        v = classify_value(vs, example[i])
        if v not in partitions.items():
            partitions[v] = ([], [])
        partitions[v][0].append(example)
        partitions[v][1].append(label)
    return partitions


def entropy2(x, y, i):
    attribute_values = set()
    [attribute_values.add(xi[i]) for xi in x]
    inf = min(attribute_values)
    sup = max(attribute_values)
    attribute_values = np.linspace(inf, sup, 3)
    label_values = set()
    [label_values.add(yi) for yi in y]
    size = float(len(x))
    e = 0.0
    attribute_value_count = {}
    label_count = {}
    for v in attribute_values:
        true_v = classify_value(attribute_values, v)
        attribute_value_count[true_v] = 0.0
        for a in label_values:
            label_count[true_v, a] = 0.0

    for xi, yi in zip(x, y):
        v = classify_value(attribute_values, xi[i])
        label_count[v, yi] += 1
        attribute_value_count[v] += 1

    for (label, label2), p in label_count.items():
        try:
            proportion = float(p) / float(attribute_value_count[label])
            if proportion > 0:
                e -= np.log2(proportion) * proportion
        except ZeroDivisionError:
            continue
    return e


def highest_information_gain(x, y, k_attributes):
    entropies = {i: entropy2(x, y, i) for i in k_attributes}
    smallest = None
    for i in k_attributes:
        if smallest is None or entropies[i] < entropies[smallest]:
            smallest = i
    return smallest


def most_common_label(y):
    try:
        return statistics.mode(y)
    except statistics.StatisticsError:
        return y[0]


def classify_value(values, v):
    if v <= values[0]:
        return values[0]
    if v >= values[len(values) - 1]:
        return values[len(values) - 1]
    for i in range(1, len(values), 1):
        if (v <= values[i]) and (v >= values[i - 1]):
            return values[i]