import re
import json
import pymysql
import requests
from lxml import etree


def get_res():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
        'Referer': 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    }

    for i in range(2, 3):
        url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,' \
              '%d.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0' \
              '&dibiaoid=0&line=&welfare= ' % i

        print('开始爬取第：%d页数据' % i)
        html = requests.get(url=url, headers=headers).text
        # yield html

        info_url_list = re.findall('"job_href":"(.*?)"', html)

        for info_url in info_url_list:
            info_url = re.sub(r'\\','',info_url)
            # print(info_url)
            info_res = requests.get(url=info_url,headers=headers)
            info_res.encoding = 'utf-8'
            info_html = info_res.text

            yield info_html


def get_info():
    html_list = get_res()

    for html in html_list:
        # print(html)
        # break
        position_list = re.findall(r'"job_name":"(.*?)"', html)
        company_list = re.findall(r'"company_name":"(.*?)"', html)
        wages_list = re.findall(r'"providesalary_text":"(.*?)"', html)
        place_list = re.findall(r'"workarea_text":"(.*?)"', html)
        education_list = re.findall(r'attribute_text".*?经验","(.+?)"',html)
        work_experience = re.findall(r'attribute_text.*?,"(.*?)"',html)

        info = {}
        for position, company, wages, place, education in zip(position_list, company_list, wages_list, place_list , education_list):

            info['position'] = re.sub(r'\\', '', position)
            info['company'] = company
            info['wages'] = re.sub(r'\\', '', wages)
            info['place'] = place
            info['education'] = education

            # yield info
            # save_infoToMysql(info)
            print(info)

def save_infoToMysql():
    db = pymysql.connect(
        host='localhost',
        user='root',
        passwd='password',
        port=3306,
        database='spiders'
    )

    infos = get_info()
    for info in infos:

        cursor = db.cursor()

        sql = """
            insert into 51job values (
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        position = "'" + info['position'] + "'"
        company = "'" + info['company'] + "'"
        wages = "'" + info['wages'] + "'"
        place = "'" + info['place'] + "'"
        education ="'" + info['education'] + "'"


        cursor.execute(sql % (position, company, wages,place,education))

        db.commit()
        print('写入数据库中...')
    db.close()


if __name__ == '__main__':
    get_info()
