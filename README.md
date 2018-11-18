# zhihu_spider
知乎首页问答爬取

## 开发环境
>python == 3.5\
>scrapy == 1.5\
>chromedriver == 2.3\
>chrome == 60.0\
>selenium == 3.1.4

## 使用说明：
- 在```settings.py```中请选择自己需要的导出方式：（支持json、mysql）
```
ITEM_PIPELINES = {
    'myspider.pipelines.JsonWithEncodingPipeline': 2,
    'myspider.pipelines.MysqlPipeline':1,
}
#若两种都需要请不必修改，若只需要JSON则请注释'myspider.pipelines.MysqlPipeline':1,
```
另外：如果需要导入数据库，请提前根据item设计表结构，同时```pip install pymysql```，并在settings.py中设置好如下信息：
```
MYSQL_HOST = 'localhost' #数据库ip地址
MYSQL_DBNAME = 'xxx' #数据库名称
MYSQL_USER = 'xxx' #用户名
MYSQL_PASSWD = 'xxx' #密码
MYSQL_PORT = 3306 #数据库端口
```
- 在spiders>zhihu.py中找到以下代码，输入自己的知乎账号和密码完成selenium模拟登陆：
```
    browser.find_element_by_css_selector(".Login-content input[name='username']").send_keys("xxx")#在“xxx”处填入账号
    browser.find_element_by_css_selector(".SignFlow-password input[name='password']").send_keys("xxx")#在“xxx”处填入密码
```
## 开发总结:
- 由于知乎更新了登录验证方式，不得不使用selenium去模仿浏览器登录爬取，但是使用chrome做调试的时候，版本问题影响很大，最新版本的chrome对不上chromedriver，摸索后发现只能降级chrom的版本
- 使用了深度优先的爬取策略，一定要对不需要的url进行过滤，比如首页里推荐的“live”、“想法”等url，没必要再进去解析查找问答了，只解析当前页面的量也可以达到目标；
- 导出的JSON文件如果乱码，请用notepad或其他支持GBK的软件打开
