import os
class Config():
    db_host:            str = os.getenv('db_host', 'mongodb+srv://jkl:Ii5ImtkQ06i754FV@cluster0.ev0dhqn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db_name:            str = os.getenv('db_name', 'blog_db')
    hash_secret:        str = os.getenv('secret', 'affdf98c14d3e6ac5b4b95017f3ccc5f9ad9272066506f680ceae9264867d8cc')

config = Config()
