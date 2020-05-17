# coding: utf-8
import json
import os
import binascii
import random

import hashlib
import rsa

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class Encrypyed():
    def __init__(self):
        self.n = "00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C2" \
                 "9ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC" \
                 "2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81"
        self.e = '10001'

    def get_w(self, gt, challenge):
        text = {"gt":gt,"challenge":challenge,"offline":"false","new_captcha":"true","product":"float","width":"300px","https":"true","protocol":"https://","static_servers":["static.geetest.com/","dn-staticdown.qbox.me/"],"pencil":"/static/js/pencil.1.0.3.js","geetest":"/static/js/geetest.6.0.9.js","click":"/static/js/click.2.8.9.js","beeline":"/static/js/beeline.1.0.1.js","voice":"/static/js/voice.1.2.0.js","fullpage":"/static/js/fullpage.8.9.4.js","slide":"/static/js/slide.7.7.1.js","maze":"/static/js/maze.1.0.1.js","type":"fullpage","aspect_radio":{"pencil":"128","voice":"128","slide":"103","beeline":"50","click":"128"},"cc":"8","ww":"true","i":"209979!!352674!!CSS1Compat!!74!!-1!!-1!!-1!!-1!!1!!-1!!-1!!1!!45!!3!!2!!9!!-1!!-1!!-1!!-1!!-1!!3!!-1!!-1!!4!!20!!-1!!-1!!-1!!0!!23!!0!!23!!1440!!245!!1440!!812!!zh-CN!!zh-CN,zh,en,de,is!!-1!!2!!24!!Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36!!1!!1!!1440!!900!!1440!!821!!1!!1!!1!!-1!!MacIntel!!0!!-8!!7c0e679ee28000fe783d3cb4d29323b1!!9b1a5ae0d307a5fe3c2938f489af2d18!!internal-pdf-viewer,mhjfbmdgcfjbbpaeojofohoefgiehjai,internal-nacl-plugin!!0!!-1!!0!!8!!AndaleMono,Arial,ArialBlack,ArialNarrow,ArialRoundedMTBold,ArialUnicodeMS,BookAntiqua,BookmanOldStyle,Calibri,Cambria,CambriaMath,Century,CenturyGothic,CenturySchoolbook,ComicSansMS,Consolas,Courier,CourierNew,Garamond,Geneva,Georgia,Helvetica,HelveticaNeue,Impact,LucidaBright,LucidaCalligraphy,LucidaConsole,LucidaFax,LUCIDAGRANDE,LucidaHandwriting,LucidaSans,LucidaSansTypewriter,LucidaSansUnicode,MicrosoftSansSerif,Monaco,MonotypeCorsiva,MSGothic,MSPGothic,MSReferenceSansSerif,Palatino,PalatinoLinotype,Tahoma,Times,TimesNewRoman,TrebuchetMS,Verdana,Wingdings,Wingdings2,Wingdings3!!1588419419169!!-1!!-1!!-1!!217!!73!!8!!25!!33!!-1!!-1"}
        text = json.dumps(text, separators=(',', ':'))
        sec_key = self.create_secret_key(8)
        # rsa 不对称性对 aes的密钥进行加密
        enc_sec_key = self.rsa_encrpt(sec_key, self.n, self.e)

        # aes 对称加密  进行轨迹加密
        iv = b"0000000000000000"
        enc_text = self.aes_encrypt(text, sec_key.decode('utf-8'), iv)

        # base64 编码
        enc_text = self.b64encode(enc_text)

        data = {
            'gt': gt,
            'challenge': challenge,
            'w': enc_text + enc_sec_key,
            # 'callback': 'geetest_' + str(int(time.time() * 1000)),
        }
        return data['w']

    def aes_encrypt(self, text, secKey, iv, style='pkcs7'):
        """
        :param text: 文本
        :param secKey: 密钥
        :param iv: 初始iv  bytes
        :param style: 返回函数类型
        :return:
        """
        encryptor = AES.new(secKey.encode('utf-8'), AES.MODE_CBC, iv)
        pad_pkcs7 = pad(text.encode('utf-8'), AES.block_size, style=style)
        ciphertext = encryptor.encrypt(pad_pkcs7)
        return ciphertext

    def rsa_encrpt(self, text, n, e):
        """
        对text 进行rsa加密   # reverseText^pubKey%modulus
        """
        PublicKey = rsa.PublicKey(int(n, 16), int(e, 16))  # rsa库公钥形式
        rs = rsa.encrypt(text, PublicKey)
        return rs.hex()

    def create_secret_key(self, size):
        # 作用是返回的二进制数据的十六进制表示。每一个字节的数据转换成相应的2位十六进制表示
        return binascii.hexlify(os.urandom(size))

    def b64encode(self, s):

        def separate_24_to_6(n, base):
            res = 0
            for i in range(24, -1, -1):
                if base >> i & 1 == 1:
                    res = (res << 1) + (n >> i & 1)
            return res

        base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789()"
        r = ""
        p = ""
        c = len(s) % 3
        if c > 0:
            for _ in range(c, 3):
                p += '.'
                s += b'\0'

        for c in range(0, len(s), 3):
            # we add newlines after every 76 output characters, according to the MIME specs
            # if c > 0 and (c / 3 * 4) % 76 == 0:
            #     r += "\r\n"

            # these three 8-bit (ASCII) characters become one 24-bit number
            n = (s[c] << 16) + (s[c + 1] << 8) + (s[c + 2])

            # this 24-bit number gets separated into four 6-bit numbers
            # n = [n >> 18 & 63, n >> 12 & 63, n >> 6 & 63, n & 63]

            n = [separate_24_to_6(n, base) for base in [7274496, 9483264, 19220, 235]]

            r += base64chars[n[0]] + base64chars[n[1]] + base64chars[n[2]] + base64chars[n[3]]

        # add the actual padding string, after removing the zero pad
        return r[0: len(r) - len(p)] + p


if __name__ == '__main__':
    ep = Encrypyed()
    print(ep.get_w('fe23d6148baf995e34decea58c12b5e4', '960780255cdadcbdebde1fb646d5cb77'))