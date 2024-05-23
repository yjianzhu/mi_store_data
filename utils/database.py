import sqlite3
import sys
import os
import pandas
import matplotlib.pyplot as plt
import streamlit as st

def get_table_columns(data_base:str='mi_items.db'):
    # 读取数据库中的每个表，大小，列名
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    # 打印所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(table)
        # 打印表的列名
        cursor.execute("PRAGMA table_info(%s)" % table)
        columns = cursor.fetchall()
        for column in columns:
            print(column)
        print()
    conn.close()


def query_all_items(data_base:str='mi_items.db'):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()  # 获取所有结果
    conn.close()
    return items

def query_all_off_shelf_items(data_base:str='mi_items.db'):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM off_shelf_items')
    off_shelf_items = cursor.fetchall()
    conn.close()
    return off_shelf_items

def query_all_comments(data_base:str ="mi_items.db"):
    conn = sqlite3.connect(data_base)
    c = conn.cursor()
    c.execute('''
    SELECT * FROM comments
    ''')
    comments = c.fetchall()
    conn.close()
    return comments

def query_comments_by_name(name,data_base:str ="mi_items.db"):
    conn = sqlite3.connect(data_base)
    c = conn.cursor()
    
    # 从comments表中查询数据，条件是name字段等于传入的name参数
    c.execute('''
    SELECT * FROM comments WHERE name = ?
    ''', (name,))
    comments = c.fetchall()
    conn.close()
    return comments

def insert_item(id_mi, name, number_of_comments=0):
    """ insert item to item table, usage: insert_item(id_mi, name, number_of_comment=0)"""
    conn = sqlite3.connect('mi_items.db')
    c = conn.cursor()
    try:
        c.execute('''
        INSERT INTO items (id_from_mi_store, name, number_of_comments)
        VALUES (?, ?, ?)
        ''', (id_mi, name, number_of_comments))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("id_mi already exists, update it")
        c.execute('''
        UPDATE items
        SET name = ?, number_of_comments = ?
        WHERE id_from_mi_store = ?
        ''', (name, number_of_comments, id_mi))
        conn.commit()
    conn.close()

def insert_comments(id_mi,date,name,comment_count):
    conn = sqlite3.connect('mi_items.db')
    c = conn.cursor()
    # get item_id from items table
    c.execute('''
    SELECT id FROM items WHERE id_from_mi_store = ?
    ''', (id_mi,))
    item_id = c.fetchall()
    if len(item_id) == 0:
        print("no such item")
        return

    item_id = item_id[0][0]
    # insert into comments table
    c.execute('''
    INSERT INTO comments (item_id, date, name, comment_count)
    VALUES (?, ?, ?, ?)
    ''', (item_id, date, name, comment_count))
    conn.commit()
   
    # update number_of_comments in items table to comments count
    c.execute('''
    UPDATE items
    SET number_of_comments = ?
    WHERE id = ?
    ''', (comment_count, item_id))
    conn.commit()
    conn.close()


def delete_item(c, id_mi):
    # 使用传入的 cursor 执行删除操作
    c.execute('''
    DELETE FROM items WHERE id_from_mi_store = ?
    ''', (id_mi,))

def insert_off_shelf_item(id_mi, name):
    # 使用 with 语句确保数据库连接正确关闭
    with sqlite3.connect('mi_items.db') as conn:
        c = conn.cursor()

        # 获取 items 表中的 number_of_comments
        c.execute('''
        SELECT number_of_comments FROM items WHERE id_from_mi_store = ?
        ''', (id_mi,))
        number_of_comments = c.fetchall()

        if len(number_of_comments) == 0:
            print("no such item")
            return

        number_of_comments = number_of_comments[0][0]

        # 插入数据到 off_shelf_items 表
        c.execute('''
        INSERT INTO off_shelf_items (id_from_mi_store, name, number_of_comments)
        VALUES (?, ?, ?)
        ''', (id_mi, name, number_of_comments))
        
        # 调用 delete_item 函数，并传入 cursor 和 id_mi
        delete_item(c, id_mi)

        # 提交事务
        conn.commit()

def clear_datebase():
    conn = sqlite3.connect('mi_items.db')
    c = conn.cursor()
    c.execute('''
    DELETE FROM items
    ''')
    c.execute('''
    DELETE FROM comments
    ''')
    c.execute('''
    DELETE FROM off_shelf_items
    ''')
    conn.commit()
    conn.close()

def clear_comments():
    conn = sqlite3.connect('mi_items.db')
    c = conn.cursor()
    c.execute('''
    DELETE FROM comments
    ''')
    conn.commit()
    conn.close()

def search_mi_id_by_name(name):
    conn = sqlite3.connect('mi_items.db')
    c = conn.cursor()
    c.execute('''
    SELECT id_from_mi_store FROM items WHERE name = ?
    ''', (name,))
    id_mi = c.fetchall()
    conn.close()
    return id_mi[0][0] if len(id_mi) > 0 else None