from flask import Flask, request, render_template
import sqlite3
import datetime
import google.generativeai as genai
import os

app = Flask(__name__)

flag = 1
api = "AIzaSyA-7ws8lDXiJWXU4GIW7wNaELeBu5Akb8o"

model = genai.GenerativeModel('gemini-1.5-flash')
genai.configure(api_key=api)

@app.route("/", methods = ["POST", "GET"])
def index():
    return(render_template("index.html"))

@app.route("/main", methods = ["POST", "GET"])
def main():
    global flag
    if flag == 1:
        user_name = request.form.get("q")
        currentDatetime = datetime.datetime.now()
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        conn.execute('INSERT INTO user (name, timestamp) VALUES (?, ?)', (user_name, currentDatetime))
        conn.commit()
        c.close()
        conn.close()
        flag = 0
    return(render_template("main.html"))

@app.route("/foodexp", methods = ["POST", "GET"])
def foodexp():
    return(render_template("foodexp.html"))

@app.route("/foodexp_pred", methods = ["POST", "GET"])
def foodexp_pred():
    q = float(request.form.get("q"))
    return(render_template("foodexp_pred.html", r=(q*0.4851)+147.4))

@app.route("/ethical_test", methods = ["POST", "GET"])
def ethical_test():
    return(render_template("ethical_test.html"))

@app.route("/test_result", methods = ["POST", "GET"])
def test_result():
    answer = request.form.get("answer")
    if answer == "false":
        return(render_template("pass.html"))
    elif answer == "true":
        return(render_template("fail.html"))
    
@app.route("/FAQ", methods = ["POST", "GET"])
def FAQ():
    return(render_template("FAQ.html"))
    
@app.route("/FAQ1", methods = ["POST", "GET"])
def FAQ1():
    r = model.generate_content("Factors for Profit")
    return(render_template("FAQ1.html", r=r.candidates[0].content.parts[0]))

@app.route("/userLog", methods = ["POST", "GET"])
def userLog():
    conn=sqlite3.connect('user.db')
    c=conn.cursor()
    c.execute("select * from user")
    r=""
    for row in c:
        r=r+str(row)+'\n'
    print(r)
    c.close()
    conn.close()
    return(render_template("userLog.html", r=r))

@app.route("/deleteLog", methods = ["POST", "GET"])
def deleteLog():
    conn=sqlite3.connect("user.db")
    c=conn.cursor()
    c.execute('DELETE FROM user;')
    conn.commit()
    c.close()
    conn.close()
    return(render_template("delete.html"))

if __name__=="__main__":
    app.run(port=8080)