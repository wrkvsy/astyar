import streamlit as st
import ephem
import requests
from datetime import datetime, timezone,timedelta
import random
st.set_page_config(page_title = "Астрофотография")
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
st.title("Навигатор для астрофотографов в Ярославле")
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
st.info(f'Лучше всего проводить наблюдения за звездами в новолуние')
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

st.text("------------------Места  в центре Ярославля")
st.text("----Ярославский планетарий им. Терешковой")
star_dict = ["Achernar", "Acrux", "Aldebaran", "Alnilam", "Alnitak","Altair", "Antares", "Arcturus", "Betelgeuse", "Canopus", "Capella", "Castor", "Deneb", "Fomalhaut", "Hadar","Polaris", "Pollux", "Regulus", "Rigel", "Sirius", "Spica"]
for i in range(21):
    name = star_dict[i]
    star = ephem.star(name)
    star.compute(yar)
    if star.alt >0 and star.az<=315*ephem.degree and star.az>=175*ephem.degree :
        const = ephem.constellation(star)
        st.text(f"Звезду {name} сейчас может быть видно видно на небе около в созвездии {const}. Азимут {star.az}, высота {star.alt}")
mars = ephem.Mars()
mars.compute(yar)
if mars.alt>10*ephem.degree and 175*ephem.degree<=mars.az<=315*ephem.degree:
    st.text(f"Марс сейчас может быть видно на азимуте {mars.az} и высоте{mars.alt}, в созвездии {ephem.constellation(mars)}")
mercury = ephem.Mercury()
mercury.compute(yar)
if mercury.alt>10*ephem.degree and 175*ephem.degree<=mercury.az<=315*ephem.degree:
    st.text(f"Меркурий сейчас может быть видно на азимуте {mercury.az} и высоте{mercury.alt}, в созвездии {ephem.constellation(mercury)}")
venus = ephem.Venus()
venus.compute(yar)
if venus.alt>10*ephem.degree and 175*ephem.degree<=venus.az<=315*ephem.degree:
    st.text(f"Венеру сейчас может быть видно на азимуте {venus.az} и высоте {venus.alt}, в созвездии {ephem.constellation(venus)}")
jupiter = ephem.Jupiter()
jupiter.compute(yar)
if jupiter.alt>10*ephem.degree and 175*ephem.degree<=jupiter.az<=315*ephem.degree :
    st.text(f"Юпитер сейчас может быть видно на азимуте {jupiter.az} и высоте {jupiter.alt}, в созвездии {ephem.constellation(jupiter)}")
saturn = ephem.Saturn()
saturn.compute(yar)
if saturn.alt>10*ephem.degree and 175*ephem.degree<=saturn.az<=315*ephem.degree:
    st.text(f"Сатурн сейчас может быть видно на азимуте {saturn.az} и высоте{saturn.alt}, в созвездии {ephem.constellation(saturn)}")
moon.compute(yar)
if moon.alt>10*ephem.degree and 175*ephem.degree<=moon.az<=315*ephem.degree:
    st.text(f"Луну сейчас может быть видно на азимуте {moon.az} и высоте{moon.alt}")
st.text("Куда смотреть:")
st.text("1) Встаньте в центр Солнечной системы около планетария. Здесь азимут около 240")
st.text("2) Если азимут меньше 240, нужно смотреть или двигаться налево, в сторону обсерватории ")
st.text("3) Если азимут больше 240, нужно смотреть или двигаться направо, тогда в кадр попадет купол")
st.text("--------Вознесенская башня")
for i in range(21):
    name = star_dict[i]
    star = ephem.star(name)
    star.compute(yar)
    if star.alt >0 and star.az<=73*ephem.degree and star.az>=30*ephem.degree :
        const = ephem.constellation(star)
        st.text(f"Звезду {name} сейчас может быть видно на небе около в созвездии {const}. Азимут {star.az}, высота {star.alt}")
mars = ephem.Mars()
mars.compute(yar)
if mars.alt>10*ephem.degree and 30*ephem.degree<=mars.az<=73*ephem.degree:
    st.text(f"Марс сейчас может быть видно на азимуте {mars.az} и высоте{mars.alt}, в созвездии {ephem.constellation(mars)}")
mercury = ephem.Mercury()
mercury.compute(yar)
if mercury.alt>10*ephem.degree and 30*ephem.degree<=mercury.az<=73*ephem.degree:
    st.text(f"Меркурий сейчас может быть видно на азимуте {mercury.az} и высоте{mercury.alt}, в созвездии {ephem.constellation(mercury)}")
venus = ephem.Venus()
venus.compute(yar)
if venus.alt>10*ephem.degree and 30*ephem.degree<=venus.az<=73*ephem.degree:
    st.text(f"Венеру сейчас может быть видно на азимуте {venus.az} и высоте {venus.alt}, в созвездии {ephem.constellation(venus)}")
