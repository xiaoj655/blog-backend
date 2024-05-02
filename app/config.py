import os

class Config():
    db_host:            str = os.getenv('db_host', '172.23.16.1')
    db_name:            str = os.getenv('db_name', 'blog_db')
    hash_secret:        str = os.getenv('secret', 'affdf98c14d3e6ac5b4b95017f3ccc5f9ad9272066506f680ceae9264867d8cc')

config = Config()