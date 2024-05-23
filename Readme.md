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