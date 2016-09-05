#!/usr/bin/env python3
#coding:utf-8
import getpass
import sys
import os


def ShopingLoginApi(InputUserName,InputPassWord):
#def ShopingLoginApi():

    Count = 1

    uname = []
    UserList = {
        'yooma':'ciki',
        'shrek':'ciki'
    }
    while 1:
        #InputUserName = input("\033[34;1mInput username:\033[0m")
        #InputPassWord = getpass.getpass("\033[34;1mInput password:\033[0m")
        if InputUserName is '' or InputPassWord is '':
            sys.exit("Input type cannot empty. Must string or int.")
        try:
            LockFileW = open('lock.txt', 'r')
            if InputUserName == LockFileW.read():
                print("%s user locked." % InputUserName)
                sys.exit(0)
        finally:
            LockFileW.close()

        if InputUserName in UserList and InputPassWord == UserList[InputUserName]:
            print("\033[31;1m~~~~~Welcome %s login success~~~~~\033[0m" % InputUserName)
            break
        elif InputUserName not in UserList or InputPassWord != UserList[InputUserName]:
            print("\033[32;1mUserName or password failed,please input again:\033[0m")
            uname.insert(Count, InputUserName)
            s = set(uname)
            for i in s:
                if Count < 4 and uname.count(i) == 3:
                    LockFile = open('lock.txt', 'w+')
                    try:
                        LockFile.write(InputUserName)
                    finally:
                        LockFile.close()
                        print("Your account is locked.")
                        sys.exit(0)
                elif Count == 3:
                    print("Input error 3 times,go out.")
                    sys.exit(0)
            Count += 1
            continue
        else:
            print("Input error.")
            break


if __name__ ==  "__main__":
    ShopingLoginApi()
