import math
import re
import time
import json
import requests


user_url = 'https://music.163.com/api/v1/user/detail/'

headers = {
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}


def getComments(page):
    songs_url = 'https://music.163.com/api/v1/resource/comments/R_SO_4_469104548?limit=20&offset=' + str(page)
    res =requests.get(url=songs_url,headers=headers)
    json = res.json()
    # print(json['comments'])
    comments_list =json["comments"]
    data_list = []
    for comments in comments_list:
        user_name = comments['user']['nickname']
        user_id = comments['user']['userId']
        icon = comments['user']['avatarUrl']
        content = comments['content']
        user_message = getUserInfo(user_id)
        print(user_message)
        data_list.append({
            "用户名": user_name,
            '头像链接': icon,
            "评论":content,
        })
    print(data_list)

def getUserInfo(user_id):
    data = []
    url = user_url + str(user_id)
    res = requests.get(url=url,headers=headers)
    js = res.json()
    if js['code'] == 200:
        # 性别
        data['gender'] = js['profile']['gender']
        # 年龄
        if int(js['profile']['birthday']) < 0:
            data['age'] = 0
        else:
            data['age'] = (2018 - 1970) - (int(js['profile']['birthday']) // (1000 * 365 * 24 * 3600))
        if int(data['age']) < 0:
            data['age'] = 0
        # 城市
        data['city'] = js['profile']['city']
        # 个人介绍
        data['sign'] = js['profile']['signature']
    else:
        data['gender'] = '无'
        data['age'] = '无'
        data['city'] = '无'
        data['sign'] = '无'
    return js

def main():
    # for i in range(0, 25000, 20):
    #     print('---------------第 ' + str(i // 20 + 1) + ' 页---------------')
        getComments(0)

if __name__ == '__main__':
    main()