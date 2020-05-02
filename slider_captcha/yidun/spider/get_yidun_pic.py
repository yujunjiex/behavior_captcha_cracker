# coding: utf-8
import execjs
import requests
import json
from spider_tools.pic_download import pic_download


def _load_js():
    """use python load js"""
    with open('./yidun_slider.js', encoding='utf-8') as f:
        js_data = f.read()

    with open('./core_fp.js', encoding='utf-8') as f:
        fp_data = f.read()
    js_text = execjs.compile(js_data)
    fp_text = execjs.compile(fp_data)
    return js_text, fp_text


jst, fp = _load_js()

url = 'http://c.dun.163yun.com/api/v2/get'
header = {
    "Referer": "https://www.yunpian.com/product/captcha",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}
slider_id = '5a0e2d04ffa44caba3f740e6a8b0fa84'
referer = 'https://www.163yun.com/trial/sense'
# callback实际编码后发现是可以随便填的，可能当请求后会将callback和其他参数构建键值对所以导致浏览器上的修改是不能随便的
callback = '__JSONP_abcdefg_0'
sess = requests.session()


def get_params(token=""):
    params = {
        "id": slider_id,
        "fp": rf"{fp.call('get_fp')}",
        "https": "false",
        "type": "2",  # 2: 滑块, 3: 点选, 5: 无感
        "version": "2.13.6",
        "dpr": "2",
        "dev": "1",
        "cb": rf"{jst.call('get_cb')}",
        "ipv6": "false",
        "runEnv": "10",
        "group": "",
        "scene": "",
        "width": "",
        "token": token,
        "referer": referer,
        "callback": callback
    }
    return params


def get_token():
    content = sess.get(url=url, params=get_params(), headers=header).text
    content = content.replace(callback, '')[1:-2]
    token = json.loads(content)['data']['token']
    return token


if __name__ == '__main__':
    import time
    import random
    token = get_token()

    cur = 1
    for i in range(20):
        content = sess.get(url=url, params=get_params(token), headers=header).text
        content = content.replace(callback, '')[1:-2]
        res = json.loads(content)
        print(res)
        if res['msg'] == 'ok':
            pic_download(res['data']['bg'][0], '{}captcha'.format(cur))
            print('{}成功！'.format(cur))
            cur += 1
        else:
            print('{}失败.'.format(cur))
        time.sleep(random.random())
