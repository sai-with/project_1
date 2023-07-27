# 아직 코드 디버깅 중입니다
class Query:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
    def accom(self, dep_date, arr_date, star, budget):
        # if budget < 0:
        #     return None, -1
        
        total_price = budget # 남은 예산
        days = int(arr_date[-2:]) - int(dep_date[-2:]) # 몇박 인지
        
        if int(arr_date[-2:]) < 10:
            accom_out = f"2023-08-0{int(arr_date[-2:])-1}"
        else:
            accom_out = f"2023-08-{int(arr_date[-2:])-1}" # 마지막 입실 날짜
        self.cursor.execute(
            f'''
                SELECT COUNT(*) days, name, star, location, type, sum(price) total_price, img, link
                FROM (
                    SELECT * FROM ACCOMADATION
                    WHERE star >= {star}
                    ) a
                JOIN A_BOOK ab
                ON a.id = ab.accom_id
                WHERE  DATE(book_date) BETWEEN  DATE({dep_date}) AND DATE('2023-08-{accom_out}')
                GROUP BY name
                HAVING days = {days}
                AND total_price <= {budget}
                ORDER BY price, star DESC
                LIMIT 1;
                '''
        )
         
        if self.cursor.fetchone() is not None and\
            total_price >= 0: # 결과값이 있고, 예산 안에서 해결된 경우
            total_price -= self.cursor.fetchone()[5] # 남은 예산 
            return [self.cursor.fetchone()], total_price # [(accom)] 리스트 안에 들어간 형태로 반환
        else:
            return None, -1
        
    def flight_low(self, dep_date, arr_date, budget):
            #print(f"dep_date: {dep_date}\narr_date:{arr_date}\nbudget: {(budget)}")
            date = [dep_date, arr_date]
            query = ['dep_time', 'price']# 가는 건 시간 기준, 오는 건 가격 기준 조회
            direction = ['go', 'back'] # 가는 편/오는 편
            total_price = budget # 남은금액 계산용
            result = []
            # 김포-부산
            for i in range(0,2):
                print(i)
                self.cursor.execute(
                    f'''
                    SELECT book_date, name, dep_time, arr_time, price FROM F_BOOK fb 
                    JOIN FLIGHT f 
                    ON f.id = fb.flight_id
                    WHERE DATE(book_date) = DATE('{date[i]}')
                    AND direction = '{direction[i]}'
                    ORDER BY {query[i]} 
                    LIMIT 1;
                    '''
                )
                # print(date[i], direction[i], query[i])
                fetch = self.cursor.fetchone()
                if fetch is not None:
                    total_price -= fetch[-1] # 예산에서 항공 요금 빼기
                    result.append(fetch) # 튜플형태로 저장
                else:
                    return None, -1
            print(f"flight: {result}, extra: {total_price}")
            return result, total_price # 예산 계산해서 반환 [(go), (back)], extra_bud: 남은 예산
     
    def flight_time(self, dep_date, arr_date, budget):
        total_price = budget # 남은 금액
        
        # 양방향 for문으로
        date = [dep_date, arr_date] 
        direction = ['go', 'back']
        result = []
        
        for i in [0, 1]:
            self.cursor.execute(
                f'''
                SELECT book_date, name, dep_time, arr_time, price FROM F_BOOK fb 
                JOIN FLIGHT f 
                ON f.id = fb.flight_id
                WHERE book_date = {date[i]}
                AND direction = '{direction[i]}'
                AND TIME(dep_time) BETWEEN TIME('13:00') AND TIME('14:00')
                ORDER BY TIME(dep_time) DESC
                LIMIT 1;
                '''
            )
            if self.cursor.fetchone() is None or total_price < 0: # 결과값이 없거나 예산이 모자란 경우
                return None, -1
            else:
                total_price -= self.cursor.fetchone()[-1]
                result.append(self.cursor.fetchone())        
            
        return result, total_price
        
    def rent_low(self, arr_date, dep_date, budget, capacity):
        
        # if budget < 0: # 연산이 의미없으면
        #     return None, -1
        days = int(arr_date[-2:]) - int(dep_date[-2:]) # 몇박 인지
        total_price = budget
        self.cursor.execute(
                f'''
                SELECT * FROM R_BOOK rb
                JOIN R_CAR rc
                ON rb.rent_id = rc.id
                WHERE capacity = {capacity} 
                AND DATE(book_date) = DATE({dep_date})
                ORDER BY saled_price
                LIMIT 1;
                '''
            )
        result = self.cursor.fetchone()
        if result is None:
            return None, -1
        else:
            total_price -= (result[-1] * days) # 총 여행기간동안의 비용 차감
            return [result], total_price   
    
    def rent_type(self, arr_date, dep_date, budget, capacity):
        # if budget < 0: # 연산이 의미없으면
        #     return None, -1
        days = int(arr_date[-2:]) - int(dep_date[-2:]) # 몇박 인지
        total_price = budget
        self.cursor.execute(
                f'''
                SELECT * FROM R_BOOK rb
                JOIN R_CAR rc
                ON rb.rent_id = rc.id
                WHERE capacity = {capacity} 
                AND DATE(book_date) = DATE({dep_date})
                AND type = '디젤'
                ORDER BY saled_price
                LIMIT 1;
                '''
            )
        result = self.cursor.fetchone()
        if result is None:
            return None, -1
        else:
            total_price -= (result[-1] * days)
            if total_price > 0:
                return [result], total_price
            else:
                None, -1


