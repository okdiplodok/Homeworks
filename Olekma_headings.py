import urllib.request
import re

def downloading():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 YaBrowser/16.7.1.20937 Yowser/2.5 Safari/537.36'
    req = urllib.request.Request('http://gazetaolekma.ru/', headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
       html = response.read().decode('utf-8')
    return html

def searching(html):
    r = re.compile('<a class="news-title" href=.*?</a>', flags=re.U | re.DOTALL)
    headings = r.findall(html)
    return headings

def cleaning(headings):
    fw = open('Olekma_headings.txt','w',encoding = 'UTF-8')
    headings_2 = []
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for t in headings:
        clean_t = regSpace.sub("", t)
        clean_t = regTag.sub("", clean_t)
        if clean_t not in headings_2:
            headings_2.append(clean_t)
    for t in headings_2:
        print(t)
        fw.write(t + '\n')
    fw.close()

def main():
    val = downloading()
    val2 = searching(val)
    val3 = cleaning(val2)

main()
