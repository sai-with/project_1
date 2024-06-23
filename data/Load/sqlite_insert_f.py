import pandas as pd
import sqlite3


f_book = pd.read_csv('./FBOOK.csv')
flight = pd.read_csv('./flight.csv')

# FLIGHT 테이블에 적재
db = sqlite3.connect('./trip.db')
cursor = db.cursor()
for row in list(flight.itertuples(index=False, name=None)):
    cursor.execute(
        '''
        INSERT INTO FLIGHT VALUES (?,?)
        ''', row
    )

for row in list(f_book.itertuples(index=False, name=None)):
    cursor.execute(
        '''
        INSERT INTO F_BOOK VALUES (?,?,?,?,?,?)
        ''', row
    )
    
db.commit()
cursor.close()
db.close()