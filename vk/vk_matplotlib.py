import requests, json, re, time
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

from collections import Counter

group_id = '-57354358'

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/' + method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

def get_from_posts(key,posts):
    fw2 = open(key + '_posts.json', 'w', encoding='UTF-8')
    keys = {}
    for id in posts:
        keys[id] = posts[id][key]
    json.dump(keys, fw2, ensure_ascii=False)
    fw2.close()
    return keys

def get_from_comments(key,comments):
    fw = open(key + '_comments.json', 'w', encoding='UTF-8')
    keys = {}
    for post_id in comments:
        for i in comments[post_id]:
            keys[i['id']] = i[key]
    json.dump(keys, fw, ensure_ascii=False)
    fw.close()
    return keys

def get_information(post_info, comm_info):
    fw = open('users.json','w',encoding='UTF-8')
    posts, post_users, post_dates, post_texts = post_info
    comm_users, comm_dates, comm_texts_id, comm_texts = comm_info
    users = dict(list(post_users.items()) + list(comm_users.items()))
    dates = dict(list(post_dates.items()) + list(comm_dates.items()))
    users_info = {}
    for i in dates:
        dates[i] = time.strftime('%d.%m.%Y',time.gmtime(dates[i]))
    reg_date = re.compile('([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})')
    for post_id in users:
        if not str(users[post_id]).startswith('-'):
            user = {}
            result = vk_api('users.get', user_ids = users[post_id], fields = 'city, bdate')
            if 'city' in result['response'][0] and result['response'][0]['city'] != 0:
                city_id = result['response'][0]['city']
                res_city = vk_api('database.getCitiesById', city_ids = city_id)
                city = res_city['response'][0]['name']
                user['city'] = city
            if 'bdate' in result['response'][0]:
                res_bdate = reg_date.search(result['response'][0]['bdate'])
                res_date = reg_date.search(dates[post_id])
                if res_bdate and res_date:
                    if res_bdate.group(2) < res_date.group(2):
                        age = int(res_date.group(3)) - int(res_bdate.group(3))
                    elif res_bdate.group(2) == res_date.group(2):
                        if res_bdate.group(1) <= res_date.group(1):
                            age = int(res_date.group(3)) - int(res_bdate.group(3))
                        else:
                            age = int(res_date.group(3)) - int(res_bdate.group(3)) - 1
                    else:
                        age = int(res_date.group(3)) - int(res_bdate.group(3)) - 1
                    user['age'] = age
            users_info[post_id] = user
    for key in list(users_info):
        if users_info[key] == {}:
            users_info.pop(key)
    json.dump(users_info, fw, ensure_ascii=False)
    fw.close()
    return users_info

def get_posts(group_id):
    item_count = 200
    fw = open("posts.json",'w',encoding='UTF-8')
    response = []
    while len(response) < item_count:
        result = vk_api('wall.get', owner_id = group_id, count = item_count, offset = len(response))
        response += result['response']
    posts = {}
    for i in range(len(response)):
        if (type(response[i]) != int and type(response[i]) != str):
            posts[response[i]['id']] = response[i]
    json.dump(posts, fw, ensure_ascii=False)
    post_texts = get_from_posts('text', posts)
    post_users = get_from_posts('from_id', posts)
    post_dates = get_from_posts('date', posts)
    fw.close()
    return posts, post_users, post_dates, post_texts

