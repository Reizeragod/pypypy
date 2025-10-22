from tinydb import TinyDB, Query

db = TinyDB('inventory.json')
Item = Query()

def adicionar_item(nome, quantidade, preco):
    db.insert({'nome': nome, 'quantidade': quantidade, 'preco': preco})
    print(f"Item '{nome}' adicionado ao inventário.")

def atualizar_quantidade(nome, nova_quantidade):
    db.update({'quantidade': nova_quantidade}, Item.nome == nome)
    print(f"Quantidade de '{nome}' atualizada para {nova_quantidade}.")

def listar_estoque_baixo(min_qtd):
    return db.search(Item.quantidade < min_qtd)

db.truncate()

adicionar_item("Teclado", 100, 50.00)
adicionar_item("Mouse", 20, 25.00)
adicionar_item("Monitor", 5, 300.00)

atualizar_quantidade("Teclado", 95)

print("\nItens com estoque abaixo de 10:")
print(listar_estoque_baixo(10))