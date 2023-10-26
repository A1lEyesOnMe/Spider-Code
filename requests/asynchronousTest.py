import time
from multiprocessing.dummy import Pool

# def get_page(str):
#     print("正在下载：",str)
#     time.sleep(2)
#     print("下载成功",str)
#
# name_list =['xiaozi','aa','bb','cc']
#
# start_time = time.time()
#
# for  i in range(len(name_list)):
#     get_page(name_list[i])
#
# end_time = time.time()
# print("%d second"%(end_time-start_time))

start_time = time.time()

def get_page(str):
    print("正在下载：",str)
    time.sleep(2)
    print("下载成功",str)

name_list =['xiaozi','aa','bb','cc']

pool = Pool(4)
pool.map(get_page,name_list)
end_time = time.time()
print(end_time-start_time)
