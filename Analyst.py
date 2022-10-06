# pylint: disable=abstract-class-instantiated
# pylint: disable=C0116, disable=C0114
from operator import index
from unicodedata import numeric
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np


def cal_mean(data):
    mean = {}
    namelist = ["optimisum", "Innovativeness", "Discomfort", "Insecurity"]
    for i in namelist:
        mean[i] = []
    mean["optimisum"] = (data.iloc[:, 1:13].mean(axis=1, numeric_only=True))
    mean["Innovativeness"] = (
        data.iloc[:, 14:22].mean(axis=1, numeric_only=True))
    #print(data.iloc[:, 13:22])
    mean["Discomfort"] = (data.iloc[:, 23:35].mean(axis=1, numeric_only=True))
    #print(data.iloc[:, 22:35])
    mean["Insecurity"] = (data.iloc[:, 36:45].mean(axis=1, numeric_only=True))
    print(data.iloc[:, 35:46])
    return mean


def to_excel(df):
    writer = pd.ExcelWriter(
        'sample_data.xlsx', engine='openpyxl')  # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name='sample_data.xlsx', index=False)
    writer.save()


def plot(df):
    axes = plt.gca()
    axes.set_ylim([0, 10])
    plt.hist(df, bins=100, range=(0, 10))
    plt.xlabel('Avg score')
    plt.ylabel('ocurrence')
    plt.title('The distribution of the average score different student\n\n',
              fontweight="bold")
    plt.show()


def plot_distribution(data):
    axes = plt.gca()
    axes.set_ylim([0, 1.5])
    plt.hist(data, bins=100, range=(0, 10), density=True)
    [mean_fit, std_fit] = scipy.stats.norm.fit(data)
    print(mean_fit)
    print(std_fit)
    x = np.linspace(np.min(data), np.max(data))
    plt.plot(x, scipy.stats.norm.pdf(x, mean_fit, std_fit),)
    plt.xlabel("Avg score")
    plt.ylabel("probability density")
    plt.title('PDF\n\n',
              fontweight="bold")
    plt.show()


data = pd.read_csv(
    r'C:\Users\clarence\Desktop\vscode\python\HW1_data.csv')

mean = cal_mean(data)
df1 = pd.DataFrame(mean)
to_excel(df1)
plot(df1["Innovativeness"])
plot_distribution(df1["Innovativeness"])
