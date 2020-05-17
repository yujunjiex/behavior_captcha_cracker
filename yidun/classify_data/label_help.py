# coding: utf-8
"""配合label_chinese_pic.py使用，可以获得当前打码进度"""

import os

TRAIN_PATH = './crop_images/'

images = os.listdir(TRAIN_PATH)
count = 0
for image_name in images:
    _, *unicode_names = image_name[:-4].split('_')
    if len(unicode_names) == 1 and len(unicode_names[0]) == 5:  # 表示已标记
        continue
    else:
        count += 1

print('总共{}张图片，已打码{}个，未打码{}个'.format(len(images), len(images)-count, count))
