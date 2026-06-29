import streamlit as st
import ephem
import requests
from datetime import datetime, timezone,timedelta
import random
st.set_page_config(page_title = "Астросайт")
st.markdown("""
    <style>
        .stApp {
            background-color: black;
            color:white;
            }
        h1, h2, h3, h4, h5, h6, p, span, label, .stText, .stMarkdown, p li {
        color: #ffffff !important;
    }

    </style>
""", unsafe_allow_html=True)
st.text("Введите дату и время")
date = st.date_input('Дата')
time = st.time_input("Время",step=60)
local_datetime = datetime.combine(date, time)
TIMEZONE_HOURS = 3
utc_datetime = local_datetime - timedelta(hours=TIMEZONE_HOURS)
user_date_string = utc_datetime.strftime("%Y/%m/%d %H:%M:%S")
month = date.month
moon = ephem.Moon()
sun = ephem.Sun()
moon.compute(user_date_string)
st.markdown("------------Информация о Луне и Солнце")
st.text(f"Луна освещена на {moon.phase:.2f}%")
if moon.phase<= 2:
    st.text("Новолуние")
elif 2<moon.phase<=45:
    st.text("Растущая или убывающая Луна")
elif 45<moon.phase<=55:
    st.text("Половина Луны")
elif 55<moon.phase<=98:
    st.text("Растущая или убывающая Луна")
else:
    st.text("Полнолуние")
next_new = ephem.next_new_moon(user_date_string)
st.text(f"Следущая новая Луна: {next_new}")
st.info(f'Лучше всего проводить наблюдения в новолуние')
yar = ephem.Observer()
yar.date = user_date_string
yar.lon = '39.893'
yar.lat = '57.626'
mr = yar.next_rising(moon).datetime()+timedelta(hours = TIMEZONE_HOURS)
ms = yar.next_setting(moon).datetime()+timedelta(hours = TIMEZONE_HOURS)
sr = yar.next_rising(sun).datetime()+timedelta(hours = TIMEZONE_HOURS)
ss = yar.next_setting(sun).datetime()+timedelta(hours = TIMEZONE_HOURS)
st.text(f"Ближайший восход Луны:{mr}\nЗаход Луны:{ms}\nВосход Солнца:{sr}\nЗаход Солнца:{ss}")
try:
    yar.horizon = "-18"
    night_start = yar.next_setting(sun).datetime()+timedelta(hours = TIMEZONE_HOURS)
    night_finish = yar.next_rising(sun).datetime()+timedelta(hours = TIMEZONE_HOURS)
    st.text(f"Астрономическая ночь начинается {night_start} и заканчивается {night_finish}")
    yar.horizon = "-0.34"
except:
    st.text("Сегодня не будет астрономической ночи")
st.info("Наблюдения удобнее проводить в астрономическую ночь")
st.markdown("-------------Некоторые небесные тела, видимые сейчас")
star_dict = ["Achernar", "Acrux", "Aldebaran", "Alnilam", "Alnitak", "Alpheratz", "Altair", "Antares", "Arcturus", "Betelgeuse", "Canopus", "Capella", "Castor", "Deneb", "Fomalhaut", "Hadar", "Mintaka", "Polaris", "Pollux", "Regulus", "Rigel", "Schedar", "Sirius", "Spica"]
for i in range(24):
    name = star_dict[i]
    star = ephem.star(name)
    star.compute(yar)
    if star.alt >0:
        const = ephem.constellation(star)
        st.text(f"Звезду {name} сейчас видно на небе в созвездии {const}. Азимут {star.az}, высота {star.alt}")
mars = ephem.Mars()
mars.compute(yar)
if mars.alt>10*ephem.degree:
    st.text(f"Марс сейчас может быть видно на азимуте {mars.az} и высоте{mars.alt}, в созвездии {ephem.constellation(mars)}")
mercury = ephem.Mercury()
mercury.compute(yar)
if mercury.alt>10*ephem.degree:
    st.text(f"Меркурий сейчас может быть видно на азимуте {mercury.az} и высоте{mercury.alt}, в созвездии {ephem.constellation(mercury)}")
