import requests
from lxml import etree
import os

if __name__ == '__main__':

    url = "http://pic.netbian.com/4kyingshi/"

    headers = {
        "User-Agent" : "Mozilla / 5.0(Macintosh;Intel\MacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36"
    }

    page = requests.get(url=url,headers=headers)
    page.encoding = page.apparent_encoding
    page_text = page.text

    parse = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(page_text,parser=parse)
    li_list = tree.xpath("//div[@class = 'slist']/ul/li")

    if not os.path.exists("./PicLibs"):
        os.mkdir('./PicLibs')

    for li in li_list:
        img_url = "http://pic.netbian.com/"+li.xpath("./a/@href")[0]
        img_name = li.xpath("./a/img/@alt")[0]+".jpeg"

        # img_page = requests.get(url=img_url,headers=headers)
        # img_page.encoding = img_page.apparent_encoding
        # img_page_text = img_page.text
        #
        # tree2 = etree.HTML(img_page_text,parser=parse)
        # pic_url = tree2.xpath("/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/a/img")
        # print(pic_url)


        # print(img_name,img_url)
        img_data = requests.get(url=img_url,headers=headers).content
        img_path = "./PicLibs/"+img_name
        with open(img_path,"wb") as fp:
            fp.write(img_data)
            print(img_name,"下载成功！")