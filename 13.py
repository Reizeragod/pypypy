# Conversor de Temperatura
print("Bem-vindo ao Conversor de Temperatura!")

temperatura = float(input("Digite a temperatura: "))
unidade_origem = input("Digite a unidade de origem (C, F ou K): ")
unidade_destino = input("Digite a unidade de destino (C, F ou K): ")

if unidade_origem == "C" and unidade_destino == "F":
    temperatura_convertida = (temperatura * 9/5) + 32
    print(f"{temperatura}°C é igual a {temperatura_convertida:.2f}°F.")
elif unidade_origem == "C" and unidade_destino == "K":
    temperatura_convertida = temperatura + 273.15
    print(f"{temperatura}°C é igual a {temperatura_convertida:.2f}K.")
elif unidade_origem == "F" and unidade_destino == "C":
    temperatura_convertida = (temperatura - 32) * 5/9
    print(f"{temperatura}°F é igual a {temperatura_convertida:.2f}°C.")
elif unidade_origem == "F" and unidade_destino == "K":
    temperatura_convertida = (temperatura - 32) * 5/9 + 273.15
    print(f"{temperatura}°F é igual a {temperatura_convertida:.2f}K.")
elif unidade_origem == "K" and unidade_destino == "C":
    temperatura_convertida = temperatura - 273.15
    print(f"{temperatura}K é igual a {temperatura_convertida:.2f}°C.")
elif unidade_origem == "K" and unidade_destino == "F":
    temperatura_convertida = (temperatura - 273.15) * 9/5 + 32
    print(f"{temperatura}K é igual a {temperatura_convertida:.2f}°F.")
else:
    print("Unidade de temperatura inválida.")
