import requests, json, re
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

from collections import Counter

group_id = '-31545597'

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/' + method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

def get_from(key,posts,name):
    fw2 = open(name + '.json', 'w', encoding='UTF-8')
    keys = {}
    for id in posts:
        keys[id] = posts[id][key]
    json.dump(keys, fw2, ensure_ascii=False)
    fw2.close()
    return keys

def get_posts(group_id):
    item_count = 101
    fw = open("posts.json",'w',encoding='UTF-8')
    fw2 = open('posts.json', 'w', encoding='UTF-8')
    response = []
    while len(response) < item_count:
        result = vk_api('wall.get', owner_id = group_id, count=100, offset=len(response))
        response += result['response']
    posts = {}
    for i in range(len(response)):
        if (type(response[i]) != int and type(response[i]) != str):
            posts[response[i]['id']] = response[i]
    json.dump(posts, fw2, ensure_ascii=False)
    post_texts = get_from('text',posts, 'post_texts')
    fw.close()
    fw2.close()
    return posts

def get_comments(group_id, posts):
    all_comments = {}
    fw = open("comments.json",'w',encoding='UTF-8')
    fw2 = open('comm_texts.json', 'w', encoding='UTF-8')
    for id in posts:
        comments = []
        item_count = posts[id]['comments']['count']
        while len(comments) < item_count:
            result = vk_api('wall.getComments', owner_id=group_id, post_id=id, count=100, offset=len(comments), v='5.63', extended=1, preview_length=0)
            comments += result['response']['items']
        all_comments[id] = comments
    json.dump(all_comments, fw, ensure_ascii=False)
    comm_texts = {}
    for id in all_comments:
        comm_texts[id] = [i['text'] for i in all_comments[id]]
    json.dump(comm_texts, fw2, ensure_ascii=False)
    fw2.close()
    fw.close()

if __name__ == '__main__':
    get_comments(group_id, get_posts(group_id))