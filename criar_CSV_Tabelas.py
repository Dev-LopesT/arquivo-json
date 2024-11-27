import sqlite3
import csv

conn = sqlite3.connect('banco_de_dados.db')
cursor = conn.cursor()

def exportar_para_csv(nome_tabela, nome_arquivo):
  
    cursor.execute(f'SELECT * FROM {nome_tabela}')
    dados = cursor.fetchall()
    colunas = [descricao[0] for descricao in cursor.description]
    
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerow(colunas)
        escritor_csv.writerows(dados)
        
    print(f'Arquivo {nome_arquivo} criado com sucesso! \n Para Arquivo {nome_arquivo}')

tabelas = [
    'funcionarios',
    'cargos',
    'departamentos',
    'historico_salarios',
    'dependentes',
    'projetos_desenvolvidos',
    'recursos_do_projeto'
] 

for tabela in tabelas:
    exportar_para_csv(tabela, f'{tabela}.csv')
    
conn.close()