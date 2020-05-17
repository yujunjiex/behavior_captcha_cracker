# coding: utf-8
from darknet import load_net, load_meta, detect, classify, load_image


# 加载模块
def load_classify_module(cfg, weights, data):
    net = load_net(cfg, weights, 0)
    meta = load_meta(data)
    return net, meta


if __name__ == '__main__':
    import os
    classify_modu = load_classify_module(b"./config/new_chinese_classify.cfg",
                                         b"./classify_checkpoints/new_chinese_classify_72.weights",
                                         b"./config/chinese_classify.data")
    # classify_modu = load_classify_module(b"./config/alexnet.cfg",
    #                                      b"./classify_checkpoints/alexnet_1129.weights",
    #                                      b"./config/chinese_classify.data")
    VALID_PATH = './classify_data/valid'

    images = os.listdir(VALID_PATH)
    images.remove('.gitignore')
    truth_count = 0
    for image_name in images:
        path = os.path.join(VALID_PATH, image_name)
        _, unicode_name = image_name[:-4].split('_')
        img = load_image(path.encode(), 0, 0)
        print(path)
        res = classify(classify_modu[0], classify_modu[1], img)
        flag = False

        if unicode_name in [pred_item[0].decode() for pred_item in res[0:5]]:
            flag = True
            truth_count += 1
        print('原图为', unicode_name, '识别结果为:', res[0:5], flag)
    print('Truth count:', truth_count)

