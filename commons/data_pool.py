#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/11
  @todo: need add another pi port
"""
import sqlite3
import os

class data_pool(object):
    instance = None
    max_size = 100

    database_file_path = '../data/terminal.db'
    pi_table_name ='pis'
    data_table_name = 'datas'
    img_table_name = 'imgs'


    def __init__(self):
        self.connect_database(self.database_file_path)
        init_sql = '''CREATE TABLE IF NOT EXISTS `{0}`
                  (`date` int(32) NOT NULL,
                   `value` VARCHAR(256) NOT NULL
                    )'''.format(self.data_table_name)
        self.create_table(init_sql)

        init_sql = '''CREATE TABLE IF NOT EXISTS `{0}`
                  (`date` int(32) NOT NULL,
                   `value` VARCHAR(256) NOT NULL
                    )'''.format(self.pi_table_name)
        self.create_table(init_sql)

        init_sql = '''CREATE TABLE IF NOT EXISTS `{0}`
                  (`date` int(32) NOT NULL,
                  `key` VARCHAR(32) NOT NULL,
                   `value` VARCHAR(256) NOT NULL
                    )'''.format(self.img_table_name)
        self.create_table(init_sql)

    def connect_database(self,path):
        self.conn = sqlite3.connect(path)
        if not os.path.exists(path) or not os.path.isfile(path):
            self.conn = sqlite3.connect(':memory:')

    def get_cursor(self):
        if self.conn is None:
            self.connect_database(self.database_file_path)
        return self.conn.cursor()

    def close_all(self):
        if self.conn is not None:
            self.conn.cursor().close()
            self.conn.close()
            self.conn = None

    @staticmethod
    def get_instance():
        if data_pool.instance == None:
            data_pool.instance = data_pool()
        return data_pool.instance

    def save_data(self, ms, data):
        save_sql = "INSERT INTO {0} values (?, ?)".format(self.data_table_name)
        save_data = [(ms,data)]
        self.save(save_sql, save_data)
    def get_data(self, count):
        sql = "SELECT * FROM {0} LIMIT {1}".format(self.data_table_name, count)
        return self.fetchall(sql)
    def del_data(self, values):
        sql = "DELETE FROM {0} WHERE `date` = ? AND `value` = ?".format(self.data_table_name)
        self.delete(sql, values)

    def save_pi(self, ms, pi):
        save_sql = "INSERT INTO {0} values (?, ?)".format(self.pi_table_name)
        save_data = [(ms,pi)]
        self.save(save_sql, save_data)

    def get_pi_value(self):
        sql = "SELECT * FROM {0}".format(self.pi_table_name)
        pis = self.fetchall(sql)
        sum_pis = 0
        for pi in pis:
            sum_pis+= int(pi[1])
        #delete
        del_sql = "DELETE FROM {0} WHERE `date`= ? AND `value`=?".format(self.pi_table_name)
        self.delete(del_sql,pis)
        return sum_pis

    def save_img(self, ms, key, img_path):
        save_sql = "INSERT INTO {0} values (?,?,?)".format(self.img_table_name)
        save_data = [(ms,key,img_path)]
        self.save(save_sql, save_data)

    def get_imgs(self, count):
        sql = "SELECT * FROM {0} LIMIT {1}".format(self.img_table_name, count)
        return self.fetchall(sql)

    def del_img(self, img):
        sql = "DELETE FROM {0} WHERE `date`= ? AND `key`=? AND `value` = ?".format(self.img_table_name)
        self.delete(sql, img)

    def create_table(self, sql):
        if sql is not None and sql != '':
            cu = self.get_cursor()
            cu.execute(sql)
            self.conn.commit()
            self.close_all()

    def save(self, sql, data):
        if sql is not None and sql !='':
            if data is not None:
                cu = self.get_cursor()
                if cu is not None:
                    for d in data:
                        cu.execute(sql, d)
                        self.conn.commit()
                        self.close_all()


    def fetchall(self, sql):
        if sql is not None and sql != '':
            cu = self.get_cursor()
            cu.execute(sql)
            r = cu.fetchall()
            return r

    def fetchone(self, sql, data):
        if sql is not None and sql!='':
            if data is not None:
                d = (data,)
                cu = self.get_cursor()
                cu.execute(sql, d)
                r = cu.fetchall()
                return r

    def delete(self, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_cursor()
                for d in data:
                    cu.execute(sql, d)
                    self.conn.commit()
if __name__ == "__main__":
    dp = data_pool.get_instance()
    imgs = dp.get_imgs(5)
    print imgs
    #dp.del_img(imgs)
    datas = dp.get_data(100)
    print len(datas)
    #dp.del_data(datas)
    
    
