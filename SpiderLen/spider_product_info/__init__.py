from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.mydb
my_set = db.test_set
my_set.insert({"name":"zhangsan","age":18})