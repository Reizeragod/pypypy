import tkinter as tk
import os

def exibir_tabuleiro(botoes):
    for i in range(3):
        for j in range(3):
            botoes[i*3 + j].config(text=botoes[i*3 + j].cget("text"))

def verificar_vencedor(tabuleiro, simbolo):
    # Verificar linhas
    for i in range(0, 9, 3):
        if tabuleiro[i].get() == tabuleiro[i+1].get() == tabuleiro[i+2].get() == simbolo:
            return True
    # Verificar colunas
    for i in range(3):
        if tabuleiro[i].get() == tabuleiro[i+3].get() == tabuleiro[i+6].get() == simbolo:
            return True
    # Verificar diagonais
    if tabuleiro[0].get() == tabuleiro[4].get() == tabuleiro[8].get() == simbolo:
        return True
    if tabuleiro[2].get() == tabuleiro[4].get() == tabuleiro[6].get() == simbolo:
        return True
    return False

def marcar_posicao(tabuleiro, posicao):
    global jogador_atual
    if tabuleiro[posicao].get() == " ":
        tabuleiro[posicao].set(jogador_atual)
        if verificar_vencedor(tabuleiro, jogador_atual):
            exibir_tabuleiro(tabuleiro)
            print(f"O jogador {jogador_atual} venceu!")
            return
        if " " not in [botao.get() for botao in tabuleiro]:
            exibir_tabuleiro(tabuleiro)
            print("Empate!")
            return
        if jogador_atual == "X":
            jogador_atual = "O"
        else:
            jogador_atual = "X"
    else:
        print("Essa posição já está ocupada. Tente novamente.")

def jogo_da_velha(janela):
    global jogador_atual
    jogador_atual = "X"
    tabuleiro = [tk.StringVar() for _ in range(9)]
    botoes = [tk.Button(janela, textvariable=tabuleiro[i], width=5, height=2, command=lambda i=i: marcar_posicao(tabuleiro, i)) for i in range(9)]
    for i in range(3):
        for j in range(3):
            botoes[i*3 + j].grid(row=i, column=j)

    while True:
        exibir_tabuleiro(botoes)
        print(f"Vez do jogador {jogador_atual}.")
        posicao = int(input("Digite a posição (0-8): "))
        marcar_posicao(tabuleiro, posicao)

def hub():
    janela = tk.Tk()
    janela.title("Hub de Jogos")

    def iniciar_jogo_da_velha():
        janela.destroy()
        jogo_da_velha(tk.Tk())

    botao_jogo_da_velha = tk.Button(janela, text="Jogar Jogo da Velha", command=iniciar_jogo_da_velha)
    botao_jogo_da_velha.pack(pady=20)

    botao_sair = tk.Button(janela, text="Sair", command=janela.destroy)
    botao_sair.pack(pady=20)

    janela.mainloop()

if __name__ == "__main__":
    hub()
