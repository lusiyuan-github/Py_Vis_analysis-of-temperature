'''
班级：信息sy1901
姓名：卢思远
学号：0121909360418
完成日期：12月6日 最终版
获取数据网站： https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data（GlobalLandTemperaturesByCountry.csv和ChinaTemperatures.csv）
            http://www.stats.gov.cn/tjsj/ndsj/
            https://www.aqistudy.cn/historydata/（城市.XLSX）
'''
from pyecharts.charts import *
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import random
import pandas as pd
from matplotlib.pyplot import *
import pyecharts.options as opts
import matplotlib.pyplot as plt
import xlrd


# 随机获取颜色
def randomcolor(kind):
    colors = []
    for i in range(kind):
        colArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        color = ""
        for i in range(6):
            color += colArr[random.randint(0, 14)]
        colors.append("#" + color)
    return colors


# 预定义和文件读取
all_country = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
China_date = pd.read_csv('ChinaTemperatures.csv')
name = list(pd.read_excel('城市.XLSX')['城市'].drop_duplicates())

# 分析各个城市污染API
data = xlrd.open_workbook('城市.XLSX')
table = data.sheets()[0]
dic1 = {k: [] for k in name}
for i in range(1, table.nrows):
    x = table.row_values(i)
    dic1[x[0]].append((x[1], x[2], x[5], x[6], x[7], x[8], x[9], x[10]))  # 城市作为键，日期和AQI作为值
lisx = list(range(0, 85))
lisy = []
lisdate = []
# plt.figure(figsize=(25,10),dpi=100)
for i in range(2013, 2021):
    lisdate.append('{}'.format(i))
color_series = randomcolor(8)
color_number = 0
for j in name:
    for i in lisx:
        lisy.append(dic1[j][i][1])
    plt.plot(lisx, lisy, color=color_series[color_number], label=j)
    lisy = []  # 清空为下次作图
    color_number = color_number + 1  # 变换随机颜色

plt.xticks(list(range(0, 85, 12)), lisdate, rotation=50)
plt.title("AQI污染指数", fontproperties='simHei')
plt.xlabel("年份", fontproperties='simHei')
plt.ylabel("AQI值", fontproperties='simHei')
plt.grid(alpha=0.4)
plt.legend(prop="simHei", loc='upper right')
plt.savefig('./AQI污染值数城市对比.png')
print('AQI污染值数城市对比已生成')
# plt.show()
plt.close()

color_number = 0
name_lable = ['PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3']
for j in range(2, 8):
    for i in lisx:
        lisy.append(dic1["武汉"][i][j])
    plt.plot(lisx, lisy, color=color_series[color_number], label=name_lable[j-2])
    lisy = []  # 清空为下次作图
    color_number = color_number + 1  # 变换随机颜色
plt.xticks(list(range(0, 85, 12)), lisdate, rotation=50)
plt.title("武汉污染物指标", fontproperties='simHei')
plt.xlabel("年份", fontproperties='simHei')
plt.ylabel("浓度", fontproperties='simHei')
plt.grid(alpha=0.4)
plt.legend(prop="simHei", loc='upper right')
plt.savefig('./武汉污染物指标.png')
print('武汉污染物指标已生成')
# plt.show()
plt.close()
#处理数据
cou_tem = all_country.groupby("Country")['AverageTemperature'].mean()  # 国家和温度平均值打包
cou_tem = cou_tem.dropna()  # 删除缺省
country = list(cou_tem.index)  # 将国家转化列表
temperature = list(cou_tem.values)  # 将温度转化列表
zip_country_temperature1 = zip(country, temperature)  # 打包成元组好排序
zip_country_temperature2 = zip(country, temperature)
top_ten_country = sorted(zip_country_temperature1, key=lambda tup: tup[1], reverse=True)[0:10]  # 打包成元组好排序,取最高温前十个
low_ten_country = sorted(zip_country_temperature2, key=lambda tup: tup[1], reverse=False)[0:5]  # 打包成元组好排序,取最高温前十个
# print(low_ten_country)

# 绘制温度地图
map = Map()
map.add("国家", [list(i) for i in zip(country, temperature)], 'world')
map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
map.set_global_opts(
    title_opts=opts.TitleOpts(title="全球温度图表"),
    visualmap_opts=opts.VisualMapOpts(max_=30, min_=-10)  # 最高温不超过30，设置为30
)
# map.render('全球温度地图.html')
print("全球温度地图已生成！！")

