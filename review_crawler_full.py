from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# headless
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument('window-size=1920x1080')
# user agent
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36")
options.add_argument("disable-gpu")

# chromedriver
driver = webdriver.Chrome(options=options)

raw_data = {
"https://play.google.com/store/apps/details?id=com.superjoy.idleheroes&hl=ko&gl=US" : "용사단 키우기",
"https://play.google.com/store/apps/details?id=com.superbox.aos.herowave&hl=ko&gl=US" : "히어로 원정대-키우기 방치형 RPG",
"https://play.google.com/store/apps/details?id=com.miHoYo.GenshinImpact&hl=ko_KR" : "원신",
"https://play.google.com/store/apps/details?id=com.abocado.eggplant&hl=ko&gl=US" : "생존법사-로그라이크 게임",
"https://play.google.com/store/apps/details?id=com.Romanbard.Jumo&hl=ko&gl=US" : "주모 키우기 - 조선시대 방치형 클리커",
"https://play.google.com/store/apps/details?id=com.neowiz.game.mok&hl=ko&gl=US" : "마스터 오브 나이츠",
"https://play.google.com/store/apps/details?id=com.patterncorp.yokai&hl=ko&gl=US" : "캣앤나이츠-사무라이 블레이드",
"https://play.google.com/store/apps/details?id=com.albiononline&hl=ko-KR": "알비온 온라인",
"https://play.google.com/store/apps/details?id=com.HoYoverse.hkrpgoversea&hl=ko-KR" : "붕괴-스타레일",
"https://play.google.com/store/apps/details?id=com.asobimo.toramonline&hl=ko-KR":  "RPG 토람 온라인",
"https://play.google.com/store/apps/details?id=com.com2us.smon.normal.freefull.google.kr.android.common&hl=ko-KR": "서머너즈 워-천공의 아레나",
"https://play.google.com/store/apps/details?id=com.tapas.heroesrestaurant&hl=ko-KR": "용사식당",
"https://play.google.com/store/apps/details?id=com.pearlabyss.blackdesertm&hl=ko-KR": "검은사막 모바일",
"https://play.google.com/store/apps/details?id=studio.gameberry.idlehunter&hl=ko_KR" : "헌터 키우기",
"https://play.google.com/store/apps/details?id=com.gear2.growslayer&hl=ko_KR" : "슬레이어 키우기",
"https://play.google.com/store/apps/details?id=com.cookapps.ShadowKnightsIdleRPG&hl=ko_KR" : "그림자 기사단",
"https://play.google.com/store/apps/details?id=com.cookapps.berserkidle&hl=ko_KR": "광전사 키우기",
"https://play.google.com/store/apps/details?id=com.gamepub.hab.g&hl=ko_KR":"합성소녀 키우기",
"https://play.google.com/store/apps/details?id=com.dev3ffactory.SweetHome&hl=ko_KR":"스위트홈",
"https://play.google.com/store/apps/details?id=com.devsisters.ck&pcampaignid=merch_published_cluster_promotion_battlestar_top_picks&hl=ko_KR" : "쿠키런 킹덤",
"https://play.google.com/store/apps/details?id=net.cravemob.zeus&hl=ko-KR": "리벤저 사가"}

URLS = list(raw_data.keys())
APPNAMES = list(raw_data.values())

for URL, NAME in zip(URLS, APPNAMES) :

    # Load Page
    # chrome을 띄워 토스 구글플레이 페이지를 킨다.
    driver.get(url=URL)
    print(f"{NAME} 스크롤 시작")

    # 최하단으로 스크롤내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 리뷰 모두보기 클릭
    spread_review = driver.find_element(by=By.XPATH, value = '/html/body/c-wiz[2]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/c-wiz[5]/section/div/div[2]/div[5]/div/div/button')
    isTrue = spread_review.is_displayed()
    if isTrue :
        driver.execute_script("arguments[0].click();", spread_review)
        #spread_review.click()
        time.sleep(1.5)


    # 리뷰 팝업창 element
    all_reviews = driver.find_element(by=By.XPATH, value ='/html/body/div[4]/div[2]/div/div/div/div/div[2]')
    # 현재 리뷰 팝업창 height 구하기
    last_height = driver.execute_script("return arguments[0].scrollHeight", all_reviews)
    # last_height = driver.execute_script("return document.getElementsByClassName('odk6He')[0].scrollHeight")

    while True :
        # 현재 height만큼 스크롤
        driver.execute_script(f'arguments[0].scrollTop = {last_height}', all_reviews)
        time.sleep(1)   # 로드 기다리는 시간

        new_height = driver.execute_script("return arguments[0].scrollHeight", all_reviews)
        # new_height = driver.execute_script("return document.getElementsByClassName('odk6He')[0].scrollHeight")

        # 스크롤을 진행했는데도 이전 height와 스크롤 이후 height가 같으면 더이상 로드할 데이터가 없다는 뜻이므로 스크롤 중단
        if new_height == last_height :
            break

        last_height = new_height

    print(f"{NAME} 데이터 수집 시작")

    data = pd.DataFrame(data=[], columns=['날짜','리뷰','별점'])
    #날짜, 리뷰, 별점 수집
    dates = driver.find_elements(by=By.XPATH, value = '//div[@class="odk6He"]//span[@class="bp9Aid"]')
    reviews=driver.find_elements(by=By.XPATH, value = '//div[@class="odk6He"]//div[@class="h3YV2d"]')
    stargrades = driver.find_elements(by=By.XPATH, value = '//div[@class="odk6He"]//div[@class="iXRFPc"]')


    # 수집한 리뷰를 DataFrame에 삽입
    for i in range(max(len(dates), len(reviews), len(stargrades))) :
        tmp = []
        if i < len(dates) :
            tmp.append(dates[i].text)
        else :
            tmp.append("")

        if i < len(reviews) :
            tmp.append(reviews[i].text)
        else :
            tmp.append("")

        if i < len(stargrades) :
            tmp.append(stargrades[i].get_attribute('aria-label'))
        else :
            tmp.append("")

        tmp = pd.DataFrame(data=[tmp], columns = data.columns)
        data = pd.concat([data,tmp])


    # 인덱스 재배열
    data.reset_index(inplace=True, drop=True)

    print(f"{NAME} 파일 추출")

    # 별점에서 숫자만 추출
    data['별점'] = data['별점'].apply(lambda x : x[5:])
    m = re.compile('[0-9][\.0-9]*') # 정규표현식
    data['별점'] = data['별점'].apply(lambda x : m.findall(x)[0])

    # 엑셀 파일로 추출
    data.to_excel(f'review_{NAME}.xlsx')

driver.close()