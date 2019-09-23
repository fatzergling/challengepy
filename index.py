from flask import Flask, request
from scraper import * # Web Scraping utility functions for Online Clubs with Penn.
import User
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
        return ret
    
    if request.method == 'POST':
        content = request.get_json()
        ret = Club(content['Club_Name'], content['Description'])
        ret.addtag(content['Tags'])
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

@app.route('/api/favorite', methods=['POST'])
def favorite():
    name = request.form['Username']
    club = request.form['Club_Name']
    return name

        
@app.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None

    return '''<h1>The language value is: {}</h1>'''.format(language)

        
    


    
 
   
    
    
if __name__ == '__main__':
    app.run()
