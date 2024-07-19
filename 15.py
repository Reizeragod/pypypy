# Jogo da Forca
import random

# Lista de palavras
palavras = ["python", "computador", "livro", "carro", "casa"]

# Escolher uma palavra aleatória
palavra_secreta = random.choice(palavras)

# Criar uma lista de underlines para a palavra secreta
letras_descobertas = ["_"] * len(palavra_secreta)

# Número de tentativas
tentativas_restantes = 6

print("Bem-vindo ao Jogo da Forca!")
print("Adivinhe a palavra secreta!")

while True:
    print(" ".join(letras_descobertas))
    print(f"Você tem {tentativas_restantes} tentativas restantes.")

    # Pedir ao usuário para adivinhar uma letra
    palpite = input("Digite uma letra: ").lower()

    if palpite in palavra_secreta:
        # Atualizar as letras descobertas
        for i in range(len(palavra_secreta)):
            if palavra_secreta[i] == palpite:
                letras_descobertas[i] = palpite
    else:
        tentativas_restantes -= 1
        print("Essa letra não está na palavra.")

    # Verificar se o jogador venceu
    if "_" not in letras_descobertas:
        print(f"Parabéns! Você acertou a palavra secreta: {palavra_secreta}.")
        break

    # Verificar se o jogador perdeu
    if tentativas_restantes == 0:
        print(f"Que pena! A palavra secreta era: {palavra_secreta}.")
        break
