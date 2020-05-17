# coding: utf-8
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def pic_rectangle(pic_path, save_path, image_name, bounds):
    """框选图片"""
    image = Image.open(pic_path)
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        bound = list(map(float, bound))
        # 坐标
        x1, y1 = bound[0:2]
        x2, y2 = bound[2:4]
        # outline 外线，fill填充
        draw.rectangle((x1, y1, x2, y2), outline="red", width=3)
    print('{}/mark{}'.format(save_path, image_name))
    image.save('{}/mark{}'.format(save_path, image_name))

    # image.show()


if __name__ == '__main__':
    # 调用
    # filepath="./1captcha.jpg"
    # bound=[186.325638, 45.903774, 251.499069, 99.604050]
    # # xmin, ymin, xmax, ymax
    # # 186.325638 45.903774 251.499069 99.604050
    # pic_rectangle(filepath, './', bound)
    valid_results_path = './comp4_det_test_character.txt'
    valid_image_dir_path = '../data/valid'
    mark_dir_path = '../data/output'
    with open(valid_results_path, 'r') as f:
        cur_img_name = f.readline().split()[0]  # 对比名
        f.seek(0)
        bounds = []
        while True:
            info = f.readline()
            if not info:
                break
            img_name, _, *bound = info.split()
            if cur_img_name == img_name:
                bounds.append(bound)
            else:
                pic_path = '/'.join([valid_image_dir_path, cur_img_name+'.jpg'])
                pic_rectangle(pic_path, mark_dir_path, cur_img_name+'.jpg', bounds)
                cur_img_name = img_name
                bounds = [bound]
            print(cur_img_name, bounds)
        pic_path = '/'.join([valid_image_dir_path, cur_img_name+'.jpg'])
        pic_rectangle(pic_path, mark_dir_path, cur_img_name+'.jpg', bounds)




