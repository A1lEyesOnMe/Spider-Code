import time
import requests
import re


def get_data(page):
    url = "https://genius.com/api/songs/chart?time_period=day&chart_genre=all&page=" + str(page) + "%s&per_page=50&text_format=html%2Cmarkdown"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    proxy={
        "https":"127.0.0.1:4780"
    }
    res = requests.get(url=url,headers=headers,proxies=proxy)
    html = res.text
    # print(html)
    title_list = re.findall(re.compile('"title":"(.*?)"'),html)
    artist_list = re.findall(re.compile('"artist_names":"(.*?)"'),html)
    time_list = re.findall(re.compile('"lyrics_updated_at":(\d+)'),html)
    for title,artist,date in zip(title_list,artist_list,time_list):
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(date)))
        # print(title,artist,date)
        date =time.strptime(date,'%Y-%m-%d %H:%M:%S')
        print(int(time.mktime(date)))


if __name__ == '__main__':
    for page in range(1,2):
        get_data(page)