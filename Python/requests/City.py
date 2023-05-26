import requests
import re
from lxml import etree
if __name__ == '__main__':

    url = "https://www.aqistudy.cn/historydata/"

    headers = {
        "User-Agent" : "Mozilla / 5.0(Macintosh;Intel\MacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36"
    }

    page = requests.get(url=url,headers=headers)
    page.encoding = page.apparent_encoding
    page_text = page.text
    #正则表达式，找到第一个<a href标签。
    pattern = "<a href='.*?city=(.*?)'"
    hot_city_name_list = re.findall(pattern,page_text)
    #存储热门城市
    with open('./City.txt','w') as fp:
        for city_name in hot_city_name_list:
            fp.write(str(city_name+'\n'))
    print("Saved")

    parse = etree.HTMLParser(encoding="utf-8")
    tree = etree.HTML(page_text,parser=parse)
    all_city_list = tree.xpath("//div[@class='bottom']/ul/div[2]/li/a")
    city_list = {}
    for city in all_city_list:
        city_name = city.xpath("./text()")[0]
        city_link = "https://www.aqistudy.cn/historydata/"+city.xpath('./@href')[0]
        # print(city_link)
        # all_city_name.append(city_name)
        city_list['cityName'] = city_name
        city_list['cityLink'] = city_link
    res = requests.get(url=city_list['cityLink'],headers=headers).text
    print(res)



