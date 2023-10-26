import json
import requests
import http.cookiejar as cookielib
from lxml import etree

vueSession = requests.session()
vueSession.cookies = cookielib.LWPCookieJar(filename='vueCookies.txt')

headers = {
        "User-Agent" : "Mozilla / 5.0(Macintosh;Intel\MacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 88.0.4324.146Safari / 537.36",
        # 'Origin':'http://vue3-admin.newbee.ltd',
        'Referer':'http://vue3-admin.newbee.ltd/',
        'token': '748e7b9fb21f28050e22f0cab77764ce',
        'sentry-trace':'d3d4a6c8b87841a3be47e78b293d4d3c-83ad0be7f47782a1-1'
    }

def login(account,password):
    print('start logging...')
    login_Url = 'http://vue3-admin.newbee.ltd/#/login/'
    postData = {
        'userName':account,
        'passwordMd5':password
    }
    res = vueSession.post(url=login_Url,headers=headers,data=postData)
    print(f'statusCode = {res.status_code}')
    print(f'text = {res.text}')
    vueSession.cookies.save()

def get_guest():
    print('get guest info...')
    count = 0
    with open('user.json', 'w', encoding='utf8') as fp:
        fp.write('[')
        for page in range(1,783):
            json_url = 'http://backend-api-02.newbee.ltd/manage-api/v1/users?pageNumber=%s&pageSize=10'%(page)
            res = vueSession.get(url=json_url,headers=headers,allow_redirects=False)
            # print(f'isLoginStatus = {res.status_code}')
            data_list = res.json()
            data_list = data_list['data'].get('list')
            # print(data_list['data'].get('list'))
            for data in data_list:
                count += 1
                fp.write(json.dumps(data, ensure_ascii=False))
                fp.write(',')
                print("正在爬取数据...")
        fp.write(']')
    print(f"==数据共有{count}条==")

def get_order():
    print('get order info...')
    count =0
    with open('order.json', 'w', encoding='utf8') as fp:
        fp.write('[')
        for page in range(1,536):
            json_url = 'http://backend-api-02.newbee.ltd/manage-api/v1/orders?pageNumber=%s&pageSize=10&orderNo=&orderStatus='%(page)
            res = vueSession.get(url=json_url,headers=headers,allow_redirects=False)
            # print(f'isLoginStatus = {res.status_code}')
            data_list = res.json()
            data_list = data_list['data'].get('list')

            for data in data_list:
                count += 1
                fp.write(json.dumps(data, ensure_ascii=False))
                fp.write(',')
                print("正在爬取数据...")
        fp.write(']')
    print(f"==数据共有{count}条==")

def del_order():
    order_data = []
    pay_data = []
    order_acc = 0
    pay_acc = 0
    with open('order.json','r+',encoding='utf-8') as fp:
        json_data = json.load(fp)
        for data in json_data:
            if data['orderStatus'] !=-1:
                order_data.append(data)
            else:
                order_acc+=1

    print(f"==手动关闭共有{order_acc}条==")
    print(len(order_data))
    for data in order_data:
        if data['payType'] != 0:
            pay_data.append(data)
        else:
            pay_acc += 1

    print(f"==无支付方式共有{pay_acc}条==")
    print(len(pay_data))

    new_data = []
    for data in pay_data:
        if data['payStatus'] == 1:
            data['payStatus'] = '以支付'
            if data['payType'] == 1:
                data['payType'] = '微信'
            elif data['payType'] == 2:
                data['payType'] = '支付宝'
                if data['isDeleted'] ==0:
                    data['isDeleted'] = '未删除订单'
                    if data['orderStatus'] == 0:
                        data['orderStatus'] = '待支付'
                    elif data['orderStatus'] == 1:
                        data['orderStatus'] = '以支付'
                    elif data['orderStatus'] == 2:
                        data['orderStatus'] = '配货完成'
                    else:
                        data['orderStatus'] = '出库成功'
        new_data.append(data)
    with open('order_v.json', 'w', encoding='utf-8') as fp:
            fp.write('[')
            for data in new_data:
                    fp.write(json.dumps(data, ensure_ascii=False))
                    fp.write(',')
                    print('开始写数据')
            fp.write(']')

def del_user():
    user_data = []
    user_count = 0
    new_data = []
    with open('user.json','r+',encoding='utf-8') as fp:
        json_data = json.load(fp)
        for data in json_data:
            if data['lockedFlag'] != 1:
                user_data.append(data)
            else:
                user_count +=1
    print(f"==禁用共有{user_count}条==")
    print(len(user_data))
    for data in user_data:
        if data['lockedFlag'] ==0:
            data['lockedFlag'] = '正常'
        new_data.append(data)
    with open('user_v.json', 'w', encoding='utf-8') as fp:
            fp.write('[')
            for data in new_data:
                    fp.write(json.dumps(data, ensure_ascii=False))
                    fp.write(',')
                    print('开始写数据')
            fp.write(']')

def rename_order():
    with open('order.json', 'r+', encoding='utf-8') as fp:
        json_data = json.load(fp)
        new_data = []
        for data in json_data:
            if data['payStatus'] == 1:
                data['payStatus'] = '以支付'
            else:
                data['payStatus'] = '待支付'
            if data['payType'] == 1:
                data['payType'] = '微信'
            elif data['payType'] == 2:
                data['payType'] = '支付宝'
            else:
                data['payType'] = '未支付'
            if data['isDeleted'] == 0:
                data['isDeleted'] = '未删除订单'
                if data['orderStatus'] == 0:
                    data['orderStatus'] = '待支付'
                elif data['orderStatus'] == 1:
                    data['orderStatus'] = '以支付'
                elif data['orderStatus'] == 2:
                    data['orderStatus'] = '配货完成'
                elif data['orderStatus'] == 3:
                    data['orderStatus'] = '出库成功'
                else:
                    data['orderStatus'] = '手动关闭'

            new_data.append(data)
        with open('order_rename.json', 'w', encoding='utf-8') as fp:
            fp.write('[')
            for data in new_data:
                fp.write(json.dumps(data, ensure_ascii=False))
                fp.write(',')
                print('开始写数据')
            fp.write(']')

def rename_user():
    with open('user.json', 'r+', encoding='utf-8') as fp:
        json_data = json.load(fp)
        new_data = []
        for data in json_data:
            if data['lockedFlag'] == 1:
                data['lockedFlag'] = '禁用'
            else:
                data['lockedFlag'] = '正常'
            new_data.append(data)
        with open('user_rename.json', 'w', encoding='utf-8') as fp:
            fp.write('[')
            for data in new_data:
                fp.write(json.dumps(data, ensure_ascii=False))
                fp.write(',')
                print('开始写数据')
            fp.write(']')


if __name__ == '__main__':
    # vueSession.cookies.load()

    # guest_json = get_guest()

    # order_json = get_order()

    # del_order()

    # del_user()

    rename_order()

    rename_user()
