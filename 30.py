from tinydb import TinyDB, Query

db = TinyDB('users.json')
User = Query()

def adicionar_usuario(nome, email, idade):
    """Adiciona um novo usuário ao banco de dados."""
    db.insert({'nome': nome, 'email': email, 'idade': idade})
    print(f"Usuário '{nome}' adicionado com sucesso.")

def buscar_por_email(email):
    """Busca um usuário por email."""
    resultado = db.search(User.email == email)
    return resultado

def listar_todos_usuarios():
    """Lista todos os usuários."""
    return db.all()

db.truncate()

adicionar_usuario("Alice", "alice@example.com", 30)
adicionar_usuario("Bob", "bob@example.com", 25)

print("\nBuscando Alice:")
print(buscar_por_email("alice@example.com"))

print("\nTodos os usuários:")
print(listar_todos_usuarios())