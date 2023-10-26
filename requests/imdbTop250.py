import re
import pymysql
import requests

if __name__ == '__main__':

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
}

    url = 'https://www.imdb.com/chart/top'

    info = {}

    res = requests.get(url=url,headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    # print(html)
    rank_re = 'span name="rk" data-value="(\d+)"'
    score_re = 'span name="ir" data-value="(\d\.\d)'
    title_re = '>(.*?)<\/a>\s.*?secondaryInfo'
    release_re = 'secondaryInfo">\((\d+)\)'

    rank_list = re.findall(rank_re,html)
    score_list = re.findall(score_re, html)
    title_list = re.findall(title_re,html)
    release_list = re.findall(release_re,html)



