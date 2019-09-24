from flask import Flask, request, render_template, redirect, url_for
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
from werkzeug.security import *
from Club import Club
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
import User
app = Flask(__name__, template_folder='templates')
app.secret_key = "I hate you forever"


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    user = User.read(username)
    return user

@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if current_user.is_authenticated:
        username = request.form['Username']
        return redirect(url_for('api'))
    if request.method == "POST":
        username = request.form['Username']
        password = request.form['Password']
        user = User.read(username)
        if user:
            print(user.checkpass(password))
            if user.checkpass(password):
                login_user(user)
                print("TESTING")
                return redirect('api')
    return '''<form method="POST">
                  Username: <input type="text" name="Username"><br>
                  Password: <input type="text" name="Password"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@app.route('/logout', methods=['GET'])

@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/api/clubs', methods=['GET','POST'])
@login_required
def getclubs():
    if request.method == 'GET':
        fileread = open("clublist.txt","r+")
        temp = fileread.read().replace('\n','')
        ctemp = json.loads(temp)
        return json.dumps(ctemp, indent=3)
    
    if request.method == 'POST':
        content = request.get_json()
        ret = Club(content['Club_Name'], content['Tags'], content['Description'], content['Who_Loves_Me?'])
        fileread = open("clublist.txt","r+")
        temp = fileread.read().replace('\n','')
        ctemp = json.loads(temp)
        for c in ctemp:
            if(c['Club_Name'] == ret.clubname): 
                fileread.close()
                return ret.clubname + " already in roster"
        ctemp.append(ret.cjson())
        fileread.seek(0)
        fileread.truncate()
        fileread.write(json.dumps(ctemp, indent = 3))
        fileread.close()
        return "Added club " + ret.clubname + " to roster."

@app.route('/api/user/<username>', methods=['GET'])
@login_required

def peek(username):
    user = User.read(username)
    return json.dumps(user.ujson())


@app.route('/api/favorite', methods=['GET','POST'])
@login_required
def favorite():
    if request.method == 'POST':
        name = request.form['Username']
        club = request.form['Club_Name']
        fileread = open("clublist.txt","r+")
        temp = fileread.read().replace('\n','')
        ctemp = json.loads(temp)
        for c in ctemp:
            tempclub = Club(c['Club_Name'],c['Tags'],c['Description'], c['Who_Loves_Me?'])
            if(tempclub.clubname == club):
                tempclub.addfav(name)
                ctemp.remove(c)
                ctemp.append(tempclub.cjson())
                fileread.seek(0)
                fileread.truncate()
                fileread.write(json.dumps(ctemp, indent = 3))
                fileread.close()
                return str(tempclub.getfav())
        fileread.close()
        return club + " not in list of clubs."


    return '''<form method="POST">
                  Username: <input type="text" name="Username"><br>
                  Club_Name: <input type="text" name="Club_Name"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''


@app.before_first_request

def setup():
   html = get_clubs_html()
   soup = soupify(html)
   clublist = make_club(soup)
   clubjson = []
   for c in clublist:
       clubjson.append(c.cjson())
   ret = json.dumps(clubjson, indent = 3)
   myfilewrite = open("clublist.txt","w")
   myfilewrite.write(ret)
   myfilewrite.close()
 
   
    
    
if __name__ == '__main__':
    
    app.run()
