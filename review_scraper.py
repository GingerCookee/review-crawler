from google_play_scraper import Sort, reviews
from urllib.parse import urlparse, parse_qs
import pandas as pd
import re

STARTDATE = pd.Timestamp('2024-07-01T00:00:00')
ENDDATE = pd.Timestamp('2024-09-01T00:00:00')

# 크롤링하고자 하는 어플리케이션 목록 엑셀 파일
file_name = 'application_list.xlsx'
application_list = pd.read_excel(file_name)

APPNAMES = list(application_list['어플'])
URLS = list(application_list['링크'])

for URL, NAME in zip(URLS, APPNAMES) :

    isRecent = True
    reviewDf = pd.DataFrame()
    token = None

    print(f"{NAME} 스크롤 시작")

    # URL 파싱
    parsed_url = urlparse(URL)
    # 쿼리 파라미터 추출
    query_params = parse_qs(parsed_url.query)
    # id 값 추출
    app_id = query_params.get('id', [None])[0]

    while isRecent :
        # google_play_scraper 리뷰 한개씩 추출
        result, continuation_token = reviews(
            app_id,
            lang='ko',
            country='kr',
            sort=Sort.NEWEST,
            count=1,
            continuation_token=token # 리뷰 크롤링을 이어가기 위한 토큰
        )
        token = continuation_token

        df = pd.DataFrame(result)

        try:
            review_date = df.iloc[0]['at']
        except IndexError:
            continue

        if STARTDATE <= review_date :
            if ENDDATE > review_date :
                reviewDf = pd.concat([reviewDf, df])
        else :
            isRecent = False

    # 인덱스 재배열
    reviewDf.reset_index(inplace=True, drop=True)
    # 파일 이름에 사용할 수 없는 특수문자 제거
    filename = re.sub('[\/:*?"<>|]','',NAME)
    reviewDf.to_excel(f'reviewData/review_{filename}.xlsx')
