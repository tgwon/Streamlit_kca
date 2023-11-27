#라이브러리 import
#필요한 경우 install
#pip install streamlit_option_menu
import streamlit as st
#from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import random

#########################################중요###########################################
# 터미널에서 명령어(streamlit run 01_🏠_HOME.py)를 실행 시켜주어야 스트림릿이 작동함
#######################################################################################

image = Image.open('images/logo.png')
image2 = Image.open('images/logo2.png')
image3 = Image.open('images/logo3.png')

#페이지를 위한 코드
#layout = wide : 화면 설정 디폴트값을 와이드로
st.set_page_config(page_title="HOME", page_icon="🏠",layout = 'wide')

#메뉴 탭 하단 사이드바에 이미지 넣기
st.sidebar.image(image2, use_column_width=True)
st.sidebar.image(image3, use_column_width=True)

#최상단에 이미지 넣기
st.image(image2, width=300) 
st.image(image, width=1800) 

#st.markdown('''
#<h2>Daily News Service by <span style="color: #6FA8DC;"> CAUsumer</span></h2>
#''', unsafe_allow_html=True)
#st.text('')

#리스트를 문자열로 인식하는 문제 해결하는 함수
def parse_list(input_str):

    return eval(input_str)


@st.cache_data
def daily_result_load_data():

    #daily news 전처리 및 모델링 결과
    daily_result = pd.read_csv("data/new_daily_result.csv", converters={'fv': parse_list})

    return daily_result

daily_result = daily_result_load_data()

random_titles = daily_result['title'].sample(n=3) 

df = pd.read_csv("data/상담다발품목.csv")

recall = pd.read_excel('data/국내 리콜.xlsx')



st.text('')

import streamlit as st
import hydralit_components as hc


# linktree 형식
st.markdown(
    """
<style>
.link-card {
    display: flex;
    flex-direction: column;
    padding: 5px;
    margin-bottom: 10px;
    border: 1px solid #E8DDDA;
    border-radius: 15px;
    background-color: white; 
    box-shadow: 0px 0px 5px #F4EDEC;
}
.link-card:hover {
background-color: #FFF6F3;
}
a {
    color: black!important;
    text-decoration: none!important;
}
</style>
""",
    unsafe_allow_html=True,
)

#하이퍼링크 만드는 함수
def create_link_card(title, url):
    container = st.container()
    container.markdown(
        f'<div class="link-card"><a href="{url}" target="_blank">{title}</a></div>',
        unsafe_allow_html=True,
    )
    return container


#can apply customisation to almost all the properties of the card, including the progress bar
theme = {'bgcolor': '#DEEFFF','title_color': 'black','content_color': 'black','icon_color': 'black', 'icon': 'fa fa-check-circle'}

cc = st.columns(3)

with cc[0]:
    cw = pd.read_csv("data/consumer_word.csv")
    num_indices1 = len(cw)
    # 랜덤으로 인덱스 3개 추출
    random_indices1 = random.sample(range(num_indices1), 3)
    hc.info_card(title='🗞 보도자료', content='<' + random_titles.values[0]+ '>', theme_override=theme)
    hc.info_card(title='📚 오늘의 소비자 단어', content=f'"{cw.단어[random_indices1[0]]}"'+'\n'+f': {cw.뜻[random_indices1[0]]}', theme_override=theme)
    st.write('')
    st.write()
    st.write()

with cc[1]:
    hc.info_card(title='🔊 피해예방주의보', content='<' + random_titles.values[1] + '>', theme_override=theme)
    # 데이터프레임에서 랜덤으로 하나의 행 선택
    random_row = recall.sample(n=1) 
    hc.info_card(title='📰 국내리콜정보', content = '<' +random_row.제품명.values[0]+ '>' + ' , ' + random_row.리콜공표일.values[0], theme_override=theme)
with cc[2]:
    hc.info_card(title='🔊 안전주의보', content='<' + random_titles.values[2] + '>', theme_override=theme)

    random_row = df.sample(n=1) 
    hc.info_card(title='📰 상담다발품목', content = '<' +random_row.MID_CLS.values[0]+ '>' + ' , ' + random_row.CNSL_RSN.values[0] + ' , ' + random_row.SLL_MTD_NM.values[0],theme_override=theme)

st.write('')
st.info("한국소비자원의 보도 자료를 추천받고 싶다면 메뉴 탭의 **PRIVATE** 을 누르세요!")
st.info("그 외의 다양한 정보가 궁금하면 좌측 메뉴 탭의 **PUBLIC** 을 누르세요!")
# 링크
create_link_card(
"💡한국소비자원이 궁금하면 클릭해주세요.  홈페이지로 이동합니다.",
"https://www.kca.go.kr/home/main.do#Page1",
)


st.write('')
st.write('👇 아래 소개를 참고해주세요')

# st.tab 함수를 통해 하단에 tab 메뉴 생성
tab1, tab2, tab3 = st.tabs(['**Who**❓',  '**PRIVATE**  👤', '**PUBLIC**  👥'])

with tab1:
    st.header('Team  Introduction')
    image = Image.open('images/face.png')
    st.image(image, width=200)
    st.write("안녕하세요, 저희는 **CAUsumer** 입니다.")
    st.write("팀 **CAUsumer**는 중앙대학교 응용통계학과 학생들로 이루어져있습니다.")
    st.text('')
    st.write("빅데이터 분석 공모전 **소비자** 부문으로 참가하며 **소비자**들에게 도움을 줄 수 있는 서비스를 고민했고, 고민 끝에  이 서비스를 기획하게 되었습니다.")
    st.write("**CAUsumer**는 **소비자들**의 결제 데이터와 **한국소비자원의 보도자료**를 이용한 다양한 서비스를 제공합니다.")

with tab2:
    st.header('Private Service')

with tab3:
    st.header('Public Service')
