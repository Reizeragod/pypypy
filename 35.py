from tinydb import TinyDB, Query

db = TinyDB('perfil.json')
Perfil = Query()

def salvar_perfil(nome, rua, cidade, hobbies):
    perfil_data = {
        'nome': nome,
        'endereco': {
            'rua': rua,
            'cidade': cidade
        },
        'hobbies': hobbies
    }
    db.insert(perfil_data)
    print(f"Perfil de '{nome}' salvo.")

def buscar_por_cidade(cidade):
    return db.search(Perfil.endereco.cidade == cidade)

db.truncate()

salvar_perfil("Carla", "Rua A", "São Paulo", ["leitura", "natação"])
salvar_perfil("David", "Avenida B", "São Paulo", ["cinema", "programação"])
salvar_perfil("Eva", "Rua C", "Rio de Janeiro", ["culinária"])

print("\nPerfis em São Paulo:")
print(buscar_por_cidade("São Paulo"))