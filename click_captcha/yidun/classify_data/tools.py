# coding: utf-8
import os
import random
import shutil

TRAIN_PATH = './crop_images/'
VALID_PATH = './valid/'


def change_images_name_to_unicode():
    """把crop_images里的图片中的中文替换成四位unicode"""
    global TRAIN_PATH
    images = os.listdir(TRAIN_PATH)
    images.remove('.gitignore')

    for image_name in images:
        unicode_list = [_s.encode('unicode_escape').decode()[1:] for _s in image_name[13:-4]]
        new_name = '_'.join([image_name[:13]] + unicode_list) + '.jpg'
        new_path = os.path.join(TRAIN_PATH, new_name)
        old_path = os.path.join(TRAIN_PATH, image_name)
        os.rename(old_path, new_path)
        print(image_name, new_name)

    # # decode
    # _, *unicode_names = new_path[:-4].split('_')
    # for unicode_name in unicode_names:
    #     print(('\\' + unicode_name).encode().decode('unicode_escape'))


def move_to_valid(count=300):
    """随机300张到测试集"""
    global TRAIN_PATH
    images = os.listdir(TRAIN_PATH)
    images.remove('.gitignore')

    for image_name in random.sample(images, count):
        old_path = os.path.join(TRAIN_PATH, image_name)
        new_path = os.path.join('./valid/', image_name)
        print(old_path, 'to', new_path)
        shutil.copyfile(old_path, new_path)
        os.remove(old_path)


def generator_train_list(train_file_path='./train.list', train_image_path='classify_data/crop_images/'):
    """生成train.list"""
    global TRAIN_PATH
    images = os.listdir(TRAIN_PATH)
    images.remove('.gitignore')

    with open(train_file_path, 'w+') as f:
        for image_name in images:
            f.write('{}\n'.format(train_image_path + image_name))


def generator_valid_list(valid_file_path='./valid.list', valid_image_path='classify_data/valid/'):
    """生成valid.list"""
    global VALID_PATH
    images = os.listdir(VALID_PATH)
    images.remove('.gitignore')

    with open(valid_file_path, 'w+') as f:
        for image_name in images:
            f.write('{}\n'.format(valid_image_path + image_name))


def generator_classify_image_txt():
    """生成chinese_classify_image.txt"""
    files = os.listdir('./images')
    files.remove('.gitignore')

    with open('./chinese_classify_image.txt', 'w+') as f:
        for file_name in files:
            f.write('classify_data/images/{}\n'.format(file_name))


def generator_classify_labels_txt():
    """生成labels.txt"""
    global TRAIN_PATH
    images = os.listdir(TRAIN_PATH)
    images.remove('.gitignore')

    words = set()
    for image_name in images:
        _, unicode_name = image_name[:-4].split('_')
        words.add(unicode_name)

    print(len(words))
    print(words)
    with open('./labels.txt', 'w+') as f:
        for word in words:
            f.write('{}\n'.format(word))


if __name__ == '__main__':
    generator_train_list()
    generator_valid_list()
    generator_classify_labels_txt()