# 绘制最高温度前十位国家的平均温度情况（条形图）
# print(top_ten_country)
country = [x[0] for x in top_ten_country]  # 前十个国家
temperature = [x[1] for x in top_ten_country]  # 前十个国家对应温度

x = []  # 空列表存温度
color_series = randomcolor(len(country))
for i in range(10):
    x.append(
        opts.BarItem(
            name=country[i],
            value=round(temperature[i], 2),
            itemstyle_opts=opts.ItemStyleOpts(color=color_series[i])  # 设置每根柱子的颜色
        )
    )
    # 绘制柱形图
bar = Bar()
bar.add_xaxis(country)
bar.add_yaxis(
    series_name='温度',
    y_axis=x,
    is_selected=True,
    label_opts=opts.LabelOpts(is_show=True))
bar.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='right'))
bar.set_global_opts(
    title_opts=opts.TitleOpts(title="排行榜前十名温度最高国家"),
    tooltip_opts=opts.TooltipOpts(
        is_show=True,
        trigger="axis",
        axis_pointer_type="shadow"),

    xaxis_opts=opts.AxisOpts(name='温度'),
    yaxis_opts=opts.AxisOpts(name='国家'),
)
bar.reversal_axis()  # 转换为条形图，不然国家无法完全显示
# bar.render("平均温度最高的十个国家.html")
print("平均温度最高的十个国家条形图已生成！！")

# 绘制温度最低五个国家（玫瑰图）

country = [x[0] for x in low_ten_country]  # 后五个国家
temperature = [x[1] for x in low_ten_country]  # 后五个国家对应温度
# print(temperature)
color_series = randomcolor(len(country))
pie = Pie()
pie.add("", [list(i) for i in zip(country, temperature)], radius=['0%', '25%'], center=['50%', '50%']
        , rosetype='area')
pie.set_global_opts(title_opts=opts.TitleOpts(title='温度最低五个国家'),
                    legend_opts=opts.LegendOpts(is_show=False)

                    )
pie.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=12
                                              , font_style='italic', font_weight='bold',
                                              font_family='Microsoft YaHei'))
pie.set_colors(color_series)
# pie.render('平均温度最低的五个国家.html')
print('平均温度最高的五个国家玫瑰图已生成！！')


# 绘制中国与全球年温度折线图
all_country['dt_year'] = pd.to_datetime(all_country['dt']).dt.year  # 统一时间格式分组年份,世界
all_country['dt_month'] = pd.to_datetime(all_country['dt']).dt.month  # 统一时间格式分组日期
China_date['dt_year'] = pd.to_datetime(China_date['dt']).dt.year  # 统一时间格式分组年份，中国
year_tem = all_country.groupby(['dt_year'])['AverageTemperature'].mean()  # 世界年份和温度平均值打包
year_tem = year_tem.dropna()  # 删除缺省
year_tem_China = China_date.groupby(['dt_year'])['AverageTemperature'].mean()  # 中国年份和温度平均值打包
year_tem_China = year_tem_China.dropna()  # 删除缺省
year = list(year_tem.index)  # 将年份转化列表

year_China = list(year_tem_China.index)
temperature = list(year_tem.values)  # 将温度转化列表
temperature_China = list(year_tem_China)
# print(year_China)
# 由于1743年左右数据有部分缺失，绘制1837年以后图形
x, y = [], []  # 空列表存温度
for i in range(90, 267):  # 从1837到2013年
    x.append(
        opts.LineItem(
            name=year[i],
            value=round(temperature[i], 2),
            itemstyle_opts=opts.ItemStyleOpts(color='purple')
        )
    )
for j in range(0, 181):  # 从1837到2013年
    y.append(
        opts.LineItem(
            name=year_China[j],
            value=round(temperature_China[j], 2),
            itemstyle_opts=opts.ItemStyleOpts(color='blue')
        )
    )
line = Line()
line.add_xaxis(year[90:])
line.add_yaxis(
    series_name='全球平均温度',
    y_axis=x,
    is_selected=True,
    label_opts=opts.LabelOpts(is_show=True))
line.add_yaxis(
    series_name='中国平均温度',
    y_axis=y,
    is_selected=True,
    label_opts=opts.LabelOpts(is_show=True))
