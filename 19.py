import mysql.connector

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='seu_usuario',
    password='sua_senha',
    database='seu_banco'
)
cursor = conn.cursor()

# Criação de tabela
cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255))''')

# Inserção de dados
cursor.execute("INSERT INTO produtos (nome) VALUES ('Produto A')")
conn.commit()

# Consulta de dados
cursor.execute("SELECT * FROM produtos")
print(cursor.fetchall())

# Fechamento da conexão
conn.close()
