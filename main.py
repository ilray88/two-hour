from flask import Flask, jsonify
import os
# -*- coding: utf-8 -*-
import datetime
import statistics
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname="SimHei.ttf") # 替换为您计算机上支持中文的字体文件路径
import time

from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/')
def get_rainfall_data():
    data = {
        "建材市场": ["114.076369,22.711629"],
        "环观南路与观平路": ["114.092839,22.699618"],
        "谷湖龙南北街": ["114.089041,22.702627"],
        "巴兰塔": ["114.049435,22.699074"],
        "富士施乐": ["114.049649,22.687161"],
        # "锦鲤站": ["114.048802,22.701543"],
        "下围站": ["114.078043,22.690873"]
    }

    fig, axs = plt.subplots(3, 2, figsize=(24, 12))
    axs = axs.ravel()  # 将子图数组展开为一维数组
    for i, (location, coord) in enumerate(data.items()):
        url = f"https://api.caiyunapp.com/v2.6/q5rFCLRaXOG7RIlS/{coord[0]}/minutely"
        params = {"unit": "metric:v2"}
        response = requests.get(url, params=params)
        data = response.json()["result"]["minutely"]
        precipitation_2h = data["precipitation_2h"]
        description = data["description"]
        probability = data["probability"]
        probability_mean = statistics.mean(probability)
        probability_mean_percent = "{:.2f}%".format(probability_mean)
        axs[i].plot(precipitation_2h)
        axs[i].set_title(f"{location}_降雨概率{probability_mean_percent}", fontproperties=font,color="red")
        axs[i].set_xlabel(u"时间 (分钟)", fontproperties=font)
        axs[i].set_ylabel(u"降水量 (毫米)", fontproperties=font)

    # 调整子图间距和边距
    plt.subplots_adjust(wspace=0.4, hspace=0.5, top=0.95, bottom=0.05, left=0.05, right=0.95)

    current_time = datetime.datetime.now()
    time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')  # 去掉了微秒
    # 绘制总图
    plt.suptitle(u"观湖积水点未来2小时降雨量预测(%s)\n%s" % (time_str, description), fontproperties=font, fontsize=16, fontweight="bold")
    plt.subplots_adjust(top=0.9)
    
    # 保存图像文件
    # 使用time模块获取当前时间
    timestr = time.strftime("%Y%m%d-%H%M%S")
    # 将时间字符串作为文件名，保存图片
    filename = f"plot_{timestr}.png"
    fig.savefig(filename, format='png')
    # 将图像数据返回给Web页面
    with open(filename, 'rb') as f:
        image_data = f.read()
    return Response(image_data, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

