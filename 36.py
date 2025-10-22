from tinydb import TinyDB, Query

db = TinyDB('votes.json')
Post = Query()

def adicionar_post(titulo):
    db.insert({'titulo': titulo, 'likes': 0, 'dislikes': 0})
    print(f"Post '{titulo}' criado.")

def dar_like(titulo):
    db.update_multiple([({'likes': Post.likes + 1}, Post.titulo == titulo)])
    print(f"Like adicionado ao post '{titulo}'.")

def ver_votos(titulo):
    return db.get(Post.titulo == titulo)

db.truncate()

adicionar_post("Melhor linguagem é Python")
adicionar_post("MongoDB é NoSQL")

dar_like("Melhor linguagem é Python")
dar_like("Melhor linguagem é Python")
dar_like("MongoDB é NoSQL")

print("\nVotos do post 'Melhor linguagem é Python':")
print(ver_votos("Melhor linguagem é Python"))