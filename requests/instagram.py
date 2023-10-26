# -*- coding: utf-8 -*-
import json
import re
from lxml import etree
import requests
from lxml import etree
from urllib import parse

url = "https://www.instagram.com/kyliejenner/"
headers = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/urnotchrislee/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36",
    "Host": "www.instagram.com",
    "Cookie":'ig_did=BB476A03-EBCD-47A9-B53C-72BE2C5FB761; ig_nrcb=1; mid=YXJkQAAEAAFz_gyp5w-GRy3q9uPY; csrftoken=TUxX5SJ53tyeezecCVySHYRlaMAI5xUK; ds_user_id=4785800522; sessionid=4785800522%3ArICbpgpUvhbUvz%3A12; shbid="14718\0544785800522\0541668769797:01f79549e9df5aef7732942911292a9908182c234ed4e542ac65280417f9f80d0e961a69"; shbts="1637233797\0544785800522\0541668769797:01f7c2e39dfb5fd0b86273abd187d9233911bab20801298122cb5925678cd94764e88827"; rur="EAG\0544785800522\0541668862745:01f7facc34abed53df7f16508269308e16c9adf7f4b66b2edb42793d9fb20f3a4eba1aa9'
}


def get_urls(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('请求错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        return None
html = get_urls(url)
# print(html)

import json
from pyquery import PyQuery as pq

urls = []
html.encode('utf-8').decode('unicode_escape')
doc = pq(html)
items = doc('script[type="text/javascript"]').items()

for item in items:
    if item.text().strip().startswith('window._sharedData'):
        js_data = json.loads(item.text()[21:-1])
        edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
        for edge in edges:
            url = edge['node']['display_url']
            print(url)
            urls.append(url)