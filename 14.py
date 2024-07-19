# Gerador de Senhas
import random
import string

print("Bem-vindo ao Gerador de Senhas!")

tamanho_senha = int(input("Digite o tamanho da senha desejada: "))

caracteres = string.ascii_letters + string.digits + string.punctuation

senha = ''.join(random.choice(caracteres) for i in range(tamanho_senha))

print(f"Sua senha é: {senha}")
