import xlrd
from pyecharts import options as opts
from pyecharts.charts import Scatter  # 导入散点图绘制模块
from pyecharts.charts import Line  # 导入折线图绘制模块
# pyecharts需要联网才能网页文件中显示图表，如果调用js代码中加入一些不符合js语法的代码不会报错，但不会显示图表

excel_file = xlrd.open_workbook('./result.xls')
table = excel_file.sheets()[0]

years = []
languages = []
values = [[] for k in range(25)]  # 多少种编程语言内部就预留多少个数组25
for j in range(219):
    cell_value = table.cell(0, j+1).value
    years.append(cell_value)
print(years)
for i in range(25):
    cell_value = table.cell(i+1, 0).value
    languages.append(cell_value)
print(languages)
for i in range(25):  # 编程语言的数量26
    for j in range(219):  # 年份的数量219
        t = table.cell(i+1, j+1).value
        if t == "" :
            cell_value = 0
        else:
            cell_value = float(t)
        # cell_value = table.cell(i+1, j+1).value
        values[i].append(cell_value)
    print(values[i])

# 使用scatter散点图可视化  可以显示每年每季度的点，但十分密集不便于观察
# 有的方法因为横坐标是字符串不能使用，暂时只能采取下面这种格式，不能利用循环（也许）对不同语言进行颜色分类
scatter1 = (
    Scatter()
    .add_xaxis(years)
    .add_yaxis(languages[0], values[0])
    .add_yaxis(languages[1], values[1])
    .add_yaxis(languages[2], values[2])
    .add_yaxis(languages[3], values[3])
    .add_yaxis(languages[4], values[4])
    .add_yaxis(languages[5], values[5])
    .add_yaxis(languages[6], values[6])
    .add_yaxis(languages[7], values[7])
    .add_yaxis(languages[8], values[8])
    .add_yaxis(languages[9], values[9])
    .add_yaxis(languages[10], values[10])
    .add_yaxis(languages[11], values[11])
    .add_yaxis(languages[12], values[12])
    .add_yaxis(languages[13], values[13])
    .add_yaxis(languages[14], values[14])
    .add_yaxis(languages[15], values[15])
    .add_yaxis(languages[16], values[16])
    .add_yaxis(languages[17], values[17])
    .add_yaxis(languages[18], values[18])
    .add_yaxis(languages[19], values[19])
    .add_yaxis(languages[20], values[20])
    .add_yaxis(languages[21], values[21])
    .add_yaxis(languages[22], values[22])
    .add_yaxis(languages[23], values[23])
    .add_yaxis(languages[24], values[24])
    .set_global_opts(
        # title_opts=opts.TitleOpts(title='scatter'),
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),  # 显示x轴分割线
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True))  # 显示y轴分割线
    )
)
scatter1.render('./Visualization/scatter.html')

# 使用line折线图可视化，貌似不能显示完整的，只能每5年取一个点显示大致趋势
line1=(
    Line() # 生成line类型图表
    .add_xaxis(years)  # 添加x轴
    .add_yaxis(languages[0], values[0])
    .add_yaxis(languages[1], values[1])
    .add_yaxis(languages[2], values[2])
    .add_yaxis(languages[3], values[3])
    .add_yaxis(languages[4], values[4])
    .add_yaxis(languages[5], values[5])
    .add_yaxis(languages[6], values[6])
    .add_yaxis(languages[7], values[7])
    .add_yaxis(languages[8], values[8])
    .add_yaxis(languages[9], values[9])
    .add_yaxis(languages[10], values[10])
    .add_yaxis(languages[11], values[11])
    .add_yaxis(languages[12], values[12])
    .add_yaxis(languages[13], values[13])
    .add_yaxis(languages[14], values[14])
    .add_yaxis(languages[15], values[15])
    .add_yaxis(languages[16], values[16])
    .add_yaxis(languages[17], values[17])
    .add_yaxis(languages[18], values[18])
    .add_yaxis(languages[19], values[19])
    .add_yaxis(languages[20], values[20])
    .add_yaxis(languages[21], values[21])
    .add_yaxis(languages[22], values[22])
    .add_yaxis(languages[23], values[23])
    .add_yaxis(languages[24], values[24])
    .set_global_opts(
        # title_opts=opts.TitleOpts(title='line'),
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),  # 显示x轴分割线
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True))  # 显示y轴分割线
    )
)
line1.render('./Visualization/line.html')
