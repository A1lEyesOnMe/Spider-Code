import re
import requests
import lxml
from bs4 import BeautifulSoup

if __name__ == "__main__":
    fp =open("./nmpa.html","r",encoding="utf-8")
    soup = BeautifulSoup(fp,'lxml')
    # print(soup)   返回html
    # print(soup.div)   findName 返回第一次出现的标签
    # print(soup.find("div"))   等同于findName
    # print(soup.find('div',class_='hzbscin'))  属性定位
    # print(soup.find_all('div',class_='hzbscin'))
    # print(soup.select(".hzbtabs > span")[0])  层级选择
    # print(soup.select('.hzbtabs > span')[0].get_text())
    # print(soup.select(".hzbtabs > span")[0]["id"])
