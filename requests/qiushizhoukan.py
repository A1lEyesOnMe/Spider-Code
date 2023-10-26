import requests
import re
import pymysql
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}
def conn_mysql():
    conn = pymysql.connect(
        host="localhost:3306",
        user="root",
        password="password",
        database="magazine",
        charset="utf-8")
    cursor = conn.cursor()
    sql = """
    create table zhoukan(
    titile varchar(100),
    writer varchar(20),
    text varchar(500)
    )
    """


def get_urls():

    url = 'http://www.qstheory.cn/dukan/qs/2014/2019-01/01/c_1123924172.htm'


    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    html_page = response.text
    # print(html_page)

    href_re = '<a href="(.*\/dukan.*?htm)'
    urls = (re.findall(href_re, html_page))

    return urls

def get_info():
    urls = get_urls()

    for url in urls:
        response = requests.get(url=url, headers=headers)
        response.encoding = 'utf-8'
        html_page = response.text
        title = []
        title_re = '"inner.*\s.*\s(.+)\s<'
        title_list = re.findall(title_re,html_page)
        # print(title_list[0])
        title.append(title_list)
        for title in title_list:
            yield title


# def save_info():
#     info = get_info()


if __name__ == "__main__":
    pass
