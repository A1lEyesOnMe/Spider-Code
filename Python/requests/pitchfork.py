import os
import re
import json
import pymysql
import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
}

url = 'https://pitchfork.com/features/lists-and-guides/the-200-best-albums-of-the-2010s/'


def get_res():
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    html = res.text

    # get_info(html)
    new_get_info(html)
    # print(html)


def get_info(html):
    parse = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(html, parser=parse)

    rank_list = tree.xpath('//div[@role="heading"]/text()')
    artist_list = tree.xpath('//div[@class ="article__chunks"]//h2/text()')
    album_list = tree.xpath('//div[@class ="article__chunks"]//h2/em/text()')
    releaseDate_list = tree.xpath('//div[@class ="article__chunks"]//h2/text()')
    pic_xpath_list = tree.xpath(
        '//picture[@class="ResponsiveImagePicture-jJiTGL jyYsQg AssetEmbedResponsiveAsset-ePfRP fhgzsG asset-embed__responsive-asset responsive-image"]/img/@src')
    # 由于懒加载，使用xpath无法爬取到所有图片，使用正则表达式提取

    cover_list_re = "1280w, (https:\/\/media.pitchfork.com\/photos\/.*?) 1600w"
    cover_name_re = "\/w_1600,c_limit\/(.*)1600w"
    cover_list = re.findall(cover_list_re, html)
    cover_name_list = re.findall(cover_name_re, html)

    rank_list.reverse()
    album_list.reverse()
    cover_list.reverse()
    cover_name_list.reverse()

    print(rank_list)
    print(artist_list[::-2])
    print(album_list)
    print(releaseDate_list[-2::-2])
    # print(cover_list)
    # print(cover_name_list)

    infos = {}

    for rank, artist, album, releaseDate, cover, cover_name in zip(rank_list, artist_list[-2::-2], album_list,
                                                                   releaseDate_list[::-2], cover_list, cover_name_list):
        # print(rank.replace('.',''),artist.replace(':',''),album,releaseDate.replace("(","").replace(")",""),cover)
        infos.update({'rank': re.sub('\.', '', rank),
                      'artist': re.sub(':', '', artist),
                      'album': album,
                      'releaseDate': releaseDate.replace("(", "").replace(")", ""),
                      'Cover_link': cover
                      })
        # print(infos)
    # 指定保存方法
    # save_infosToLocal(infos)
    # save_infosToMysql(infos)
    # save_cover(cover, cover_name, rank)


def new_get_info(html):
    global cover, cover_name
    parse = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(html, parser=parse)

    allData = tree.xpath(
        '//*[@id="main-content"]/article/div[2]/div[1]/div[1]')

    for data in allData:
        releaseDate_list = data.xpath('.//div/h2/text()')[1::2]
        artist_list = data.xpath('.//div/h2/text()')[::2]
        album_list = data.xpath('.//div/h2/em/text()')
        rank_list = data.xpath('.//div[@class="heading-h3"]/text()')

        cover_list_re = "1280w, (https:\/\/media.pitchfork.com\/photos\/.*?) 1600w"
        cover_name_re = "\/w_1600,c_limit\/(.*)1600w"
        cover_list = re.findall(cover_list_re, html)
        cover_name_list = re.findall(cover_name_re, html)

        infos = []

        for rank, album, artist, releaseDate, cover, cover_name in zip(rank_list, album_list, artist_list,
                                                                       releaseDate_list, cover_list, cover_name_list):
            info = {
                'rank': re.sub('\.', '', rank),
                'album': album,
                'artist': re.sub(':', '', artist),
                'releaseYear': releaseDate.replace('(', '').replace(')', '').strip(),
                'cover_link': cover
            }
            infos.append(info)
            save_cover(cover, cover_name)
            save_infosToMysql(infos)
        # save_infosToLocal(infos)


def save_cover(cover, cover_name):
    if not os.path.exists('/Users/mac/Desktop/cover'):
        os.mkdir('/Users/mac/Desktop/cover')
    cover_content = requests.get(url=cover, headers=headers).content
    cover_path = '/Users/mac/Desktop/cover/' + cover_name.replace('.jpg', '').strip() + '.jpg'
    with open(cover_path, 'wb') as fp:
        fp.write(cover_content)
        print(cover_name + '下载完成！！！')


def save_infosToLocal(infos):
    with open('pitchfork.json', 'a', encoding='utf8') as fp:
        json.dump(infos, ensure_ascii=False, fp=fp)
        print("正在爬取数据...")


def save_infosToMysql(infos):
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="password",
        port=3306,
        database='spiders'
    )
    cursor = db.cursor()

    sqlToTable = '''
        insert into pitchfork values 
        (
            %s,
            %s,
            %s,
            %s
        )
    '''

    rank = infos["rank"]
    artist = "'" + infos["artist"] + "'"
    album = "'" + infos["album"] + "'"
    releaseDate = "'" + infos["releaseDate"] + "'"

    # print(rank,artist,album,releaseDate)
    cursor.execute(sqlToTable % (rank, artist, album, releaseDate))
    db.commit()
    cursor.close()
    db.close()


if __name__ == '__main__':
    get_res()
    # print('downloaded')
