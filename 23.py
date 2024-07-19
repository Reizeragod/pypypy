import sqlite3

# Criação de uma conexão com o banco de dados SQLite
conn = sqlite3.connect('tarefas.db')
cursor = conn.cursor()

# Criação de uma tabela para tarefas
cursor.execute('''
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY,
    descricao TEXT NOT NULL,
    concluida BOOLEAN NOT NULL DEFAULT 0
)
''')

# Função para adicionar uma nova tarefa
def adicionar_tarefa(descricao):
    cursor.execute("INSERT INTO tarefas (descricao) VALUES (?)", (descricao,))
    conn.commit()
    print(f'Tarefa adicionada: {descricao}')

# Função para listar todas as tarefas
def listar_tarefas():
    cursor.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()
    for tarefa in tarefas:
        status = "Concluída" if tarefa[2] else "Pendente"
        print(f'ID: {tarefa[0]}, Descrição: {tarefa[1]}, Status: {status}')

# Função para atualizar uma tarefa
def atualizar_tarefa(tarefa_id, concluida):
    cursor.execute("UPDATE tarefas SET concluida = ? WHERE id = ?", (concluida, tarefa_id))
    conn.commit()
    print(f'Tarefa ID {tarefa_id} atualizada.')

# Função para excluir uma tarefa
def excluir_tarefa(tarefa_id):
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conn.commit()
    print(f'Tarefa ID {tarefa_id} excluída.')

# Adicionando algumas tarefas
adicionar_tarefa("Estudar Python")
adicionar_tarefa("Fazer compras")
adicionar_tarefa("Ir ao ginásio")

# Listando tarefas
print("\nLista de Tarefas:")
listar_tarefas()

# Atualizando uma tarefa
atualizar_tarefa(1, True)

# Listando tarefas novamente
print("\nLista de Tarefas Atualizada:")
listar_tarefas()

# Excluindo uma tarefa
excluir_tarefa(2)

# Listando tarefas finais
print("\nLista de Tarefas Finais:")
listar_tarefas()

# Fechamento da conexão
conn.close()
