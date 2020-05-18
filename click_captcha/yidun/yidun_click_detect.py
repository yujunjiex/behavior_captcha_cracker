# coding: utf-8
import os
from click_captcha.yidun.darknet import load_net, load_meta, detect, classify, load_image
import time
from PIL import Image
Cur_Path = os.path.abspath(os.path.dirname(__file__))


class YidunClickDetector:
    temp_dir = os.path.join(Cur_Path, './server_temp/')

    def __init__(self):
        self.detect_modu = None
        self.classify_modu = None
        self.load_dtc_module(os.path.join(Cur_Path, "./config/yolov3-captcha.cfg").encode(),
                             os.path.join(Cur_Path, "./checkpoints/yolov3-captcha_1800.weights").encode(),
                             os.path.join(Cur_Path, "./config/captcha.data").encode())
        self.load_classify_module(os.path.join(Cur_Path, "./config/new_chinese_classify.cfg").encode(),
                                  os.path.join(Cur_Path, "./classify_checkpoints/new_chinese_classify_72.weights").encode(),
                                  os.path.join(Cur_Path, "./config/chinese_classify.data").encode())
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)

    def load_dtc_module(self, cfg, weights, data):
        net = load_net(cfg, weights, 0)
        meta = load_meta(data)
        self.detect_modu = (net, meta)

    def load_classify_module(self, cfg, weights, data):
        net = load_net(cfg, weights, 0)
        meta = load_meta(data)
        self.classify_modu = (net, meta)

    def detect(self, content, target_words):
        begin_time = time.time()
        input_imgs_path = self.save_pic(content)
        rets = detect(self.detect_modu[0], self.detect_modu[1], input_imgs_path.encode('utf-8'))
        input_imgs = Image.open(input_imgs_path)
        predict_item = {}  # 汉字-中心区域
        for ret in rets:
            if ret[1] > 0.5:
                point = ret[2]
                center = (int(point[0]), int(point[1]))
                x, y, w, h = point  # (中心点x，中心点y，宽，高)
                a = x - (h / 2)
                c = x + (h / 2)
                b = y - (w / 2)
                d = y + (w / 2)

                chinese_char = input_imgs.crop((a, b, c, d))
                # 将截取的图片规范化为64*64*3
                normal_img = chinese_char.resize((64, 64), resample=Image.BICUBIC)
                path = os.path.join(self.temp_dir, '{}.jpg'.format(self.get_ms_timestamp()))
                normal_img.save(path)

                # 重新载入为DarknetImage类型
                img = load_image(path.encode(), 0, 0)
                predicts = classify(self.classify_modu[0], self.classify_modu[1], img)
                unicode_name = predicts[0][0].decode()  # 默认取top1
                word = ('\\' + unicode_name).encode().decode('unicode_escape')
                predict_item[word] = center
                # 执行完删除pic
                os.remove(path)

        os.remove(input_imgs_path)
        if len(predict_item) >= len(target_words):
            order_rets = [predict_item[word] for word in target_words]
            spend_time = time.time() - begin_time
            return spend_time, order_rets, target_words
        else:
            return False

    @classmethod
    def save_pic(cls, content):
        save_path = os.path.join(cls.temp_dir, str(cls.get_ms_timestamp())) + '.jpg'
        with open(save_path, 'wb+') as f:
            f.write(content)
        return save_path

    @staticmethod
    def get_ms_timestamp():
        """毫秒级时间戳"""
        return int(time.time() * 1000)


click_detector = YidunClickDetector()

if __name__ == '__main__':
    import requests

    yidun_content = requests.get("https://necaptcha.nosdn.127.net/d334c8c3754f41e2b36ee3f62a5528f4@2x.jpg").content
    target_words = '健母主'
    detector = YidunClickDetector()
    print(detector.detect(yidun_content, target_words))





