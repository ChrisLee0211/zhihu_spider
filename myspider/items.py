# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from myspider.utils.common import extract_num
from myspider.settings import SQL_DTAETIME_FORMAT, SQL_DATE_FORMAT
import datetime


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass




class ZhihuQuestionItem(scrapy.Item):
    # 知乎问题item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into zhihu_question(
            zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title=VALUES(title),
            content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
            watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
        zhihu_id = self["zhihu_id"][0]
        topics = "".join(self["topics"])
        url = "".join(self["url"])
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))
        comments_num = extract_num("".join(self["comments_num"]))
        watch_user_num = extract_num("".join(self["watch_user_num"]))
        click_num = extract_num("".join(self["click_num"]))
        crawl_time = datetime.datetime.now().strftime(SQL_DTAETIME_FORMAT)  # 将datetime类型转换为str

        params = (
            zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    # 知乎问题回答
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        """
        备注：插入mysql语句加上on duplicate key xxx条件，因为每次爬取同一个问题的答案是有可能更新的，但id一定冲突，那就只更新变动的内容
        """
        insert_sql = """
            insert into zhihu_answer(
            zhihu_id, url, question_id, author_id, content, praise_num, comments_num, create_time, update_time, crawl_time
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(content), praise_num=VALUES(praise_num),
            comments_num=VALUES(comments_num), update_time=VALUES(update_time)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DTAETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DTAETIME_FORMAT)

        params = (
            self["zhihu_id"], self["url"], self["question_id"], self["author_id"], self["content"], self["praise_num"],
            self["comments_num"], create_time, update_time, self["crawl_time"].strftime(SQL_DTAETIME_FORMAT)
        )

        return insert_sql, params
