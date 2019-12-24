import matplotlib.pyplot as plt
import csv

with open('1.csv')as f:
    f_csv = csv.reader(f)
    for csvrow in f_csv:
        title=csvrow[0]
        x=[]
        y=[]
        csvrow=csvrow[1:]
        for i in range(len(csvrow)):
            if i%2==0:
                x.append(csvrow[i])
            else:
                csvrow[i]=float(csvrow[i])
                y.append(csvrow[i])

        # 清除当前轴域
        plt.cla()
        # 绘制水平柱状图
        plt.title(title,fontsize=15)
        plt.bar(x, y, facecolor = 'lightskyblue',edgecolor = 'white')
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        for x, y in zip(x, y):  # zip是将X，Y1分别传到x,y中，传两个
            plt.text(x, y + 0.05, '%.2f' % y,fontsize=15, ha='center', va='bottom')  # ha,va规定坐标表示的点，默认左下
        plt.pause(0.05)
    plt.show()