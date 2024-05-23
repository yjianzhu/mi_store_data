from utils import *
import schedule
import time

def single_run():
    driver = get_global_driver()
    try:
        update_all_comment(driver=driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

# 定时调用爬虫脚本
if __name__=='__main__':
    # 每隔一天，update_all_comment 一次
    schedule.every().day.at("12:00").do(single_run)

    while True:
        schedule.run_pending()
        time.sleep(10)