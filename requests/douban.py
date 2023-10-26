import pandas as pd
import requests
from bs4 import BeautifulSoup
import jieba


all_movie_name=[]#电影名称
all_movie_class=[]#电影类型
all_movie_region=[]#电影产出地区
all_movie_time=[]#电影产出时间
all_movie_score=[]#电影评分
all_movie_people=[]#电影评论人数
for offset in range(0, 250, 25):
    url = 'https://movie.douban.com/top250?start=' + str(offset) +'&filter='
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
            }
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
    all_movies = soup.find('ol', class_ ="grid_view")
    #print(all_movies)
    for each_movie in all_movies.find_all('div', class_ ="hd"):
        all_span=each_movie.find_all('span')
        #爬取电影名称
        movie_name = all_span[0].text
        # print(movie_name)
        all_movie_name.append(movie_name)

    for each_movie in all_movies.find_all('div', class_ ="bd"):
        all_p=each_movie.find_all('p')
        movie_info = all_p[0].text
        movie_info = movie_info.split('/')
        #爬取电影类型
        movie_class = movie_info[len(movie_info)-1]
        movie_class= movie_class.strip()
        # print(movie_class)
        all_movie_class.append(movie_class)
        #爬取电影产出地区
        movie_region = movie_info[len(movie_info)-2]
        movie_region = movie_region.strip()
        # movie_region = movie_region.replace(' ','')
        # print(movie_region)
        all_movie_region.append(movie_region)
        #爬取电影产出时间
        movie_time = movie_info[len(movie_info)-3]
        movie_time="".join(filter(str.isdigit,movie_time))
        # print(movie_time)
        all_movie_time.append(movie_time)
    for each_movie in all_movies.find_all('div', class_ ="star"):
        all_span=each_movie.find_all('span',class_ ="rating_num")
        #爬取电影评分
        movie_score = all_span[0].text
        movie_score=movie_score.strip()
        # print(movie_score)
        all_movie_score.append(movie_score)
        all_span1=each_movie.find_all('span')
        #爬取电影评论人数
        movie_people = all_span1[3].contents[0]
        movie_people = "".join(filter(str.isdigit,movie_people))
        # print(movie_people)
        all_movie_people.append(movie_people)

# 将list转化为dataframe
movie_name = pd.DataFrame(all_movie_name)
movie_class = pd.DataFrame(all_movie_class)
movie_region = pd.DataFrame(all_movie_region)
movie_time = pd.DataFrame(all_movie_time)
movie_score = pd.DataFrame(all_movie_score)
movie_people = pd.DataFrame(all_movie_people)

# 拼接数据
movie_data = pd.concat([movie_name, movie_class, movie_region, movie_time, movie_score, movie_people], axis=1)
movie_data.columns=['movie_name','movie_class','movie_region','movie_time','movie_sorce','movie_people']

# 输出
movie_data.to_excel('./douban.xlsx')