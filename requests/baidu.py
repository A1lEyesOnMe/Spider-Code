from selenium import webdriver
from time import sleep

chrome = webdriver.Chrome(executable_path='../selenium/chromedriver')
chrome.get('https://www.baidu.com')

sleep(1)
input = chrome.find_element_by_id('kw')
sleep(1)
input.send_keys('周杰伦')
sleep(1)
btn = chrome.find_element_by_id('su')
btn.click()

sleep(1)
toBottom = 'document.documentElement.scrollTop=100000'
chrome.execute_script(toBottom)
sleep(3)

next_page = chrome.find_element_by_class_name('n')
next_page.click()
sleep(3)
chrome.back()
sleep(3)
chrome.forward()
sleep(3)
chrome.quit()