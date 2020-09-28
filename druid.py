#!/usr/bin/python
# -- coding: utf-8 --
import os
import sys
import json
import time

import requests
from requests.auth import HTTPBasicAuth

overlord = 'http://overloadleaderIP:18090'
coordinator = 'http://coordinatorleaderIP:18081'
user = 'xiaodongxi'
password = 'abcdefg'

status_api = '/status'
running_api = '/druid/indexer/v1/runningTasks'
pending_api = '/druid/indexer/v1/pendingTasks'
task_api = '/druid/indexer/v1/tasks'
datasource_api = '/druid/coordinator/v1/datasources'
overlord_api = '/druid/indexer/v1/leader'
coordinator_api = '/druid/coordinator/v1/leader'

auth = HTTPBasicAuth(user, password)
##################################################
#      datasource 要在coordinator 上查询          #
##################################################

targets = [
    'task',
    'datasource',
    'running',
    'pending',
    'overlord',
    'coordinator'
]


def rawdata(refreshtime=30):
    if sys.argv[2] in targets:
        tmp_file = '/tmp/druidmonitor/' + target + '.tmp'
        tmp_file_exists = True if os.path.isfile(tmp_file) else False

        if tmp_file_exists and (time.time()-os.path.getmtime(tmp_file)) <= refreshtime:
            with open(tmp_file, 'r') as f:
                raw_data = f.read()
                f.close()
        else:
            raw_data_web = requests.get(url=url, auth=auth)
            with open(tmp_file, 'wb') as f:
                f.write(raw_data_web.text)
                f.close()

            raw_data = raw_data_web.text
            if not tmp_file_exists:
                os.chmod(tmp_file, 0o777)
        return raw_data
    else:
        return False


def discovery():
    result = {'data': []}
    data = json.loads(rawdata())
    for item in data:
        if 'datasource' == sys.argv[2]:
            result['data'].append({'{#NAME}': item})
    print json.dumps(result)


def status():
    total_failed_task = 0
    data = json.loads(rawdata(60))
    if 'task' == sys.argv[2]:
        for item in data:
            if item['dataSource'] == sys.argv[3]:
                if item['status'] == 'FAILED':
                    total_failed_task += 1
                    break
        print total_failed_task


def count():
    task_count = 0
    data = json.loads(rawdata(60))
    for item in data:
         task_count+=1
    print task_count


def getboss():
    data = rawdata(120)
    print data



if __name__ == '__main__':
    target = sys.argv[2]

    if target == 'task':
        url = overlord + task_api
    elif target == 'datasource':
        url = coordinator + datasource_api
    elif target == 'running':
        url = overlord + running_api
    elif target == 'pending':
        url = overlord + pending_api
    elif target == 'overlord':
        url = overlord + overlord_api
    elif target == 'coordinator':
        url = coordinator + coordinator_api

    if sys.argv[1] == 'discovery':
        discovery()
    elif sys.argv[1] == 'status':
        status()
    elif sys.argv[1] == 'count':
        count()
    elif sys.argv[1] == 'getboss':
        getboss()
