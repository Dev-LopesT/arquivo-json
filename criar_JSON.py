import sqlite3
import json

def consulta_media_salarios_por_departamento():
    # Conectar ao banco de dados
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    # Consulta SQL
    query = '''
    SELECT d.nome_departamento, AVG(f.salario) AS media_salario
    FROM projetos_desenvolvidos p
    JOIN funcionarios f ON p.id_funcionario = f.id_funcionario
    JOIN departamentos d ON f.id_departamento = d.id_departamento
    WHERE p.status = 'Concluído'
    GROUP BY d.id_departamento;
    '''

    # Executar a consulta
    cursor.execute(query)

    # Recuperar os resultados
    resultados = cursor.fetchall()

    # Estrutura dos dados em formato JSON
    dados_json = []
    for row in resultados:
        dados_json.append({
            'departamento': row[0],
            'media_salario': row[1]
        })

    # Fechar a conexão
    conn.close()

    # Salvar os dados no arquivo JSON
    with open('media_salarios_por_departamento.json', 'w', encoding="utf-8") as file:
        json.dump(dados_json, file, indent=4,  ensure_ascii=False)

# Chamar a função
consulta_media_salarios_por_departamento()

def consulta_recursos_mais_usados():
    # Conectar ao banco de dados
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    # Consulta SQL
    query = '''
    SELECT r.descricao, SUM(r.quantidade) AS total_quantidade
    FROM recursos_projeto r
    GROUP BY r.descricao
    ORDER BY total_quantidade DESC
    LIMIT 3;
    '''

    # Executar a consulta
    cursor.execute(query)

    # Recuperar os resultados
    resultados = cursor.fetchall()

    # Estrutura dos dados em formato JSON
    dados_json = []
    for row in resultados:
        dados_json.append({
            'recurso': row[0],
            'quantidade_total': row[1]
        })

    # Fechar a conexão
    conn.close()

    # Salvar os dados no arquivo JSON
    with open('recursos_mais_usados.json', 'w', encoding="utf-8") as file:
        json.dump(dados_json, file, indent=4, ensure_ascii=False)

# Chamar a função
consulta_recursos_mais_usados()

def consulta_projeto_com_mais_dependentes():
    # Conectar ao banco de dados
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    # Consulta SQL
    query = '''
    SELECT p.nome_projeto, COUNT(d.id_dependente) AS num_dependentes
    FROM projetos_desenvolvidos p
    JOIN funcionarios f ON p.id_funcionario = f.id_funcionario
    LEFT JOIN dependentes d ON f.id_funcionario = d.id_funcionario
    GROUP BY p.id_projeto
    ORDER BY num_dependentes DESC
    LIMIT 1;
    '''

    # Executar a consulta
    cursor.execute(query)

    # Recuperar o resultado
    resultado = cursor.fetchone()

    # Estrutura dos dados em formato JSON
    dados_json = {}
    if resultado:
        dados_json = {
            'projeto': resultado[0],
            'num_dependentes': resultado[1]
        }

    # Fechar a conexão
    conn.close()

    # Salvar os dados no arquivo JSON
    with open('projeto_com_mais_dependentes.json', 'w', encoding="utf-8") as file:
        json.dump(dados_json, file, indent=4,  ensure_ascii=False)

# Chamar a função
consulta_projeto_com_mais_dependentes()
