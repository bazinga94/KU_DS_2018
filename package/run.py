import subway
from subway import *
from flask import Flask, render_template, request

app = Flask(__name__)

html = "index.html"

@app.route('/')
def student():
    return render_template(html)

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        start = request.form["start"]
        finish = request.form["finish"]
        stopover=request.form["stopover"]
        if(stopover):
            path1, time1 = findPath_flask(start,stopover)
            path2, time2 = findPath_flask(stopover,finish)
            pathlist = path1 + path2
            time = float(time1) + float(time2)
            time = str(time)
        
        else:
            pathlist, time = findPath_flask(start,finish)
            time = str(time)
        percent = percent_flask(start)
        marker = save_path(pathlist)
        path = ""
        for i in range(len(pathlist)):
            if i == len(pathlist)-1:
                path = path + pathlist[i]
            else:
                path = path + pathlist[i] + "  ->  "
        return render_template(html,result = path, result2 = time,result3=percent, result4=marker)
    else:
        result = "request 실패"
        return render_template(html,result = result)
if __name__ == '__main__':
    app.run(debug = False)
