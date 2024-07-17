if __name__ == '__main__':
    n = int(input())
    alunos = []
    
    for _ in range(n):
        nome = input()
        nota = float(input())
        alunos.append([nome, nota])
    
    # Ordenar a lista de alunos por nota
    alunos.sort(key=lambda x: x[1])
    
    # Encontrar a segunda menor nota
    segunda_menor_nota = None
    for nota in [aluno[1] for aluno in alunos]:
        if nota != alunos[0][1]:
            segunda_menor_nota = nota
            break
    
    # Imprimir os nomes dos alunos com a segunda menor nota
    nomes = [aluno[0] for aluno in alunos if aluno[1] == segunda_menor_nota]
    nomes.sort()
    for nome in nomes:
        print(nome)
