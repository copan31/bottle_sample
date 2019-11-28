#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging 
from peewee import *
from ConfigManager import ConfigManager
import csv
import time
import json
from datetime import datetime

# for Log about peewee
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
# logger.addHandle
# r(logging.StreamHandler())

logging.basicConfig(level=logging.DEBUG)

BUY_FILE_NAME = 'buy_test_data.csv'
SELL_FILE_NAME = 'sell_test_data.csv'

class BaseModel(Model):
    class Meta:
        curConnectionParam = ConfigManager.getConnectionParams()
        db = MySQLDatabase(**curConnectionParam)
        database = db
        
class Buy(BaseModel):
    code = IntegerField()
    price = IntegerField()
    count = IntegerField()
    date = DateTimeField()
    reason = TextField()

class Sell(BaseModel):
    buy_id =  ForeignKeyField(Buy, related_name='buy_sell_relation')
    price = IntegerField()
    count = IntegerField()
    date = DateTimeField()
    reason = TextField()

class StockManagerDBHelper:

    # 存在しない場合のみTableを作成する
    @classmethod
    def createTables(cls):
        # dbインスタンスを使えば複数一気に処理できる
        # db.create_tables([Buy, Sell], True)
        Buy.create_table(True)
        Sell.create_table(True)
        
        # if not Buy.table_exists():
        #     Buy.create_table()
        
        # if not Sell.table_exists():
        #     Sell.create_table()
        
    @classmethod
    def dropTables(cls):
        Sell.drop_table()
        Buy.drop_table()

    @classmethod
    def saveBuyTestData(cls, csvfile):
    
        f = open(csvfile, "r")
        reader = csv.reader(f)
        # header = next(reader)
        
        for row in reader:
            print row
            buy_code = int(row[0])
            buy_price = int(row[1])
            buy_count = int(row[2])
            buy_date = row[3]
            buy_reason = unicode(row[4], 'utf_8')   

            Buy.create(
                code = buy_code, 
                price = buy_price,
                count = buy_count,
                date = buy_date,
                reason = buy_reason
                )
                
        f.close()

    @classmethod
    def saveSellTestData(cls, csvfile):
        
        f = open(csvfile, "r")
        reader = csv.reader(f)
        # header = next(reader)
        
        for row in reader:
            logging.debug ("row : %s", row)
            
            sell_buy_id = int(row[0])
            sell_price = int(row[1])
            sell_count = int(row[2])
            sell_date = row[3]
            sell_reason = unicode(row[4], 'utf_8')   

            Sell.create(
                buy_id = sell_buy_id, 
                price = sell_price,
                count = sell_count,
                date = sell_date,
                reason = sell_reason
                )
                
        f.close()

    @classmethod
    def saveBuyData(cls, buy_code, buy_price, buy_count, buy_date, buy_reason):
        logging.debug("buy %s, %s, %s, %s", buy_code, buy_price, buy_count, buy_date, buy_reason)
        Buy.create(
            code = buy_code, 
            price = buy_price,
            count = buy_count,
            date = buy_date,
            reason = buy_reason
            )

    @classmethod
    def saveSellData(cls, sell_buy_id, sell_price, sell_count, sell_date, sell_reason):
        logging.debug("sell %s, %s, %s, %s, %s", sell_buy_id, sell_price, sell_count, sell_date, sell_reason)
        Sell.create(
            buy_id = sell_buy_id, 
            price = sell_price,
            count = sell_count,
            date = sell_date,
            reason = sell_reason
            )

    @classmethod
    def makeJsonData(cls):
        json_data = []

        buy_datas = Buy.select()
        for buy_data in buy_datas :
            buy_id = buy_data.id
            buy_code = buy_data.code
            buy_price = buy_data.price
            buy_count = buy_data.count
            buy_date = buy_data.date
            buy_reason = buy_data.reason
            #logging.debug("buy [ %s, %s, %s, %s, %s, %s]", buy_id, buy_code, buy_price, buy_count, buy_date, buy_reason)
            buy_obj = { "id" : buy_id, "code" : buy_code , "price": buy_price, "count": buy_count, "date" : str(buy_date), "reason" : buy_reason}

            p_l_price = 0
            p_l_remain_count = buy_count

            sell_objs = []
            sell_datas = Sell.select().where(Sell.buy_id == buy_data.id)
            for sell_data in sell_datas :
                sell_price = sell_data.price
                sell_count = sell_data.count
                sell_date = sell_data.date
                sell_reason = sell_data.reason
                #logging.debug("sell [ %s, %s, %s, %s]", sell_price, sell_count, sell_date, sell_reason)
                sell_obj = { "price" : sell_price, "count" : sell_count, "date" : str(sell_date), "reason" : sell_reason}
                sell_objs.append(sell_obj)

                p_l_price = p_l_price + (sell_price - buy_price) * sell_count
                p_l_remain_count = p_l_remain_count - sell_count

            #logging.debug("p_l [ %s, %s ]", p_l_price, p_l_remain_count)
            p_l_obj = { "price" : p_l_price, "remain_count" : p_l_remain_count}

            data_obj = { "buy" : buy_obj, "sell" : sell_objs, "p_l" : p_l_obj}
            json_data.append(data_obj)
            #logging.debug("json_data %s", json_data)

        logging.debug("json_obj: %s", json_data)
        return json.dumps(json_data, ensure_ascii=False, indent = 4, sort_keys = True)

if __name__ == '__main__':
    logging.debug ("main start")

    StockManagerDBHelper.dropTables()
    StockManagerDBHelper.createTables()
    StockManagerDBHelper.saveBuyTestData(BUY_FILE_NAME)
    StockManagerDBHelper.saveSellTestData(SELL_FILE_NAME)

    #StockManagerDBHelper.makeJsonData()
    #　単体デバッグ用
    # stationId = StockManagerDBHelper.findStationId(u"稲荷町")
    # logging.debug (" stationId :  %d", stationId)
