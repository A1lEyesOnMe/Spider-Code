import  requests
from lxml import etree

if __name__ == '__main__':

    url = "https://bj.58.com/ershoufang/"

    headers = {
        "User-Agent" : "Mozilla / 5.0(Macintosh;Intel\MacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36"
    }

    page_text = requests.get(url=url,headers=headers).text

    parse = etree.HTMLParser(encoding='utf-8')
    tree = etree.HTML(page_text,parser=parse)

    title_list = tree.xpath("//div[@class = 'property-content-title']")
    fp = open("Beijing.txt",'w',encoding="utf-8")
    for title in title_list:
        house = title.xpath("./h3[@class = 'property-content-title-name']//text()")[0]
        fp.write(house+"\n")
    print("Done")