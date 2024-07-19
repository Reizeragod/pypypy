import sqlite3

# Criação de uma conexão com o banco de dados SQLite
conn = sqlite3.connect('exemplo.db')
cursor = conn.cursor()

# Criação de uma tabela
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT)''')

# Inserção de dados
cursor.execute("INSERT INTO usuarios (nome) VALUES ('João')")
conn.commit()

# Consulta de dados
cursor.execute("SELECT * FROM usuarios")
print(cursor.fetchall())

# Fechamento da conexão
conn.close()
