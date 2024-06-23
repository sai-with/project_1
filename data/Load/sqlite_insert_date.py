import sqlite3
import warnings

warnings.filterwarnings(action='ignore')

holidays = [5,6,12,13,15,19,20,26,27]
# 공휴일인날
is_holidays = ['1' if i in holidays else '0' for i in range(1, 31)]
# 공휴일은 아니지만 다음 날이 공휴일인 날
is_near_holidays = ['1' if i+1 in holidays else '0' for i in range(1, 31)]

date = [f"2023-08-{i}" if i >=10 else f"2023-08-0{i}" for i in range (1, 31)]     

# db 연결
db = sqlite3.connect('./trip.db')
cursor = db.cursor()
cursor.execute(
    '''
    DELETE FROM DATE;
    '''
)
for i in range(0, 30):
    cursor.execute(
        '''
        INSERT INTO DATE VALUES (?,?,?);
        ''', (date[i], is_holidays[i], is_near_holidays[i])
    )  
    
# db 연결해제
db.commit()
cursor.close()
db.close()