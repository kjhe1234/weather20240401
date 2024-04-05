import sys
import requests
from bs4 import BeautifulSoup

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import time
import threading

form_class = uic.loadUiType("ui/weatherUi.ui")[0]
# ui 폴더 내의 디자인된 ui 불러오기

class WeatherApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨 검색 프로그램")
        self.setWindowIcon(QIcon("icon/weather.png"))
        self.statusBar().showMessage("Weather Search App Ver 0.5")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # 윈도우를 항상 맨위로 유지


        #self.search_btn.clicked.connect(self.weather_search)
        self.search_btn.clicked.connect(self.reflashTimer)
        #self.area_input.returnPressed.connect(self.weather_search)
        # 라인에디터 상에서 엔터키 이벤트가 발생시 함수 호출 -> returnPressed
        self.area_input.returnPressed.connect(self.reflashTimer)


    def weather_search(self):
        inputArea = self.area_input.text()  # 사용자가 입력한 지역명 텍스트 가져오기

        weatherHtml = requests.get(f"https://search.naver.com/search.naver?&query={inputArea}날씨")
        # 네이버에서 {날씨}로 검색한 결과 html 파일 가져오기
        # print(weatherHtml.text)

        weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')
        # print(weatherSoup)

        try:
            areaText = weatherSoup.find("h2", {"class": "title"}).text
            areaText = areaText.strip()  # 양쪽 공백 제거
            print(f"지역이름 : {areaText}")


            todayTempText = weatherSoup.find("div", {"class": "temperature_text"}).text
            todayTempText = todayTempText[6:12].strip()  # 6번째 글자부터 슬라이싱 후 양쪽 공백 제거
            print(f"현재온도 : {todayTempText}")

            # yesterdayTempText = weatherSoup.find("span", {"class":"temperature"}).text


            yesterdayTempText = weatherSoup.find("p", {"class": "summary"}).text
            yesterdayTempText = yesterdayTempText[:15].strip()
            print(f"어제날씨비교 : {yesterdayTempText}")

            todayWeatherText = weatherSoup.find("span", {"class": "weather before_slash"}).text
            todayWeatherText = todayWeatherText.strip()
            print(f"오늘날씨 : {todayWeatherText}")


            senseTempeText = weatherSoup.find("dd", {"class": "desc"}).text
            senseTempeText = senseTempeText.strip()
            print(f"체감온도 : {senseTempeText}")

            todayInfoText = weatherSoup.select("ul.today_chart_list>li")

            # print(todayInfoText[0])
            # todayInfoText 에서 첫번째 리스트 확인

            dust1Info = todayInfoText[0].find("span", {"class": "txt"}).text
            dust1Info = dust1Info.strip()
            print(f"미세먼지 : {dust1Info}")

            dust2Info = todayInfoText[1].find("span", {"class": "txt"}).text
            dust2Info = dust2Info.strip()
            print(f"초미세먼지 : {dust2Info}")

            self.area_title.setText(areaText)
            self.setWeatherImage(todayWeatherText)  # 날씨 이미지 출력 함수 호출
            self.now_temper.setText(todayTempText)
            self.yester_temper.setText(yesterdayTempText)
            self.sense_temper.setText(senseTempeText)
            self.dust1_info.setText(dust1Info)
            self.dust2_info.setText(dust2Info)


        except:

            try:
                # 해외날씨 처리 구문
                areaText = weatherSoup.find("h2", {"class": "title"}).text  # 날씨 지역 이름 가져오기
                areaText = areaText.strip()
                todayTempAllText = weatherSoup.find("div", {"class": "temperature_text"}).text
                todayTempAllText = todayTempAllText.strip()
                print(todayTempAllText)



                #todayTempText = todayTempAllText[6:9].strip()  # 해외 도시 현재 온도
                todayTempText = weatherSoup.select("div.temperature_text>strong")[0].text
                todayTempText = todayTempText[5:]
                #todayWeatherText = todayTempAllText[10:12].strip()  # 해외 도시 날씨 텍스트
                todayWeatherText = weatherSoup.select("div.temperature_text>p.summary")[0].text
                todayWeatherText = todayWeatherText[:3].strip()
                print(todayWeatherText)

                #senseTempeText = todayTempAllText[18:].strip()  # 해외 도시 체감 온도
                senseTempeText = weatherSoup.select("p.summary>span.text>em")[0].text


                self.setWeatherImage(todayWeatherText)  # 날씨 이미지 출력 함수 호출

                self.area_title.setText(areaText)
                self.now_temper.setText(todayTempText)
                self.sense_temper.setText(senseTempeText)
                self.yester_temper.setText("")  # 해외도시 어제와 날씨 비교 정보 없음 빈공간 출력
                self.dust1_info.setText("-")
                self.dust2_info.setText("-")


            except:
                self.area_title.setText("입력된 지역명 오류")
                self.setWeatherImage("")
                self.now_temper.setText("")
                self.yester_temper.setText(f"{inputArea}지역은 없습니다.")
                self.sense_temper.setText("")
                self.dust1_info.setText("")
                self.dust2_info.setText("")

    def setWeatherImage(self, weatherText):  # 날씨에 따른 이미지 출력
        if weatherText == "맑음":
            weatherImage = QPixmap("icon/sun.png") # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
            # ui에 준비된 label 이름에 이미지 출력하기

        elif "화창" in weatherText:
            weatherImage = QPixmap("icon/sun.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))

        elif weatherText == "구름많음":
            weatherImage = QPixmap("icon/cloud.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))

        elif "흐림" in weatherText:
            weatherImage = QPixmap("icon/cloud.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))

        elif "비" in weatherText:
            weatherImage = QPixmap("icon/rain.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))

        elif weatherText == "소나기":
            weatherImage = QPixmap("icon/rain.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))

        elif weatherText == "눈":
            weatherImage = QPixmap("icon/snow.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))

        else:
            self.weather_img.setText(weatherText)

    def reflashTimer(self):  # 다시 크롤링을 해오는 타이머
        self.weather_search()  # 날씨 조회 함수 호출
        threading.Timer(60, self.reflashTimer).start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WeatherApp()
    win.show()
    sys.exit(app.exec_())




