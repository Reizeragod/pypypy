#Calcule a soma dos elementos de uma lista.
#@Mateus Reis

numeros = []

for i in range(5):
    numero = int(input(f"Digite o {i+1}º número: "))
    
    numeros.append(numero)
    
    soma_total = sum(numeros)

print("A soma de todos os números digitados é:", soma_total)