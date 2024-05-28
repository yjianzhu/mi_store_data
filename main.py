from utils import *

# 从我的数据库中读取数据，绘制图表
if __name__=='__main__':

    # 定时
    
    goods_shown = ["Xiaomi 14","Xiaomi 13",'Redmi Note 13 5G',"Redmi Note 12 5G",'Redmi K70',"Redmi K60",'Redmi Turbo 3',"Redmi Note 12 Turbo","Xiaomi 14 Ultra","Xiaomi 13 Ultra"]

    st.title('小米商城评论数')
    fig = plot_items(goods_shown)
    st.pyplot(fig)

    goods_shown = ["Xiaomi 14",'Redmi Note 13 5G','Redmi K70','Redmi Turbo 3']
    for item in goods_shown:
        st.subheader(item)
        fig = plot_daily_data_by_name(item)
        if fig:
            st.pyplot(fig)
        else:
            st.write(f'No data for {item}')
