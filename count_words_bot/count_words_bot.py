# -*- coding: utf-8 -*-
import flask, telebot, re, conf

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN,
                      threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

app = flask.Flask(__name__)


# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который считает длину вашего сообщения.")


@bot.message_handler(func=lambda message: True)#, content_types=['text']
def send_len(message):
    text = message.text
    text = text.replace('\n', ' ')
    reg = re.compile('[ /&\.!?,:\-\–\\()]+')
    words = reg.split(text)
    rm = ['', ' ']
    for i in rm:
        for n, w in enumerate(words):
            if w == i:
                words.pop(n)
    if str(len(words)).endswith('1') and not str(len(words)).endswith('11'):
        ending = 'о'
    elif str(len(words)).endswith('2') or str(len(words)).endswith('3') or str(len(words)).endswith('4'):
        ending = 'а'
    else:
        ending = ''
    bot.send_message(message.chat.id, 'В вашем сообщении {} слов{}.'.format(len(words), ending))


# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)