jupiter = ephem.Jupiter()
jupiter.compute(yar)
if jupiter.alt>10*ephem.degree and 30*ephem.degree<=jupiter.az<=73*ephem.degree :
    st.text(f"Юпитер сейчас может быть видно на азимуте {jupiter.az} и высоте {jupiter.alt}, в созвездии {ephem.constellation(jupiter)}")
saturn = ephem.Saturn()
saturn.compute(yar)
if saturn.alt>10*ephem.degree and 30*ephem.degree<=saturn.az<=73*ephem.degree:
    st.text(f"Сатурн сейчас может быть видно на азимуте {saturn.az} и высоте{saturn.alt}, в созвездии {ephem.constellation(saturn)}")
moon.compute(yar)
if moon.alt>10*ephem.degree and 30*ephem.degree<=moon.az<=73*ephem.degree:
    st.text(f"Луну сейчас может быть видно на азимуте {moon.az} и высоте{moon.alt}")
st.text("Куда смотреть:")
st.text("1) Встаньте рядом с Универмагом,напротив парка")
st.text("2) Если азимут меньше 65, нужно смотреть или двигаться направо, к боковой стороне Универмага ")
st.text("3) Если азимут больше 65, нужно смотреть или двигаться налево, к пешеходному переходу в парк")
st.text("------Церковь Ильи пророка(колокольня)")
for i in range(21):
    name = star_dict[i]
    star = ephem.star(name)
    star.compute(yar)
    if star.alt >0 and((star.az >= 335 * ephem.degree) or (star.az <= 100 * ephem.degree))  :
        const = ephem.constellation(star)
        st.text(f"Звезду {name} сейчас может быть видно на небе около в созвездии {const}. Азимут {star.az}, высота {star.alt}")
mars = ephem.Mars()
mars.compute(yar)
if mars.alt>10*ephem.degree and ((mars.az >= 335 * ephem.degree) or (mars.az <= 100 * ephem.degree)):
    st.text(f"Марс сейчас может быть видно на азимуте {mars.az} и высоте{mars.alt}, в созвездии {ephem.constellation(mars)}")
mercury = ephem.Mercury()
mercury.compute(yar)
if mercury.alt>10*ephem.degree and ((mercury.az >= 335 * ephem.degree) or (mercury.az <= 100 * ephem.degree)):
    st.text(f"Меркурий сейчас может быть видно на азимуте {mercury.az} и высоте{mercury.alt}, в созвездии {ephem.constellation(mercury)}")
venus = ephem.Venus()
venus.compute(yar)
if venus.alt>10*ephem.degree and ((venus.az >= 335 * ephem.degree) or (venus.az <= 100 * ephem.degree)):
    st.text(f"Венеру сейчас может быть видно на азимуте {venus.az} и высоте {venus.alt}, в созвездии {ephem.constellation(venus)}")
jupiter = ephem.Jupiter()
jupiter.compute(yar)
if jupiter.alt>10*ephem.degree and ((jupiter.az >= 335 * ephem.degree) or (jupiter.az <= 100 * ephem.degree)) :
    st.text(f"Юпитер сейчас может быть видно на азимуте {jupiter.az} и высоте {jupiter.alt}, в созвездии {ephem.constellation(jupiter)}")
saturn = ephem.Saturn()
saturn.compute(yar)
if saturn.alt>10*ephem.degree and((saturn.az >= 335 * ephem.degree) or (saturn.az <= 100 * ephem.degree)) :
    st.text(f"Сатурн сейчас может быть видно на азимуте {saturn.az} и высоте{saturn.alt}, в созвездии {ephem.constellation(saturn)}")
moon.compute(yar)
if moon.alt>10*ephem.degree and ((moon.az >= 335 * ephem.degree) or (moon.az <= 100 * ephem.degree)):
    st.text(f"Луну сейчас может быть видно на азимуте {moon.az} и высоте{moon.alt}")
st.text("Куда смотреть:")
st.text("1) Встаньте прямо по середине Советской площади(вперед от основного входа). Здесь ваш азимут около 80")
st.text("2) Если азимут меньше 80 , нужно смотреть или двигаться направо. То же самое, если азимут больше 300")
st.text("3) Если азимут больше 80, нужно смотреть или двигаться налево")
st.info("Азимут дан в градусах, где Север — 0°, Восток — 90°, Юг — 180°, а Запад — 270°. Высота 90° у вас над головой, а 0° на горизонте.Для точного определения азимута рекомендуется использовать компас.")
st.markdown("--------------Данные, актуальные только для текущей даты")
st.markdown("--------Погодные условия")
try:
    city = 'Yaroslavl'
    url = "https://api.openweathermap.org/data/2.5/weather?q=Yaroslavl&units=metric&lang=ru&appid=f4eedf2ea2c518255177400f0cda353f"
    weather_data = requests.get(url, timeout = 10).json()
    cloudi = weather_data['clouds']['all']
    temp = weather_data['main']['temp'] 
    st.text(f'Облачность {cloudi}%, температура {temp}°С')
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


