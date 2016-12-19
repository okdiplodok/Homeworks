import re, html, os

def search_words():
    f = open('newspaper.html','r',encoding = 'UTF-8')
    fr = f.read()
    reg = re.compile('<div class="categories">.*?<h1><a href=\".*?\">(.*?)<div class="posted">',flags=re.U | re.DOTALL)
    lines_news = re.findall(reg, fr)
    lines_clean = []
    sub_a = re.compile('<.*?>', flags=re.U | re.DOTALL)
    sub_n = re.compile('[0-9]+?.*?[.,\"\'\«\»;\\:\(\)?—!/ ]')
    for l in lines_news:
        new_l = sub_a.sub('', html.unescape(l))
        new_l = new_l.replace('\xad','')
        new_l = new_l.replace('\xa0', '')
        new_l = new_l.replace('\t', ' ')
        new_l = new_l.replace('\n', ' ')
        new_l = sub_n.sub(' ', new_l)
        lines_clean.append(new_l)
    lines = ' '.join(lines_clean)
    words = lines.split()
    for i, word in enumerate(words):
        words[i] = word.strip(',. \"\'\«\»;:\(\)?!/')
        words[i] = words[i].lower()
    f.close()
    return words

def compare_words(words):
    f = open('adyghe-unparsed-words.txt','r',encoding = 'UTF-8')
    fr = f.read()
    dict = fr.split('\n')
    words_dict = []
    for word in words:
        for w in dict:
            if word == w:
                words_dict.append(word)
    p = ''
    for i, m in enumerate(words_dict):
        if p in words_dict:
            p = words_dict.pop(i)
    words_dict = set(words_dict)
    fw = open('wordlist.txt', 'a', encoding='UTF-8')
    for w in words_dict:
        fw.write(w + '\n')
    fw.close()
    f.close()

def mystem_():
    path = 'C:' + os.sep + 'Users' + os.sep + 'zu_ann' + os.sep + 'Desktop' + os.sep + 'wordlist.txt'
    words_analysed = 'C:' + os.sep + 'Users' + os.sep + 'zu_ann' + os.sep + 'Desktop' + os.sep + 'words_analysed.txt'
    os.system('C:\mystem.exe ' + path + ' ' + words_analysed + ' -nid')
    return words_analysed

def rus_nouns(words_analysed):
    f = open('words_analysed.txt','r',encoding = 'UTF-8')
    fr = f.read()
    reg = re.compile('(.*?){.*?=S.*?=им,ед.*?')
    regex = re.findall(reg,fr)
    fw = open('rus_nouns.txt', 'a', encoding='UTF-8')
    for word in regex:
        fw.write(word + '\n')
    fw.close()
    f.close()
    return regex

def table_rus_words(regex):
    f = open('words_analysed.txt', 'r',encoding='UTF-8')
    fr = f.read()
    fw = open('sql.txt', 'a', encoding='UTF-8')
    fw.write("CREATE TABLE rus_words (id INTEGER PRIMARY KEY, wordform VARCHAR (100), lemma VARCHAR (100));\n")
    i = 0
    for word in regex:
        reg_wordform = re.compile(word + '{.*?=(.*?)}')
        wordforms = re.search(reg_wordform,fr)
        if wordforms:
            analyse = wordforms.group(1)
            if '|' in analyse:
                analyse = analyse.split('|')
                for elem in analyse:
                    fw.write('INSERT INTO rus_words (id, wordform, lemma) VALUES (' + str(i) + ', ' + word + ', '
                             + elem + ');\n')
                    i += 1
            else:
                fw.write('INSERT INTO rus_words (id, wordform, lemma) VALUES (' + str(i) + ', ' + word + ', '
                         + analyse + ');\n')
                i += 1
    f.close()
    fw.close()

def main ():
    val = search_words()
    val2 = compare_words(val)
    val3 = mystem_()
    val4 = rus_nouns(val3)
    val5 = table_rus_words(val4)

if __name__ == '__main__':
    main()
