from flask import Flask, render_template, request
from recommend import Recommend # recommend.py(추천 로직 파이썬)
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        start = request.form['dep_date']
        end = request.form['arr_date']
        car_capacity = int(request.form['car_capacity'])
        budget = int(request.form['budget'])
        conn = sql.connect('./view/trip.db')
        recommender = Recommend(start, end, budget, car_capacity, conn)
        value = recommender.recommender()

        # accom_fir: 숙소 우선
        # flight_fir: 항공기 우선
        # rent_fir: 렌트 우선
        value2= ['accom_fir', 'flight_fir', 'rent_fir']
        all_none = all(value[v] is None for v in value2) # value2가 모두 None인지 확인

        # 1. value2가 모두 None이면 fail.html 연결
        if all_none:
            return render_template('fail.html')
        
        # 2. None이 아니라면 result.html 연결
        # 2-1. 호텔
        # hotel 변수 형식
        # [['이름', '숙소우선 호텔이름', '항공기우선 호텔이름', '렌트우선 호텔이름'], ['평점', '숙소우선 호텔평점', '항공기우선 호텔평점', '렌트우선 호텔평점']...]
        hotel= [['이름'], ['평점'], ['위치'], ['금액(1박)']] # result.html 테이블 형식을 따름\
        if value["accom_fir"] is not None: # 숙소우선 경로가 없으면 인덱싱 시도시 에러나서 수정했습니다 (07/30/23 20:50))
            hotel_total= f'{value["accom_fir"][-1]:,}' # 호텔우선 총합(천 단위 콤마 포맷) # 
        else:
            hotel_total = ' '
        for v in value2:
            if value[v] != None:
                
                hotel[0].append(value[v][0][0]) # 이름
                hotel[1].append(value[v][0][1]) # 평점
                hotel[2].append(value[v][0][2]) # 위치
                hotel[3].append(f'{value[v][0][4]:,}') # 금액(천 단위 콤마 포맷)

            # [['이름', ' ', ' ', ' '], ['평점', ' ', ' ', ' ']...]
            else:
                hotel[0].append(' ') # 이름
                hotel[1].append(' ') # 평점
                hotel[2].append(' ') # 위치
                hotel[3].append(' ') # 금액

        # 2-2. 항공기
        # flight 변수 형식
        # [['항공사', '숙소우선 가는 항공사이름', '숙소우선 오는 항공사이름' '항공기우선 가는 항공사이름', '항공기우선 오는 항공사이름' '렌트우선 가는 항공사이름', '렌트우선 오는 항공사이름']...]
        flight= [['항공사'], ['일자'], ['출발시간'], ['도착시간'], ['금액(원)']] # result.html 테이블 형식을 따름
        if value["flight_fir"] is not None:
            flight_total= f'{value["flight_fir"][-1]:,}'
        else:
            flight_total = " "
        for v in value2:
            if value[v] != None:
                  # 호텔우선 총합(천 단위 콤마 포맷)
                flight[0].extend([value[v][1][1],value[v][2][1]]) # 항공사
                flight[1].extend([value[v][1][0],value[v][2][0]]) # 일자
                flight[2].extend([value[v][1][2],value[v][2][2]]) # 출발시간
                flight[3].extend([value[v][1][3],value[v][2][3]]) # 도착시간
                flight[4].extend([f'{value[v][1][4]:,}',f'{value[v][2][4]:,}']) # 금액(천 단위 콤마 포맷)
            
            # [['항공사', ' ', ' ', ' '], ['일자', ' ', ' ', ' ']...]
            else:
                flight[0].extend([' ', ' ']) # 항공사
                flight[1].extend([' ', ' ']) # 일자
                flight[2].extend([' ', ' ']) # 출발시간
                flight[3].extend([' ', ' ']) # 도착시간
                flight[4].extend([' ', ' ']) # 금액

        # 2-3. 렌트
        # rent 변수 형식
        # [['이름', '숙소우선 렌트카 이름', '항공기우선 렌트카 이름', '렌트우선 렌트카 이름'], ['타입', '숙소우선 렌트카 타입', '항공기우선 렌트카 타입', '렌트우선 렌트카 타입']...]
        rent= [['이름'], ['타입'], ['일자'], ['인승'], ['금액(1일)']] # result.html 테이블 형식을 따름
        # 렌트카를 선택했다면
        if value['rent_fir'] != None:
            rent_total= f'{value["flight_fir"][-1]:,}' # 렌트우선 총합(천 단위 콤마 포맷)
            for v in value2:
                if value[v] != None:
                    rent[0].append(value[v][3][1])
                    rent[1].append(value[v][3][3])
                    rent[2].append(value[v][3][0])
                    rent[3].append(value[v][3][4])
                    print(value[v][2])
                    rent[4].append(f'{value[v][3][2]:,}')
                
                # [['이름', ' ', ' ', ' '], ['타입', ' ', ' ', ' ']...]
                else:
                    rent[0].append(' ')
                    rent[1].append(' ')
                    rent[2].append(' ')
                    rent[3].append(' ')
                    rent[4].append(' ')
        
        # 렌트카를 선택하지 않았다면
        # [['이름', ' ', ' ', ' '], ['타입', ' ', ' ', ' ']...]               
        else:
            rent_total= ' '
            rent[0].extend([' ', ' ', ' '])
            rent[1].extend([' ', ' ', ' '])
            rent[2].extend([' ', ' ', ' '])
            rent[3].extend([' ', ' ', ' '])
            rent[4].extend([' ', ' ', ' '])

        return render_template('result.html', hotel=hotel, rent=rent, flight=flight, hotel_total= hotel_total,
                               flight_total= flight_total, rent_total= rent_total)

if __name__ == '__main__':
    app.debug = True
    app.run()
