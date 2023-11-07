import mysql.connector

# Variáveis para fazer a conexão com o banco de dados
myDb = mysql.connector.connect(
    user='root',
    host='localhost',
    password='',
    database='usersdatabase'
)