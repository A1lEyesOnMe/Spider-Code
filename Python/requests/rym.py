import re
import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
}

url = "https://rateyourmusic.com/charts/top/album/all-time/deweight:live,archival,soundtrack/"


def get_html(page):
    res = requests.get(url=url + str(page), headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    # print(html)
    get_infos(html)


def get_infos(html):
    parse = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(html, parser=parse)

    albumAndArtist_list = tree.xpath('//span[@class="ui_name_locale_original"]/text()')
    Artist_list = tree.xpath('//div[@class="page_charts_section_charts_item_credited_links_primary"]/a//span/text()')
    releaseDate_list = tree.xpath('//div[@class="page_charts_section_charts_item_date"]/span/text()')
    averageScore_list = tree.xpath('//span[@class="page_charts_section_charts_item_details_average_num"]/text()')
    ratings_list = tree.xpath('//span[@class="page_charts_section_charts_item_details_ratings"]//span[@class="full"]/text()')

    # print(albumAndArtist_list[1::2])
    # print(albumAndArtist_list[::2])
    # print(releaseDate_list[::2])
    # print(averageScore_list)

    # i = 0
    # for album, artis, releaseDate, averageScore in zip(albumAndArtist_list[1::2], albumAndArtist_list[::2],releaseDate_list[::2], averageScore_list):
    #     i += 1
    #     print(str(i) + "|" + album + "|", artis + "|", releaseDate + "|", averageScore)


if __name__ == '__main__':
    for page in range(1, 2):
        get_html(page)