def get_comments(group_id, posts):
    all_comments = {}
    fw = open('comments.json','w',encoding='UTF-8')
    fw2 = open('text_comments_id.json', 'w', encoding='UTF-8')
    posts = posts[0]
    for id in posts:
        comments = []
        item_count = posts[id]['comments']['count']
        while len(comments) < item_count:
            result = vk_api('wall.getComments', owner_id = group_id, post_id = id, count = 100, offset = len(comments), v = '5.63', preview_length = 0)
            comments += result['response']['items']
        all_comments[id] = comments
    json.dump(all_comments, fw, ensure_ascii=False)
    for key in list(all_comments):
        if all_comments[key] == []:
            all_comments.pop(key)
    comm_texts_id = {}
    for id in all_comments:
        comm_texts_id[id] = [comment['text'] for comment in all_comments[id]]
    json.dump(comm_texts_id, fw2, ensure_ascii=False)
    comm_texts = get_from_comments('text', all_comments)
    comm_users = get_from_comments('from_id', all_comments)
    comm_dates = get_from_comments('date', all_comments)
    fw.close()
    fw2.close()
    return comm_users, comm_dates, comm_texts_id, comm_texts

def plots1(post_info, comm_info):
    post_texts = post_info[3]
    comm_texts_id = comm_info[2]
    length = {}
    for id in post_texts:
        num_post = count_words(post_texts[id])
        if id in comm_texts_id:
            num_comm = []
            for comm in comm_texts_id[id]:
                num_comm.append(count_words(comm))
            length[num_post] = sum(num_comm)/len(num_comm)
    keys = [i for i in length.keys()]
    values = [i for i in length.values()]
    plt.plot(keys, values)
    plt.title('Соотношение длины поста и средней длины комментариев')
    plt.xlabel('Длина поста')
    plt.ylabel('Средняя длина комментариев')
    plt.grid(True, color='orchid')
    plt.show()
    #plt.savefig('Соотношение длины поста и средней длины комментариев.pdf')
    plt.close()

def plots2(users_info, post_info, comm_info):
    post_texts = post_info[3]
    comm_texts = comm_info[3]
    texts = dict(list(post_texts.items()) + list(comm_texts.items()))
    length_age = {}
    for id in sorted(users_info):
        if 'age' in users_info[id]:
            length_age[users_info[id]['age']] = count_words(texts[id])
    print(length_age)
    age = [i for i in length_age.keys()]
    values2 = [i for i in length_age.values()]
    plt.bar(age, values2)
    plt.title('Соотношение возраста и средней длины поста/комментария')
    plt.xlabel('Возраст')
    plt.ylabel('Средняя длина поста/комментария')
    plt.grid(True, color='orchid')
    plt.show()
    #plt.savefig('Соотношение возраста и средней длины поста/комментария.pdf')
    plt.close()
    return texts

def plots3(users_info, texts):
    length_city = {}
    for id in sorted(users_info):
        if 'city' in users_info[id]:
            length_city[users_info[id]['city']] = count_words(str(texts[id]))
    print(length_city)
    city = [i for i in length_city.keys()]
    values3 = [i for i in length_city.values()]
    plt.bar(range(len(city)), values3)
    plt.xticks(range(len(city)), city, rotation='vertical')
    plt.title('Соотношение города и средней длины поста/комментария')
    plt.xlabel('Города')
    plt.ylabel('Средняя длина поста/комментария')
    plt.show()
    #plt.savefig('Соотношение города и средней длины поста/комментария.pdf')
    plt.close()

def count_words(text):
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace(' - ', ' ')
    text = text.replace('<br>', ' ')
    url = re.compile('(https?|www)[0-9a-zA-Z/.\-%=?:&_]+')
    pers = re.compile('\[.*?\]')
    text = re.sub(url, '', text)
    text = re.sub(pers, '<reference>', text)
    for sym in text:
        if (ord(sym) > 1327 and ord(sym) not in range(8192, 8303)):
            text = text.replace(sym, ' ')
    eos = re.compile('[ /\.!?,:\-\–\\\'\"()]+')
    words = eos.split(text)
    rm = ['', ' ']
    for i in rm:
        for n,w in enumerate(words):
            if w == i:
                words.pop(n)
    return len(words)

def main(group_id):
    a = get_posts(group_id)
    b = get_comments(group_id, a)
    c = get_information(a,b)
    plots1(a,b)
    plots3(c, plots2(c, a, b))

if __name__ == '__main__':
    main(group_id)
