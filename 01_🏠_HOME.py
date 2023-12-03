#########################################중요###########################################
# 터미널에서 명령어(streamlit run 01_🏠_HOME.py)를 실행 시켜주어야 스트림릿이 작동함
#######################################################################################

import streamlit as st
import hydralit_components as hc
from PIL import Image
import pandas as pd
import random
import streamlit.components.v1 as components

#페이지를 위한 코드
#layout = wide : 화면 설정 디폴트값을 와이드로
st.set_page_config(page_title="HOME", page_icon="🏠",layout = 'wide')

# 직접 HTML 및 CSS를 사용하여 화면 비율 조정
st.markdown(
    """
    <style>
        body {
            width: 100%;
            margin: 0;
        }
        .stApp {
            max-width: 2000px;  # 조정하려는 최대 너비
            margin: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.spinner("# ⏳ 잠시만 기다려주세요."):

    image = Image.open('images/logo.png')
    image2 = Image.open('images/logo2.png')
    image3 = Image.open('images/face.png')

    #메뉴 탭 하단 사이드바에 이미지 넣기
    st.sidebar.image(image2, use_column_width=True)

    #최상단에 이미지 넣기
    st.image(image, width=1590) 

    #리스트를 문자열로 인식하는 문제 해결하는 함수
    def parse_list(input_str):

        return eval(input_str)


    @st.cache_data
    def daily_result_load_data():

        #daily news 전처리 및 모델링 결과
        daily_result = pd.read_csv("data/new_daily_result.csv", converters={'fv': parse_list})

        return daily_result

    daily_result = daily_result_load_data()

    # 리콜 정보
    # df1 = pd.read_excel('data/국내 리콜.xlsx')

    # 소비자 단어
    df2 = pd.read_csv("data/consumer_word.csv")

    # 상담다발품목
    df = pd.read_csv("data/상담다발품목.csv")
    
    # CDN 가능
    # Bootstrap
    # 문자열 포매팅을 활용하여 변수 지정 후 HTML로 표현

    random_number = random.randint(0, 2)
    recall_image_list = ['https://www.consumer.go.kr/site/consumer/upload/recall/RCLL_000000000565212_20231121030002601.jpg'
                    ,'https://www.consumer.go.kr/site/consumer/upload/recall/RCLL_000000000565892_20231202053014578.jpg'
                    ,'https://www.consumer.go.kr/site/consumer/upload/recall/RCLL_000000000565860_20231201053011419.jpg']
    recall_product_list = ['동물 슬리퍼','빠투능','큰맘 해장국']
    recall_company_list = ['(주) 현주무역','(주) 씨암푸드','(주) 포듀미트']
    recall_date_list = ['2023.11.14~', '~2024.11.22','~2024.11.12']

    random_titles = daily_result['title'].sample(n=3) 
    news1 = random_titles.values[0]
    news2 = random_titles.values[1]
    news3 = random_titles.values[2]

    cc = st.columns(3)
    with cc[0]:
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
        <font size=5>
        <div class="card" style="width: 32.5rem; background-color: #F0FAFF;">
        <div class="card-body">
            <style>
                .card-title strong {{font-size: 2em;}}
            </style>
            <h5 class="card-title"><strong>🗞 보도자료</strong></h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">아래는 보도자료의 제목입니다. </h6>
            <p class="card-text"><strong>{news1}</strong></p>
            <style>
            .link-card {{
                display: flex;
                flex-direction: column;
                padding: 5px;
                margin-bottom: 10px;
                border: 1px solid #E8DDDA;
                border-radius: 15px;
                background-color: white; 
                box-shadow: 0px 0px 5px #F4EDEC;
            }}
            .link-card:hover {{
            background-color: #DEEFFF;
            }}
            a {{
                color: black!important;
                text-decoration: none!important;
            }}
            </style>
            <div class="link-card"><a href="https://www.consumer.go.kr/consumer/index.do" target="_blank">🔍 더 많은 정보를 알아보세요.</a></div>
        </div>
        </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
        </font></br>
        </body>
        </html>
        """
        ,height=300
        )


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
            <font size=5>
                <div class="card" style="width: 32.5rem; background-color: #F0FAFF;">
                    <img src="{recall_image_list[random_number]}" class="card-img-top" alt="...">
                    <div class="card-body">
                        <h5 class="card-title"></h5>
                        <font size=6>
                            <p class="card-text"><strong>📰 국내리콜정보</strong></p>
                        </font></br>
                        <table class="table">
                            <thead>
                                <td class="table-secondary"><strong>제품명</strong></td>
                                <td class="table-secondary"><strong>사업자명</strong></td>
                                <td class="table-secondary"><strong>리콜공표일</strong></td>

                            </thead>
                            <tbody>
                                <tr>
                                <td>{recall_product_list[random_number]}</td>
                                <td>{recall_company_list[random_number]}</td>
                                <td>{recall_date_list[random_number]}</td>
                                </tr>
                            </tbody>
                            </table>
                        <style>
                        .link-card {{
                            display: flex;
                            flex-direction: column;
                            padding: 5px;
                            margin-bottom: 10px;
                            border: 1px solid #E8DDDA;
                            border-radius: 15px;
                            background-color: white; 
                            box-shadow: 0px 0px 5px #F4EDEC;
                        }}
                        .link-card:hover {{
                        background-color: #DEEFFF;
                        }}
                        a {{
                            color: black!important;
                            text-decoration: none!important;
                        }}
                        </style>
                        <div class="link-card"><a href="https://www.consumer.go.kr/consumer/index.do" target="_blank">🔍 소비자24에서 더 자세히 알아보세요.</a></div>
                    </div>
                </div>
            </font></br>
        </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
        </body>
        </html>
        """
        ,height=800
        )
    
    with cc[1]:
        st.write('')
    with cc[2]:
        st.write('')


    #can apply customisation to almost all the properties of the card, including the progress bar
    theme = {'bgcolor': '#DEEFFF','title_color': 'black','content_color': 'black','icon_color': 'black', 'icon': 'fa fa-check-circle'}

    c = st.columns(3)

    with c[0]:
        hc.info_card(title='🗞 보도자료', content='<' + random_titles.values[0]+ '>', theme_override=theme)
        st.write('')

    with c[1]:
        hc.info_card(title='🔊 피해예방주의보', content='<' + random_titles.values[1] + '>', theme_override=theme)
        
    with c[2]:
        hc.info_card(title='🔊 안전주의보', content='<' + random_titles.values[2] + '>', theme_override=theme)

        random_row = df.sample(n=1) 
        hc.info_card(title='📰 상담다발품목', content = '<' +random_row.MID_CLS.values[0]+ '>' + ' , ' + random_row.CNSL_RSN.values[0] + ' , ' + random_row.SLL_MTD_NM.values[0],theme_override=theme)

    cc = st.columns([6,3])

    with cc[0]:
        # 데이터프레임에서 랜덤으로 하나의 행 선택
        st.write("")
    with cc[1]:
        num_indices1 = len(df2)
        # 랜덤으로 인덱스 3개 추출
        random_indices1 = random.sample(range(num_indices1), 3)
        hc.info_card(title='📚 오늘의 소비자 단어', content=f'"{df2.단어[random_indices1[0]]}"'+'\n'+f': {df2.뜻[random_indices1[0]]}', theme_override=theme)

    st.write('')
    st.write('## 👇 아래 소개를 참고해주세요')

    # st.tab 함수를 통해 하단에 tab 메뉴 생성
    tab1, tab2, tab3 = st.tabs([' **Who** ❓' , ' **Home**  🏠' , ' **PRIVATE**  👤'])

    with tab1:
        st.header('Team  소개')
        st.image(image3, width=200)
        st.write("### 안녕하세요, 저희는 **중앙대학교 응용통계학과 학생들** 입니다.")
        st.text('')
        st.write("### 빅데이터 분석 공모전 **소비자** 부문으로 참가하며 이 서비스를 기획하게 되었습니다.")
        st.write("### **소비자들**의 결제 데이터와 **한국소비자원의 보도자료**를 이용한 다양한 서비스를 제공합니다.")

    with tab2:
        st.header('Home 화면 소개')

    with tab3:
        st.header('Private 화면 소개')

