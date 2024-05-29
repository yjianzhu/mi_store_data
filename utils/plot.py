import matplotlib.pyplot as plt
from .database import *

def create_chart(dates, daily_data, cumulative_data):
    fig, ax1 = plt.subplots()

    # 柱状图：单日数据
    ax1.bar(dates, daily_data, color='b', label='Daily Data')
    # 在每个柱条上显示数值
    for bar in bars:
        height = int(bar.get_height())
        ax1.text(
            bar.get_x() + bar.get_width() / 2,  # x 坐标
            height,  # y 坐标
            f'{height}', # 显示的文本是整数
            ha='center',  # 水平对齐方式
            va='bottom'  # 垂直对齐方式
        )
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
    if len(df) > 10:
        df = df[-10:]

    # 绘制双轴图，横轴为日期，左轴为单日数据，右轴为累计数据
    dates = df['date']
    daily_data = df['total_comments'].diff().fillna(0)
    daily_data = daily_data.astype(int)
    cumulative_data = df['total_comments']

    fig, ax1 = plt.subplots()
    bars = ax1.bar(dates, daily_data, color='r', label='Daily Data')
    # 在每个柱条上显示数值
    for bar in bars:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,  # x 坐标
            height,  # y 坐标
            f'{height}',  # 显示的文本
            ha='center',  # 水平对齐方式
            va='bottom'  # 垂直对齐方式
        )

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

def plot_items(names):
    """绘制多个商品的评论数图表，柱状图，横坐标为名称，纵坐标为评论数，title是最新日期"""
    counts = []

    for name in names:
        if name == "Xiaomi 14 Ultra":
            counts.append(get_mi_14_ultra())
            continue
        all_data = query_comments_by_name(name)
        df = pandas.DataFrame(all_data, columns=['id', 'item_id', 'date', 'name', 'total_comments'])
        # 向 counts 中添加最新的评论数
        if len(df) == 0:
            counts.append(0)
        else:
            counts.append(df['total_comments'].iloc[-1])
    
    # 绘制柱状图
    fig, ax = plt.subplots()
    bars = ax.bar(names, counts)
    ax.set_xlabel('Name')
    ax.set_ylabel('Total Comments')

    # 在每个柱条上显示数值
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # x 坐标
            height,  # y 坐标
            f'{height}',  # 显示的文本
            ha='center',  # 水平对齐方式
            va='bottom'  # 垂直对齐方式
        )
    try:
        ax.set_title(df['date'].iloc[-1])
    except:
        pass
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def get_mi_14_ultra():

    mi14_ultra_and_photography = query_comments_by_name("Xiaomi 14 Ultra 12GB+256GB专业影像套装")
    df = pandas.DataFrame(mi14_ultra_and_photography, columns=['id', 'item_id', 'date', 'name', 'total_comments'])
    mi14_ultra_and_photography = df['total_comments'].iloc[-1]

    mi_photography = query_comments_by_name("Xiaomi 14 Ultra 专业影像套装")
    df = pandas.DataFrame(mi_photography, columns=['id', 'item_id', 'date', 'name', 'total_comments'])
    mi_photography = df['total_comments'].iloc[-1]

    mi14_ultra = mi14_ultra_and_photography - mi_photography
    return mi14_ultra