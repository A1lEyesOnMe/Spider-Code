import random
import requests
import re
import csv

if __name__ == '__main__':

    url = "https://www.metacritic.com/browse/albums/score/metascore/all/filtered?sort=desc&page=%d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    }

    # 因访问网站次数太多，使用代理随机访问
    proxy_list = [
        'http://176.113.73.104:3128',
        'http://176.113.73.99:3128',
        'http://67.205.190.164:8080',
        'http://46.21.153.16:3128',
        'http://84.17.35.129:3128',
        'http://104.248.59.38:80'
    ]


    with open('./MetaChart.csv', "w", newline="", encoding='utf-8') as fp:
        title = ['Title', 'Artist', 'ReleaseDate', 'Info', 'MetaScore', 'UserScore', 'Cover']
        writer = csv.writer(fp)
        writer.writerow(title)

    #翻页操作
    for pageNum in range(0,136):
        new_url = format(url%pageNum)
        # print(new_url)

        #随机使用代理
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}

        response = requests.get(url=new_url,headers=headers,proxies=proxies).text
        # print(response)
        print("开始下载第%d页"%(pageNum+1))

        title_re = 'class="title"><h3>(.*?)<\/h3>'
        artist_re = 'class="artist">\s*by.(.*?)\s*<\/div>'
        releaseDate_re ='class="artist">\s*.*?\s*<\/div>\s+<span>(.*?)<\/span>'
        cover_re ='image-wrap">\s+.*src="(.*)".*alt'
        info_re = 'summary">\s+(.*)\s+?<\/div>'
        metaScore_re = 'metascore_anchor.*\s.*>(\d+.*?)<.*\s+.*\s+.*\s+<div.+\s+<.+'
        userScore_re = 'metascore_anchor.*\s.+user.+">(\d+.*?)<'

        title_list = re.findall(title_re,response,re.S)
        artist_list = re.findall(artist_re,response,re.S)
        releaseDate_list = re.findall(releaseDate_re, response, re.S)
        cover_list = re.findall(cover_re, response)
        info_list = re.findall(info_re, response)
        metaScore_list = re.findall(metaScore_re, response)
        userScore_list = re.findall(userScore_re, response)

        # print(title_list)
        # print(artist_list)
        # print(releaseDate_list)
        # print(cover_list)
        # print(info_list)
        # print(metaScore_list)
        # print(userScore_list)
        # print(len(title_list),len(artist_list),len(releaseDate_list),len(metaScore_list),len(userScore_list))


        for title,artist,releaseDate,info,metaScore,userScore,cover in zip(title_list,artist_list,releaseDate_list,info_list,metaScore_list,userScore_list,cover_list):
            with open('./MetaChart.csv',"a",newline="",encoding='utf-8') as fp:
                data = (title, artist, releaseDate, info, metaScore, userScore,cover)

                writer = csv.writer(fp)
                writer.writerow(data)

        print("第%d页下载完成"%(pageNum+1))

    print("chart is downloaded !!")



