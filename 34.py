from tinydb import TinyDB, Query

db = TinyDB('config.json')
Config = Query()

def salvar_config(chave, valor):
    """Atualiza ou insere uma configuração."""
    if not db:
        db.insert({})
    
    config_doc = db.get(doc_id=1)
    if config_doc is None: 
        db.insert({chave: valor})
    else:
        db.update({chave: valor}, doc_ids=[1])

    print(f"Configuração '{chave}' salva.")

def obter_config(chave):
    """Obtém o valor de uma configuração."""
    config_doc = db.get(doc_id=1)
    return config_doc.get(chave) if config_doc else None

db.truncate()

salvar_config("tema", "dark")
salvar_config("tamanho_fonte", 14)

print("\nTema atual:")
print(obter_config("tema"))