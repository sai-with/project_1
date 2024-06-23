import sqlite3
import pandas as pd

r_car = pd.read_csv('./r_car.csv')
r_book = pd.read_csv('./r_book.csv')

db = sqlite3.connect('./trip.db')
cursor = db.cursor()

# R_CAR 테이블에 데이터 입력
for row in list(r_car.itertuples(index=False, name=None)):
    cursor.execute(
        '''
        INSERT INTO R_CAR VALUES (?,?,?,?);
        ''', row
    )
    
# R_BOOK 테이블에 데이터 입력
for row in list(r_book.itertuples(index=False, name=None)):
    cursor.execute(
        '''
        INSERT INTO R_BOOK VALUES (?,?,?);
        ''', row
    )

# 커밋 후 연결 해제
db.commit()
cursor.close()
db.close()