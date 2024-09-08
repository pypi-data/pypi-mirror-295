import csv
import glob
import os
import random

import numpy as np


def IOU(ann, centroids):
    w, h = ann
    similarities = []

    for centroid in centroids:
        c_w, c_h = centroid

        if c_w >= w and c_h >= h:
            similarity = w * h / (c_w * c_h)
        elif c_w >= w and c_h <= h:
            similarity = w * c_h / (w * h + (c_w - w) * c_h)
        elif c_w <= w and c_h >= h:
            similarity = c_w * h / (w * h + c_w * (c_h - h))
        else:  # means both w,h are bigger than c_w and c_h respectively
            similarity = (c_w * c_h) / (w * h)
        similarities.append(similarity)  # will become (k,) shape

    return np.array(similarities)


def avg_IOU(anns, centroids):
    n, d = anns.shape
    sum = 0.0

    for i in range(anns.shape[0]):
        sum += max(IOU(anns[i], centroids))

    return sum / n


def print_anchors(centroids):
    anchors = centroids.copy()

    widths = anchors[:, 0]
    sorted_indices = np.argsort(widths)

    r = "anchors: ["
    for i in sorted_indices[:-1]:
        r += f"{anchors[i, 0]:0.2f},{anchors[i, 1]:0.2f}, "

    # there should not be comma after last anchor, that's why
    r += "{:0.2f},{:0.2f}".format(
        anchors[sorted_indices[-1:], 0], anchors[sorted_indices[-1:], 1]
    )
    r += "]"

    print(r)


def run_kmeans(ann_dims, anchor_num):
    ann_num = ann_dims.shape[0]
    prev_assignments = np.ones(ann_num) * (-1)
    iteration = 0
    old_distances = np.zeros((ann_num, anchor_num))

    indices = [random.randrange(ann_dims.shape[0]) for i in range(anchor_num)]
    centroids = ann_dims[indices]
    anchor_dim = ann_dims.shape[1]

    while True:
        distances = []
        iteration += 1
        for i in range(ann_num):
            d = 1 - IOU(ann_dims[i], centroids)
            distances.append(d)
        distances = np.array(
            distances
        )  # distances.shape = (ann_num, anchor_num)

        print(
            f"iteration {iteration}: dists = {np.sum(np.abs(old_distances-distances))}"
        )

        # assign samples to centroids
        assignments = np.argmin(distances, axis=1)

        if (assignments == prev_assignments).all():
            return centroids

        # calculate new centroids
        centroid_sums = np.zeros((anchor_num, anchor_dim), np.float)
        for i in range(ann_num):
            centroid_sums[assignments[i]] += ann_dims[i]
        for j in range(anchor_num):
            centroids[j] = centroid_sums[j] / (np.sum(assignments == j) + 1e-6)

        prev_assignments = assignments.copy()
        old_distances = distances.copy()


def main():
    CSVDir = "/data/u934/service_imagerie/v_kapoor/FinalONEATTraining/Bin2OYoloneatV1/"
    Csv_path = os.path.join(CSVDir, "*csv")
    filesCsv = glob.glob(Csv_path)
    filesCsv.sort
    num_anchors = 5

    # run k_mean to find the anchors
    annotation_dims = []
    for csvfname in filesCsv:

        with open(csvfname) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for train_vec in reader:

                arr = [float(s) for s in train_vec[0:]]
        train_vec = arr

        relative_w = float(train_vec[6])
        relative_h = float(train_vec[7])

        annotation_dims.append(tuple(map(float, (relative_w, relative_h))))

    annotation_dims = np.array(annotation_dims)
    centroids = run_kmeans(annotation_dims, num_anchors)

    # write anchors to file
    print(
        "\naverage IOU for",
        num_anchors,
        "anchors:",
        "%0.2f" % avg_IOU(annotation_dims, centroids),
    )
    print_anchors(centroids)


if __name__ == "__main__":

    main()
