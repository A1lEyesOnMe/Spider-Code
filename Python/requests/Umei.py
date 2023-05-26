import os
import requests
from lxml import etree

if __name__ == '__main__':

    if not os.path.exists("./PicLibs"):
        os.mkdir('./PicLibs')

    headers = {
        "User-Agent" : "Mozilla / 5.0(Macintosh;Intel\MacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36"
    }

    parse = etree.HTMLParser(encoding='utf-8')

    for i in range(2,3):
        url = "https://www.umei.cc/meinvtupian/meinvxiezhen/index_%s.htm"%i

        page = requests.get(url=url,headers=headers)
        page.encoding = page.apparent_encoding
        page_text = page.text

        tree = etree.HTML(page_text,parser=parse)

        all_pic_list = tree.xpath("//*[@class = 'TypeList']/ul/li")
        for pic in all_pic_list:
            pic_url = "https://www.umei.net"+pic.xpath("./a/@href")[0]
            # print(pic_url)

            page2 = requests.get(url=pic_url,headers=headers)
            page2.encoding = page2.apparent_encoding
            page2_text = page2.text
            # print(page2_text)

            tree2 = etree.HTML(page2_text,parser=parse)
            pic_name = tree2.xpath("/html/body/div[2]/div[3]/strong/text()")[0]+'.jpg'
            # print(pic_name)
            pic_data = tree2.xpath("//*[@class = 'ImageBody']/p/a/img/@src")[0]
            # print(pic_data)
            pic_content = requests.get(url=pic_data,headers=headers).content
            pic_path = "./PicLibs/"+pic_name
            with open(pic_path,'wb') as fp:
                fp.write(pic_content)
                print(pic_name+"，下载成功")





