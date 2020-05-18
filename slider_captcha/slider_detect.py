# coding: utf-8
from models import *
from utils.utils import *
from utils.datasets import *
import time
import datetime
import argparse

from PIL import Image
from io import BytesIO

import torch
from torch.autograd import Variable
Cur_Path = os.path.abspath(os.path.dirname(__file__))


class SliderDetector:
    def __init__(self):
        self.opt = {
            "model_def": os.path.join(Cur_Path, "common_train/config/yolov3-captcha.cfg"),
            "weights_path": os.path.join(Cur_Path, "common_train/checkpoints/yolov3_ckpt.pth"),
            "class_path": os.path.join(Cur_Path, "common_train/data/classes.names"),
            "conf_thres": 0.8,
            "nms_thres": 0.4,
            "img_size": 416,
        }
        self.init_model()

    def init_model(self):
        """初始化model及相关参数"""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Set up model
        self.model = Darknet(self.opt["model_def"],
                             img_size=self.opt["img_size"]).to(self.device)

        # Load checkpoint weights
        # model.load_state_dict(torch.load(opt.weights_path))
        self.model.load_state_dict(torch.load(self.opt["weights_path"],
                                              map_location="cuda" if torch.cuda.is_available() else "cpu"))
        self.model.eval()  # Set in evaluation mode
        self.classes = load_classes(self.opt["class_path"])  # Extracts class labels from file
        self.Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

    def detect(self, content):
        # load image
        begin_time = time.time()
        origin_img = Image.open(BytesIO(content))
        input_imgs = transforms.ToTensor()(origin_img.convert('RGB'))
        # Pad to square resolution
        input_imgs, _ = pad_to_square(input_imgs, 0)
        # Resize
        input_imgs = resize(input_imgs, self.opt["img_size"])
        input_imgs = torch.unsqueeze(input_imgs, dim=0)  # transform to 4-dimensional
        input_imgs = Variable(input_imgs.type(self.Tensor))

        with torch.no_grad():
            detections = self.model(input_imgs)
            detections = non_max_suppression(detections, self.opt["conf_thres"], self.opt["nms_thres"])[0]

        # rescale_to_the_origin_predict
        detections = rescale_boxes(detections, self.opt["img_size"], np.array(origin_img).shape[:2])
        x1, y1, x2, y2, conf, cls_conf, cls_pred = detections[0]
        box_w = x2 - x1
        box_h = y2 - y1
        x_center = x1 + (box_w / 2)  # 目标x轴中心点(用于计算拖动距离)
        spend_time = time.time() - begin_time
        return spend_time, float(conf), float(x_center)


slider_detector = SliderDetector()

if __name__ == '__main__':
    import requests

    content = requests.get("https://captcha.yunpian.com/v1/image/2461a2462c7348fcb0c5b8ba22027133.jpg").content
    detector = SliderDetector()
    print(detector.detect(content))
    yidun_content = requests.get('https://necaptcha.nosdn.127.net/482eeb7bc5ff418b8daef221d618bb15@2x.jpg').content
    print(detector.detect(yidun_content))
