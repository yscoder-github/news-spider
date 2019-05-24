```
1、目前一共三个爬虫，分别为：
    1) 趣头条 ： QuTouTiao.py
    2) 巴比特 ：Babite.py
```
```
2、后续内容：
    1）三个爬虫最终存储到同一个 Item 对象，Item 对象会经过 pipeline/pipelines.py 类进行处理，使用者需要在 pipelines.py 类中将视频图片转存，并把内容进行上传至点点服务器处理
    2) settings中设置七牛云的认证信息，方便图片下载后转存
```
```
3、执行(二选一)：
    1) 打开entryPoint.py内相应注释，运行 entryPoint.py 即可
    2) cd 至爬虫项目根目录下执行 （ scrapy crawl 爬虫名称(如：QuTouTiao、Babite) ）
```
```
4、结果示例：
```
![](https://github.com/Jiang-Fallen/source/blob/master/image/img_info_spider_02.png)




## My Own experience ## 
1. file ImageUrlTool (there is not essential to use qiqiu service, i just want pure text )
``` python 
# comment follow lines 
# qi_img_baseurl = 'https://image.yuanchain.tech/'
# qi = Auth(access_key=quSetting.QiniuAccess, secret_key=quSetting.QiniuSecret)
# bucket_name = 'yuandianpic'
``` 

2. Comment qiqiu upload service 
