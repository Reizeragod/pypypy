from tinydb import TinyDB, Query
from datetime import datetime, timedelta

db = TinyDB('cache.json')
Cache = Query()

def set_cache(chave, valor, ttl_segundos=60):
    expira_em = datetime.now() + timedelta(seconds=ttl_segundos)
    expira_em_str = expira_em.isoformat()

    db.upsert({'chave': chave, 'valor': valor, 'expira_em': expira_em_str}, Cache.chave == chave)
    print(f"Chave '{chave}' armazenada no cache.")

def get_cache(chave):
    item = db.get(Cache.chave == chave)
    
    if item:
        data_expiracao = datetime.fromisoformat(item['expira_em'])
        if datetime.now() < data_expiracao:
            return item['valor']
        else:
            db.remove(Cache.chave == chave)
            print(f"Chave '{chave}' expirada e removida.")
            return None
    return None

db.truncate()

set_cache("dados_usuario_1", {"nome": "Zeca", "session": "abc123"}, ttl_segundos=10)

print("\nTentativa 1 (imediata):", get_cache("dados_usuario_1"))
