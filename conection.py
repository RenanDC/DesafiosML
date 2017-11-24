import sys
import pymysql
import MySQLdb

def conn():
  try:
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "kei110891",
                            db = "email_db")
    return conn
  except:
    exit("sorry can't connect")
