import telebot
import datetime
import schedule
import time
import random
import emojis
import threading

# расписание генуборок по дням недели
def choseWeekDay(day):
    today = []
    if day == 0: today = [emojis.encode(':one: туалет ресторана\n'), emojis.encode(':two: ресторан\n'), emojis.encode(':three: кассовая зона\n'), emojis.encode(':four: витрина\n'), emojis.encode(':five: холодильник для напитков')]
    if day == 1: today = [emojis.encode(':one: печь\n'), emojis.encode(':two: морозильный стол\n'), emojis.encode(':three: линия начинения\n'), emojis.encode(':four: горячий цех')]
    if day == 2: today = [emojis.encode(':one: левая часть\n'), emojis.encode(':two: персоналка\n'), emojis.encode(':three: сухой склад\n'), emojis.encode(':four: туалет персонала')]
    if day == 3: today = [emojis.encode(':one: горячий цех\n'), emojis.encode(':two: туалет ресторана\n'), emojis.encode(':three: курьерская')]
    if day == 4: today = [emojis.encode(':one: мойка\n'), emojis.encode(':two: упаковка\n'), emojis.encode(':three: печь')]
    if day == 5: today = [emojis.encode(':one: холодный цех\n'), emojis.encode(':two: холодильник в хц')]
    if day == 6: today = [emojis.encode(':one: холодильник в левой части\n'), emojis.encode(':two: морозильник\n'), emojis.encode(':three: левая часть\n'), emojis.encode(':four: горячий цех')]
    return today

# инициализация токена и переменных для обращения к боту
TOKEN = '6170200659:AAHPfCK0ccv9SjA03hl4Q3HtOKsxUh1eLcw'
TODAY = choseWeekDay(datetime.datetime.today().weekday())
TIMES = ['12:00', '14:00', '16:00', '18:00', '20:00', '22:00']
CHAT_ID = -821822815
MY_ID = 949347911
MEDIA_GROUP = set()

# стандартные фразы для бота
REMIND = '<i><b>НАПОМИНАЮ\nПлан на сегодня:\n</b></i>\n' + ''.join(TODAY)
INFO = '<i><b>План на сегодня:\n</b></i>\n' + ''.join(TODAY)
HELLO = '<i><b>Привет, я - Гена и теперь я слежу за генуборками на Лиге. \n</b></i>\nКаждые два часа с 12:00 до 22:00 я буду напоминать о сегодняшнем плане генуборки.\n\nПроверить план уборок на сегодня: <i>/info</i>\nВключить напоминания: <i>/remind_on</i>\nОтключить напоминания: <i>/remind_off</i>'
EMODJIS = [':heart_eyes_cat:', ':kissing_heart:', ':call_me_hand:', ':eyes:', ':blush:']
WAIT = 'Менеджер СПБ01, жду фоточек '
REMIND_ON = 'Теперь буду напоминать про уборки'
REMIND_OFF = 'Больше не буду напоминать про уборки'
BOSS = ['Хорошо. Будет блестеть, босс!', 'Будет сделано!', 'Считайте, что уже вымыто!', 'Мы что-нибудь придумаем с этим!', 'Обязательно почистим!', 'Уже бежим мыть!', 'Натрем до блеска!']
THANKS = ['вау! Вы молодцы сегодня, спасибо', 'большое спасибо!', 'как чисто, спасибо!', 'класс!', 'это заслуживает похвалы, спасибо!', 'вы крутые. Спасибо!', 'так быстро? Вы молодцы!']

# инициализация бота
bot = telebot.TeleBot(TOKEN)

# установка напоминаний
def set_schedule():
    schedule.every().day.at(TIMES[0]).do(remind).tag('task')
    schedule.every().day.at(TIMES[1]).do(remind).tag('task')
    schedule.every().day.at(TIMES[2]).do(remind).tag('task')
    schedule.every().day.at(TIMES[3]).do(remind).tag('task')
    schedule.every().day.at(TIMES[4]).do(remind).tag('task')
    schedule.every().day.at(TIMES[5]).do(remind).tag('task')
    schedule.every(5).seconds.do(remind).tag('task')
def send_remind():
    while True:
        schedule.run_pending()
        time.sleep(1)

# отправка напоминания в чат
def remind():
    bot.send_message(MY_ID, REMIND, parse_mode='html')
    bot.send_message(MY_ID, WAIT + emojis.encode(random.choice(EMODJIS)))

# распознование пользовательских команд
def active():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, HELLO, parse_mode='html')

    @bot.message_handler(commands=['info'])
    def info(message):
        bot.send_message(message.chat.id, INFO, parse_mode='html')
        bot.send_message(message.chat.id, '@' + message.from_user.username + ', жду фоточек', parse_mode='html')

    @bot.message_handler(content_types=['photo', 'document'])
    def getUserPhoto(message):
        group = message.media_group_id
        if (message.from_user.username == 'lena_Voronyna') and (group not in MEDIA_GROUP):
            MEDIA_GROUP.add(group)
            bot.reply_to(message, random.choice(BOSS))
        elif group not in MEDIA_GROUP:
            MEDIA_GROUP.add(group)
            bot.reply_to(message, '@' + message.from_user.username + ', ' + random.choice(THANKS))

    @bot.message_handler(commands=['remind_on'])
    def remind_on(message):
        bot.send_message(message.chat.id, REMIND_ON)
        set_schedule()

    @bot.message_handler(commands=['remind_off'])
    def remind_off(message):
        bot.send_message(message.chat.id, REMIND_OFF)
        schedule.clear('task')

    # запуск бота на постоянную активность
    bot.polling(none_stop = True)

# создание и запуск основного потока
th1 = threading.Thread(target=active)
th1.start()

# дополнительный поток
while True: send_remind()