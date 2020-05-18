# coding: utf-8
import requests


content = requests.get("https://captcha.yunpian.com/v1/image/2461a2462c7348fcb0c5b8ba22027133.jpg").content

print(content)
print(type(content))
res = requests.post('http://127.0.0.1:5000/detect', files={'image': content},
                    data={'choice': 'slider'}).json()

print(res)


yidun_content = requests.get("https://necaptcha.nosdn.127.net/d334c8c3754f41e2b36ee3f62a5528f4@2x.jpg").content
target_words = '健母主'
print(requests.post('http://127.0.0.1:5000/detect',
                    files={'image': yidun_content},
                    data={'choice': 'click', 'words': target_words}).json())
