import psycopg2

# Conexão com o banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname='seu_banco',
    user='seu_usuario',
    password='sua_senha',
    host='localhost'
)
cursor = conn.cursor()

# Criação de tabela
cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (id SERIAL PRIMARY KEY, nome VARCHAR(255))''')

# Inserção de dados
cursor.execute("INSERT INTO clientes (nome) VALUES ('Maria')")
conn.commit()

# Consulta de dados
cursor.execute("SELECT * FROM clientes")
print(cursor.fetchall())

# Fechamento da conexão
conn.close()
