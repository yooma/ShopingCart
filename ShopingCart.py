#!/usr/bin/env python3
# _*_ encoding:utf-8 _*_
# Auther: Yooma
import sys
import time,datetime
import ShopingLogin
import getpass
FMT='%Y%m%d%H%M%S'

ShopList = {
    1:{
        "汽车类":{
            1:{"BMW 328": 350000},
            2:{"BMW 525": 450000},
            3:{"Audi A4L": 270000},
            4:{"Audi A5": 380000},
            5:{"Benz E260": 430000}
        }
    },
    2:{
        "家电类":{
            1:{"冰箱":3000},
            2:{"彩电":4000},
            3:{"洗衣机":3500},
            4:{"电脑":9999},
            5:{"微波炉":2789},
        }
    },
    3:{
        "服装类":{
            1:{"耐克T恤":250},
            2:{"阿迪T恤":255},
            3:{"李宁裤衩":180},
            4:{"美邦拖鞋":100},
            5:{"彪马帽子":333}
        }
    },
    4:{
        "手机类":{
            1:{"苹果 8 Plus":4500},
            2:{"小米 note2":2000},
            3:{"华为 xxx":3000},
            4:{"锤子 xxx":2400},
            5:{"坚果 xxx":3333}
        }
    }
}

Red = '\033[31;1m'
Blue = '\033[34;1m'
Green = '\033[36;1m'

ColorEnd = '\033[0m'

def LoginJDMall():
    InputUserName = input(Blue+"Input username:"+ColorEnd )
    InputPassWord = getpass.getpass(Blue+"Input password:"+ColorEnd)
    ShopingLogin.ShopingLoginApi(InputUserName, InputPassWord)
    SeeBeforeBougth = input(Blue+"You want to look before bought list?[y|n]:"+ColorEnd)
    if SeeBeforeBougth is '' or SeeBeforeBougth == "y":
        print(Blue+"<---------------Historical shopping information--------------->"+ColorEnd)
        ReadShopCart()


def Recharge(money):
    global Money
    Money = Money + money
    return Money

def ReadShopCart():
    try:
        ShopCartFile = open('ShopCartFile.txt','r')
        ShopCartFileFuBen=eval(ShopCartFile.read())
        for x, y in ShopCartFileFuBen.items():
            print("\033[34;1m[%s]: %s \t [\033[31;1m%sRMB\033[0m\033[34;1m]\033[0m" % \
                  (x, list(y.keys())[0], list(y.values())[0]))
    finally:
        ShopCartFile.close()

def UpdateShopCart(ShopCartDict):
    try:
        ShopCartFile = open('ShopCartFile.txt', 'w+')
        if type(ShopCartDict) is dict:
            ShopCartFile.write(str(ShopCartDict))
    finally:
        ShopCartFile.close()


def EchoShopList(shoplist,oldshoplist):
    ListDict = ""
    BottomDict = ""
    if type(shoplist) is not int:
        for k,v in shoplist.items():
            if type(list(v.values())[0]) is int:
                ListDict = ListDict + '\t' + str(k) + '.' + ' %s %s\n' % (list(v.keys())[0], list(v.values())[0])
                BottomDict = type(list(v.values())[0])
            else:
                ListDict = ListDict + '\t' + str(k) + '.' + ' %s\n' % (list(v.keys())[0])
        while 1:
            InputBuyNum = input("\033[36;1m%sInput goods number:\033[0m" % ListDict)
            if InputBuyNum != '' and InputBuyNum != "b" and InputBuyNum != "q":
                if BottomDict is not int:
                    BuySomeThings(InputBuyNum,shoplist)
                    break
                else:
                    CountBuyInput = input(Green+"Input buy count:"+ColorEnd)
                    BuySomeThings(InputBuyNum, shoplist, CountBuyInput)
                    break
            elif InputBuyNum == "b":
                EchoShopList(ShopList, shoplist)
                break
            elif InputBuyNum == "q":
                print(Blue+"-----------<Welcome to JDFather mall again>-----------\033[0m"+ColorEnd)
                sys.exit()
            else:
                print(Red+"[Input Error]: Cannot empty!"+ColorEnd)
                continue
    else:
        while 1:
            for k,v in oldshoplist.items():
                #print(list(v.keys())[0])
                ListDict = ListDict + '\t' + str(k) + '.' + ' %s %s\n' % (list(v.keys())[0],list(v.values())[0])
            InputBuyNum = input("\033[36;1m%sInput buy number:\033[0m" % ListDict)
            if InputBuyNum == "b":
                EchoShopList(ShopList, shoplist)
                break
            elif InputBuyNum == "q":
                print(Blue+"-----------------<ShopingCartList>-----------------"+ColorEnd)
                UpdateShopCart(ShopCart)
                ReadShopCart()
                print(Blue+"-----------<Welcome to JDFather mall again>-----------"+ColorEnd)
                sys.exit()
            elif InputBuyNum == '':
                print(Red+"[Input Error]: Cannot empty!"+ColorEnd)
                EchoShopList(ShopList, shoplist)
            else:
                try:
                    CountBuyInput = int(input(Green+"Input buy count:"+ColorEnd))
                    BuySomeThings(InputBuyNum,oldshoplist,CountBuyInput)
                except ValueError:
                    print(Red + "[ ValueError ]: Mast input int type." + ColorEnd)
                    EchoShopList(ShopList, shoplist)

        #print("i am oldshoplist %s" % oldshoplist)

