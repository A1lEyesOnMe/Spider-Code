import re
import requests

url = "http://1.15.245.63/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
}

def get_url():
    response = requests.get(url=url,headers=headers)
    print(response.text)

if __name__ == '__main__':
    get_url()
