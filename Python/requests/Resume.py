import requests
from lxml import etree
import os

if __name__ == '__main__':

    if not os.path.exists("./ResumeLibs"):
        os.mkdir('./ResumeLibs')

    headers = {
        "User-Agent" : "Mozilla / 5.0(Macintosh;Intel\MacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36"
    }

    for i in range(2,10):
        url = "https://sc.chinaz.com/jianli/free_%s.html"%i

        page = requests.get(url=url,headers=headers)
        page.encoding = page.apparent_encoding
        page_text = page.text

        parse = etree.HTMLParser(encoding="utf-8")
        tree = etree.HTML(page_text,parser=parse)

        all_resume_list = tree.xpath("//*[@id='container']/div")
        for resume in all_resume_list:
            resume_name = resume.xpath("./a/img/@alt")[0]+".rar"
            # print(resume_name)
            resume_url = "https:"+resume.xpath("./a/@href")[0]
            # print(resume_url)

            page2 = requests.get(url=resume_url,headers=headers)
            page2.encoding = page2.apparent_encoding
            page2_text = page2.text
            # print(page2_text)

            tree2 = etree.HTML(page2_text,parser=parse)
            download_url = tree2.xpath("//*[@class='clearfix']/li[1]/a/@href")[0]
            # print(download_url)

            resume_content = requests.get(url=download_url,headers=headers).content
            resume_path = "./ResumeLibs/"+resume_name
            with open(resume_path, "wb") as fp:
                fp.write(resume_content)
                print(resume_name, "下载成功！")

    print("Done")




