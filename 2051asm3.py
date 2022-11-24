import pandas as pd
import numpy as np
import array
import sys


def Q1(data):
    cnt = [0, 0, 0]
    for i in data["ACT"]:
        if (i == 6):
            cnt[0] = cnt[0]+1
        elif (i == 7):
            cnt[1] = cnt[1]+1
        elif (i == 8):
            cnt[2] = cnt[2]+1
    print(cnt)
    return cnt


def Q1_rate(cnt):
    rate = [0, 0, 0]
    for i in range(2):
        rate[i] = ((cnt[i]-cnt[i+1])/cnt[i])*100
    rate[2] = ((cnt[0]-cnt[2])/cnt[0])*100
    print(rate)
    return rate


def switch(a, b):
    tmp = a
    a = b
    b = tmp
    return a, b


def to_excel(df):
    writer = pd.ExcelWriter(
        'data.xlsx', engine='openpyxl')  # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name='data.xlsx', index=False)
    writer.save()


def clear():
    my_file = open("text.txt", "w")
    my_file.write("")
    my_file.close()


def Q2(data, act):
    clear()
    rows, cols = (100, 100)
    arr = [[0]*cols for _ in range(rows)]
    i = 0
    for j, k in zip(data["MYID"], data["FRDID"]):
        if (data["ACT"][i] == act):
            if (j > k):
                j, k = switch(j, k)
            arr[j][k] += 1
            my_file = open("text.txt", "a")
            my_file.write("The number of connections made is "+str(i)+"  ")
            my_file.write("The count of each node "+str(arr[j][k])+"\n")
            my_file.close()
        else:
            break
        i = i+1
    df = pd.DataFrame(arr)
    to_excel(df)


def compare(a, b):
    cnt = 0
    total = 6
    for i in range(2, 8):
        if (a[i] == b[i]):
            cnt += 1
        elif (isnan(a[i])):
            total -= 1
    percent = (cnt/total)*100
    print(percent)


def isnan(value):
    try:
        import math
        return math.isnan(float(value))
    except:
        return False


def Q3(data):
    i = 0
    a = 0
    simple = []
    list = [[]*6]*10
    for j, k in zip(data["sid"], data["fid"]):
        if (j == k):
            simple = data.loc[i, :]
        if (k == 50):
            if (j != 50):
                list[a] = data.loc[i, :]
                a += 1
        i += 1
    print(list[3])
    for i in range(a):
        print(i)
        compare(simple, list[i])


def Q3_cnt_empty(data):
    arr = [0]*6
    arr[0] = data['year_f'].isna().sum()
    arr[1] = data['birthmonth_f'].isna().sum()
    arr[2] = data['birthdate_f'].isna().sum()
    arr[3] = data['college_f'].isna().sum()
    arr[4] = data['favcolor_f'].isna().sum()
    arr[5] = data['favnumber_f'].isna().sum()
    total = sum(arr)
    percentage = total/(6*114)*100
    print(percentage)


data = pd.read_csv(
    r'C:\Users\clarence\Desktop\vscode\hw3_data_2051B.csv')

id_list = {}
name = ["MYID", "FRDID", "ACT"]
for i in name:
    id_list[i] = []
id_list["MYID"] = data["sid"]
id_list["FRDID"] = data["fid"]
id_list["ACT"] = data["act"]

#cnt = Q1(id_list)
# Q1_rate(cnt)
Q2(id_list, 6)
# Q3(data)
# Q3_cnt_empty(data)
