import sqlite3

db = sqlite3.connect('./trip.db') # db생성
cursor = db.cursor() # 커서 생성

# 이미 테이블이 있다면 삭제 후 진행
cursor.execute('DROP TABLE IF EXISTS DATE;')
cursor.execute('DROP TABLE IF EXISTS ACCOMADATION;')
cursor.execute('DROP TABLE IF EXISTS FLIGHT;')
cursor.execute('DROP TABLE IF EXISTS R_CAR;')
cursor.execute('DROP TABLE IF EXISTS A_BOOK;')
cursor.execute('DROP TABLE IF EXISTS F_BOOK;')
cursor.execute('DROP TABLE IF EXISTS R_BOOK;')



# 테이블 생성
cursor.execute(
    '''
    CREATE TABLE DATE(
        date VARCHAR(10) NOT NULL,
        is_holiday VARCHAR(2) NOT NULL,
        is_near_holiday VARCHAR(2) NOT NULL,
        PRIMARY KEY(date)); 
    '''
) # sqlite에는 날짜 데이터 타입이 없음...
# ACCOMADATION
cursor.execute(
    '''
    CREATE TABLE ACCOMADATION(
        id VARCHAR(20) NOT NULL,
        name VARCHAR(30) NOT NULL,
        star REAL,
        img VARCHAR(150),
        location VARCHAR(10),
        type VARCHAR(5),
        PRIMARY KEY(id)
    );
    '''
) # sqlite에서의 float type => real, 별점 데이터 -1(평점없음)은 null값으로 입력할 것.
# FLIGHT
cursor.execute(
    '''
    CREATE TABLE FLIGHT(
        id VARCHAR(20) NOT NULL,
        name VARCHAR(10) NOT NULL,
        PRIMARY KEY(id)
    );
    '''
)
# R_CAR
cursor.execute(
    '''
    CREATE TABLE R_CAR(
        id VARCHAR(20) NOT NULL,
        name VARCHAR(30) NOT NULL,
        type VARCHAR(10),
        capacity INTEGER,
        PRIMARY KEY(id)
    );
    '''
)
# A_BOOK
cursor.execute(
    '''
    CREATE TABLE A_BOOK(
        book_date VARCHAR(10) NOT NULL,
        accom_id VARCHAR(20) NOT NULL,
        price INTEGER,
        link VARCHAR(150),
        FOREIGN KEY(book_date) REFERENCES DATE(date),
        FOREIGN KEY(accom_id) REFERENCES ACCOMADATION(id)
    );
    '''
)
# F_BOOK
cursor.execute(
    '''
    CREATE TABLE F_BOOK(
        book_date VARCHAR(10) NOT NULL,
        flight_id VARCHAR(20) NOT NULL,
        dep_time VARCHAR(10) NOT NULL,
        arr_time VARCHAR(10) NOT NULL,
        price INTEGER,
        direction VARCHAR(5),
        FOREIGN KEY(book_date) REFERENCES DATE(date),
        FOREIGN KEY(flight_id) REFERENCES FLIGHT(id)
    );
    ''')
# R_BOOK
cursor.execute(
    '''
    CREATE TABLE R_BOOK(
        book_date VARCHAR(10) NOT NULL,
        rent_id VARCHAR(20) NOT NULL,
        saled_price INTEGER,
        FOREIGN KEY(book_date) REFERENCES DATE(date),
        FOREIGN KEY(rent_id) REFERENCES R_CAR(id)
    );
    ''')

db.commit()
cursor.close()
db.close()