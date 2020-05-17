# coding: utf-8
import requests
import os


def pic_download(url, name):
    """
    图片下载
    :param url:
    :param name:
    :return:
    """
    # os.pardir
    # save_path = '/Users/mac/PycharmProjects/behavior_captcha_cracker/click_captcha/yidun/classify_data/images/'
    save_path = os.path.dirname(os.getcwd()) + '/data/images/'

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    img_path = save_path + '{}.jpg'.format(name)
    img_data = requests.get(url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path
