import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import random
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.io as pio
from collections import Counter
from wordcloud import WordCloud
from io import BytesIO
import base64
from plotly.subplots import make_subplots
from keybert import KeyBERT
import numpy as np
from numpy.linalg import norm
from numpy import dot


# plotly 시각화 오류시 실행시킬 코드
#import plotly.offline as pyo
#import plotly.graph_objs as go
# 오프라인 모드로 변경하기
#pyo.init_notebook_mode()

#private 페이지를 위한 코드
st.set_page_config(page_title="PRIVATE", page_icon="👤",layout = 'wide')

# 직접 HTML 및 CSS를 사용하여 화면 비율 조정
st.markdown(
    """
    <style>
        body {
            width: 100%;
            margin: 0;
        }
        .stApp {
            max-width: 1500px;  # 조정하려는 최대 너비
            margin: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.spinner("# ⏳ 잠시만 기다려주세요."):

    image = Image.open('images/logo2.png')
    st.sidebar.image(image, use_column_width=True)

    #리스트를 문자열로 인식하는 문제 해결하는 함수
    def parse_list(input_str):

        return eval(input_str)

    @st.cache_data
    def load_data():

        # 보도자료
        # fv : 모델링 결과
        # wc : 배포시 konlpy java 환경변수 오류 때문에 명사 추출 결과를 컬럼에 미리 담아놓음
        df1 = pd.read_csv("data/보도자료.csv", converters={'fv' : parse_list, 'wc' : parse_list,  'subsubtitle' : parse_list})

        # 고객
        df2 = pd.read_csv("data/고객.csv", converters={'feature' : parse_list})

        df3 = pd.read_csv("data/상담다발품목.csv")

        return df1, df2, df3

    df1, df2, df3 = load_data()


    #코사인유사도를 위한 함수 정의
    def cos_sim(A, B):
        return dot(A, B)/(norm(A)*norm(B))

    #하이퍼링크 만드는 함수
    def create_link_card(title, url):
        container = st.container()
        container.markdown(
        f'<div class="link-card"><a href="{url}" target="_blank">{title}</a></div>',
        unsafe_allow_html=True,
        )
        return container


    #value 파라미터로 디폴트 값 지정 가능
    #페이지가 열리면 value 값이 자동으로 input_user_name에 할당됨
    st.write(" ##### 고객 ID를 입력해주세요. 고객 ID의 앞자리는 연령대(1~8), 뒷자리는 성별(0,1)을 의미합니다.")

    input_user_name = st.text_input(label="**고객 ID 예시) 20 : 20대 남자 , 41 : 40대 여자**", value = "") 

    if st.button("📰 추천 받기"):
        try:
            if input_user_name != '':
                
                # 고객-보도자료 간의 코사인 유사도 계산
                cosine_similarities = [cos_sim(df2[df2.고객ID == int(input_user_name)]['feature'].iloc[0], fv) for fv in df1.fv]
                
                # 가장 유사한 보도자료 상위 3개 값의 인덱스 찾기
                top_indices = sorted(range(len(df1)), key=lambda i: cosine_similarities[i], reverse=True)[:3]

                # 요약문
                # 변수에 할당할 개수를 리스트의 길이에 맞게 조절 2개 이상이면 2개로. 1개는 오류남.
                s11, s21, *_= df1.subsubtitle[top_indices[0]]
                s12, s22, *_= df1.subsubtitle[top_indices[1]]
                s13, s23, *_= df1.subsubtitle[top_indices[2]]

                # KeyBERT
                # 키워드 3개
                n=3 
                kw_model = KeyBERT()
                keywords_mmr1 = kw_model.extract_keywords(df1.content[top_indices[0]],
                                                        keyphrase_ngram_range=(1,1),
                                                                use_mmr = False,
                                                                top_n = n,
                                                                diversity = 0.2,
                                                                stop_words = [''])

                keywords_mmr2 = kw_model.extract_keywords(df1.content[top_indices[1]],
                                                        keyphrase_ngram_range=(1,1),
                                                                use_mmr = False,
                                                                top_n = n,
                                                                diversity = 0.2,
                                                                stop_words = [''])

                keywords_mmr3 = kw_model.extract_keywords(df1.content[top_indices[2]],
                                                        keyphrase_ngram_range=(1,1),
                                                                use_mmr = False,
                                                                top_n = n,
                                                                diversity = 0.2,
                                                                stop_words = [''])

                # 워드클라우드 생성 함수
                def generate_wordcloud(c):
                    wordcloud = WordCloud(
                                width=750,
                                height=450,
                                font_path = 'malgun.ttf',
                                background_color='white'#, 
                                #colormap='Blues' 
                                        ).generate_from_frequencies(c)

                    # 이미지를 바이트 형식으로 변환하여 Base64로 인코딩
                    img_buffer = BytesIO()
                    wordcloud.to_image().save(img_buffer, format='PNG')
                    img_str = "data:image/png;base64," + base64.b64encode(img_buffer.getvalue()).decode()

                    return img_str

                # 단어별 빈도수 형태의 딕셔너리 데이터를 구성
                # 워드클라우드 생성
                wordcloud_html1 = generate_wordcloud(Counter(df1.wc[top_indices[0]]))
                wordcloud_html2 = generate_wordcloud(Counter(df1.wc[top_indices[1]]))
                wordcloud_html3 = generate_wordcloud(Counter(df1.wc[top_indices[2]]))


                # 서브플롯 생성
                fig1 = make_subplots(rows=1, cols=2, subplot_titles=['지출 분석', '보도자료 분석'], specs=[[{'type': 'pie'}, {'type': 'pie'}]])

                value_a1 = df2[df2.고객ID == int(input_user_name)]['feature'].iloc[0]
                data11 = {'category' : ['여행', '취미', 'IT_전자', '생활', '패션_뷰티', '교육', '의료', '외식'],
                        'value' : value_a1 }
                figdf11 = pd.DataFrame(data11)

                fig11 = px.pie(figdf11
                                , names='category'
                                , values='value'
                                , width=600
                                , height=400
                                , color_discrete_map={'여행': 'lightblue', '취미': 'lightgreen', 'IT_전자': 'lightcoral', '생활': 'lightskyblue', '패션_뷰티': 'lightpink', '교육': 'lightyellow', '의료': 'lightcyan', '외식': 'lightgrey'})
                
                fig11.update_layout(
                    title = '지출 분석',
                    legend_yanchor="top",
                    legend_y=1,
                    legend_xanchor="left",
                    legend_x=-0.1,
                    template='plotly_white'
                )

                value_b1 = df1.fv[top_indices[0]]
                data21 = {'category' : ['여행', '취미', 'IT_전자', '생활', '패션_뷰티', '교육', '의료', '외식'],
                        'value' : value_b1 }
                figdf21 = pd.DataFrame(data21)

                fig21 = px.pie(figdf21
                                , names='category'
                                , values='value'
                                , width=600
                                , height=400
                                , color_discrete_map={'여행': 'lightblue', '취미': 'lightgreen', 'IT_전자': 'lightcoral', '생활': 'lightskyblue', '패션_뷰티': 'lightpink', '교육': 'lightyellow', '의료': 'lightcyan', '외식': 'lightgrey'})
                
                fig21.update_layout(
                    title = '보도자료 분석',
                    legend_yanchor="top",
                    legend_y=1,
                    legend_xanchor="left",
                    legend_x=-0.1,
                    template='plotly_white'
                )

                # 서브플롯에 추가
                fig1.add_trace(fig11['data'][0], row=1, col=1)
                fig1.add_trace(fig21['data'][0], row=1, col=2)

                fig1.update_layout(
                    template='plotly_white'
                )

                # Plotly 그래픽을 HTML로 변환
                html_plot1 = pio.to_html(fig1, full_html=False)

                sim1 = round(cos_sim(value_a1, value_b1) * 100, 1)


                # 서브플롯 생성
                fig2 = make_subplots(rows=1, cols=2, subplot_titles=['지출 분석', '보도자료 분석'], specs=[[{'type': 'pie'}, {'type': 'pie'}]])

                value_a2 = df2[df2.고객ID == int(input_user_name)]['feature'].iloc[0]
                data12 = {'category' : ['여행', '취미', 'IT_전자', '생활', '패션_뷰티', '교육', '의료', '외식'],
                        'value' : value_a2 }
                figdf12 = pd.DataFrame(data12)

                fig12 = px.pie(figdf12
                                , names='category'
                                , values='value'
                                , width=600
                                , height=400
                                , color_discrete_map={'여행': 'lightblue', '취미': 'lightgreen', 'IT_전자': 'lightcoral', '생활': 'lightskyblue', '패션_뷰티': 'lightpink', '교육': 'lightyellow', '의료': 'lightcyan', '외식': 'lightgrey'})
                
                fig12.update_layout(
                    title = '지출 분석',
                    legend_yanchor="top",
                    legend_y=1,
                    legend_xanchor="left",
                    legend_x=-0.1,
                    template='plotly_white'
                )

                value_b2 = df1.fv[top_indices[1]]
                data22 = {'category' : ['여행', '취미', 'IT_전자', '생활', '패션_뷰티', '교육', '의료', '외식'],
                        'value' : value_b2 }
                figdf22 = pd.DataFrame(data22)

                fig22 = px.pie(figdf22
                                , names='category'
                                , values='value'
                                , width=600
                                , height=400
                                , color_discrete_map={'여행': 'lightblue', '취미': 'lightgreen', 'IT_전자': 'lightcoral', '생활': 'lightskyblue', '패션_뷰티': 'lightpink', '교육': 'lightyellow', '의료': 'lightcyan', '외식': 'lightgrey'})
                
                fig22.update_layout(
                    title = '보도자료 분석',
                    legend_yanchor="top",
                    legend_y=1,
                    legend_xanchor="left",
                    legend_x=-0.1,
                    template='plotly_white'
                )

                # 서브플롯에 추가
                fig2.add_trace(fig12['data'][0], row=1, col=1)
                fig2.add_trace(fig22['data'][0], row=1, col=2)

                fig2.update_layout(
                    template='plotly_white'
                )

                # Plotly 그래픽을 HTML로 변환
                html_plot2 = pio.to_html(fig2, full_html=False)

                sim2 = round(cos_sim(value_a2, value_b2) * 100, 1)

                                
                                
                # 서브플롯 생성
                fig3 = make_subplots(rows=1, cols=2, subplot_titles=['지출 분석', '보도자료 분석'], specs=[[{'type': 'pie'}, {'type': 'pie'}]])

                value_a3 = df2[df2.고객ID == int(input_user_name)]['feature'].iloc[0]
                data13 = {'category' : ['여행', '취미', 'IT_전자', '생활', '패션_뷰티', '교육', '의료', '외식'],
                        'value' : value_a3 }
                figdf13 = pd.DataFrame(data13)

                fig13 = px.pie(figdf13
                                , names='category'
                                , values='value'
                                , width=600
                                , height=400
                                , color_discrete_map={'여행': 'lightblue', '취미': 'lightgreen', 'IT_전자': 'lightcoral', '생활': 'lightskyblue', '패션_뷰티': 'lightpink', '교육': 'lightyellow', '의료': 'lightcyan', '외식': 'lightgrey'})
                
                fig13.update_layout(
                    title = '지출 분석',
                    legend_yanchor="top",
                    legend_y=1,
                    legend_xanchor="left",
                    legend_x=-0.1,
                    template='plotly_white'
                )

                value_b3 = df1.fv[top_indices[2]]
                data23 = {'category' : ['여행', '취미', 'IT_전자', '생활', '패션_뷰티', '교육', '의료', '외식'],
                        'value' : value_b3 }
                figdf23 = pd.DataFrame(data23)

                fig23 = px.pie(figdf23
                                , names='category'
                                , values='value'
                                , width=600
                                , height=400
                                , color_discrete_map={'여행': 'lightblue', '취미': 'lightgreen', 'IT_전자': 'lightcoral', '생활': 'lightskyblue', '패션_뷰티': 'lightpink', '교육': 'lightyellow', '의료': 'lightcyan', '외식': 'lightgrey'})
                
                fig23.update_layout(
                    title = '보도자료 분석',
                    legend_yanchor="top",
                    legend_y=1,
                    legend_xanchor="left",
                    legend_x=-0.1,
                    template='plotly_white'
                )

                # 서브플롯에 추가
                fig3.add_trace(fig13['data'][0], row=1, col=1)
                fig3.add_trace(fig23['data'][0], row=1, col=2)

                fig3.update_layout(
                    template='plotly_white'
                )

                # Plotly 그래픽을 HTML로 변환
                html_plot3 = pio.to_html(fig3, full_html=False)

                sim3 = round(cos_sim(value_a3, value_b3) * 100, 1)


                if input_user_name == '10':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 10) & (df3['AGE'] < 20)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5 = sorted_df[sorted_df['SEX'] == '남성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['blue'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='10대 남성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)

                elif input_user_name == '11':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 10) & (df3['AGE'] < 20)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '여성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['red'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='10대 여성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)

                elif input_user_name == '20':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 20) & (df3['AGE'] < 30)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '남성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['blue'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='20대 남성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)


                elif input_user_name == '21':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 20) & (df3['AGE'] < 30)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '여성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['red'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='20대 여성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)


                elif input_user_name == '30':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 30) & (df3['AGE'] < 40)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '남성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['blue'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='30대 남성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        emplate='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)

                elif input_user_name == '31':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 30) & (df3['AGE'] < 40)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '여성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['red'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='30대 여성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)

                elif input_user_name == '40':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 40) & (df3['AGE'] < 50)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '남성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['blue'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='40대 남성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)


                elif input_user_name == '41':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 40) & (df3['AGE'] < 50)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '여성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['red'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='40대 여성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)


                elif input_user_name == '50':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 50) & (df3['AGE'] < 60)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '남성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['blue'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='50대 남성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)


                elif input_user_name == '51':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 50) & (df3['AGE'] < 60)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '여성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['red'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='50대 여성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)


                elif input_user_name == '60':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 60) & (df3['AGE'] < 70)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '남성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['blue'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='60대 남성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)

                elif input_user_name == '61':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 60) & (df3['AGE'] < 70)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '여성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['red'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='60대 여성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)

                elif input_user_name == '70':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 70) & (df3['AGE'] < 80)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '남성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['blue'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='70대 남성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)

                elif input_user_name == '71':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 70) & (df3['AGE'] < 80)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '여성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['red'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='70대 여성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)


                elif input_user_name == '80':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 80) & (df3['AGE'] < 90)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '남성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['blue'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='80대 남성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender = pio.to_html(g, full_html=False)

                elif input_user_name == '81':

                    # 데이터프레임에서 조건에 맞는 행을 추출
                    filtered_df = df3[(df3['AGE'] >= 80) & (df3['AGE'] < 90)]
                    grouped_df = filtered_df.groupby(['SEX', 'TOP_CLS']).size().reset_index(name='COUNT')

                    # COUNT 열을 기준으로 내림차순 정렬
                    sorted_df = grouped_df.sort_values(by='COUNT', ascending=False)

                    # 각 성별에 대해 상위 5개 항목 선택
                    top5= sorted_df[sorted_df['SEX'] == '여성'].head(5)

                    # Plotly Express를 사용하여 그래프 생성
                    g = px.bar(
                        top5,
                        x='TOP_CLS',
                        y='COUNT',
                        color_discrete_sequence=['red'],
                        category_orders={"TOP_CLS": top5['TOP_CLS'].tolist()}
                    )

                    # 레이아웃 설정
                    g.update_layout(
                        title='80대 여성 상담다발품목',
                        xaxis_title='품목',
                        yaxis_title='상담횟수',
                        font=dict(size=20),
                        width=800,
                        height=550,
                        template='plotly_white',
                        title_x=0.5
                    )

                    gender1 = pio.to_html(g, full_html=False)
                    gender2 = pio.to_html(g, full_html=False)
                    gender3 = pio.to_html(g, full_html=False)

                else:
                    st.write('')

                st.info(f'**안녕하세요🙂 소비 패턴 분석을 통해 3개의 보도자료가 추천되었습니다.**')

                components.html(
                f"""
                <!doctype html>
                <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>Bootstrap demo</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
                </head>
                <body>
                    <div class="accordion accordion-flush" id="accordionFlushExample">
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
                                <strong>1st</strong>
                            </button>
                            </h2>
                            <div id="flush-collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div class="accordion-body">
                            <font size=5>
                            <font size=6><strong>📰 제목</strong></font><br>&nbsp"{df1.title[top_indices].iloc[0]}"<br><br>
                            <font size=6><strong>📝 요약</strong></font><br>&nbsp{s11}<br>&nbsp{s21}<br><br>
                            <font size=6><strong>🔑 키워드</strong></font><br><strong>&nbsp#</strong>{keywords_mmr1[0][0]}<strong>&nbsp#</strong>{keywords_mmr1[1][0]}<strong>&nbsp#</strong>{keywords_mmr1[2][0]}<br><br>
                            <font size=6><strong>👀 시각화</strong></font><br><br>&nbsp<img src="{wordcloud_html1}" alt="wordcloud"><br><br><br>
                            <font size=6><strong>✍ 분석결과 ➡ {sim1}%</strong></font>{html_plot1}
                            <font size=6><strong>🧺 상담다발품목</strong></font><br><br>{gender1}
                            </font></br>    
                            </div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
                                <strong>2nd</strong>
                            </button>
                            </h2>
                            <div id="flush-collapseTwo" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div class="accordion-body">
                            <font size=5>
                            <font size=6><strong>📰 제목</strong></font><br>&nbsp"{df1.title[top_indices].iloc[1]}"<br><br>
                            <font size=6><strong>📝 요약</strong></font><br>&nbsp{s12}<br>&nbsp{s22}<br><br>
                            <font size=6><strong>🔑 키워드</strong></font><br><strong>&nbsp#</strong>{keywords_mmr2[0][0]}<strong>&nbsp#</strong>{keywords_mmr2[1][0]}<strong>&nbsp#</strong>{keywords_mmr2[2][0]}<br><br>
                            <font size=6><strong>👀 시각화</strong></font><br><br>&nbsp<img src="{wordcloud_html2}" alt="wordcloud"><br><br><br>
                            <font size=6><strong>✍ 분석결과 ➡ {sim2}%</strong></font>{html_plot2}
                            <font size=6><strong>🧺 상담다발품목</strong></font><br><br>{gender2}
                            </font></br>   
                            </div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseThree" aria-expanded="false" aria-controls="flush-collapseThree">
                                <strong>3rd</strong>
                            </button>
                            </h2>
                            <div id="flush-collapseThree" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div class="accordion-body">
                            <font size=5>
                            <font size=6><strong>📰 제목</strong></font><br>&nbsp"{df1.title[top_indices].iloc[2]}"<br><br>
                            <font size=6><strong>📝 요약</strong></font><br>&nbsp{s13}<br>&nbsp{s23}<br><br>
                            <font size=6><strong>🔑 키워드</strong></font><br><strong>&nbsp#</strong>{keywords_mmr3[0][0]}<strong>&nbsp#</strong>{keywords_mmr3[1][0]}<strong>&nbsp#</strong>{keywords_mmr3[2][0]}<br><br>
                            <font size=6><strong>👀 시각화</strong></font><br><br>&nbsp<img src="{wordcloud_html3}" alt="wordcloud"><br><br><br>
                            <font size=6><strong>✍ 분석결과 ➡ {sim3}%</strong></font>{html_plot3}
                            <font size=6><strong>🧺 상담다발품목</strong></font><br><br>{gender3}
                            </font></br>   
                            </div>
                            </div>
                        </div>
                    </div>
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
                </body>
                </html>
                """
                ,height = 2500)


            else:
                st.warning("**고객 ID를 먼저 입력하신 뒤 버튼을 눌러주세요.**")
        except:
            st.warning("**고객 ID를 올바르게 다시 입력해주세요.**")