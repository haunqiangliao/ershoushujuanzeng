import streamlit as st
import pandas as pd
from datetime import datetime

# 页面设置
st.set_page_config(
    page_title="校园二手书捐赠平台",
    page_icon="📚",
    layout="centered"
)

# 初始化数据
if 'books' not in st.session_state:
    st.session_state.books = pd.DataFrame(columns=[
        "书名", "学科", "版本", "使用年限", 
        "捐赠人", "联系方式", "捐赠时间", "状态"
    ])
    # 添加一些示例数据
    st.session_state.books.loc[0] = [
        "Python编程：从入门到实践", "计算机", "第2版", "1年", 
        "张学长", "wx:zhang123", datetime.now().strftime("%Y-%m-%d"), "可领取"
    ]

# 主界面
st.title("📚 校园二手书捐赠平台")
st.write("让知识流动，让爱心传递")

# 功能导航
tab1, tab2 = st.tabs(["我要捐书", "我要找书"])

with tab1:
    # 捐赠书籍表单
    st.subheader("捐赠书籍信息")
    
    with st.form("donate_form"):
        col1, col2 = st.columns(2)
        with col1:
            book_name = st.text_input("书名*", max_chars=50)
            subject = st.text_input("学科*", max_chars=20, 
                                  placeholder="如：计算机/数学/英语")
        with col2:
            edition = st.text_input("版本", max_chars=20, 
                                  placeholder="如：第2版/2020年版")
            used_years = st.text_input("使用年限", max_chars=10, 
                                      placeholder="如：1年/2学期")
        
        col3, col4 = st.columns(2)
        with col3:
            donor = st.text_input("捐赠人*", max_chars=20)
        with col4:
            contact = st.text_input("联系方式*", max_chars=50,
                                  placeholder="微信/电话/邮箱")
        
        if st.form_submit_button("提交捐赠"):
            if book_name and subject and donor and contact:
                new_book = {
                    "书名": book_name,
                    "学科": subject,
                    "版本": edition,
                    "使用年限": used_years,
                    "捐赠人": donor,
                    "联系方式": contact,
                    "捐赠时间": datetime.now().strftime("%Y-%m-%d"),
                    "状态": "可领取"
                }
                st.session_state.books = pd.concat([
                    st.session_state.books, 
                    pd.DataFrame([new_book])
                ], ignore_index=True)
                st.success("捐赠成功！感谢您的爱心！")
            else:
                st.error("请填写带*的必填项")

with tab2:
    # 查找书籍
    st.subheader("查找所需书籍")
    
    # 搜索筛选
    search_col1, search_col2 = st.columns(2)
    with search_col1:
        search_name = st.text_input("按书名搜索")
    with search_col2:
        search_subject = st.text_input("按学科搜索")
    
    # 显示书籍列表
    filtered_books = st.session_state.books
    if search_name:
        filtered_books = filtered_books[filtered_books["书名"].str.contains(search_name, na=False)]
    if search_subject:
        filtered_books = filtered_books[filtered_books["学科"].str.contains(search_subject, na=False)]
    
    if not filtered_books.empty:
        st.write("找到以下书籍：")
        for idx, row in filtered_books.iterrows():
            with st.expander(f"{row['书名']} ({row['学科']}, {row.get('版本', '')}"):
                st.write(f"**使用情况**: {row.get('使用年限', '未知')}")
                st.write(f"**捐赠人**: {row['捐赠人']}")
                st.write(f"**联系方式**: {row['联系方式']}")
                st.write(f"**捐赠时间**: {row['捐赠时间']}")
                st.write(f"**状态**: {row['状态']}")
                
                if st.button("我已领取", key=f"received_{idx}"):
                    st.session_state.books.at[idx, "状态"] = "已领取"
                    st.rerun()
    else:
        st.info("暂无符合条件的书籍")

# 页脚
st.divider()
st.write("""
**平台公约**:
1. 请如实填写书籍信息
2. 领取后请及时标记状态
3. 禁止商业倒卖行为
""")
