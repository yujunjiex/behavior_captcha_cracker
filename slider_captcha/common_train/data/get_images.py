# coding: utf-8
import os
import random
import shutil

# train: geetest: 15, yunpian: 150, yidun: 150
# test: geetest: 6, yunpian: 30, yidun: 30


def mix_train_img(train_paths: dict, train_counts: dict, target_save_path: str):
    old_image_path = {}
    for name, root_path in train_paths.items():
        old_image_path[name] = []
        for root, dirs, files in os.walk(root_path):
            if '.DS_Store' in files:  # mac的隐藏文件
                files.remove('.DS_Store')
            if '.gitignore' in files:
                files.remove('.gitignore')
            for file_path in files:
                old_image_path[name].append(f'{root}/{file_path}')

    result = []
    for name, image_count in train_counts.items():
        # 随机选取文件列表中的不重复指定个数
        print(name, len(old_image_path[name]), image_count)
        result += random.sample(old_image_path[name], image_count)
    random.shuffle(result)

    if not os.path.exists(target_save_path):
        os.mkdir(target_save_path)
    for i, old_path in enumerate(result):
        shutil.copyfile(old_path, f'{target_save_path}/{i+1}captcha.jpg')
        print(f'第{i+1}个图片拷贝完成, 原路径{old_path}')


def mix_test_img(test_paths: dict, test_counts: dict, target_save_path: str):
    mix_train_img(test_paths, test_counts, target_save_path)


if __name__ == '__main__':
    mix_train_img({'geetest': '/Users/mac/PycharmProjects/behavior_captcha_cracker/slider_captcha/geetest/data/images',
                   'yunpian': '/Users/mac/PycharmProjects/behavior_captcha_cracker/slider_captcha/yunpian/data/images',
                   'yidun': '/Users/mac/PycharmProjects/behavior_captcha_cracker/slider_captcha/yidun/data/images'},
                  {'geetest': 15, 'yunpian': 150, 'yidun': 150},
                  '/Users/mac/PycharmProjects/behavior_captcha_cracker/slider_captcha/common_train/data/images')

    mix_test_img({'geetest': '/Users/mac/PycharmProjects/behavior_captcha_cracker/slider_captcha/geetest/data/test_images',
                   'yunpian': '/Users/mac/PycharmProjects/behavior_captcha_cracker/slider_captcha/yunpian/data/test_images',
                   'yidun': '/Users/mac/PycharmProjects/behavior_captcha_cracker/slider_captcha/yidun/data/test_images'},
                  {'geetest': 6, 'yunpian': 30, 'yidun': 30},
                  '/Users/mac/PycharmProjects/behavior_captcha_cracker/slider_captcha/common_train/data/test_images')
