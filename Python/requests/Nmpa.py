import requests
import json
if __name__ == "__main__":

    url = "http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList"

    for page in range(1,368):
        page = str(page)
    data = {
        "on": "true",
        "page": page,
        "pageSize": "15",
        "productName": "",
        "conditionType": "1",
        "applyname": "",
        "applysn": "",
    }

    headers = {
        "User-Agent" : "Mozilla / 5.0(Macintosh;Intel\MacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36"
    }

    id_list = []
    all_data_list = []

    json_ids = requests.post(url=url,headers=headers,data=data).json()
    for dic in json_ids['list']:
        id_list.append(dic['ID'])

    post_url="http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById"
    for id in id_list:
        data = {
            "id":id
        }
        detail_json = requests.post(url=post_url,headers=headers,data=data).json()
        all_data_list.append(detail_json)
        fp = open("./AllData.json",'w',encoding='utf-8')
        json.dump(all_data_list, fp=fp, indent=True, ensure_ascii=False)
print("done")