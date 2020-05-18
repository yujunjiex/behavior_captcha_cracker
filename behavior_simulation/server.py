# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, flash, \
                abort
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

from click_captcha.yidun.yidun_click_detect import click_detector
from slider_captcha.slider_detect import slider_detector


app = Flask(__name__)
# app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds=10)  # 将缓存时间设置为10s
# app.config['UPLOAD_FOLDER'] = 'static/images'   # 设置图片上传路径
app.config['SECRET_KEY'] = '123456'  # 设置SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/detect', methods=['POST'])
def captcha_detect():
    """
    Restful API
    :param: slider/click
    :return:
    """
    choices = ['slider', 'click']  # 可选的验证码
    choice = request.form["choice"]
    if choice not in choices:
        abort(400)
    file = request.files["image"]
    content = file.read()
    if choice == 'slider':
        result = slider_detector.detect(content)
        if result:
            spend_time, conf, x_center, box_w = result
            return jsonify(code=200, spend_time=spend_time,
                           conf=conf, x_center=x_center, width=box_w)
    else:
        words = request.form["words"]
        result = click_detector.detect(content, words)
        if result:
            spend_time, order_rets, target_words = result
            return jsonify(code=200, spend_time=spend_time,
                           rets=order_rets, words=target_words)
    return '请检查post的内容', 400


@app.route('/', methods=['GET'])
def index():
    return 'Hello World'


if __name__ == '__main__':
    app.run()
