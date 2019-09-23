# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 12:44:12 2019

@author: Andrew Zhao
"""

class Club:
    
    def __init__(self, clubname, tags, clubdis,favorite):
        self.clubname = clubname
        self.clubdis = clubdis
        self.tags = tags
        self.favorite = favorite
   
    def addtag(self, tag):
        self.tags.append(tag)
        
    def addfav(self,name):
        if name not in self.favorite:
            self.favorite.append(name)
        
    
    def getfav(self):
        return len(self.favorite)
        
    def cjson(self):
        json_data = {}
        json_data['Club_Name'] = self.clubname
        json_data['Tags'] = self.tags
        json_data['Description'] = self.clubdis
        json_data['Who_Loves_Me?'] = self.favorite
        return json_data



        
        
        