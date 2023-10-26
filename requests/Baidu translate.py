import json
import requests
import re

if __name__ == '__main__':

    url = 'https://fanyi.baidu.com/sug'

    headers = {
        "User-Agent" : "Mozilla / 5.0(Macintosh;Intel\MacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36"
    }

    data = {
        'kw':'nose'
    }
    response = requests.post(url=url,headers=headers,data=data)
    obj = json.loads(response.text)
    print(obj)
