import json
import psycopg2
import sys

class DBWriterPipeline(object):
    def __init__(self):
        self.file = open('items', 'wb')
        self.con = None

    def open_spider(self, spider):
        try:
            self.con = psycopg2.connect(database='spiderdb', user='kira')
            cur = self.con.cursor()
            print("connected")
            cur.execute("CREATE TABLE IF NOT EXISTS picture (id SERIAL PRIMARY KEY, pic_link VARCHAR(2083) NOT NULL, pic_src VARCHAR(2083) NOT NULL, site varchar(200) NOT NULL);")
            cur.execute("CREATE TABLE IF NOT EXISTS search_query (id SERIAL PRIMARY KEY, phrase VARCHAR(500) NOT NULL, picture integer REFERENCES picture (id));")
            print("created")
        except:
            print("psycopg2.CreateError")
            if self.con:
                self.con.rollback()
        finally:
            if self.con:
                self.con.commit()


    def close_spider(self, spider):
        if self.con:
            self.con.close()

    def process_item(self, item, spider):
        item = dict(item)
        cur = self.con.cursor()
        for key,val in item.items():
            try:
                #query = "INSERT INTO picture (pic_link, pic_src, site) VALUES ('{}', '{}','google.com') RETURNING id;".format(key, val)
                query = "INSERT INTO picture (pic_link, pic_src, site) VALUES ('"+key+"', '"+val+"','"+spider.name+"') RETURNING id;"
                cur.execute(query)
                id = cur.fetchone()[0]
                print("inserted", id)
                query = "INSERT INTO search_query (phrase, picture) VALUES( '" + spider.search_phrase + "', " + str(id) + ");"
                cur.execute(query)
            except:
                print("psycopg2.InsertError")
            finally:
                if self.con:
                    self.con.commit()
        return item


