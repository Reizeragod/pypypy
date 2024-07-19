from pymongo import MongoClient

# Conexão com o banco de dados MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['meu_banco']
collection = db['usuarios']

# Inserção de dados
collection.insert_one({'nome': 'Carlos'})

# Consulta de dados
usuarios = collection.find()
for usuario in usuarios:
    print(usuario)

# Fechamento da conexão
client.close()
