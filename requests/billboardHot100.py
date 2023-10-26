import os
import re
import json
import pymysql
import requests
from lxml import etree


def get_html(url, headers):
    html = requests.get(url=url, headers=headers)
    text = html.text

    parse = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(text, parser=parse)

    infos = []

    allChart = tree.xpath(
        '//div[@class="chart-results-list // lrv-u-padding-t-150 lrv-u-padding-t-050@mobile-max"]/div[@class="o-chart-results-list-row-container"]')

    for data in allChart:
        # info_list.append(data.xpath('./ul/@data-detail-target')[0])
        info = {'rank': data.xpath('./ul/@data-detail-target')[0],
                'songName': data.xpath('./ul/li[4]/ul/li/h3/text()')[0].strip(),
                'singer': data.xpath('./ul/li[4]/ul/li/span/text()')[0].strip(),
                'lastWeekRank': data.xpath('./ul/li[4]/ul/li/span/text()')[1].strip(),
                'peakRank': data.xpath('./ul/li[4]/ul/li/span/text()')[2].strip(),
                'weekOnChart': data.xpath('./ul/li[4]/ul/li/span/text()')[3].strip()}
        # info['photo'] = data.xpath('./ul/li[2]//@src')[0]  #lazyload try another way
        
        # infos.append(info)

    # save_info('billboardHot100list.json', infos)
    # print("写入完成")


def save_info(filename, data):
    with open(filename, 'a', encoding='utf-8') as fp:
        json.dump(data, ensure_ascii=False, fp=fp)
        print("写入中")


def save_db():
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="password",
        port=3306,
        database='spiders'
    )

    cursor = db.cursor()
    dropSql = r'drop table if exists billboard;'
    cursor.execute(dropSql)
    createSql = r'create table billboard(' \
                r'songRank varchar(255),' \
                r'song varchar(255),' \
                r'singer varchar(255),' \
                r'lastWeekRank varchar(255),' \
                r'peakRank varchar(255),' \
                r'weekOnChart int)'
    cursor.execute(createSql)

    insertSql = r'insert into billboard values (' \
                r''

    db.commit()
    db.close()



if __name__ == '__main__':
    url = "https://www.billboard.com/charts/hot-100/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    get_html(url, headers)
