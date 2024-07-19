# Calculadora Simples
print("Bem-vindo à Calculadora Simples!")

numero1 = float(input("Digite o primeiro número: "))
numero2 = float(input("Digite o segundo número: "))

operacao = input("Escolha a operação (+, -, *, /): ")

if operacao == "+":
    resultado = numero1 + numero2
    print(f"O resultado é: {resultado}")
elif operacao == "-":
    resultado = numero1 - numero2
    print(f"O resultado é: {resultado}")
elif operacao == "*":
    resultado = numero1 * numero2
    print(f"O resultado é: {resultado}")
elif operacao == "/":
    if numero2 == 0:
        print("Erro: Não é possível dividir por zero.")
    else:
        resultado = numero1 / numero2
        print(f"O resultado é: {resultado}")
else:
    print("Operação inválida.")
