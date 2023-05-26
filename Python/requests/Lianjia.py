import requests
from lxml import etree
import pymysql
import json
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
}

def get_res():

    regions = ['baohe','shushan','luyang','yaohai','binhuxinqu','jinkai2','gaoxin8','xinzhan','feixi','changfeng']
    for region in regions:
        for pageNum in range(1,101):
            url = 'https://hf.lianjia.com/ershoufang/%s/pg%d'%(region,pageNum)
            print('开始爬取%s地区，第%d页'%(region,pageNum))
            response = requests.get(url=url,headers=headers)
            response.encoding = 'utf8'
            html = response.text
            yield html

def get_info():
    html_list = get_res()
    for html in html_list:

        parse = etree.HTMLParser(encoding='utf-8')
        tree = etree.HTML(html,parser=parse)

        infos = {}

        title_list = tree.xpath('//div[@class="title"]/a/text()')
        community_list = tree.xpath('//div[@class="flood"]//a[1]/text()')
        region_list = tree.xpath('//div[@class="flood"]//a[2]/text()')
        info_list = tree.xpath('//div[@class="houseInfo"]/text()')
        totalPrice_list = tree.xpath('//div[@class="totalPrice totalPrice2"]/span/text()')
        unitPrice_list = tree.xpath('//div[@class="unitPrice"]/span/text()')
        for title,community,region,totalPrice,unitPrice,info in zip(title_list,community_list,region_list,totalPrice_list,unitPrice_list,info_list):
            infos.update({'title':title,'community':community,'region':region,'totalPrice':totalPrice,'unitPrice':unitPrice,'info':info})
            # print(infos)
            yield infos

def save_infoToLocal():
    dirs = get_info()
    for dir in dirs:
        # for key in dir:
        #     print(dir[key])
        with open('lianjia.json','a',encoding='utf8') as fp:
            fp.write(json.dumps(dir, ensure_ascii=False))
            print("正在爬取数据...")

def save_infoToMysql():

    db = pymysql.connect(
        host="localhost",
        user="root",
        password="password",
        port=3306,
        database='lianjia'
    )
    cursor = db.cursor()
    dropSql = '''
    DROP TABLE IF EXISTS `lianjia`;
    '''
    cursor.execute(dropSql)
    createSql =  '''
    create table lianjia(
    title varchar(255),
    community varchar(255),
    region varchar (255),
    totalPrice int,
    unitPrice varchar (255),
    info varchar(255)
    )
    '''
    cursor.execute(createSql)
    dirs = get_info()
    for dir in dirs:
        insertSql = '''
            insert into lianjia values(
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
            )
        '''

        title = ("'" + dir['title'] + "'")
        community = ("'" + dir['community'] + "'")
        region = ("'" + dir['region'] + "'")
        totalPrice = dir['totalPrice']
        unitPrice = ("'" + dir['unitPrice'] + "'")
        info = ("'" + dir['info'] + "'")

        # print(title, community, region, totalPrice, unitPrice, info)
        cursor.execute(insertSql %(title, community, region, totalPrice, unitPrice, info))
        db.commit()
        print('储存中...')
    db.close()

if __name__ == '__main__':
    save_infoToLocal()
    # save_infoToMysql()
    print('downloaded')