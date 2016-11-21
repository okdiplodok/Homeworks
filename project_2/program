import json
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def mainpage():
    if request.args:
        fr = open('data.json', 'r', encoding = 'utf-8')
        try:
            f = json.load(fr)
        except:
            f = []
        fr.close()
        fw = open('data.json', 'w', encoding = 'utf-8')
        n = []
        for l in sorted(request.args):
            n.append(request.args[l])
        f.append(n)
        u = json.dump(f, fw,ensure_ascii = False)
        fw.close()  
    return render_template('main.html')

@app.route('/stats')
def stats():
    f = open('data.json', 'r', encoding = 'utf-8')
    data = json.load(f)
    f.close()
    return render_template('stats.html', data = data)

@app.route('/json')
def json_file():
    f = open('data.json','r', encoding = 'utf-8')
    d = json.load(f)
    f.close()
    return render_template('json_file.html', show_json=d)

@app.route('/search')
def searchpage():
    return render_template('searchpage.html')
    
@app.route('/results')
def results():
    if request.args:
        print(request.args)
        f = open('data.json','r', encoding = 'utf-8')
        data = json.load(f)
        f.close()
        show_results = []
        for line in data:
            if line[1] == request.args['name'] or line[2] == request.args['language']:
                show_results.append(line)
            else:
                for k in range(5,12):
                    if line[k] == request.args['prep']:
                        show_results.append(line)
                        break
        return render_template('results.html', show_results = show_results)
                
if __name__ == '__main__':
    app.run(debug=True)
