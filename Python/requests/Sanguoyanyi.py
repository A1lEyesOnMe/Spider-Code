#BS4实例
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":

    url = "https://www.shicimingju.com/book/sanguoyanyi.html"
    headers = {
        "User-Agent": "Mozilla / 5.0(Macintosh;Intel\MacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36"
    }

    page_text = requests.get(url=url, headers=headers)
    page_text.encoding = 'utf-8'
    html = page_text.text

    soup = BeautifulSoup(html,"lxml")
    li_list = soup.select('.book-mulu > ul > li')

    fp = open("./Sanguoyanyi.txt","w",encoding="utf-8")

    for li in li_list:
        title = li.a.string
        detail_url = "https://www.shicimingju.com/"+li.a["href"]

        detail_text = requests.get(url=detail_url,headers=headers)
        detail_text.encoding = "utf-8"
        html1 = detail_text.text

        soup2 = BeautifulSoup(html1,"lxml")
        div_tag = soup2.find("div",class_="chapter_content")
        text = div_tag.text
        fp.write(title+":"+text+'\n')
        print(title+" 保存成功")