import streamlit as st
import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
# import webbrowser

my_katalk_df = pd.read_csv("preprocessed_data/" +  "challenge_msg_2023-09-26.csv")

challenge_url_df = my_katalk_df[my_katalk_df['text'].str.contains('https://cafe.naver.com/roalnam/')]
challenge_url_count_df = challenge_url_df[['year_month_day','user_name','text', 'user_class']]
challenge_url_count_df = challenge_url_count_df.drop_duplicates()

day = challenge_url_df.year_month_day.unique()
day_sorted = sorted(day, reverse = True)

user = challenge_url_df.user_name.unique()
user_sorted = sorted(user)
user_sorted.insert(0, '전체보기')

st.header(":blue[로마드] :red[2주 챌린지] 현황")
#if st.button('로마드 카페 바로가기 !'):
#    webbrowser.open_new_tab("https://cafe.naver.com/roalnam")

st.text('챌린지 인증 채팅 분포')
challenge_groupby_df = challenge_url_count_df.groupby(['year_month_day'])['year_month_day'].size().reset_index(name='user_name_day_count')
# total_pivot_df = total_groupby_df.pivot(index='year_month_day',columns='user_name',values='user_name_day_count').reset_index()
challenge_chart_df = challenge_groupby_df.fillna(0)
challenge_chart_df_columns = challenge_chart_df.columns.to_list()
challenge_chart_df_columns.remove('year_month_day')
st.bar_chart(
    challenge_chart_df,
    x='year_month_day',
    y= challenge_chart_df_columns
)

st.subheader("🙋🏻:orange[회원 별] 챌린지 참여 인증 확인")
st.caption("ℹ️ 챌린지 인증 횟수는 채팅 url 올린 것 기준으로 카운트하였습니다.")

challenge_groupby_user_name = challenge_url_count_df.groupby(['user_name'])['user_name'].size().reset_index(name='user_name_count')
challenge_result_df = challenge_groupby_user_name.fillna(0)
count = challenge_result_df.user_name_count.unique()
count_sorted = sorted(count, reverse = True)

target_count = st.selectbox(
    '참여 횟수 별 회원 리스트 조회하기',
    (count_sorted))
target_count_df = challenge_result_df[challenge_result_df.user_name_count == target_count]
n = len(target_count_df.user_name)
st.info(f'총 {target_count}회 인증한 회원은 {n}명 입니다 !', icon="📢")
st.dataframe(target_count_df)

target_user_name = st.selectbox(
    '누구의 현황을 볼래?',
    (user_sorted))

if target_user_name == "전체보기":
    st.dataframe(challenge_url_count_df[['year_month_day','user_name','text', 'user_class']])
else:
    target_df = challenge_url_count_df[challenge_url_count_df.user_name == target_user_name]
    st.dataframe(target_df[['year_month_day','user_name','text', 'user_class']])

st.subheader("📆:orange[날짜 별] 채팅 현황")
start_date = st.selectbox(
    '어떤 날짜의 현황을 볼래?',
    (day_sorted))

start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
new_date_obj = start_date_obj + timedelta(days=1)
end_date = new_date_obj.strftime('%Y-%m-%d')

# 날짜 범위를 적용하여 데이터 프레임 필터링
def filer_df_by_date(df, start_date, end_date):
    return df[(df['date_time'] >= start_date) & (df['date_time'] <= end_date)]

my_katalk_df_today = filer_df_by_date(my_katalk_df, start_date, end_date)
challenge_url_df_today = filer_df_by_date(challenge_url_df, start_date, end_date)
weekday_today = challenge_url_df_today.weekday.unique()


st.text(f'{start_date} {weekday_today[0]}의 채팅 분포')
groupby_df = my_katalk_df_today.groupby(['hour', 'user_class'])['hour'].size().reset_index(name='user_class_hour_count')
pivot_df = groupby_df.pivot(index='hour',columns='user_class',values='user_class_hour_count').reset_index()
chart_df = pivot_df.fillna(0)
chart_df_columns = chart_df.columns.to_list()
chart_df_columns.remove('hour')
st.area_chart(
    chart_df,
    x='hour',
    y= chart_df_columns
)

st.text('오늘의 챌린지 인증 내용')
st.dataframe(challenge_url_df_today[['year_month_day','user_name','text', 'user_class']])

st.text('오늘의 오픈 카톡 참여자')
heavy_talker = my_katalk_df_today.user_name.value_counts().to_frame()
st.dataframe(heavy_talker)

st.text('전체 채팅 분포')
total_groupby_df = my_katalk_df.groupby(['year_month_day', 'user_name'])['year_month_day'].size().reset_index(name='user_name_day_count')
total_pivot_df = total_groupby_df.pivot(index='year_month_day',columns='user_name',values='user_name_day_count').reset_index()
total_chart_df = total_pivot_df.fillna(0)
total_chart_df_columns = total_chart_df.columns.to_list()
total_chart_df_columns.remove('year_month_day')
st.area_chart(
    total_chart_df,
    x='year_month_day',
    y= total_chart_df_columns
)
