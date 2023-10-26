import json
import re
import os
import pymysql
import requests
from lxml import etree


def get_res(url, headers):
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    get_info(html)


def get_info(html):
    parse = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(html, parser=parse)

    allPic_list = tree.xpath('//ul[@class="rank-list pgc-list"]/li')

    infos = []

    for pic in allPic_list:
        info = {'raxnk': pic.xpath('./div/div[i]/i/span/text()')[0],
                'title': pic.xpath('./div/div[2]/a/text()')[0],
                'date': pic.xpath('./div/div[2]/div/span/text()')[0].replace('上映', '').replace('\n', '').strip()}

        # print(pic.xpath('./div/div[i]/i/span/text()'))
        infos.append(info)
    save_info('bilibilirank.json', infos)
    print("写入完成")


def save_info(filename, data):
    with open(filename, 'a', encoding='utf-8') as fp:
        json.dump(data, ensure_ascii=False, fp=fp)
        print("写入中")


def main():
    url = 'https://www.bilibili.com/v/popular/rank/movie'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    get_res(url, headers)


if __name__ == '__main__':
    main()
