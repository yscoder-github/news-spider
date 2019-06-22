该项目目前涵盖的新闻应用如下：

## 趣头条 ： QuTouTiao.py   



趣头条api: 

``` shell 
scrapy crawl QuTouTiao
``` 
    """
    in qutoutiap api : page is of no use!!!!! 
    # the most important fields : 
       (1) limit: max can set to 100, at here i set it to 100 to decrease uncertain
       (2) min_time param *********** 
          case limit set to 100: 
          ------------------
           when min_time in api is 1560908221000 (2019-6-19 09:37:01)
           response in first time:
               min_time: 1560906659000 (2019-6-19 09:10:59)   --- 
               max_time: 1560908216000 (2019-6-19 09:36:56)
           response in second time : 
                min_time:  1560904891000:(2019-6-19 08:41:31) 
                max_time:  1560906360000: (2019-6-19 09:06:00) 
          --------------------
          when min_time in api is 1560906659000 (2019-6-19 09:10:59)
          response in first time:
               min_time: 1560905203000 (2019-6-19 8:46:43)
               max_time: 1560906644000 (2019-6-19 9:10:44)
          response in second time:
               min_time: 1560903527000 (2019-6-19 8:18:47)
               max_time: 1560905185000 (2019-6-19 8:46:25)

          ---------------------

        从上面可以看出: 在每次结果反馈中， 返回的每条结果的 publish_info的时间值是位于response中 min_time与max_time之间的
        而且只有奇数次访问，才能得到时间段合理的数据。 
        故，请求次序如下: 
        I. request: https:///xxx?limit=100&min_time=1560908221000&xxxx 
        II. GET min_time field from response, At here is 1560906659000
        III. request: https:///xxx?limit=100&min_time=1560906659000&xxxx   
        IV. GET min_time field from response, At here is 1560905203000
        V. request: 

        总结： 看来是通过min_time来进行数据的滚动的！！而且仅限于第一次请求！！！！！
        每次解析出来min_time 然后进行遍历即可

      
    """







Todo: modify Readme.md 
Todo: 避免出现跳跃情况。 趣头条的降级策略：滑动两次之后，会把当次和上上次的给出来，怎么避免这个结果。 


Todo:   
   头条财经专题爬虫   
   新浪财经爬虫

