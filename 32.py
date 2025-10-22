from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB('logs.json')
Log = Query()

def registrar_log(nivel, mensagem):
    timestamp = datetime.now().isoformat()
    db.insert({'nivel': nivel, 'mensagem': mensagem, 'timestamp': timestamp})
    print(f"Log [{nivel}] registrado em {timestamp}")

def buscar_logs_de_erro():
    return db.search(Log.nivel == 'ERRO')

db.truncate()

registrar_log("INFO", "Aplicação iniciada.")
registrar_log("ERRO", "Falha na conexão com o serviço externo.")
registrar_log("INFO", "Usuário logado.")

print("\nLogs de ERRO:")
print(buscar_logs_de_erro())