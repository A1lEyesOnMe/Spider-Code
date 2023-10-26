import requests
import re
import os

if __name__ == "__main__":

    headers = {
        "User-Agent": "Mozilla / 5.0(Macintosh;Intel\MacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36"
    }

    if not os.path.exists("./QiutuLibs"):
        os.mkdir("./QiutuLibs")

    url = "https://www.qiushibaike.com/imgrank/page/%d"
    for pageNum in range(1,2):
        new_url = format(url%pageNum)

        page_text = requests.get(url=new_url,headers=headers).text

        #数据解析
        ex = '<img src="(.*?)"'
        image_src_list = re.findall(ex,page_text,re.S)
        # print(image_src_list)
        for src in image_src_list:
            src = "https:"+src
            image_data = requests.get(url=src,headers=headers).content
            image_name = src.split("/")[-1]
            imagePath = "./QiutuLibs/"+image_name
            with open(imagePath,'a') as fp:
                fp.write(image_data)
                print(image_name,'写入成功！')