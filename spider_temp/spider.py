import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
from selenium.webdriver.common.by import By
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3

jspath_number_of_comment = "#app > div.contain-box > div > div > div.comment-mid.clearfix > div.mid-right > div.m-t > span"
jspath_goods_name = ("#app > div:nth-child(2) > div:nth-child(1) > div > div > h2")

def get_comment(url):
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        return "", 0
    time.sleep(random.randint(5, 10))
    
    # 获取商品名
    try:
        element = driver.find_elements(By.CSS_SELECTOR, jspath_goods_name)
        if len(element) == 0:
            print("no such item")
            return "", 0
    except Exception as e:
        print(e)
        return "", 0
    
    goods_name = element[0].text
    # 获取评论数
    try:
        element = driver.find_element(By.CSS_SELECTOR, jspath_number_of_comment)
        if element == None:
            print("no such element")
            return "", 0
        number_of_comment = int(element.text)
        print(goods_name, number_of_comment)
    except Exception as e:
        print(e)
        return "", 0
    return goods_name, number_of_comment



if __name__=="__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # 添加自定义User-Agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    options.add_argument(f"user-agent={user_agent}")

    # 使用 Service 对象指定 ChromeDriver 路径
    print(ChromeDriverManager().install())
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)
    
    # 每隔一天，update_all_comment 一次
    schedule.every().day.at("19:45").do(update_all_comment)

    while True:
        schedule.run_pending()
        time.sleep(30)