import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
}

target_url='https://gol.gg/players/list/season-ALL/split-ALL/tournament-LPL%20Spring%202021/'

# 利用python访问网页需要的request
res = requests.get(target_url,headers)
html_data=res.text

# 烹饪soup(创建一个名为soup的DOM对象)
soup = BeautifulSoup(html_data,"html.parser")

header=[]

# 通过soup对象寻找table-->thead-->tr-->th内的text内容
for a in soup.select('table thead tr th'):
  header.append(a.text)
print(header)