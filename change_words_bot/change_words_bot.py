# -*- coding: utf-8 -*-
import flask, telebot, re, conf, random, json
from pymorphy2 import MorphAnalyzer

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN,
                      threaded=False)

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

morph = MorphAnalyzer()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Это бот, который генерирует ответы, используя слова из антиутопии Дж.Оруэлла \"1984\". 
                     \Напиши что-нибудь!")

def split_sentence(message):
    text = message.text
    regex = re.compile('([ /\.!?,:\-\–\\\'\"()]+)')
    words = regex.split(text)
    return words

def check_verb(p, data):
    if 'tran' in p.tag:
        if 'perf' in p.tag:
            lst = data['verb']['tran']['perf']
        else:
            lst = data['verb']['tran']['impf']
    elif 'intr' in p.tag:
        if 'perf' in p.tag:
            lst = data['verb']['intr']['perf']
        else:
            lst = data['verb']['intr']['impf']
    return lst

def check_noun(p, data):
    if 'anim' in p.tag:
        if 'femn' in p.tag:
            lst = data['noun']['anim']['femn']
        elif 'masc' in p.tag:
            lst = data['noun']['anim']['masc']
        elif 'neut' in p.tag:
            lst = data['noun']['anim']['neut']
        elif 'Ms-f' in p.tag:
            lst = data['noun']['anim']['ms-f']
    elif 'inan' in p.tag:
        if 'femn' in p.tag:
            lst = data['noun']['inan']['femn']
        elif 'masc' in p.tag:
            lst = data['noun']['inan']['masc']
        elif 'neut' in p.tag:
            lst = data['noun']['inan']['neut']
        elif 'Ms-f' in p.tag:
            lst = data['noun']['inan']['ms-f']
    elif 'ANim' in p.tag:
        if 'femn' in p.tag:
            lst = data['noun']['ANim']['femn']
        elif 'masc' in p.tag:
            lst = data['noun']['ANim']['masc']
        elif 'neut' in p.tag:
            lst = data['noun']['ANim']['neut']
        elif 'Ms-f' in p.tag:
            lst = data['noun']['ANim']['ms-f']
    return lst

def check_adv(p, data):
    if 'Ques' in p.tag:
        lst = data['adv']['Ques']
    elif 'Dmns' in p.tag:
        lst = data['adv']['Dmns']
    else:
        lst = data['adv']['others']
    return lst

def create_word(p, lst):
    try:
        new_word = random.choice(lst)
        gram = str(p.tag).split(' ')[1]
        gram = set(gram.split(','))
        p_new_word = morph.parse(new_word)[0]
        new_word = p_new_word.inflect(gram).word
    except:
        pass
    return new_word

@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_answer(message):
    f = open('/home/zuann/change_words_bot/data.json', 'r', encoding='utf-8')
    data = json.load(f)
    let = re.compile('[а-яёА-ЯЁ]')
    words = split_sentence(message)
    reply = ''
    for word in words:
        if let.match(word):
            p = morph.parse(word)[0]
            pos = p.tag.POS
            print('info: {}'.format(p.tag))
            if pos == 'PREP' or pos == 'CONJ' or pos == 'PRCL' or pos == 'INTJ' or pos == 'NPRO':
                reply += word
            else:
                if pos == 'VERB':
                    lst = check_verb(p, data)
                elif pos == 'NOUN':
                    lst = check_noun(p, data)
                elif pos == 'ADVB':
                    lst = check_adv(p, data)
                else:
                    lst = data[str(pos).lower()]
                try:
                    new_word = create_word(p, lst)
                except:
                    new_word = word
                    print('unfortunately, old word')
                if word[0].isupper():
                    new_word = new_word[0].upper() + new_word[1:]
                reply += str(new_word)
        else:
            reply += word
    print(reply)
    bot.send_message(message.chat.id, reply)

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
