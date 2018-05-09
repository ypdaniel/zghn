#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis, MySQLdb, json

def process_item():
    rediscli = redis.Redis(host="192.168.3.30", port="6379", db=0)

    mysqlcli = MySQLdb.connect(host="192.168.3.32", port=3306, user="root", passwd="123456", db="zghn", charset="utf8")

    offset = 0

    while True:
        try:
            source, data = rediscli.blpop("yy:items")

            cursor = mysqlcli.cursor()

            item = json.loads(data)

            cursor.execute("insert into sz_w_mm VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item['username'], item['age'], item['images_url'], item['content'], item['birthplace'], item['education'], item['income'], item['hobby'], item['source_url'], item['source']))

            mysqlcli.commit()

            cursor.close()

            offset += 1
            print offset

        except:
            pass


if __name__ == "__main__":
    process_item()