class Recommand():
    def __init__(self, dep_date, arr_date, budget, car_capacity, conn):
        # 클래스 변수 할당
        self.dep_date = dep_date # 출발날짜
        self.arr_date = arr_date # 도착날짜
        self.car_capacity = car_capacity # 렌트 수용인원
        self.budget = budget # 예산
        # db연결, 커서 생성
        self.conn = conn
        self.cursor = self.conn.cursor()
        
    def recommander(self):
        _query = Query(self.conn, self.cursor)
        def case1(dep_date, arr_date, budget): # 렌트 안하는 경우
            result = {} # 두 경우의 수를 담을 딕셔너리
            
            ## 숙소 우선
            flight1, extra1 = _query.flight_low(dep_date, arr_date, budget)
            accom1, bud = _query.accom(dep_date, arr_date, 8, extra1) # 숙소 우선이기 때문에 별점 기준 8, 남은 예산 전달

            if None in [accom1 ,flight1] or bud < 0:# 예산이 모자랐거나, 조회된 데이터(예약가능한)가 없을 경우
                result['accom_fir'] = None 
            else: # 제대로 조회된경우 
                result['accom_fir'] = accom1 + flight1 # 숙소 우선 계획[(숙소), (가는편), (오는편)] 
            ## 항공 우선
            flight2, extra2 = _query.flight_time(dep_date, arr_date, budget)
            accom2, _ = _query.accom(dep_date, arr_date, 7, extra2) # 숙소 차선이기 때문에 별점 기준 7, 남은 예산 전달
            if None in [accom2, flight2] or bud < 0: 
                result['flight_fir'] = None 
            else:
                result['flight_fir'] = accom2 + flight2 # 항공 우선 계획[(숙소), (가는편), (오는편)]
            
            # 연결 해제
            self.cursor.close()
            self.conn.close()
            
            return result #{숙소 우선: 결과, 항공 우선:결과} 형태로 반환 | 결과는 list of tuples
            # 예)
        
        def case2(dep_date, arr_date, budget, car_capacity):
            result = {} # 세 경우의 수를 담을 딕셔너리
            ## 숙소 우선
            flight1, extra1 = _query.flight_low(dep_date, arr_date, budget)
            print(f"flight: {flight1}\nextra1: {extra1}")
            rent1, extra1_1 = _query.rent_low(dep_date, arr_date, extra1, car_capacity)
            print(f"rent1: {rent1}\nextra1_1: {extra1_1}")
            accom1, bud1 = _query.accom(dep_date, arr_date, 8, extra1_1) # 숙소 우선이기 때문에 별점 기준 8, 남은 예산 전달
            print(f"accom1: {accom1}\nbud1: {bud1}")
            
            if None in [accom1, flight1, rent1] or bud1 < 0:# 예산이 모자랐거나, 조회된 데이터(예약가능한)가 없을 경우
                result['accom_fir'] = None 
            else: # 제대로 조회된경우 
                result['accom_fir'] = accom1 + flight1 + rent1 # 숙소 우선 계획[(숙소), (가는편), (오는편)] 
            
            ## 항공 우선
            flight2, extra2 = _query.flight_time(dep_date, arr_date, budget)
            rent2, extra2_1 = _query.rent_low(dep_date, arr_date, extra2, car_capacity)
            accom2, bud2 = _query.accom(dep_date, arr_date, 7, extra2_1) # 숙소 차선이기 때문에 별점 기준 7, 남은 예산 전달
            if None in [accom2, flight2, rent2] or bud2 < 0: 
                result['flight_fir'] = None 
            else:
                result['flight_fir'] = accom2 + flight2 + rent2 # 항공 우선 계획[(숙소), (가는편), (오는편)]

            ## 렌트 우선
            flight3, extra3 = _query.flight_low(dep_date, arr_date, budget)
            rent3, extra3_1 = _query.rent_type(dep_date, arr_date, extra3, car_capacity)
            accom3, bud3 = _query.accom(dep_date, arr_date, 7, extra3_1) 
            if None in [accom3, flight3, rent3] or bud3 < 0: 
                result['rent_fir'] = None
            else:
                result['rent_fir'] = accom3 + flight3 + rent3
            # 연결 해제
            self.cursor.close()
            self.conn.close()
            return result
        
        if self.car_capacity == 0:
            return case1(self.dep_date, self.arr_date, self.budget)
        else:
            return case2(self.dep_date, self.arr_date, self.budget, self.car_capacity)
         

