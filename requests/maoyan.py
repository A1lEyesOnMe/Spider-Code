import requests
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/71.0.3578.98 Safari/537.36'}
url = 'https://www.maoyan.com/films?yearId=17&showType=3&sortId=3&offset={}'

#遍历获得新链接
for i in range(0, 31, 30):
    url = url.format(i)
    # requests取得html
    response = requests.get(url, headers=headers).text

    # 使用etree解析网页
    tree = etree.HTML(response)

    movie_list = tree.xpath('//dl[@class="movie-list"]')
    for movie in movie_list:
        print(movie.xpath('./dd/div[2]/a/text()')[0])

