from tinydb import TinyDB, Query

db = TinyDB('tasks.json')
Task = Query()

def adicionar_tarefa(descricao):
    db.insert({'descricao': descricao, 'concluida': False})
    print(f"Tarefa '{descricao}' adicionada.")

def marcar_concluida(descricao):
    db.update({'concluida': True}, Task.descricao == descricao)
    print(f"Tarefa '{descricao}' marcada como concluída.")

def listar_pendentes():
    return db.search(Task.concluida == False)

db.truncate()

adicionar_tarefa("Comprar leite")
adicionar_tarefa("Estudar Python")
marcar_concluida("Comprar leite")

print("\nTarefas Pendentes:")
print(listar_pendentes())