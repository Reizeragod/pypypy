from tinydb import TinyDB, Query

db = TinyDB('sales.json')
Sale = Query()

def registrar_venda(produto, quantidade, valor_unitario):
    valor_total = quantidade * valor_unitario
    db.insert({'produto': produto, 'quantidade': quantidade, 'valor_total': valor_total})
    print(f"Venda de '{produto}' registrada. Total: {valor_total:.2f}")

def calcular_total_vendas_por_produto(produto):
    vendas = db.search(Sale.produto == produto)
    total = sum(venda['valor_total'] for venda in vendas)
    return total

db.truncate()

registrar_venda("Laptop", 1, 1500.00)
registrar_venda("Mouse", 5, 25.00)
registrar_venda("Laptop", 2, 1500.00)
registrar_venda("Teclado", 3, 50.00)

total_laptop = calcular_total_vendas_por_produto("Laptop")
print(f"\nTotal vendido de Laptop: R$ {total_laptop:.2f}")