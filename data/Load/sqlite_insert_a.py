import sqlite3
import pandas as pd
import warnings

warnings.filterwarnings(action='ignore')

# 숙박 데이터 불러오기
accomadation = pd.read_csv('accomadation.csv')
# 숙소 정보 테이블: id, name, star, img, location, type

dup_name = accomadation[accomadation.name.duplicated()]
acc_info = accomadation.drop(dup_name.index, axis=0)
acc_info.reset_index(drop=True, inplace=True)
acc_info = acc_info[['name', 'star', 'img', 'location', 'type']]

# 예약 테이블에 id값을 넣기위한 dict 생성
acc_dict = {row[1]:row[0] for row in list(acc_info.itertuples(name=None))} # ex) 티티호텔: 1 (name: id)

# 데이터 입력을 위한 db연결
db = sqlite3.connect('./trip.db') # db생성
cursor = db.cursor() # 커서 생성

# 숙박 정보 테이블 입력
for row in list(acc_info.itertuples(name=None)):
    cursor.execute(
        '''
        INSERT INTO ACCOMADATION VALUES (?,?,?,?,?,?);
        ''', row
    )

# 숙박 예약 테이블 입력
# : date, id, price, link
acc_id = [acc_dict[row] for row in accomadation.name]
accomadation['id'] = acc_id # id 컬럼 생성
accomadation = accomadation[['date', 'id', 'lowest_price', 'link']]

for row in list(accomadation.itertuples(index=False, name=None)):
    cursor.execute(
        '''
        INSERT INTO A_BOOK VALUES (?,?,?,?);
        ''', row
    )
    
# 커밋, 연결해제
db.commit()
cursor.close()
db.close()