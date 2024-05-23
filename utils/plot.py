import matplotlib.pyplot as plt
from .database import *

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