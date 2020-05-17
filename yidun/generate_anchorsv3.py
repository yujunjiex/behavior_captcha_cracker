# -*- coding: utf-8 -*-
"""通过聚类算法生成yolov3 anchors初始预选框位置"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np
import os
import random
from tqdm import tqdm
import sklearn.cluster as cluster


def iou(x, centroids):
    dists = []
    for centroid in centroids:
        c_w, c_h = centroid
        w, h = x
        if c_w >= w and c_h >= h:
            dist = w * h / (c_w * c_h)
        elif c_w >= w and c_h <= h:
            dist = w * c_h / (w * h + (c_w - w) * c_h)
        elif c_w <= w and c_h >= h:
            dist = c_w * h / (w * h + c_w * (c_h - h))
        else:  # means both w,h are bigger than c_w and c_h respectively
            dist = (c_w * c_h) / (w * h)
        dists.append(dist)
    return np.array(dists)


def avg_iou(x, centroids):
    n, d = x.shape
    sums = 0.
    for i in range(x.shape[0]):
        # note IOU() will return array which contains IoU for each centroid and X[i]
        # slightly ineffective, but I am too lazy
        sums += max(iou(x[i], centroids))
    return sums / n


def write_anchors_to_file(centroids, distance, anchor_file):
    # anchors = centroids * 416 / 32      # I do not know whi it is 416/32

    anchors = centroids * 416
    anchors = [str(i) for i in anchors.ravel()]
    print(
        "\n",
        "Cluster Result:\n",
        "Clusters:", len(centroids), "\n",
        "Average IoU:", distance, "\n",
        "Anchors:\n",
        ", ".join(anchors)
    )

    with open(anchor_file, 'w') as f:
        f.write(", ".join(anchors))
        f.write('\n%f\n' % distance)


def k_means(x, n_clusters, eps):
    init_index = [random.randrange(x.shape[0]) for _ in range(n_clusters)]
    centroids = x[init_index]

    d = old_d = []
    iterations = 0
    diff = 1e10
    c, dim = centroids.shape

    while True:
        iterations += 1
        d = np.array([1 - iou(i, centroids) for i in x])
        if len(old_d) > 0:
            diff = np.sum(np.abs(d - old_d))

        print('diff = %f' % diff)

        if diff < eps or iterations > 1000:
            print("Number of iterations took = %d" % iterations)
            print("Centroids = ", centroids)
            return centroids

        # assign samples to centroids
        belonging_centroids = np.argmin(d, axis=1)

        # calculate the new centroids
        centroid_sums = np.zeros((c, dim), np.float)
        for i in range(belonging_centroids.shape[0]):
            centroid_sums[belonging_centroids[i]] += x[i]

        for j in range(c):
            centroids[j] = centroid_sums[j] / \
                np.sum(belonging_centroids == j)

        old_d = d.copy()


def get_file_content(fnm):
    with open(fnm) as f:
        return [line.strip() for line in f]


def main(args):
    print("Reading Data ...")

    file_list = []
    for f in args.file_list:
        file_list.extend(get_file_content(f))

    data = []
    for one_file in tqdm(file_list):
        one_file = one_file.replace('images', 'labels') \
            .replace('JPEGImages', 'labels') \
            .replace('.png', '.txt') \
            .replace('.jpg', '.txt')
        # print("one_file is:\n",one_file)
        for line in get_file_content(one_file):
            clazz, xx, yy, w, h = line.split()
            data.append([float(w), float(h)])

    data = np.array(data)
    if args.engine.startswith("sklearn"):
        if args.engine == "sklearn":
            km = cluster.KMeans(
                n_clusters=args.num_clusters, tol=args.tol, verbose=True)
        elif args.engine == "sklearn-mini":
            km = cluster.MiniBatchKMeans(
                n_clusters=args.num_clusters, tol=args.tol, verbose=True)
        km.fit(data)
        result = km.cluster_centers_
        # distance = km.inertia_ / data.shape[0]
        distance = avg_iou(data, result)
    else:
        result = k_means(data, args.num_clusters, args.tol)
        distance = avg_iou(data, result)

    write_anchors_to_file(result, distance, args.output)


if "__main__" == __name__:
    parser = argparse.ArgumentParser() # 创建解析器
    parser.add_argument('file_list', nargs='+', help='TrainList') 
    parser.add_argument('--num_clusters', '-n', default=9,
                        type=int, help='Number of Clusters')
    parser.add_argument(
        '--output', '-o', default='results/anchor.txt', type=str, help='Result Output File')
    parser.add_argument('--tol', '-t', default=0.005,
                        type=float, help='Tolerate')
    parser.add_argument('--engine', '-m', default='sklearn', type=str,
                        choices=['original', 'sklearn', 'sklearn-mini'], help='Method to use')

    args = parser.parse_args()  # 解析参数

    main(args)
