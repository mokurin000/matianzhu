from typing import Any

import scrapy
from scrapy.http import HtmlResponse, Response

from matianzhu.items import MatianzhuItem


class MtzSpider(scrapy.Spider):
    name = "mtz"
    allowed_domains = ["nbufe.edu.cn"]
    start_urls = ["https://www.nbufe.edu.cn/xsc/list.htm?typeid=203&typeid2=188"]

    def parse(self, response: HtmlResponse, **_):
        """
        提取列表
        """
        categories = response.css("div.show_li_1 a::attr(href)")
        for url in categories.getall():
            yield response.follow(
                url=url,
                callback=self.parse_get_pages,
            )

    def parse_get_pages(self, response: HtmlResponse):
        """
        爬取文章链接、进行翻页
        """
        total_page_nums = int(response.css("#form1 font:nth-child(3)::text").get())
        for page_num in range(1, total_page_nums + 1):
            yield response.follow(
                f"{response.url}&page={page_num}",
                callback=self.parse_get_articles,
            )

    def parse_get_articles(self, response: HtmlResponse):
        """
        爬取文章链接
        """
        for url in response.css("div.list_bt a::attr(href)").getall():
            yield response.follow(
                url,
                callback=self.parse_article,
            )

    def parse_article(self, response: HtmlResponse):
        """
        爬取文章标题，时间，来源和内容
        """

        # document.querySelector(".show_bt_2").innerText.replace("：", ": ").split(" ")
        metainfo = response.css(".show_bt_2::text").get().replace("：", ": ").split()
        source = metainfo[1].strip()
        author = metainfo[3].strip()
        publish_date = metainfo[5].strip()
        title = response.css(".show_bt_h3::text").get()
        content = "".join(response.css("div.show_txt1 *::text").getall()).strip()

        item = MatianzhuItem()
        item["title"] = title
        item["publish_date"] = publish_date
        item["author"] = author
        item["source"] = source
        item["content"] = content
        yield item
