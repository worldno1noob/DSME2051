from networkx.algorithms import community
import pandas as pd
import numpy as np
import array
import sys
import matplotlib.pyplot as plt
import networkx as nx


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


def Q2(data):
    clear()
    rows, cols = (100, 100)
    arr = [[0]*cols for _ in range(rows)]
    i = 0
    for j, k in zip(data["MYID"], data["FRDID"]):
        if (j > k):
            j, k = switch(j, k)
        arr[j][k] += 1
        my_file = open("text.txt", "a")
        my_file.write("There are "+str(i+1)+" connection(s) made\n")
        my_file.write("The connection is between " +
                      str(j)+" and "+str(k)+"\n")
        my_file.write("The count of this node "+str(arr[j][k])+"\n\n")
        my_file.close()
        i = i+1
    df = pd.DataFrame(arr)
    to_excel(df)
    return arr


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
    for i in range(a):
        # print(i)
        compare(simple, list[i])


def Q3_cnt_empty(data):
    arr = [0]*6
    #arr[0] = data['year_f'].isna().sum()
    arr[1] = data['birthmonth_f'].isna().sum()
    arr[2] = data['birthdate_f'].isna().sum()
    arr[3] = data['college_f'].isna().sum()
    arr[4] = data['favcolor_f'].isna().sum()
    arr[5] = data['favnumber_f'].isna().sum()
    total = sum(arr)
    print(arr)
    percentage = total/(5*114)*100
    print(percentage)


def Q4_plt(df):
    G = nx.from_pandas_edgelist(
        df, source='sid', target='fid', create_using=nx.DiGraph())
    plt.subplots(figsize=(20, 20))
    plt.title('Friendship, DSME2051 Students\' network')
    nx.draw_kamada_kawai(G, with_labels=True)
    return G
    # plt.show()


def Q4_degree(G):
    degree_centrality = nx.algorithms.centrality.degree_centrality(G)
    for i, w in enumerate(sorted(degree_centrality, key=degree_centrality.get, reverse=True)):
        if (i < 10):
            print(w, degree_centrality[w])
        else:
            break
    plt.subplots(figsize=(20, 20))
    plt.title('The the degree centrality, DSME2051 Students\' network')
    nx.draw_kamada_kawai(G, with_labels=True, node_size=list(
        np.array(list(degree_centrality.values()))*500))
    # plt.show()


def Q4_betweenness(G):
    btw_centrality = nx.algorithms.centrality.betweenness_centrality(G)
    for i, w in enumerate(sorted(btw_centrality.items(), key=lambda item: item[1], reverse=True)):
        if (i < 10):
            print(w)
        else:
            break
    plt.subplots(figsize=(20, 20))
    plt.title('The the betweenness centrality, DSME2051 Students\' network')
    nx.draw_kamada_kawai(G, with_labels=True, node_size=list(
        np.array(list(btw_centrality.values()))*5000))
    # plt.show()


def Q4_page_rank(G):
    ev_centrality = nx.algorithms.centrality.eigenvector_centrality(G)
    for i, w in enumerate(sorted(ev_centrality.items(), key=lambda item: item[1], reverse=True)):
        if (i < 10):
            print(w)
        else:
            break
    plt.subplots(figsize=(20, 20))
    plt.title('The the page rank centrality, DSME2051 Students\' network')
    nx.draw_kamada_kawai(G, with_labels=True, node_size=list(
        np.array(list(ev_centrality.values()))*2500))
    # plt.show()


def Q5_graph_community(G):
    plt.figure(figsize=(10, 10))
    pos_spring = nx.spring_layout(G)
    pos_circular = nx.circular_layout(G)
    plt.title('The clustered network, DSME2051 Students\' network')
    nx.draw(G, pos=pos_spring, with_labels=True, font_weight='bold')
    plt.show()

    community1 = nx.algorithms.community.girvan_newman(G)
    community2 = nx.algorithms.community.greedy_modularity_communities(G)
    print(*community1)
    print(community2)


def Q5_cluster_coe(df):
    G_undir = nx.from_pandas_edgelist(df, source='sid', target='fid')
    a = nx.algorithms.cluster.average_clustering(G_undir)
    print(a)


data = pd.read_csv(
    r'C:\Users\clarence\Desktop\vscode\hw3_data_2051B.csv')

id_list = {}
name = ["MYID", "FRDID", "ACT"]
for i in name:
    id_list[i] = []
id_list["MYID"] = data["sid"]
id_list["FRDID"] = data["fid"]
id_list["ACT"] = data["act"]
df1 = data.loc[(data.sid < 60) & (data.fid < 60)]
df1.head()

df2 = data.loc[(data.sid < 99) & (data.fid < 99)]
df2.head()

df3 = data.loc[(data.sid < 115) & (data.fid < 115)]
df3.head()

# here is the code about each question erase the # to excute 

#cnt = Q1(id_list)
# Q1_rate(cnt)

# Q2(id_list)

# arr=Q3(data)
# Q3_cnt_empty(data)

#G1 = Q4_plt(df1)
# Q4_betweenness(G1)
# print("\n")
#G2 = Q4_plt(df2)
# Q4_betweenness(G2)
# print("\n")
xG3 = Q4_plt(df3)
# Q4_betweenness(G3)
# print("\n")
# print(community2)
# Q4_betweenness(G)
# Q4_page_rank(G)
# plt.show()
Q5_graph_community(G3)
# Q5_cluster_coe(df3)
