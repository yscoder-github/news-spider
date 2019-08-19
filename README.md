### 该项目目前涵盖的新闻应用如下：

### 1.趣头条爬虫

**需要自己安装mongodb** 

#### 环境配置
``` shell 
conda create --name commercial_scrapy  python=3.6
conda activate commercial_scrapy
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r ./requirements.txt

``` 
#### 执行脚本
``` shell 
cd QuTouTiao 
conda activate commercial_scrapy
python entrypoint.py 
```


Todo: 避免出现跳跃情况。 趣头条的降级策略：滑动两次之后，会把当次和上上次的给出来，怎么避免这个结果。 


Todo:   
   头条财经专题爬虫   
   新浪财经爬虫

