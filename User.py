# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 13:42:13 2019

@author: Andrew Zhao
"""
import json
class User:
    
    def __init__(self, username):
        self.username = username
        self.favorites = []
        self.clubs = []
        
    def addclub(self,club):
        self.clubs.append(club)  
        
    def ujson(self):
        json_data = {}
        json_data["Username"] = self.username
        json_data["Favorites"] = self.favorites
        json_data["Clubs"] = self.clubs
        return json_data
    
    def write(self):
        fileread = open(str(self.username) + ".txt","w")
        fileread.write(json.dumps(self.ujson()))
        fileread.close()

def read(username):
    fileread = open(str(username)+ ".txt","r")
    temp = json.load(fileread)
    ret = User(temp["Username"])
    for c in temp["Clubs"]:
        ret.addclub(c)
    return ret



        
        
jen = User("jen")
jen.addclub("Arun Fan Club")
print(jen.username)
jen.write()
Test = read("jen")
print(Test.clubs[0])


        