def BuySomeThings(GetInputBuyNumber,shoplist,GetCountBuyInput=0):
    #print(GetInputBuyNumber,GetCountBuyInput,shoplist)
    for k,v in shoplist.items():
        #print(v)
        SendVlues = list(shoplist[int(k)].values())[0]
        #print(SendVlues)

        if str(GetInputBuyNumber) == str(k):
            if type(SendVlues) is not dict:
                global Money

                if int(Money) >= int(GetCountBuyInput)*int(SendVlues):
                    GoodsTotalPrice = int(GetCountBuyInput)*int(SendVlues)
                    print("\033[34;1m[You buy \033[0m\033[31;1m%s\033[0m\033[34;1m %s sent [\033[0m\033[31;1m%sRMB\033[0m\033[34;1m]]\033[0m" % (GetCountBuyInput,list(v.keys())[0],GoodsTotalPrice))
                    BuyTime = str(time.strftime(FMT, time.localtime(time.time()))) + str(datetime.datetime.now().microsecond)
                    GoodsName = list(v.keys())[0] + '*' + str(GetCountBuyInput)
                    ShopCart.setdefault(BuyTime,{GoodsName:GoodsTotalPrice})
                    Money -= GoodsTotalPrice
                    print("\033[34;1mRemaining: [\033[31;1m%sRMB\033[0m\033[34;1m]\033[0m" % Money)
                    #print bought goods list.
                    print(Blue+"-------------------ShopingCartList------------------"+ColorEnd)
                    for x, y in ShopCart.items():
                        print("\033[34;1m[%s]: %s \t [\033[31;1m%sRMB\033[0m\033[34;1m]\033[0m" % \
                              (x, list(y.keys())[0], list(y.values())[0]))
                    global ChongZhi
                    Balance = ChongZhi + Hmoney - Money
                    print("\033[34;1m[Shoping Cart Total]: [\033[31;1m%sRMB\033[0m\033[34;1m]\033[0m" % (Balance))
                    EchoShopList(SendVlues, shoplist)
                else:
                    print("\033[34;1mYou don't have enough money to buy %s.\n\tYou has only [\033[31;1m%sRMB\033[0m\033[34;1m]\033[0m" % (list(v.keys())[0],Money))
                    try:
                        QueRen = input("\033[34;1mDo you want to recharge now?[y|n]:\033[0m")
                        if QueRen == '' or  QueRen == "y":
                            try:
                                RechargeInput = int(input("\033[34;1mInput the amount you want to recharge:"))
                                if RechargeInput != '' and RechargeInput > 0:
                                    ChongZhi = RechargeInput
                                    Recharge(RechargeInput)
                                    print("\033[34;1mRecharge [\033[0m\033[31;1m%s\033[0m\033[34;1m] success,now you has [\033[0m\033[31;1m%s\033[0m\033[34;1mRMB]\033[0m" % (RechargeInput,Money))
                                    EchoShopList(SendVlues, shoplist)
                            except ValueError:
                                print(Red + "[ ValueError ]: Mast input int type." + ColorEnd)
                                EchoShopList(SendVlues, shoplist)
                                break
                        else:
                            EchoShopList(SendVlues, shoplist)
                            break
                    except ValueError:
                        print(Red + "[ ValueError ]: Mast input int type." + ColorEnd)

            else:
                EchoShopList(SendVlues,shoplist)
        else:
            continue

if __name__ == '__main__':
    print(Blue+"----------Welcome to JingDongFather Shoping Center----------"+ColorEnd)
    LoginJDMall()
    while 1:
        try:
            Money = int(input(Blue+"Please Input your assets:"+ColorEnd))
            Hmoney = Money
            break
        except ValueError:
            print(Red+"[ ValueError ]: Mast input int type."+ColorEnd)
    ChongZhi = 0
    ShopCart = {}
    EchoShopList(ShopList,ShopList)


