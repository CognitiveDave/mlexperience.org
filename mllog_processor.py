#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 19:05:34 2019

@author: david
"""
import pandas as pd
import datetime as dt
import os
import gzip
import boto3
import config
par = config.config
par = config.config
import os
import ipinfo
import time

access_token = '26c7ea35038bf1'
handler = ipinfo.getHandler(access_token)
ip_address = '216.239.36.21'
details = handler.getDetails(ip_address)
print(details.all)

uri = os.getenv('MONGODB_URI',par['mongo'])
DATABASE = os.getenv('DATABASE',par['database'])
#with gzip.open('input.gz','r') as fin:        
#    for line in fin:        
#        print('got line', line)
prefix = '/papertrail/logs/11108912/'

import time
from time import gmtime, strftime
import pymongo
from datetime import datetime
now = datetime.now() 
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:",date_time)


def mongo_database_setup():

    # Try to connect to MongoDB,  exit if not successful.
    try:
        client = pymongo.MongoClient(uri)
        db = client[DATABASE]
        print ("Connected successfully!!!")
        
    except:
        print ("Could not connect to MongoDB: %s" % e )

    #Use todays date for the database name:
    #name='ip_data'

    #db = conn[name] #Create the database
    #Create two collections in the database
    reports = db.reports  
    data = db.data
    #return the connection, database name, collections names.     
    return client,db,reports,data


def ipInfo(addr=''):
    time.sleep(3)
    ip_address = addr
    details = handler.getDetails(ip_address)
    data = details.all
    return data    

def s3():
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)

def s3_list():
    files = []
    s3client = boto3.client('s3')
    bucket = 'mlexperience-papertrail'
    startAfter = prefix
    theobjects = s3client.list_objects_v2(Bucket=bucket, StartAfter=startAfter )
    for object in theobjects['Contents']:
        files.append(object['Key'])
    return files

def s3_download(files):
    bucket_name = 'mlexperience-papertrail'
    for file in files:
        filename = file.split('/')[4]
        s3_file_path= file
        save_as = '/home/david/logs_ml/'+filename
        s3 = boto3.client('s3')
        s3.download_file(bucket_name , s3_file_path, save_as)

def s3_reconcile():
    s3 = s3_list()
    location = '/home/david/logs_ml'
    local = os.listdir(location)
    missing = []
    print(local)
    for file in s3:
        filename = file.split('/')[4]
        if not(filename in local):
            missing.append(file)
    print(len(s3),' files in S3 and ', len(local), ' files on local')
    if len(missing)>0:
        print('downloading...')
        print(missing)
        s3_download(missing)
    return missing        

s3_reconcile()

location = '/home/david/logs_ml'
files = os.listdir(location)
field_list = ['id',
              'generated_at',
              'received_at',
              'source_id',
              'source_name',
              'source_ip',
              'facility_name',
              'severity_name',
              'program',
              'message'
              ]

def parse(text):
    log = {}
    fields = text.decode('utf8').split('\t')
    for count, field in enumerate(fields):
        log[field_list[count]] = field
    return log

def parse_app1(text):
    return text.split('"')


lines = []
extra = []
lined = {}
count = 0
# Open the file with read only permit
for file in files:
    path = location+'/'+file
    f = gzip.open(path,'r')
    # use readline() to read the first line 
    line = f.readline()
    # use the read line to read further.
    # If the file is not empty keep reading one line
    # at a time, till the file is empty
    while line:
        log = parse(line)    
        if log['program'] =='heroku/router':
            lines.append(log)
            mes = log['message'].strip().replace('\n','').replace('- -','').split(' ')
            for m in mes:
                n = m.split('=')
                try:
                    log[n[0]] = n[1]
                    extra.append(n[0])
                except:
                    continue
            log['file'] = file
            lined[count] = log             
            count = count+1
        
        elif (log['program'].split('/')[0] == 'app'):
            request = lines[:-1]        
            prog = log['program'].split('/')
            if (prog[0]=='app'): 
                mess = log['message']
                if mess[:7] != "measure":
                    parsed = parse_app1(log['message'])
                    try:
                        lined[count-1]['additional'] = parsed[-2:-1][0]
                    except:
                        error = ''                        
        
        # in python 2+
        # print line
        # in python 3 print is a builtin function, so
        #print(line)
        # use realine() to read next line
        line = f.readline()
    f.close()

extra = list(set(extra))
for e in extra:
    field_list.append(e)
field_list.append('file')
field_list.append('ip_add')    
field_list.append('additional')    
df = pd.DataFrame.from_dict(lined, orient='index', columns=field_list)
print(df.groupby(['method','fwd']).count()['id'])
print(df.groupby(['method','fwd','path']).count()['id'])
df['c'] = 1
df['date'] = pd.to_datetime(df['generated_at'])
df['dates'] = df['date'].dt.date
f=df.groupby(['dates']).sum()['c']
#f.plot.bar()
ip_database = {}
conn, db, reports, data = mongo_database_setup()
df['fwd'] = df['fwd'].apply(lambda x: x.strip('"'))
stored_ip = list(db.reports.find())
if len(stored_ip) > 0:
    dbs = len(stored_ip)
    sel_dbs = stored_ip[dbs-1]
    keyed = list(sel_dbs.keys())[1]
    ip_database = sel_dbs[keyed]

ips=df['fwd'].unique()
ip_list = []
for ip in ips:
    try:
        data = ip_database[ip.replace('.','-')]  
        data['ip'] = ip
    except: 
        print('new ip ', ip)
        if len(ip) < 20:
            data = ipInfo(ip)
            ip_database[ip.replace('.','-')] = data
        if len(ip) > 20:
            ipp = ip.split(',')
            data = ipInfo(ipp[0])        
            ip_database[ip.replace('.','-')] = data
    ip_list.append(data)
    
    
    
ip_dict = {}
names = ['ip', 'city', 'region', 'country', 'loc', 'hostname', 'postal', 
         'org', 'country_name', 'latitude', 'longitude']
            
for ipd in ip_list:
    dic = {}
    for n in names:
        dic[n] = ''
        try:
            dic[n] = ipd[n]
        except:
            continue
    
    ip_dict[ipd['ip']] = dic
 
for n in names:
    new_col = 'ip_'+n
    try:
        df[new_col] = df['fwd'].apply(lambda x: ip_dict[x][n]) 
    except:
        df[new_col] = df['fwd']

    
mon_out = {}    
for key,value in ip_dict.items():
    mon_out[key.replace('.','-')] = value
  
db.reports.insert_one({date_time: mon_out})
now = datetime.now() 
date_time = str(now.strftime("%m/%d/%Y, %H:%M:%S"))
del df['dates']
del df['message']
df = df.fillna('-')
db.data.insert_one({date_time: df.to_dict('records')})

#df.groupby(['ip_country','ip_city']).count()['c'].plot.bar()
#df.groupby(['ip_city']).count()['c'].plot.bar()

data = list(db.data.find())
for d in data:
    keys = list(d.keys())

key = keys[1]

for d in data:
    dic = d
 
data = dic[list(dic.keys())[1]]
  
ff = pd.DataFrame.from_records(data)



