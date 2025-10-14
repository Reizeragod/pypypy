import pandas as pd
import re

# Ajustando o caminho e o nome do arquivo de texto bruto
CAMINHO_ARQUIVO_BRUTO = 'C:/caminho/para/seu/relatorio_bruto.txt'
CAMINHO_ARQUIVO_EXCEL = 'C:/caminho/para/seu/Relatorio_Processado.xlsx'

# Definindo as posições de largura fixa 
# [Posição Inicial, Posição Final] (0-based)
# Exemplo: Se 'Est' vai do caractere 1 ao 4, e 'Mec' do 6 ao 10:
# [0, 4] e [5, 10]
colspecs = [
    (0, 5),   # Est
    (5, 11),  # Mec
    (11, 38), # Nome Mecânico
    (38, 45), # Ordem
    (45, 56), # Tarefa
    (57, 66), # Tp Pad
    (66, 77), # Dt Início
    (77, 88), # Dt Fatur
    (88, 98), # Vl Hora
    (98, 112),# Desconto
    (112, 123),# Tp Serviço
    (123, 136) # Fat. Líquido
]

# Definindo nomes das colunas
names = [
    'Est', 'Mec', 'Nome Mecânico', 'Ordem', 'Tarefa', 'Tp Pad', 
    'Dt Início', 'Dt Fatur', 'Vl Hora', 'Desconto', 'Tp Serviço', 'Fat. Líquido'
]

try:
    df = pd.read_fwf(
        CAMINHO_ARQUIVO_BRUTO,
        colspecs=colspecs,
        header=None, 
        names=names,
        encoding='latin-1' # Use 'latin-1' ou 'cp1252' se houver acentuação
    )

    df.dropna(subset=['Nome Mecânico', 'Tp Serviço'], how='all', inplace=True)
    df = df[~df['Nome Mecânico'].str.contains('Nome Mecânico|---', na=False)] # Remove cabeçalho e separadores

    colunas_preencher = ['Est', 'Mec', 'Nome Mecânico', 'Ordem']
    df[colunas_preencher] = df[colunas_preencher].ffill()

    def limpar_numero(texto):
        if isinstance(texto, str):
            
            texto_limpo = texto.replace('.', '').replace(',', '.')
            
            try:
                return pd.to_numeric(texto_limpo)
            except ValueError:
                return None
        return texto 

    colunas_numericas = ['Tp Pad', 'Vl Hora', 'Desconto', 'Fat. Líquido']
    for col in colunas_numericas:
        df[col] = df[col].apply(limpar_numero)

    # Filtro Final
    df_filtrado = df[df['Tp Serviço'].str.strip() == 'FATURAMENT']

    # Exportação para Excel
    df_filtrado.to_excel(CAMINHO_ARQUIVO_EXCEL, index=False, sheet_name='Faturamento')
    
    print(f"Processamento concluído. {len(df_filtrado)} linhas exportadas para {CAMINHO_ARQUIVO_EXCEL}")

except FileNotFoundError:
    print(f"Erro: Arquivo não encontrado no caminho: {CAMINHO_ARQUIVO_BRUTO}")
except Exception as e:
    print(f"Ocorreu um erro durante o processamento: {e}")