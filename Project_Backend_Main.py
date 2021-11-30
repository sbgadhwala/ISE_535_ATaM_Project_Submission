# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:52:30 2021

@author: sbgadhwa
"""

import psutil
import os
import time
import shutil
import csv
import pandas as pd
import datetime as dt


#class Project_Backend_Main:



def get_pname(id):
    return os.system("ps -o cmd= {}".format(id))

def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           pinfo['cpu']=proc.cpu_percent()
           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)
    return listOfProcObjects

def getUsersCount():
    userList = []
    for i in getListOfProcessSortedByMemory():
        if str(type(i['username']))!='NoneType':
            
            userList.append(i['username'])
            
            #print("Yes")
    userList = set(userList)
    return userList
    

def runCheck():
    
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    total, used, free = shutil.disk_usage("/")
    usedPer = 100*used/total
    return current_time, psutil.cpu_percent(), psutil.virtual_memory().percent, usedPer



def takeFinalAction(component, rule, app, val, thr):
    if rule.lower() == "kill":
        appList = app.split(",")
        for i in appList:
            if not i.endswith(".exe"):
                i = i +".exe"
            i = i.lower()
            try:
                for process in (process for process in psutil.process_iter() if process.name().lower() == i):
                    process.kill()
                    print(f"{process.name()} was killed")
                    appendRowData = [str(dt.datetime.now()), component, str(val), str(thr), 'ATaM ' + rule + 'ed ' + app]
                    if not os.path.exists(r'ATam_Actions_Data.csv'):
                        with open(r'ATam_Actions_Data.csv', 'w') as file:
                            writer = csv.writer(file)
                            writer.writerow(['Timestamp', 'Component', 'Observed Value', 'Threshold', 'Action'])
                            writer.writerow(appendRowData)
                    else:
                        with open(r'ATam_Actions_Data.csv', 'a') as file:
                            writer = csv.writer(file)
                            writer.writerow(appendRowData)
            except:
                print(f"Issue wihle killing {i} ")

    if rule.lower() == "restart":
        count = 0
        appList = app.split(",")
        for i in appList:
            j = i.split("\\")[-1]
            if not j.endswith(".exe") :
                if count < 1:
                    j = i.split("\\")[-1]
                    j = j +".exe"
                
                    j = j.lower()
            
                    try:
                        for process in (process for process in psutil.process_iter() if process.name().lower() == j):
                            process.kill()
                            
                            print(f"{process.name()} was killed")

                            print("restarting ", i.split("\\")[-1])
                            os.startfile(fr"{i}")
                            
                            appendRowData = [str(dt.datetime.now()), component, str(val), str(thr), 'ATaM ' + rule + 'ed ' + app]
                            if not os.path.exists(r'ATam_Actions_Data.csv'):
                                with open(r'ATam_Actions_Data.csv', 'w') as file:
                                    writer = csv.writer(file)
                                    writer.writerow(['Timestamp', 'Component', 'Observed Value', 'Threshold', 'Action'])
                                    writer.writerow(appendRowData)
                            else:
                                with open(r'ATam_Actions_Data.csv', 'a') as file:
                                    writer = csv.writer(file)
                                    writer.writerow(appendRowData)
                            
                            count = count + 1
                            
                    except:
                       print(f"Issue wihle restarting {j} ")
            
            
            
    if rule.lower()=="delete":
        try:
            shutil.rmtree(fr"{app}")
            print(f"{app} folder was deleted")
            appendRowData = [str(dt.datetime.now()), component, str(val), str(thr), 'ATaM ' + rule + 'ed ' + app]
            if not os.path.exists(r'ATam_Actions_Data.csv'):
                with open(r'ATam_Actions_Data.csv', 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Timestamp', 'Component', 'Observed Value', 'Threshold', 'Action'])
                    writer.writerow(appendRowData)
            else:
                with open(r'ATam_Actions_Data.csv', 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow(appendRowData)
        except:
            print(f"Error while deleteing {app}")
            
def takeInputFromUI(cpuVal, ramVal, diskVal, cpu_dropdown, ram_dropdown, disk_dropdown, actionCpu, actionRam, actionDisk):
    
    curTime, cpuUtil, ramUtil, diskUtil = runCheck()
    
    latest_cpu_thr = 0
    latest_ram_thr = 0
    latest_disk_thr = 0
    latest_cpu_rule = ''
    latest_ram_rule = ''
    latest_disk_rule = ''
    latest_cpu_action = ''
    latest_ram_action = ''
    latest_disk_action = ''
    if str(cpuVal)!='None':
        latest_cpu_thr = cpuVal
    if str(cpu_dropdown)!='None':
        latest_cpu_rule = cpu_dropdown
    if str(actionCpu)!='None':
        latest_cpu_action = actionCpu
        
    if str(ramVal)!='None':
        latest_ram_thr = ramVal
    if str(ram_dropdown)!='None':
        latest_ram_rule = ram_dropdown
    if str(actionRam)!='None':
        latest_ram_action = actionRam
        
    if str(diskVal)!='None':
        latest_disk_thr = diskVal
    if str(disk_dropdown)!='None':
        latest_disk_rule = disk_dropdown
    if str(actionDisk)!='None':
        latest_disk_action = actionDisk
    
    if latest_cpu_thr > 0 and cpuUtil > latest_cpu_thr:
        if latest_cpu_rule != '':
            if latest_cpu_action != '':
                #method (rule, and action item)
                print("satisfied condition for CPU")
                takeFinalAction("CPU", latest_cpu_rule, latest_cpu_action, cpuUtil, latest_cpu_thr)
    
    if latest_ram_thr > 0 and ramUtil > latest_ram_thr:
        if latest_ram_rule != '':
            if latest_ram_action != '':
                print("sending to take action.....")
                takeFinalAction("RAM", latest_ram_rule, latest_ram_action, ramUtil, latest_ram_thr)
                #print("Satisfied Condition for RAM")
                
    if latest_disk_thr > 0 and diskUtil > latest_disk_thr:
        if latest_disk_rule != '':
            if latest_disk_action != '':
                print("Satisfied conditon for Disk")
                takeFinalAction("Disk", latest_disk_rule, latest_disk_action, diskUtil, latest_disk_thr)
    
def createDataFrameFromUserInput(latest_cpu_thr, latest_cpu_rule, latest_cpu_action, latest_ram_thr, latest_ram_rule, latest_ram_action, latest_disk_thr, latest_disk_rule, latest_disk_action):
    
    
    data = [['CPU', latest_cpu_thr, latest_cpu_rule, latest_cpu_action], ['RAM', latest_ram_thr, latest_ram_rule, latest_ram_action], ['Disk', latest_disk_thr, latest_disk_rule, latest_disk_action]]
    df = pd.DataFrame(data, columns = ['Monitoring Component', 'Threshold', 'Action', 'Action Item'])
    df.set_index('Monitoring Component', inplace=True)
    print(df)
    df.to_csv("User_Input.csv")