venus = ephem.Venus()
venus.compute(yar)
if venus.alt>10*ephem.degree:
    st.text(f"Венеру сейчас может быть видно на азимуте {venus.az} и высоте {venus.alt}, в созвездии {ephem.constellation(venus)}")
jupiter = ephem.Jupiter()
jupiter.compute(yar)
if jupiter.alt>10*ephem.degree:
    st.text(f"Юпитер сейчас может быть видно на азимуте {jupiter.az} и высоте {jupiter.alt}, в созвездии {ephem.constellation(jupiter)}")
saturn = ephem.Saturn()
saturn.compute(yar)
if saturn.alt>10*ephem.degree:
    st.text(f"Сатурн сейчас может быть видно на азимуте {saturn.az} и высоте{saturn.alt}, в созвездии {ephem.constellation(saturn)}")
uran = ephem.Uranus()
uran.compute(yar)
if uran.alt>10*ephem.degree:
    st.text(f"Уран сейчас может быть видно на азимуте {uran.az} и высоте {uran.alt}, в созвездии {ephem.constellation(uran)}(потребуется телескоп)")
neptun = ephem.Neptune()
neptun.compute(yar)
if neptun.alt>10*ephem.degree:
    st.text(f"Нептун сейчас может быть видно на азимуте {neptun.az} и высоте {neptun.alt}, в созвездии {ephem.constellation(neptun)}(потребуется телескоп)")
st.info("Азимут дан в градусах, где Север — 0°, Восток — 90°, Юг — 180°, а Запад — 270°. Высота звезды 90° у вас над головой, а 0° на горизонте.")
st.markdown("--------------Данные, актуальные только для текущей даты")
st.markdown("--------Погодные условия")
try:
    city = 'Yaroslavl'
    url = "https://api.openweathermap.org/data/2.5/weather?q=Yaroslavl&units=metric&lang=ru&appid=f4eedf2ea2c518255177400f0cda353f"
    weather_data = requests.get(url, timeout = 10).json()
    cloudi = weather_data['clouds']['all']
    temp = weather_data['main']['temp'] 
    st.text(f'Облачность {cloudi}%, температура {temp}°С (по данным openweathermap.org)')
    if cloudi<=10:
        st.text('Ясно. Идеальная облачность для наблюдений')
    elif 10<cloudi<=30:
        st.text("Малооблачно. Отлично для наблюдений")
    elif 30<cloudi<=60:
        st.text("Переменная облачность. Наблюдать сложнее, облака закрывают часть неба")
    elif 60<cloudi<=80:
        st.text("Облачно с прояснениями. Наблюдения почти невозможны")
    else:
        st.text("Пасмурно. Наблюдения невозможны")
except:
    st.error("Не удалось подключиться с сервису прогноза погоды")
st.markdown("-------Текущее положение МКС")
try:
    url1 = "http://api.open-notify.org/iss-now.json"
    iss_data = requests.get(url1, timeout = 10).json()
    iss_lat = iss_data["iss_position"]['latitude']
    iss_lon = iss_data["iss_position"]['longitude']
    iss_lat = float(iss_lat)
    iss_lon = float(iss_lon)
    if iss_lat>=0 and iss_lon>=0:
        st.text(f"Сейчас МКС находится на {iss_lat} с.ш. и {iss_lon} в.д.")
    elif iss_lat<0 and iss_lon>0:
        st.text(f"Сейчас МКС находится на {abs(iss_lat)} ю.ш. и {iss_lon} в.д.")
    elif iss_lat<0 and iss_lon<0:
        st.text(f"Сейчас МКС находится на {abs(iss_lat)} ю.ш. и {abs(iss_lon)} з.д.")
    else:
        st.text(f"Сейчас МКС находится на {iss_lat} с.ш. и {abs(iss_lon)} з.д.")
    st.text("Данные получены у open-notify.org")
except:
    st.error("Не удалось подключиться к серверу")
expand = st.expander("Полезные советы", icon=":material/info:")
advices = ['Для наблюдений лучше выбирать открытые площадки вдали от города','Следите за температурой воздуха. Одевайтесь по погоде!','Постарайтесь найти знакомые астеризмы - так вам будет проще искать звёзды','Для нахождения объекта по азимуту лучше использовать компас','Используйте интерактивные карты ночного неба']
expand.write(f"{random.choice(advices)}")

