import requests
import re
import pandas as pd
import os

# 用于爬取剧集页面数据
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }

    r = requests.get(url, headers=headers)
    # 乱码修正
    r.encoding = r.apparent_encoding
    text = r.text
    # 去掉非字符数据
    html = re.sub('\s', '', text)

    return html

# 传入电视剧等的id，用于爬取剧集id和评论id
def get_comment_ids(video_id):
    # 剧目地址

    url = f'https://v.qq.com/x/cover/{video_id}.html'
    html = get_html(url)
    data_list = eval(re.findall(r'"vip_ids":(\[.*?\])', html)[0])    
    data_df = pd.DataFrame(data_list)
    
    comment_ids = []
    for tid in data_df.V:
        # 每集地址
        url = f'https://v.qq.com/x/cover/{video_id}/{tid}.html'
        html = get_html(url)
        comment_id = eval(re.findall(r'"comment_id":"(\d+)"', html)[0])
        comment_ids.append(comment_id)
    
    data_df['comment_id'] = comment_ids
    data_df['剧集'] = range(1,len(comment_ids)+1)
    return data_df

# 获取全部剧集评论
def get_comment_content(data_df):
    for i, comment_id in enumerate(data_df.comment_id):
        i = i+1
        # 初始 cursor
        cursor = 0
        num = 0
        while True:
            url = f'https://video.coral.qq.com/varticle/{comment_id}/comment/v2?'
            params = {
                'orinum': 30,
                'cursor': cursor,
                'oriorder': 't'
            }    
            r = requests.get(url, params=params)
            data = r.json()
            data = data['data']
            if len(data['oriCommList'])==0:
                break
            # 评论数据
            data_content = pd.DataFrame(data['oriCommList'])
            data_content = data_content[['id', 'targetid', 'parent', 'time', 'userid', 'content', 'up']]
            # 评论员信息
            userinfo = pd.DataFrame(data['userList']).T
            userinfo = userinfo[['userid', 'nick', 'head', 'gender', 'hwlevel']].reset_index(drop=True)
            # 合并评论信息与评论员信息
            data_content = data_content.merge(userinfo, how='left')
            data_content.time = pd.to_datetime(data_content.time, unit='s') + pd.Timedelta(days=8/24)
            data_content['剧集'] = i
            data_content.id = data_content.id.astype('string')
            save_csv(data_content)
            # 下一个 cursor
            cursor = data['last']
            num =num + 1
            pages = data['oritotal']//30 + 1
            print(f'第{i}集的第{num}/{pages}页评论已经采集！')

# 将评论数据保存本地
def save_csv(df):
    file_name = '评论数据.csv'
    if os.path.exists(file_name):
        df.to_csv(file_name, mode='a', header=False,
          index=None, encoding='utf_8_sig')
    else:
        df.to_csv(file_name, index=None, encoding='utf_8_sig')
    print('数据保存完成！')

        
        