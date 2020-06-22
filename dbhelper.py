#!/usr/bin/python3.5
#-*-coding: utf-8 -*-

import pymongo
import gridfs
import config
par = config.config
import os
import json

uri = os.getenv('MONGODB_URI',par['mongo'])
DATABASE = os.getenv('DATABASE',par['database'])
from bson.json_util import dumps

class DBHelper:

    def __init__(self):
        client = pymongo.MongoClient(uri)
        self.db = client[DATABASE]
        self.fs = gridfs.GridFS(self.db)

    def get_user(self, email):
        return self.db.users.find_one({"email": email})  

    def get_log(self):
        data = list(self.db.data.find())
        data_r = dumps(self.db.data.find())
        for d in data:
            keys = list(d.keys())

        key = keys[1]

        for d in data:
            dic = d

        #data =json.loads(dic[key])    
        return dic[list(dic.keys())[1]]

    def get_ip(self):
        stored_ip = list(self.db.reports.find())
        
        for d in stored_ip:
            keys = list(d.keys())

        key = keys[1] 
       
        for d in stored_ip:
            dic = d
            
        dic = dic[key]    
            
        ips = []    
        for key,value in dic.items():
            ips.append(value)
         
        ip_database = ips

        return ip_database
       
    def add_acc(self, acc):
        self.db.acc.insert_one(acc)
        
    def acc_list(self):
        BOOKS = []        
        for token in self.db.acc.find():
            del token['_id']
            BOOKS.append(token)
        return BOOKS        

    def add_proj(self, proj):
        self.db.projects.insert_one(proj)
    
    def proj_list(self):
        BOOKS = []        
        for token in self.db.projects.find():
            del token['_id']
            BOOKS.append(token)
        return BOOKS     

    def add_task(self, task):
         self.db.tasks.insert_one(task)  
         
    def tasks(self):
        BOOKS = []        
        for token in self.db.tasks.find():
            del token['_id']    
            BOOKS.append(token)
        return BOOKS        
        
    def user_delete(self, email):
        self.db.users.delete_many({'email' : email})
        self.db.user_profiles.delete_many({'email' : email})

    def delete(self, comd, key1,key2=' ', user_mode=' '):
        result = ''+comd+key1+key2+user_mode
        if (comd=='acc'):
            self.db.acc.delete_many({'ID': key1})
        elif (comd=='proj'):
            print('proj')
            self.db.projects.delete_many({'ID': key1})
            if (user_mode=='delete'):
                print('delete all tasks mode')
                self.db.tasks.delete_many({'PR_ID': key1})
                self.file_del(key1,key2)
        elif (comd=='task'):
            self.db.tasks.delete_many({'PR_ID': key1, 'ID': key2})
            self.file_del(key1,key2)  
        else:
            result = 'err' + comd + key1 + key2 + user_mode
        return result

    def att(self, obj,filename,pr_id='',task_id=''):
        with self.fs.new_file(
                filename=filename, content_type='text/plain',
                metadata=dict(my_other_attribute=42,
                              project=pr_id,
                              task=task_id),
                encoding='utf-8'
                ) as fp:
            fp.write(obj)
        return 'done'   
    
    def att_list(self, pr_id='', task_id=''):
        exists = self.fs.find({'metadata.project':pr_id, 'metadata.task':task_id})
        file = {}
        files = []
        for i, ex, in enumerate(exists):
            file = {
                'name': ex.filename,
                'key': i,
                'date': ex.uploadDate,
                'size': ex.length
            }
            files.append(file)
        return files

    def file_del(self, pr_id='', task_id='', name=''):
        if len(name) < 2:
            exists = self.fs.find({'metadata.project':pr_id, 'metadata.task':task_id})
            for ex in exists:
                fp = self.fs.get_last_version(ex.filename)
                self.fs.delete(fp._id)
        else:
            fp = self.fs.get_last_version(name)   
            self.fs.delete(fp._id)
            print(fp._id)
        return ('done')
    
    def get_file(self,name):
        fp = self.fs.get_last_version(name)
        return fp.read()
    
    
        
    
    

