# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 13:42:13 2019

@author: Andrew Zhao
"""
from werkzeug.security import *
import json
class User:
    
    def __init__(self, username, favorites, clubs, password, login):
        self.username = username
        self.favorites = favorites
        self.clubs = clubs
        self.password = password
        self.login = False
        
    def hashpass(self):
        self.password = generate_password_hash(self.password)
        
        
    def addclub(self,club):
        self.clubs.append(club)  
        
    def addfav(self,club):
        self.favorites.append(club)    
        
    def delclub(self,club):
        if club in self.clubs:
            self.clubs.remove(club)
        
    def delfav(self,club):
        if club in self.favorites:
            self.favorites.remove(club)  
        
    def ujson(self):
        json_data = {}
        json_data["Username"] = self.username
        json_data["Favorites"] = self.favorites
        json_data["Clubs"] = self.clubs
        json_data["Password"] = self.password
        json_data["Log"] = self.login
                 
                
        return json_data
    
    def write(self):
        fileread = open(str(self.username) + ".txt","w")
        fileread.write(json.dumps(self.ujson()))
        fileread.close()
    
    def checkpass(self,password2):
        return check_password_hash(self.password, password2)
    
    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.login

    def is_anonymous(self):
        return False


def read(username):
    fileread = open(str(username)+ ".txt","r")
    temp = json.load(fileread)
    ret = User(temp["Username"], temp["Favorites"], temp["Clubs"], temp["Password"], temp["Log"])
    return ret



        
        
jen = User("jen", [], [], "password", False)
jen.addclub("Arun Fan Club")
jen.hashpass()
print(jen.username)
jen.write()


        