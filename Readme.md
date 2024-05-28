# Xiaomi Store Data

### Requirements

python, numpy, matplotlib, pandas, streamlit, sqlite3

### How to run

创建浏览器页面
`streamlit run main.py`

爬虫脚本
`python spider.py`

### Database

```
c.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_from_mi_store INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,
    number_of_comments INTEGER NOT NULL DEFAULT 0
)
''')

# 创建另一个表，comments
c.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    comment_count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (item_id) REFERENCES items (id)
)
''')

# 创建另一个表，已经下架的商品 off_shelf_items
c.execute('''
CREATE TABLE IF NOT EXISTS off_shelf_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_from_mi_store INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,
    number_of_comments INTEGER NOT NULL DEFAULT 0
)
''')
```


### 数据细节
小米商城对于很多商品采用叠加形式，例如小米14的总评论数是包含了小米14 Pro的评论数的，偶尔包括14ultra。

小米14ultra的具体数据可以用'Xiaomi 14 Ultra 12GB+256GB专业影像套装' 减去'Xiaomi 14 Ultra 专业影像套装'

