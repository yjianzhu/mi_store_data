from utils import *


if __name__ == "__main__":
    # get mi_id and name in the mi store.
    driver = get_global_driver()
    for mi_id in range(19301,19999):
        goods_name, number_of_comment = get_comment(driver,f"https://www.mi.com/shop/comment/{mi_id}.html")
        # 如果goods_name为空
        if goods_name == "":
            print("no such item")
            continue
        insert_item(mi_id, goods_name, number_of_comment)