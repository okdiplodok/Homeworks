import os, re, html

def mystem_():
    path = 'C:' + os.sep + 'Users' + os.sep + 'zu_ann' + os.sep + 'Desktop' + os.sep + 'text.txt'
    new_file = 'C:' + os.sep + 'Users' + os.sep + 'zu_ann' + os.sep + 'Desktop' + os.sep + 'lines_words.txt'
    os.system('C:\mystem.exe ' + path + ' ' + new_file + ' -cnd')
    return new_file

def table_lemmas(new_file):
    f = open(new_file,'r',encoding = 'UTF-8')
    fr = f.readlines()
    fw = open('C:' + os.sep + 'Users' + os.sep + 'zu_ann' + os.sep + 'Desktop' + os.sep + 'script_lines.sql','a',encoding = 'UTF-8')
    fw.write("CREATE TABLE Lemmas (id INTEGER PRIMARY KEY, wordform VARCHAR (100), lemma VARCHAR (100));\n")
    reg_wordform = re.compile('(.*?){')
    reg_lemma = re.compile('{(.*?)[}?]')
    wordforms = []
    i = 0
    for line in fr:
        res_wordform = re.search(reg_wordform, line)
        if res_wordform:
            wordform = res_wordform.group(1).lower()
            if wordform not in wordforms:
                wordforms.append(wordform)
                res_lemma = re.search(reg_lemma, line)
                if res_lemma:
                    lemma = res_lemma.group(1)
                fw.write('INSERT INTO Lemmas (id, wordform, lemma) VALUES (' + str(i) + ', \'' + wordform + '\', \'' + lemma + '\');\n')
                i += 1
    f.close()
    fw.close()
    return wordforms

def table_wordforms(new_file,wordforms):
    f = open(new_file, 'r', encoding='UTF-8')
    fw = open('C:' + os.sep + 'Users' + os.sep + 'zu_ann' + os.sep + 'Desktop' + os.sep + 'script_lines.sql', 'a', encoding='UTF-8')
    fw.write("CREATE TABLE Wordforms (id INTEGER PRIMARY KEY, punctuation_mark_l VARCHAR (100), wordform VARCHAR (100), punctuation_mark_r VARCHAR (100), id_lemma VARCHAR (100), Nword VARCHAR (100));\n")
    brace = re.compile('{.*?}')
    reg_num = re.compile('[0-9%]+')
    fr = f.read()
    fr = brace.sub('',html.unescape(fr))
    fr = re.sub(reg_num, ' ', fr)
    fr = fr.replace('_',' ')
    fr = fr.replace('\n','\s')
    fr = fr.replace('\t', '\s')
    fr = fr.replace('\\u', '\s')
    fr = fr.strip('\n\n')
    fr = fr.strip('\\n\\n')
    fr = fr.split('\s')
    n = 0
    for i,word_mark in enumerate(fr):
        for k,elem in enumerate(wordforms):
            if fr[i].lower() == elem:
                fw.write('INSERT INTO Wordforms (id, punctuation_mark_l, wordform, punctuation_mark_r, id_lemma, Nword) VALUES (' + str(n) + ', \'' + fr[i-1] + '\', \'' + word_mark + '\', \'' + fr[i+1] + '\', ' + str(k) + ', ' + str(n + 1) + ');\n')
                n += 1
    f.close()
    fw.close()

def main():
    val = mystem_()
    val2 = table_lemmas(val)
    val3 = table_wordforms(val, val2)

if __name__ == '__main__':
    main()
