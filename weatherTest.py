import requests  # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4

inputArea = input("날씨를 조회하려는 지역을 입력하세요 :")

weatherHtml = requests.get(f"https://search.naver.com/search.naver?&query={inputArea}날씨")
# 네이버에서 {날씨}로 검색한 결과 html 파일 가져오기
#print(weatherHtml.text)

weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')
#print(weatherSoup)

areaText = weatherSoup.find("h2", {"class":"title"}).text
# 지역 이름 가져오기
areaText = areaText.strip() # 양쪽 공백 제거
print(f"지역이름 : {areaText}")

todayTempText = weatherSoup.find("div", {"class":"temperature_text"}).text
#현재 온도
todayTempText = todayTempText[6:12].strip()  # 6번째 글자부터 슬라이싱 후 양쪽 공백 제거
print(f"현재온도 : {todayTempText}")

yesterdayTempText = weatherSoup.find("span", {"class":"temperature up"}).text
#어제와의 온도 비교
yesterdayTempText = yesterdayTempText.strip()
print(f"어제와 온도비교 : {yesterdayTempText}")

todayWeatherText = weatherSoup.find("span", {"class":"weather before_slash"}).text
#어제와의 날씨 비교
todayWeatherText = todayWeatherText.strip()
print(f"어제와 날씨비교 : {todayWeatherText}")

senseTempeText = weatherSoup.find("dd", {"class":"desc"}).text
#체감 온도
senseTempeText = senseTempeText.strip()
print(f"체감온도 : {senseTempeText}")

todayInfoText = weatherSoup.select("ul.today_chart_list>li")
# 미세먼지, 초미세먼지,자외선,일몰 이 있는 리스트
#print(todayInfoText[0])
#todayInfoText 에서 첫번째 리스트 확인
dust1Info = todayInfoText[0].find("span", {"class":"txt"}).text
#미세먼지 정보
dust1Info = dust1Info.strip()
print(f"미세먼지 : {dust1Info}")

dust2Info = todayInfoText[1].find("span", {"class":"txt"}).text
#초미세먼지 정보
dust2Info = dust2Info.strip()
print(f"초미세먼지 : {dust2Info}")







