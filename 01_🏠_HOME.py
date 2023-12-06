#########################################중요###########################################
# 터미널에서 명령어(streamlit run 01_🏠_HOME.py)를 실행 시켜주어야 스트림릿이 작동함
#######################################################################################

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import random

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
            max-width: 1500px;  # 조정하려는 최대 너비
            margin: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.spinner("# ⏳ 잠시만 기다려주세요."):

    image = Image.open('images/logo1.png')
    image2 = Image.open('images/logo2.png')

    #메뉴 탭 하단 사이드바에 이미지 넣기
    st.sidebar.image(image2, use_column_width=True)

    #최상단에 이미지 넣기
    st.image(image, width=1000) 

    #리스트를 문자열로 인식하는 문제 해결하는 함수
    def parse_list(input_str):
        return eval(input_str)

    #화면이 업데이트될 때 마다 변수 할당이 된다면 시간이 오래 걸려서 @st.cache_data 사용(캐싱)
    @st.cache_data
    def load_data():

        # 보도자료
        # fv : 모델링 결과
        # wc : 배포시 konlpy java 환경변수 오류 때문에 명사 추출 결과를 컬럼에 미리 담아놓음
        df1 = pd.read_csv("data/보도자료.csv", converters={'fv' : parse_list, 'wc' : parse_list})

        # 상담다발품목
        df2 = pd.read_csv("data/상담다발품목.csv")

         # 소비자 단어
        df3 = pd.read_csv("data/소비자단어.csv")

        return df1,df2,df3

    df1, df2, df3 = load_data()

    # Home 화면에서 랜덤으로 보여줄 보도자료 정보 담아두기
    random1 = df1[['title','subtitle']].sample(n=3, replace=False) 
    news1 = random1.title.values[0]
    subnews1 = random1.subtitle.values[0]
    news2 = random1.title.values[1]
    subnews2 = random1.subtitle.values[1]
    news3 = random1.title.values[2]
    subnews3 = random1.subtitle.values[2]


    # Home 화면에서 랜덤으로 보여줄 상담다발품목 정보 담아두기
    # 품목, 피해유형, 거래유형
    random2 = df2[['GDNM','CNSL_RSN','SLL_MTD_NM']].sample(n=4, replace=False) 
    product1 = random2.GDNM.values[0]
    type11 = random2.CNSL_RSN.values[0]
    type21 = random2.SLL_MTD_NM.values[0]
    product2 = random2.GDNM.values[1]
    type12 = random2.CNSL_RSN.values[1]
    type22 = random2.SLL_MTD_NM.values[1]
    product3 = random2.GDNM.values[2]
    type13 = random2.CNSL_RSN.values[2]
    type23 = random2.SLL_MTD_NM.values[2]
    product4 = random2.GDNM.values[3]
    type14 = random2.CNSL_RSN.values[3]
    type24 = random2.SLL_MTD_NM.values[3]

    # Home 화면에서 랜덤으로 보여줄 소비자단어 정보 담아두기
    random3 = df3[['단어','뜻','url']].sample(n=1, replace=False) 
    word1 = random3.단어.values[0]
    word2 = random3.뜻.values[0]
    word3 = random3.url.values[0]

    # Home 화면에서 랜덤으로 보여줄 리콜 정보 변수에 담아두기
    random_number = random.randint(0, 3)
    recall_image_list = ['https://www.consumer.go.kr/site/consumer/upload/recall/RCLL_000000000565212_20231121030002601.jpg'
                    ,'https://www.consumer.go.kr/site/consumer/upload/recall/RCLL_000000000565892_20231202053014578.jpg'
                    ,'https://www.consumer.go.kr/site/consumer/upload/recall/RCLL_000000000565860_20231201053011419.jpg'
                    ,'https://www.consumer.go.kr/site/consumer/upload/recall/RCLL_000000000562223_20230923053015919.jpg']
    recall_product_list = ['동물 슬리퍼','빠투능','큰맘 해장국','에너스웰 캡슐']
    recall_company_list = ['(주) 현주무역','(주) 씨암푸드','(주) 포듀미트','영풍제약']
    recall_date_list = ['23.11.14~','~24.11.22','~24.11.12','~24.01.24']

    st.write('')
    cc = st.columns(3)

    # CDN 가능
    # Bootstrap
    # 문자열 포매팅을 활용하여 변수 지정 후 HTML로 표현

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
        <font size=3>
        <div class="card" style="width: 21rem; background-color: #F0FAFF;">
        <div class="card-body">
            <style>
                .card-title strong {{font-size: 1.4em;}}
            </style>
            <h5 class="card-title"><strong>🗞 보도자료</strong></h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">&nbsp</h6>
            <p class="card-text"><strong>"{news1}"</strong></p>
            <h6 class="card-subtitle mb-2 text-body-secondary">: {subnews1}</h6>
            <h6 class="card-subtitle mb-2 text-body-secondary">&nbsp</h6>
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
            <div class="link-card"><a href="https://www.kca.go.kr/home/main.do" target="_blank">🔍 더 많은 정보를 알아보세요.</a></div>
        </div>
        </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
        </font></br>
        </body>
        </html>
        """
        ,height=300
        ,width=360
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
            <font size=3>
                <div class="card" style="width: 21rem; background-color: #F0FAFF;">
                    <img src="{recall_image_list[random_number]}" class="card-img-top" alt="...">
                    <div class="card-body">
                    <style>
                        .card-title strong {{font-size: 1.4em;}}
                    </style>
                    <h5 class="card-title"><strong>📰 국내리콜정보</strong></h5>
                    <h6 class="card-subtitle mb-2 text-body-secondary">&nbsp</h6>
                        <table class="table">
                            <thead>
                                <td class="table-secondary"><strong>제품명</strong></td>
                                <td class="table-secondary"><strong>사업자명</strong></td>
                                <td class="table-secondary"><strong>공표일</strong></td>

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
                        <div class="link-card"><a href="https://www.consumer.go.kr/consumer/index.do" target="_blank">🔍 소비자24로 바로가기</a></div>
                    </div>
                </div>
            </font></br>
        </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
        </body>
        </html>
        """
        ,width=360
        ,height=700
        )
    
    with cc[1]:
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
        <font size=3>
        <div class="card" style="width: 21rem; background-color: #F0FAFF;">
        <div class="card-body">
            <style>
                .card-title strong {{font-size: 1.4em;}}
            </style>
            <h5 class="card-title"><strong>🔊 피해예방주의보</strong></h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">&nbsp</h6>
            <p class="card-text"><strong>"{news2}"</strong></p>
            <h6 class="card-subtitle mb-2 text-body-secondary">: {subnews2}</h6>
            <h6 class="card-subtitle mb-2 text-body-secondary">&nbsp;</h6>
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
            <div class="link-card"><a href="https://www.kca.go.kr/home/main.do" target="_blank">🔍 더 많은 정보를 알아보세요.</a></div>
        </div>
        </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
        </font></br>
        </body>
        </html>
        """
        ,height=300
        ,width=360
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
        <font size=3>
        <div class="card" style="width: 21rem; background-color: #F0FAFF;">
        <div class="card-body">
            <style>
                .card-title strong {{font-size: 1.4em;}}
            </style>
            <h5 class="card-title"><strong>🧺 상담다발품목</strong></h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">&nbsp</h6>
            <table class="table">
            <thead>
                <td class="table-secondary"><strong>품목</strong></td>
                <td class="table-secondary"><strong>피해유형</strong></td>
                <td class="table-secondary"><strong>거래유형</strong></td>
            </thead>
            <tbody>
                <tr>
                <td>{product1}</td>
                <td>{type11}</td>
                <td>{type21}</td>
                </tr>
                <tr>
                <td>{product2}</td>
                <td>{type12}</td>
                <td>{type22}</td>
                </tr>
                <tr>
                <td>{product3}</td>
                <td>{type13}</td>
                <td>{type23}</td>
                </tr>
                <tr>
                <td>{product4}</td>
                <td>{type14}</td>
                <td>{type24}</td>
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
            <div class="link-card"><a href="https://crossborder.kca.go.kr/home/sub.do?menukey=134" target="_blank">🔍 더 많은 정보를 알아보세요.</a></div>
        </div>
        </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
        </font></br>
        </body>
        </html>
        """
        ,height=700
        ,width=360
        )

    with cc[2]:
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
        <font size=3>
        <div class="card" style="width: 21rem; background-color: #F0FAFF;">
        <div class="card-body">
            <style>
                .card-title strong {{font-size: 1.4em;}}
            </style>
            <h5 class="card-title"><strong>🔊 소비자안전주의보</strong></h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">&nbsp</h6>
            <p class="card-text"><strong>"{news3}"</strong></p>
            <h6 class="card-subtitle mb-2 text-body-secondary">: {subnews3}</h6>
            <h6 class="card-subtitle mb-2 text-body-secondary">&nbsp</h6>
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
            <div class="link-card"><a href="https://www.kca.go.kr/home/main.do" target="_blank">🔍 더 많은 정보를 알아보세요.</a></div>
        </div>
        </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
        </font></br>
        </body>
        </html>
        """
        ,height=300
        ,width=360
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
        <font size=3>
        <div class="card" style="width: 21rem; background-color: #F0FAFF;">
        <div class="card-body">
            <style>
                .card-title strong {{font-size: 1.5em;}}
            </style>
            <h5 class="card-title"><strong>📚 소비자 단어</strong></h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">&nbsp</h6>
            <p class="card-text"><strong>"{word1}"</strong></p>
            <p class="card-text"><strong>: {word2}</strong></p>
            <h6 class="card-subtitle mb-2 text-body-secondary">&nbsp</h6>
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
            <div class="link-card"><a href={word3} target="_blank">🔍 네이버 지식백과로 바로가기</a></div>
        </div>
        </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
        </font></br>
        </body>
        </html>
        """
        ,height=500
        ,width=360
        )