line.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
line.set_global_opts(
    title_opts=opts.TitleOpts(title="年全球温度折线图"),
    tooltip_opts=opts.TooltipOpts(
        is_show=True,
        trigger="axis",
        axis_pointer_type="shadow"),

    xaxis_opts=opts.AxisOpts(name='年份'),
    yaxis_opts=opts.AxisOpts(name='温度'),
)

# line.render("中国与全球年温度折线图.html")
print("全球温度折线图已生成！！")
# print(year)

# 模型预测分析线性和多项式分析
start = year.index(1900)  # 从1900年开始回归方程
start_China = year_China.index(1900)
year_start = year[start:]
year_start_China = year_China[start_China:]
year_start = [int(i) for i in year_start]  # 线性回归方程均为整数
year_start_China = [int(i) for i in year_start_China]
temp_start = temperature[start:]
temp_start_China = temperature_China[start_China:]
clf = LinearRegression()  # 线性回归分析
clf1 = LinearRegression()  # 后缀为1为中国
x = np.array(year_start).reshape(114, 1)
y = np.array(temp_start).reshape(114, 1)
x1 = np.array(year_start_China).reshape(114, 1)
y1 = np.array(temp_start_China).reshape(114, 1)
clf.fit(x, y)
clf1.fit(x1, y1)  # 一次分析

year_set_China = year_set = list(range(2014, 2036))  # 将预测的年份
predict_temp = clf.predict([[i] for i in year_set])  # 按线性回归方程估计计算未来温度
predict_temp_China = clf1.predict([[i] for i in year_set_China])  # 按线性回归方程估计计算中国未来温度
predict_temp_list = [i[0] for i in predict_temp]  # 化为一维列表
predict_temp_China_list = [i[0] for i in predict_temp_China]  # 化为一维列表

ploy = PolynomialFeatures(degree=2)  # 设置为2次项，多项式预测
x_ploy = ploy.fit_transform(x)
clf_ = LinearRegression()  # 设置二次线性实例
clf_.fit(x_ploy, y)
x_ployed = ploy.transform(x)
y_predict = clf_.predict(x_ployed)
predict_temp_two_list = [i[0] for i in y_predict]  # 化为一维列表

x, x1, x_dimensional = [], [], []  # 空列表存温度
for i in range(0, 22):
    x.append(
        opts.LineItem(
            name=year_set[i],
            value=round(predict_temp_list[i], 2),
            itemstyle_opts=opts.ItemStyleOpts(color='purple')
        )
    )
for i in range(0, 22):
    x1.append(
        opts.LineItem(
            name=year_set_China[i],
            value=round(predict_temp_China_list[i], 2),
            itemstyle_opts=opts.ItemStyleOpts(color='blue')
        )
    )
for i in range(0, 22):
    x_dimensional.append(
        opts.LineItem(
            name=year_set[i],
            value=round(predict_temp_two_list[i], 2),
            itemstyle_opts=opts.ItemStyleOpts(color='green')
        )
    )
line1 = Line()
line1.add_xaxis(year_set)
line1.add_yaxis(
    series_name='全球平均温度预测(一次)',
    y_axis=x,
    is_selected=True,
    label_opts=opts.LabelOpts(is_show=True))
line1.add_yaxis(
    series_name='中国平均温度预测(一次)',
    y_axis=x1,
    is_selected=True,
    label_opts=opts.LabelOpts(is_show=True))
line1.add_yaxis(
    series_name='全球平均温度预测(二次)',
    y_axis=x_dimensional,
    is_selected=True,
    label_opts=opts.LabelOpts(is_show=True))
line1.set_series_opts(label_opts=opts.LabelOpts(is_show=True))
line1.set_global_opts(
    title_opts=opts.TitleOpts(title="全球平均温度预测"),
    tooltip_opts=opts.TooltipOpts(
        is_show=True,
        trigger="axis",
        axis_pointer_type="shadow"),

    xaxis_opts=opts.AxisOpts(name='年份'),
    yaxis_opts=opts.AxisOpts(name='温度'),
)
# line1.render("中国与全球预测温度图.html")
print("中国与全球预测温度图已生成！！")

# 将图表合并到一个网页
page = Page()
page.add(map)
page.add(pie)
page.add(bar)
page.add(line)
page.add(line1)

page.render('全球温度可视化汇总.html')
print("全球温度可视化汇总已生成！！")
