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

def query_all_comments():
    conn = sqlite3.connect('mi_items.db')
    c = conn.cursor()
    c.execute('''
    SELECT * FROM comments
    ''')
    comments = c.fetchall()
    conn.close()
    return comments

def query_comments_by_name(name):
    conn = sqlite3.connect('mi_items.db')
    c = conn.cursor()
    
    # 从comments表中查询数据，条件是name字段等于传入的name参数
    c.execute('''
    SELECT * FROM comments WHERE name = ?
    ''', (name,))
    comments = c.fetchall()
    conn.close()
    return comments

def insert_item(id_mi, name, number_of_comments=0):
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

def create_chart(dates, daily_data, cumulative_data):
    fig, ax1 = plt.subplots()

    # 柱状图：单日数据
    ax1.bar(dates, daily_data, color='b', label='Daily Data')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Daily Data', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    
    # 线图：累计数据
    ax2 = ax1.twinx()  # 创建第二个轴
    ax2.plot(dates, cumulative_data, color='r', label='Cumulative Data')
    ax2.set_ylabel('Cumulative Data', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # 添加图例
    fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
    plt.tight_layout()

    return fig

def plot_daily_data_by_name(name):
    all_data = query_comments_by_name(name)
    df = pandas.DataFrame(all_data, columns=['id', 'item_id', 'date', 'name', 'total_comments'])
    # 如果数据量太大，可以只取最近的 30 天
    if len(df) > 30:
        df = df[-30:]

    # 绘制双轴图，横轴为日期，左轴为单日数据，右轴为累计数据
    dates = df['date']
    daily_data = df['total_comments'].diff().fillna(0)
    cumulative_data = df['total_comments']

    fig, ax1 = plt.subplots()
    ax1.bar(dates, daily_data, color='r', label='Daily Data')
    ax1.set_xlabel('Date')
    # 日期旋转 45 度
    plt.xticks(rotation=45)
    ax1.set_ylabel('Daily Data', color='r')
    ax1.tick_params(axis='y', labelcolor='r')

    ax2 = ax1.twinx()
    ax2.plot(dates, cumulative_data, color='b', label='Cumulative Data')
    ax2.set_ylabel('Cumulative Data', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    fig.legend(loc='upper left', bbox_to_anchor=(0.2,0.9))
    plt.tight_layout()
    
    return fig

# 从我的数据库中读取数据，绘制图表
if __name__=='__main__':
    
    goods_shown = ["Xiaomi 14",'Redmi Note 13 5G','Redmi K70','Redmi Turbo 3']

    st.title('小米商城评论数')

    for item in goods_shown:
        st.subheader(item)
        fig = plot_daily_data_by_name(item)
        if fig:
            st.pyplot(fig)
        else:
            st.write(f'No data for {item}')

