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
from .database import *

jspath_number_of_comment = "#app > div.contain-box > div > div > div.comment-mid.clearfix > div.mid-right > div.m-t > span"
jspath_goods_name = ("#app > div:nth-child(2) > div:nth-child(1) > div > div > h2")

def get_global_driver():
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
    return driver

def get_comment(driver,url):
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


def update_all_comment(driver):
    items = query_all_items()
    for item in items:
        id_mi = item[1]
        name = item[2]
        number_of_comments = item[3]
        goods_name, number_of_comment = get_comment(driver,f"https://www.mi.com/shop/comment/{id_mi}.html")   #'https://www.mi.com/shop/comment/19300.html'
        # 如果goods_name为空
        if goods_name == "":
            print("no such item")
            # 插入到off_shelf_items中
            insert_off_shelf_item(id_mi=id_mi,name=name)
            continue
        if goods_name != name:
            print("name is different, update it")
            insert_item(id_mi, goods_name, number_of_comment)
        
        # 时间只保留到天
        insert_comments(id_mi, time.strftime("%Y-%m-%d", time.localtime()),name, number_of_comment)
