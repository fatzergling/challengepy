from flask import Flask, request
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
import User
from Club import Club
app = Flask(__name__)

@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return "Welcome to the Penn Club Review API!."

@app.route('/api/clubs', methods=['GET','POST'])
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
def peek(username):
    user = User.read(username)
    return json.dumps(user.ujson())

@app.route('/api/favorite', methods=['GET','POST'])
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
