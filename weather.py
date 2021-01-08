import urllib.parse

import requests


def send(msg):
    print(msg)
    url = "https://api.day.app/MQiDfGtNgX3jAgCRKmohrf/今日天气预报/" + urllib.parse.quote(msg)
    requests.get(url)
    pass


# 获取今天当前部分信息数据
def now_weather():
    url = 'https://devapi.heweather.net/v7/weather/now?location=101270119&key=818c832c460b46cd84e4ad34b75aca26'
    now_res = requests.get(url)
    now_res_json = now_res.json()

    # 获取信息返回
    return now_res_json['now']


def now_and_future_twodays_weather():
    url = 'https://devapi.heweather.net/v7/weather/3d?location=101270119&key=818c832c460b46cd84e4ad34b75aca26'
    forecast_res = requests.get(url)
    forecast_res_json = forecast_res.json()
    updateTime = forecast_res_json['updateTime']
    daily_forecast = forecast_res_json['daily']
    return updateTime, daily_forecast

def getRemark():
    url="https://v1.hitokoto.cn/"
    forecast_res = requests.get(url)
    return forecast_res.json()



def main():
    now = now_weather()
    updateTime, daily_forecast = now_and_future_twodays_weather()
    remark = getRemark()

    today = daily_forecast[0]
    msg = '''当前天气：%s\t|\t气温：%s度\t|\t体感：%s度\t\n夜间天气：%s\t|\t最高：%s度\t|\t最低：%s度\t\n%s\t--%s''' \
          % (now['text'], now['temp'], now['feelsLike'], today['textNight'], today['tempMax'], today['tempMin'],
             remark['hitokoto'],remark['from'])
    send(msg)


if __name__ == "__main__":
    main()
