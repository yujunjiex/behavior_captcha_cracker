# coding: utf-8
"""
对crop_images下的图片抽样，计算训练集正确率
样本大小n，总体N。若n=10, N=100, 则n/N=0.1
"""

import random
import os
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
plt.ion()  # 开启交互模式

TRAIN_PATH = './crop_images/'

images = os.listdir(TRAIN_PATH)
images.remove('.gitignore')

proportion = 0.01
sample_count = int(len(images)*0.01)

correct = 0
random.shuffle(images)
for image_name in random.sample(images, sample_count):
    _, unicode_name = image_name[:-4].split('_')
    image_path = os.path.join(TRAIN_PATH, image_name)  # 图片地址
    img = mpimg.imread(image_path)
    plt.imshow(img)
    plt.pause(0.001)  # 给到事件绘制时间
    select_char = input("该图片内的文字是否是 '{}' ?(y or n): ".format(('\\' + unicode_name).encode().decode('unicode_escape')))
    plt.close()
    if select_char.lower() == 'n':
        continue
    correct += 1
    print(correct)

print('抽取样本比例为:{}'.format(proportion))
print('抽取样本数为:{}'.format(sample_count))

print('正确样本数:{}, 错误样本数:{}, 训练集抽样准确率为{}'.format(
                                                            correct,
                                                            sample_count-correct,
                                                            correct/sample_count
                                                           ))



