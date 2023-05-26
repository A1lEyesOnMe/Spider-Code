import requests
import re
import csv
# import xlwt

if __name__ == '__main__':

    url = "https://www.metacritic.com/browse/albums/score/metascore/all/filtered?sort=desc&page=%d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    proxy = {
        'http':'121.232.148.117:3256'
    }
    # with open('./BestAlbumsAllTheTime.csv', "w", newline="", encoding='utf_8_sig') as f:
    #     f_csv =csv.writer(f)
    #     headers = ['Title','Artist','ReleaseDate','Info','MetaScore','UserScore','Cover']
    #     f_csv.writerow(headers)

    for pageNum in range(0,129):

        title_list = []
        artist_list = []
        releaseDate_list = []
        cover_list = []
        info_list = []
        metaScore_list = []
        userScore_list = []

        new_url = format(url%pageNum)
        # print(new_url)
        response = requests.get(url=new_url,headers=headers).text
        # print(response)
        print("开始下载第%d页"%pageNum)

        title_re = 'class="title"><h3>(.*?)<\/h3>'
        artist_re = 'class="artist">\s*by.(.*?)\s*<\/div>'
        releaseDate_re ='class="artist">\s*.*?\s*<\/div>\s+<span>(.*?)<\/span>'
        cover_re ='image-wrap">\s+.*src="(.*)".*alt'
        info_re = 'summary">\s+(.*)\s+?<\/div>'
        metaScore_re = 'metascore_anchor.*\s.*>(\d+.*?)<.*\s+.*\s+.*\s+<div.+\s+<.+'
        userScore_re = 'metascore_anchor.*\s.+user.+">(\d+.*?)<'

        title_list.append(re.findall(title_re,response,re.S))
        artist_list.append(re.findall(artist_re,response,re.S))
        releaseDate_list.append(re.findall(releaseDate_re,response,re.S))
        cover_list.append(re.findall(cover_re,response))
        info_list.append(re.findall(info_re,response))
        metaScore_list.append(re.findall(metaScore_re,response))
        userScore_list.append(re.findall(userScore_re,response))

        # print(title_li
        # print(artist_list)
        # print(releaseDate_list)
        # print(cover_list)
        # print(info_list)
        # print(metaScore_list)
        # print(userScore_list)


        for titlelist,artistlist,releaseDatelist,infolist,metaScorelist,userScorelist,coverlist in zip(title_list,artist_list,releaseDate_list,info_list,metaScore_list,userScore_list,cover_list):
            for title,artist,releaseDate,info,metaScore,userScore,cover in zip(titlelist,artistlist,releaseDatelist,infolist,metaScorelist,userScorelist,coverlist):
                with open('./BestAlbumsAllTheTime.csv',"a",newline="",encoding='utf_8_sig') as fp:
                    fp_csv = csv.writer(fp)
                    fp_csv.writerow([title,artist,releaseDate,info,metaScore,userScore,cover])
        print("第%d页下载完成"%pageNum)

    print("Greats albums of all time list is fully downloaded!!!!")


