import requests
import re
import json


url_2020 = 'http://weekly.chinacdc.cn/news/TrackingtheEpidemic2020.htm'
url_2021 = 'http://weekly.chinacdc.cn/news/TrackingtheEpidemic.htm#b.html'
def get_html(url):
    response = requests.get(url)
    response.encoding =  response.apparent_encoding
    html = response.text
    return html

html_2020 = get_html(url_2020)
html_2021 = get_html(url_2021)

selector_2020 = re.findall(r'([A-Za-z]+.{0,1}[0-9]+,.{0,1}\d{4})</a>(<.{1,6}>)?</p><p >[A-Za-z\s]+:.(\d*).new,.(\d*,?\d+)',html_2020)
selector_2021 = re.findall(r'([A-Za-z]+.{0,1}[0-9]+,.{0,1}\d{4})</a>(<.{1,6}>)?</p><p >[A-Za-z\s]+:.(\d*).new,.(\d*,?\d+)',html_2021)

list_2020 = list(zip(*selector_2020))
list_2021 = list(zip(*selector_2021))
date = list(list_2021[0]+list_2020[0])
new = list(list_2021[2]+list_2020[2])
count = list(list_2021[3]+list_2020[2])

print(count)