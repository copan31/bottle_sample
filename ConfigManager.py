#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging 
# logging.basicConfig(level=logging.DEBUG)

import ConfigParser

import os

CONFIG_FILE_NAME = 'stockmanager.cfg'

class ConfigManager: 

    @classmethod
    def getExecTopDir(cls):

        execDir = os.getcwd() + "/"
        
        #cron実行だと実行パスが/rootになってしまうことに対するワークアラウンド
#         if ( os.getcwd() == "/root") : 
#             execDir = "/hoge/exec/path/"
    
        return execDir


    @classmethod
    def getConfig(cls, curSecStr, curConfigStr):
        config = ConfigParser.ConfigParser()
        
        filePath = ConfigManager.getExecTopDir() + CONFIG_FILE_NAME
        
        logging.debug ("filePath : %s", filePath)
        
        config.read( filePath )
        return config.get(curSecStr, curConfigStr)

        
    @classmethod
    def getDatabaseConfig(cls, curConfigStr):
        return ConfigManager.getConfig("database", curConfigStr)
        
    @classmethod
    def getConnectionParams(cls):

        curUser=        ConfigManager.getDatabaseConfig('user')
        curPassword=ConfigManager.getDatabaseConfig('password')
        curHost=         ConfigManager.getDatabaseConfig('host')
        curDatabase= ConfigManager.getDatabaseConfig('dbname')
        curPort=          ConfigManager.getDatabaseConfig('port')
        
        connectionDic = {}
        if (curUser) :
            connectionDic['user'] = curUser
        if (curPassword) :
            connectionDic['password'] = curPassword
        if (curHost) :
            connectionDic['host'] = curHost
        if (curDatabase) :
            connectionDic['database'] = curDatabase
        if (curPort) :
            connectionDic['port'] = int(curPort)
            
        
        logging.debug ("DB Connection Config : %s", connectionDic)
        
        return connectionDic
          
if __name__ == '__main__':
    curUser = ConfigManager.getDatabaseConfig("user")
    print "curUser : " + curUser
    
    curDB = ConfigManager.getConfig( "database", "dbname")
    print "curDB : " + curDB
    
    params = ConfigManager.getConnectionParams()
    print "[Database Config]"
    print  params

    
