<img src="https://capsule-render.vercel.app/api?type=waving&color=BDBDC8&height=150&section=header" />


# 구글 플레이스토어 웹 리뷰 크롤러
Notion | https://www.notion.so/yimsebin/08288af861a94970ac98e8e4693fe2e6?pvs=4


## 🚧 Update LOG
@2024-04-04
파일 업로드.

## 🎨 코드 설명
#### 라이브러리 설치하기
```python
!pip install selenium
!pip install pandas
```

#### '리뷰 모두 보기' 버튼 클릭
```python
import time
​
# 최하단으로 스크롤내리기
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 리뷰 모두보기 클릭
spread_review = driver.find_element(by=By.XPATH, value = '/html/body/c-wiz[2]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/c-wiz[5]/section/div/div[2]/div[5]/div/div/button')
isTrue = spread_review.is_displayed()
if isTrue :
    driver.execute_script("arguments[0].click();", spread_review)
    # spread_review.click()
    time.sleep(1.5)
```

#### 무한스크롤
```python
# 리뷰 팝업창 element
all_reviews = driver.find_element(by=By.XPATH, value ='/html/body/div[4]/div[2]/div/div/div/div/div[2]')
# 현재 리뷰 팝업창 height 구하기
last_height = driver.execute_script("return arguments[0].scrollHeight", all_reviews)
# last_height = driver.execute_script("return document.getElementsByClassName('odk6He')[0].scrollHeight")
​
for _ in range(5) :
    # 현재 height만큼 스크롤
    driver.execute_script(f'arguments[0].scrollTop = {last_height}', all_reviews)
    time.sleep(1)   # 로드 기다리는 시간
​
    new_height = driver.execute_script("return arguments[0].scrollHeight", all_reviews)
    # new_height = driver.execute_script("return document.getElementsByClassName('odk6He')[0].scrollHeight")
​
    # 스크롤을 진행했는데도 이전 height와 스크롤 이후 height가 같으면 더이상 로드할 데이터가 없다는 뜻이므로 스크롤 중단
    if new_height == last_height :
        break
​
    last_height = new_height
```

#### 데이터 수집
```python
import pandas as pd
​
data = pd.DataFrame(data=[], columns=['날짜','리뷰','별점'])
#날짜, 리뷰, 별점 수집
dates = driver.find_elements(by=By.XPATH, value = '//div[@class="odk6He"]//span[@class="bp9Aid"]')
reviews=driver.find_elements(by=By.XPATH, value = '//div[@class="odk6He"]//div[@class="h3YV2d"]')
stargrades = driver.find_elements(by=By.XPATH, value = '//div[@class="odk6He"]//div[@class="iXRFPc"]')
​
​
# 수집한 리뷰를 DataFrame에 삽입
for i in range(len(reviews)):
    tmp = []
    tmp.append(dates[i].text)
    tmp.append(reviews[i].text)
    tmp.append(stargrades[i].get_attribute('aria-label'))
​
    tmp = pd.DataFrame(data=[tmp], columns = data.columns)
    data = pd.concat([data,tmp])
​
# 인덱스 재배열
data.reset_index(inplace=True, drop=True)
```

## 💡 Reference
- https://brave-greenfrog.tistory.com/category/DeepLearning/2022-1%20Crawling%20Project
- https://blog-of-gon.tistory.com/324
- https://velog.io/@devmin/selenium-crawling-infinite-scroll-click
- https://velog.io/@parkeu/youtubeshorts

<img src="https://capsule-render.vercel.app/api?type=waving&color=BDBDC8&height=150&section=footer" />
