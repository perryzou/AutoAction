import urllib.parse

import requests
import sys, getopt


class WeatherTask:
    def __init__(self, b, w, c):
        self.b = b
        self.w = w
        self.c = c

    def send(self, msg):
        print(msg)
        url = "https://api.day.app/%s/今日天气预报/%s" % (self.b, urllib.parse.quote(msg))
        requests.get(url)
        pass

    # 获取今天当前部分信息数据
    def now_weather(self, ):
        url = 'https://devapi.heweather.net/v7/weather/now?location=%s&key=%s' % (self.c, self.w)
        now_res = requests.get(url)
        now_res_json = now_res.json()

        # 获取信息返回
        return now_res_json['now']

    def now_and_future_twodays_weather(self):
        url = 'https://devapi.heweather.net/v7/weather/3d?location=%s&key=%s' % (self.c, self.w)
        forecast_res = requests.get(url)
        forecast_res_json = forecast_res.json()
        updateTime = forecast_res_json['updateTime']
        daily_forecast = forecast_res_json['daily']
        return updateTime, daily_forecast

    def getRemark(self):
        url = "https://v1.hitokoto.cn/"
        forecast_res = requests.get(url)
        return forecast_res.json()

    def main(self):
        now = self.now_weather()
        updateTime, daily_forecast = self.now_and_future_twodays_weather()
        remark = self.getRemark()

        today = daily_forecast[0]
        msg = '''当前天气：%s\t|\t气温：%s度\t|\t体感：%s度\t\n夜间天气：%s\t|\t最高：%s度\t|\t最低：%s度\t\n%s\t--%s''' \
              % (now['text'], now['temp'], now['feelsLike'], today['textNight'], today['tempMax'], today['tempMin'],
                 remark['hitokoto'], remark['from'])
        self.send(msg)


def getArg(argv):
    try:
        options, args = getopt.getopt(argv, "b:w:c:")
    except getopt.GetoptError:
        sys.exit()
    b = ""
    w = ""
    c = ""
    for option, value in options:
        if option == '-b':
            b = value
        if option == '-w':
            w = value
        if option == '-c':
            c = value
    return b, w, c


if __name__ == "__main__":
    b, w, c = getArg(sys.argv[1:])
    if b == '':
        print("请设置push key")
    elif w == '':
        print("请设置天气key")
    elif c == '':
        print("请设置城市代码")
    else:
        task = WeatherTask(b, w, c)
        task.main()
