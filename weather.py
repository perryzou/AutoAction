import getopt
import sys
from datetime import datetime
import urllib.parse
import requests
import json


def get_current_weather(location, key):
    url = f"https://devapi.qweather.com/v7/weather/now?location={location}&key={key}"
    response = requests.get(url)
    data = json.loads(response.text)
    current_weather = data['now']

    return data['fxLink'], \
           f"{current_weather['text']} 温度:{current_weather['temp']}℃ 体感:{current_weather['feelsLike']}℃ "


def get_current_air(location, key):
    url = f"https://devapi.qweather.com/v7/air/now?location={location}&key={key}"
    response = requests.get(url)
    data = json.loads(response.text)
    current_air = data['now']
    return f"空气:{current_air['category']} {current_air['aqi']}\n"


def get_current_warning(location, key):
    url = f"https://devapi.qweather.com/v7/warning/now?location={location}&key={key}"
    response = requests.get(url)
    data = json.loads(response.text)
    warning = data['warning']
    msg = ""
    for w in warning:
        msg = msg + f"{w['title']}\n"
    return msg


def get_hourly_weather(location, key):
    url = f"https://devapi.qweather.com/v7/weather/24h?location={location}&key={key}"
    response = requests.get(url)
    data = json.loads(response.text)
    hourly_weather = data['hourly']
    msg = ""
    for hour in hourly_weather[:2]:
        fx_time = hour['fxTime']
        dt = datetime.fromisoformat(fx_time)
        formatted_time = dt.strftime("%H:%M")
        msg = msg + f"{formatted_time}:{hour['text']} 温度:{hour['temp']}℃ 降雨:{hour['pop']}% {hour['precip']}mm\n"
    return msg


def get_daily_weather(location, key):
    url = f"https://devapi.qweather.com/v7/weather/3d?location={location}&key={key}"
    response = requests.get(url)
    data = json.loads(response.text)
    daily_weather = data['daily']
    tomorrow = daily_weather[1]
    max_temp = tomorrow['tempMax']
    min_temp = tomorrow['tempMin']
    weather_text_day = tomorrow['textDay']
    weather_text_night = tomorrow['textNight']
    return f"明天:{min_temp}℃-{max_temp}℃ 白天:{weather_text_day} 夜晚:{weather_text_night}"


def send(key, title, msg, link):
    print(msg)
    url = "https://api.day.app/%s/%s/%s?url=%s" % (key, title, urllib.parse.quote(msg), link)
    requests.get(url)


def getArg(argv):
    try:
        options, args = getopt.getopt(argv, "b:w:c:")
    except getopt.GetoptError:
        print('arg error')
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
        locations = c.split("|")
        for location in locations:
            split = location.split(":")
            location_name = split[0]
            link, msg = get_current_weather(split[1], w)
            msg = msg + get_current_air(split[1], w)
            msg = msg + get_current_warning(split[1], w)
            msg = msg + get_hourly_weather(split[1], w)
            msg = msg + get_daily_weather(split[1], w)

            send(b, location_name + '天气预报', msg, link)
