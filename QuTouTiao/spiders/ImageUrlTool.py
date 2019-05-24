
import requests
import os
from qiniu import Auth, put_file, etag
import QuTouTiao.settings as quSetting
import hashlib




# shuai
# qi_img_baseurl = 'https://image.yuanchain.tech/'
# qi = Auth(access_key=quSetting.QiniuAccess, secret_key=quSetting.QiniuSecret)
# bucket_name = 'yuandianpic'

md5Handle = hashlib.md5()

def uploadImage(down_img_url):
    file_path, file_name = getImageUrl(down_img_url)
    token = qi.upload_token(bucket_name, file_name, 3600)
    ret, info = put_file(token, file_name, file_path)
    qi_img_url = qi_img_baseurl + ret['key']
    os.remove(file_path)

    print('----------获取七牛图片地址:' + qi_img_url)
    return qi_img_url


def getImageUrl(img_url):
    print('----------下载图片:' + img_url)
    filePath = './imgs/'
    try:
        if not os.path.exists(filePath):
            os.makedirs(filePath)

        file_suffix = '.png'
        md5Handle.update(img_url.encode(encoding='gb2312'))
        img_name = md5Handle.hexdigest()
        file_path = filePath + img_name + file_suffix
        file_name = img_name + file_suffix
        r = requests.get(img_url)
        r.raise_for_status()
        # 使用with语句可以不用自己手动关闭已经打开的文件流
        with open(file_path, "wb") as f:  # 开始写文件，wb代表写二进制文件
            f.write(r.content)
        return file_path, file_name

    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        print('错误', e)