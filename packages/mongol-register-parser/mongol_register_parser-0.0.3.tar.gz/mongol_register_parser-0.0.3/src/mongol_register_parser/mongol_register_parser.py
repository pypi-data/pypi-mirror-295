
"""
Тайлбар:
-Уг parser нь 1930-с 1940 онд хүртэлх төрсөн хүмүүсийг Регистрийн дугаарыг бододгүй.
-Хэрэв буруу Регистрийн дугаар орж ирвэл 1700 оны 01 сарын 01 гэж хадгалдаг тул анхаарна уу.

Монгол регистрийн дугаарын эхний 2 орон буюу үсэг нь регистрийн дугаар авч байгаа иргэний байнга 
оршин суудаг аймаг /дүүрэг/, сум /хороо/-ны код, дараагийн 6 орон нь төрсөн он, сар, өдөр 9 дэх орон нь хүйс, 
сүүлийн нэг орон нь хяналтын код байна.

Регистрийн эхний 2 тоон орон нь тухайн иргэний төрсөн оны сүүлийн 2 тоог тэмдэглэдэг. 
Түүний дараагийн 2 орон төрсөн сарыг илэрхийлэх бөгөөд 2000 он болон түүнээс хойш төрсөн хүмүүсийн
хувьд төрсөн сар дээр нь 20-ийг нэмж тэмдэглэдэг. Харин дараагийн 2 орон төрсөн өдрийг илэрхийлнэ.

Регистрийн дугаарын сүүлээсээ 2 дахь тоо нь хүйсийг заах бөгөөд хэрвээ тус тоо сондгой бол хүйс нь эрэгтэй,
үгүй бол эмэгтэй гэж үзнэ. Харин хамгийн сүүлийн орон бол, тус регистрийн дугаарыг үнэн оруулсан эсэхийг шалгахад
ашиглагддаг тоо болно. Хэрхэн уг тоог ашиглан шалгаж болох талаар нээлттэй эх сурвалжуудад баттай мэдээлэл байхгүй ч,
энэхүү нийтлэлийн коммент хэсэгт уг тоо регистрийн дугаарт орж байгаа үсэг болон тоонуудын нийлбэрийг тодорхой нэг
тоонд хуваасны үлдэгдэлтэй тэнцэх ёстой гэх мэдээлэл байна.
"""


import pandas as pd
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np


newPandasDataFrame = pd.DataFrame()


#extract_birthday
def extract_birthday(birth):

    print('-----input:', birth)
    print('-----input birth year cut: ', birth[0:2])
    print('-----input birth month cut: ', birth[3:5])
    print('-----input birth day cut: ', birth[4:6])
    birthYear = int(birth[0:2])
    birthMonth = int(birth[2:4])
    birthDay = int(birth[4:6])
    # gender = int(birth[6:])
    if (birthMonth==2 and birthDay>29) or (birthMonth == 4 and birthDay>30) or (birthMonth == 6 and birthDay>30) or (birthMonth == 9 and birthDay>30) or (birthMonth == 11 and birthDay>30):
        print('wrong datetime 1')
        birthYear = 1700
        birthMonth = 1
        birthDay = 1
    elif (birthYear)>40 and birthMonth<13 and birthDay<32:
        birthYear = 1900 + birthYear
        birthMonth = birthMonth
        birthDay = birthDay
    elif (birthYear)<30 and(birthYear)<25 and birthMonth<13 and birthDay<32:
        birthYear = 2000 + birthYear
        birthMonth = abs(birthMonth - 20)
        birthDay = birthDay
        # gender = gender
        # print("genzGender: ", gender)
    else:
        print('wrong datetime 2 - else')
        birthYear = 1700
        birthMonth = 1
        birthDay = 1

    print("birthYear: ", birthYear)
    print("birthMonth: ", birthMonth)
    print("birthDay: ", birthDay)
    
    #month date fixer
    if birthMonth>12 or birthMonth<1:
        birthMonth=1
    if birthDay>31 or birthDay<1:
        birthDay=1
        
    #birthdate calculator
    birthYear = str(birthYear)
    birthMonth = str(birthMonth)
    birthDay = str(birthDay)
    date_str  = birthYear + "-" + birthMonth + "-" + birthDay
    print("--birth_date: ", date_str)
    date_format = '%Y-%m-%d'
    date_obj = datetime.strptime(date_str, date_format)
    print(date_obj)
    now = date.today()
    print(now)
    age = relativedelta(now, date_obj).years
        
    return age, birthYear, birthMonth, birthDay


#looper
def looper(data_frame, register_number_column):
    df = data_frame

    for index, row in df.iterrows():
        print('\n\nreg_number: ', "[",df[register_number_column][index],"]", "\nindex: ", index)
        text = df.loc[index, 'reg_number_cut']
        text = str(text)
        text = text.replace(" ", "")
        birth = text[:7]
        
        if len(birth)<6:
            birth="3211111"

        print('birth: ', birth, len(birth))
        age, birthYear, birthMonth, birthDay = extract_birthday(birth)
        
        df.loc[index, 'age'] = age
        df.loc[index, 'birthYear'] = birthYear
        df.loc[index, 'birthMonth'] = birthMonth
        df.loc[index, 'birthDay'] = birthDay
        print('age: ', df.loc[index, 'age'])
        
    newPandasDataFrame = df

    return newPandasDataFrame 
    

#mongol_register_parser
def mongol_register_parser(fileName, register_number_column):
    # register number fixer


    df = pd.read_csv(fileName) #, low_memory=False


    #cut 500 samples for test
    df = df.sample(n=min(50, len(df)), replace=True, random_state=42)
    # #to csv
    # df.to_csv('fiveHundred.csv', index=False)


    print('\n-----', fileName, len(df))
    df.head(3)

    # Fill the empty rows in register_number_column column with 'aa33333333'
    df[register_number_column] = df[register_number_column].fillna('aa3311111').replace('', 'aa3311111')


    empty_rows = df[df[register_number_column].isna() | (df[register_number_column] == '')]
    # Optionally display the rows with empty register_number_column column
    print('empty rows:  ', len(empty_rows))

    #change dtype
    df.reg_number_cut = df[register_number_column].astype('string')

    df['reg_number_cut'] = df[register_number_column].str[2:9]
    data_frame = df

    newPandasDataFrame = looper(data_frame, register_number_column)

    print(newPandasDataFrame)
    print("\nDone--------------------------")
    
    return newPandasDataFrame


# test result:
# fileName='first_merged_result.csv'
# register_number_column = "reg_number"
# newPandasDataFrame = mongol_register_parser(fileName, register_number_column)
