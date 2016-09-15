#!/usr/bin/env python3

import MySQLdb
import numpy as np

class ErrorConnectingDB(Exception):
    def __init__(self, descr):
        self.descr = descr

class DB:

    DEBUG = 1
    user = "root"
    passwd = "qwerty12345"
    db_name = "quest"

    def __init__(self):
        #self.connect()
        self.db = MySQLdb.connect(user=self.user,
                                 passwd=self.passwd,
                                 db=self.db_name)
        self.c = self.db.cursor()

    def __del__(self):
        self.db.commit()
        self.db.close()

    #Do we really need this function?
    def connect(self):
        self.db = MySQLdb.connect(user=self.user,
                                 passwd=self.passwd,
                                 db=self.db_name)
        return self.db
        
    def query(self, s):
        if self.c is None:
            self.c = db.cursor()

        cnt = self.c.execute(s)
        if self.DEBUG == 1:
            #print (self.c.info())
            pass
        #self.db.commit()
        self.db.commit()
        return np.array(self.c.fetchall())
            

    def get_judge_id(self, judge):
        if isinstance(judge, int):
            return judge

        query = 'SELECT id FROM judges WHERE name = \'%s\';' % judge
        data = self.query(query)
        #print ('data=', data)
        #print ('data.size=', data.size)
        if data.size == 0:
            raise ErrorConnectingDB('Can\'t find judge with this name')

        return data[0,0]

    def get_player_id(self, player, par='team_name'):
    #par - culumn name, where we want to find text stored in 'player'
        if isinstance(player, int):
            return player

        query = """SELECT id FROM players
                   WHERE %s = \'%s\;'""" % (par, player)
        data = self.query(query)
        if data.size == 0:
            raise ErrorConnectingDB('Can\'t get player with this %s' % par)

        return data[0,0]
        
        
    def add_score(self, judge, team, score):
        judge_id = self.get_judge_id(judge)
        team_id  = self.get_player_id(team)
        query = """INSERT INTO scores (team_id, judge_id, score)
                   VALUES (%s, %s, %s);""" % (team_id, judge_id, score)
        self.query(query)
        #self.db.commit()


db = DB()

db.add_score('test', 1, 10)

        
