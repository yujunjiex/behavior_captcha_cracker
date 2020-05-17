# coding: utf-8
import time
import requests
import json
from unfinished_click_captcha.geetest.spider.encrypt import Encrypyed
from spider_tools.pic_download import pic_download


# 发现极验在获取gt/challenge之后还需要对w参数也就是轨迹进行获取并通过ajax接口激活，
# 但是之后的获取不需要携带w参数
# 尝试后发现w参数的js逆向较为困难，所以这里去浏览器获取后自行填入
params_url = "https://www.geetest.com/demo/gt/register-click-official"

header = {
    'Referer': 'https://www.geetest.com/Sensebot',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
}


def get_ms_timestamp():
    """毫秒级时间戳"""
    return int(time.time() * 1000)


def get_params_data():
    return requests.get(params_url,
                        params={'t': get_ms_timestamp()},
                        headers=header).json()


def get_ajax_params(gt_chanllenge):
    ep = Encrypyed()
    w = ep.get_w(gt_chanllenge['gt'], gt_chanllenge['challenge'])
    return {
            'gt': gt_chanllenge['gt'],
            'challenge': gt_chanllenge['challenge'],
            'lang': 'zh-cn',
            'pt': '0',
            'w': w,
            'callback': '_'.join(['geetest', str(get_ms_timestamp())])
    }


# params_data = get_params_data()

# params = {
#     'is_next': 'true',
#     'type': 'click',
#     'gt': params_data['gt'],
#     'challenge': params_data['challenge'],
#     'lang': 'zh-cn',
#     'https': 'true',
#     'protocol': 'https://',
#     'offline': 'false',
#     'product': 'float',
#     'api_server': 'api.geetest.com',
#     'isPC': 'true',
#     'width': '100%',
#     'callback': '_'.join(['geetest', str(get_ms_timestamp())])
# }

# # 这里要先执行ajax接口激活gt和challenge
# ajax_url = 'https://api.geetest.com/ajax.php'
#
# # w
# print(requests.get(ajax_url, params=get_ajax_params(params_data)).text)


def get_click_img_json():
    url = 'https://api.geetest.com/refresh.php'
    # TODO:这里的参数在浏览器执行完ajax.php接口激活challenge后复制过来使用
    # Tip:一个challenge只能用五次...可以让一个同学帮忙刷新着给
    params = {
        'gt': '9dd4b398509fd4b2a2cbf2a7c0a7c605', #params_data['gt'],
        'challenge': 'af8ce3e3f53b07ba5ea5c3e04730bdd8',
        'lang': 'zh-cn',
        'type': 'click',
        'callback': '_'.join(['geetest', str(get_ms_timestamp())])
    }

    res = requests.get(url, headers=header, params=params).text
    json_data = json.loads(res.replace(params['callback'], '')[1:-1])
    return json_data


if __name__ == '__main__':
    img_base_url = 'https://static.geetest.com'

    cur = 452
    for i in range(500):
        json_data = get_click_img_json()
        if json_data['status'] == 'success':
            pic_download(img_base_url + json_data['data']['pic'], '{}captcha'.format(cur))
            print('{}成功！'.format(cur))
            cur += 1
        else:
            print('{}失败.'.format(cur))
            break
        # time.sleep(random.random())
