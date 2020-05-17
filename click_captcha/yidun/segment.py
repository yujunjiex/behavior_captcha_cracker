# coding: utf-8
from darknet import load_net, load_meta, detect
import time
from PIL import Image


def get_ms_timestamp():
    """毫秒级时间戳"""
    return int(time.time() * 1000)


# 切割汉字
def seg_one_img(img_path, rets):
    img = Image.open(img_path)
    # hanzi_list = []
    for ret in rets:
        # per_dict = {}
        if ret[1] > 0.5:
            point = ret[2]

            center = (int(point[0]), int(point[1]))
            x, y, w, h = point  # (中心点x，中心点y，宽，高)
            a = x - (h / 2)
            c = x + (h / 2)
            b = y - (w / 2)
            d = y + (w / 2)
            try:
                chinese_char = img.crop((a, b, c, d))
                # 将截取的图片规范化为64*64*3
                normal_img = chinese_char.resize((64, 64), resample=Image.BICUBIC)
                # img_path[-18:-4]表示易盾的中文名，用来在标注时提供一些备选字
                path = './classify_data/crop_images/{}_{}.jpg'.format(get_ms_timestamp(), img_path[-18:-4])
                print(path)
                normal_img.save(path)
            except Exception as e:
                print(e)

                # print('#'*20)
                # print('存在不规则的图片')
                # print(e)
    # return hanzi_list


def load_dtc_module(cfg, weights, data):
    net = load_net(cfg, weights, 0)
    meta = load_meta(data)
    return net, meta


def seg_all_img(path_file, net, meta):
    # 打开存储图片存储路径的文件，并读取所有行赋值给列表lines
    with open(path_file, 'r') as f:
        lines = f.readlines()
    # 遍历所有图片，进行扣字
    for line in lines:
        img_path = line.strip()  # 从文件读取的路径后面有一个换行符'\n'
        rets = detect(net, meta, img_path.encode('utf-8'))
        seg_one_img(img_path, rets)


if __name__ == '__main__':
    # 加载模型
    # net, meta = load_dtc_module("../cfg/yolo-origin.cfg", "../jiyan/backup/yolo-origin.backup" , "../cfg/yolo-origin.data")
    net, meta = load_dtc_module(b"./config/yolov3-captcha.cfg", b"./checkpoints/yolov3-captcha_1800.weights",
                                b"./config/captcha.data")

    # 切割所有图片
    seg_all_img('./classify_data/chinese_classify_image.txt',
                net, meta)


    # 切割一张图片
    # img_path = '../11.jpg'
    # rets = detect(net,meta,img_path)
    # seg_one_img(img_path, rets)




