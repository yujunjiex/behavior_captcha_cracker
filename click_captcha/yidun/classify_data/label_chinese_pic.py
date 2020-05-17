# coding: utf-8
"""
标注crop_images文件内每张图片的中文名
标注成功的话图片名后的三个unicode字符会变成标注的那一个
# 程序可随时停止，标记到哪下次就从哪开始
# 如果框选的图片内没有文字或者无法识别，输入空格后回车
# 如果在pycharm专业版中，关闭Python Scientific中的plots show
"""
import os
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
plt.ion()  # 开启交互模式
TRAIN_PATH = './crop_images/'

images = os.listdir(TRAIN_PATH)
print('说明：1.图片内的汉字可能并不在提示的三个字符里，这种情况仍要输入.\n'
      '\t2.当图片内没有文字或者无法识别，输入空格后回车跳过.\n'
      '\t3.程序可随时停止，标记到哪下次就从哪开始')
for image_name in images:
    _, *unicode_names = image_name[:-4].split('_')
    if len(unicode_names) == 1:  # 表示已标记
        continue
    tip_chars = []
    for unicode_name in unicode_names:
        tip_chars.append(('\\' + unicode_name).encode().decode('unicode_escape'))
    image_path = os.path.join(TRAIN_PATH, image_name)  # 图片地址
    img = mpimg.imread(image_path)
    plt.imshow(img)
    plt.pause(0.001)  # 给到事件绘制时间
    char = input('请输入该图片中的汉字(提示:{})：'.format(tip_chars))
    assert len(char) == 1, '只能输入一个汉字.'
    if char == ' ':  # 脏数据直接删除
        os.remove(TRAIN_PATH)
        print('已删除.')
    else:
        input_unicode_char = char.encode('unicode_escape').decode()[1:]
        print(char, input_unicode_char, f'图片时间戳:{image_name[:13]}')
        os.rename(image_path,
                  os.path.join(TRAIN_PATH, f'{image_name[:13]}_{input_unicode_char}.jpg'))
    plt.close()


