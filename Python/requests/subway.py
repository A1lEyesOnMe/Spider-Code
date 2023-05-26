import json
import requests
from lxml import etree
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


def get_city():
    url = 'http://map.amap.com/subway/index.html?&1100'
    time.sleep(2)
    res = requests.get(url=url, headers=headers)
    res.raise_for_status()
    res.encoding = res.apparent_encoding
    html = res.text
    Html = etree.HTML(html)
    # 城市列表
    res1 = Html.xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/a')
    res2 = Html.xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/a')
    for i in res1:
        # 城市ID值
        ID = ''.join(i.xpath('.//@id'))
        # 城市拼音名
        cityname = ''.join(i.xpath('.//@cityname'))
        # 城市名
        name = ''.join(i.xpath('./text()'))
        get_message(ID, cityname, name)

    for i in res2:
        # 城市ID值
        ID = ''.join(i.xpath('.//@id'))
        # 城市拼音名
        cityname = ''.join(i.xpath('.//@cityname'))
        # 城市名
        name = ''.join(i.xpath('./text()'))
        get_message(ID, cityname, name)


def get_message(ID, cityname, name):
    """
    地铁线路信息获取
    """
    url = 'http://map.amap.com/service/subway?_1555502190153&srhdata=' + ID + '_drw_' + cityname + '.json'
    response = requests.get(url=url, headers=headers)
    time.sleep(2)
    html = response.text
    result = json.loads(html)
    for i in result['l']:
        for j in i['st']:
            # 判断是否含有地铁分线
            if len(i['la']) > 0:
                print(name, i['ln'] + '(' + i['la'] + ')', j['n'])
                with open('subway.csv', 'a+', encoding='utf-8') as f:
                    f.write(name + ',' + i['ln'] + '(' + i['la'] + ')' + ',' + j['n'] + '\n')
            else:
                print(name, i['ln'], j['n'])
                with open('subway.csv', 'a+', encoding='utf-8')as f:
                    f.write(name + ',' + i['ln'] + ',' + j['n'] + '\n')


if __name__ == '__main__':
    get_city()