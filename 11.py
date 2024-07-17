# Leitura do script da matriz
script_matriz = "Tsi\nh%x\ni#\nsM\n$a\n#t\nr!\ni"

# Separacao das linhas do script
linhas_script = script_matriz.split('\n')

# Determinacao do numero de linhas e colunas
num_linhas = len(linhas_script)
num_colunas = len(linhas_script[0])

# Criacao da matriz
matriz = []
for linha in linhas_script:
    linha_matriz = list(linha)
    matriz.append(linha_matriz)

# Decodificacao da matriz
script_decodificado = ""
for coluna in range(num_colunas):
    for linha in range(num_linhas):
        caractere = matriz[linha][coluna]
        if caractere.isalnum():
            script_decodificado += caractere
        elif caractere != " ":
            script_decodificado += " "

# Exibicao do resultado
print("Visao Geral:")
print(script_decodificado.strip())
#deu errado sa merda