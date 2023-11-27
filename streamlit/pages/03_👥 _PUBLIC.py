#라이브러리 import
#필요한 경우 install
import streamlit as st
from streamlit import components
from keybert import KeyBERT
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import seaborn as sns
import numpy as np
from numpy.linalg import norm
from numpy import nan
from numpy import dot
import ast
from PIL import Image
import pandas as pd
import time
import random
from konlpy.tag import Twitter
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import re
import math
from sklearn.preprocessing import normalize
from konlpy.tag import Komoran

#plotly 시각화 오류시 실행시킬 코드
#import plotly.offline as pyo
#import plotly.graph_objs as go
# 오프라인 모드로 변경하기
#pyo.init_notebook_mode()

#public 페이지를 위한 코드
st.set_page_config(page_title="PUBLIC", page_icon="👥",layout = 'wide')

image = Image.open('images/logo.png')
image2 = Image.open('images/logo2.png')
image3 = Image.open('images/logo3.png')

st.sidebar.image(image2, use_column_width=True)
st.sidebar.image(image3, use_column_width=True)

#최상단에 이미지 넣기
st.image(image2, width=300) 

df = pd.read_csv("data/상담다발품목.csv")

recall = pd.read_excel('data/국내 리콜.xlsx')

st.markdown('''
<h2>Daily Report For <span style="color: #6FA8DC;"> EVERYONE 👥</span></h2>
''', unsafe_allow_html=True)
st.text('')
########################################################################################################################################
#st.columns 함수로 화면 레이아웃을 열로 분리
col1, col2= st.columns([5,5])

with col1:
    # 데이터프레임에서 조건에 맞는 행을 추출
    filtered_df = df[(df['AGE'] >= 20) & (df['AGE'] < 30)]
    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

    # COUNT 열을 기준으로 내림차순 정렬
    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

    # 각 성별에 대해 상위 5개 항목 선택
    top5_male = sorted_df[sorted_df['SEX'] == '남성'].head(5)
    top5_female = sorted_df[sorted_df['SEX'] == '여성'].head(5)

    # Plotly Express를 사용하여 그래프 생성
    fig1 = px.bar(
        top5_male,
        x='TOP_CLS',
        y='COUNT',
        category_orders={"TOP_CLS": top5_male['TOP_CLS'].tolist()}
    )

    # 레이아웃 설정
    fig1.update_layout(
        title='20대 남성 상담다발품목',
        xaxis_title='품목',
        yaxis_title='상담횟수',
        font=dict(size=20),
        width=800,
        height=500
    )

    # 그래프 표시
    st.plotly_chart(fig1)


with col2:
    # 데이터프레임에서 조건에 맞는 행을 추출
    filtered_df = df[(df['AGE'] >= 20) & (df['AGE'] < 30)]
    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

    # COUNT 열을 기준으로 내림차순 정렬
    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

    # 각 성별에 대해 상위 5개 항목 선택
    top5_female = sorted_df[sorted_df['SEX'] == '여성'].head(5)

    # Plotly Express를 사용하여 그래프 생성
    fig2 = px.bar(
        top5_female,
        x='TOP_CLS',
        y='COUNT',
        color_discrete_sequence=['red'],
        category_orders={"TOP_CLS": top5_female['TOP_CLS'].tolist()}
    )

    # 레이아웃 설정
    fig2.update_layout(
        title='20대 여성 상담다발품목',
        xaxis_title='품목',
        yaxis_title='상담횟수',
        font=dict(size=30),
        width=800,
        height=500
    )

    # 그래프 표시
    st.plotly_chart(fig2)

########################################################################################################################################
st.write('')
st.subheader('👇 카테고리별 국내 리콜 제품을 확인하세요')

#8개의 탭에 대해서 동일한 코드 적용
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(['**여행** ✈', 
                                                            '**취미**  🏟',
                                                            '**IT_전자** 💻',
                                                            '**생활**  🏪',
                                                            '**패션_뷰티**  👕',
                                                            '**교육**  📖',
                                                            '**의료**  🩺',
                                                            '**외식**  🍣'])

with tab1:
    st.subheader('**리콜 제품이 없습니다.**')
with tab2:
    st.subheader('**리콜 제품이 없습니다.**')
with tab3:
    r3 = recall[recall.Label == '자동차'].drop(columns = 'Label').reset_index(drop=True)
    st.dataframe(r3)
with tab4:
    r4 = recall[recall.Label == '생활'].drop(columns = 'Label').reset_index(drop=True)
    st.dataframe(r4)
with tab5:
    r5 = recall[recall.Label == '패션_뷰티'].drop(columns = 'Label').reset_index(drop=True)
    st.dataframe(r5)
with tab6:
    st.subheader('**리콜 제품이 없습니다.**')
with tab7:
    r6 = recall[recall.Label == '의료'].drop(columns = 'Label').reset_index(drop=True)
    st.dataframe(r6)
with tab8:
    r7 = recall[recall.Label == '외식'].drop(columns = 'Label').reset_index(drop=True)
    st.dataframe(r7)