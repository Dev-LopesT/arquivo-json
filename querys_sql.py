import sqlite3



def consulta_media_salarios_por_departamento():
    """
    Realiza uma consulta no banco de dados SQLite para calcular a média salarial dos funcionários 
    responsáveis por projetos concluídos, agrupados por departamento.

    A consulta junta as tabelas `funcionarios`, `projetos_desenvolvidos` e `departamentos` para
    recuperar os funcionários que estão associados a projetos com o status 'Concluído'. 
    Em seguida, calcula a média salarial desses funcionários, agrupando os resultados por 
    departamento e exibindo o nome do departamento juntamente com a média salarial.

    A função exibe os resultados no formato:
    "Departamento: [nome_departamento], Média Salarial: [valor_média]".

    A conexão com o banco de dados é fechada após a execução da consulta.
    """
    
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    
    query_um = '''
    SELECT d.nome_departamento, AVG(f.salario) AS media_salario
    FROM funcionarios f
    JOIN projetos_desenvolvidos p ON f.id_funcionario = p.id_funcionario
    JOIN departamentos d ON f.id_departamento = d.id_departamento
    WHERE p.status = 'Concluído'
    GROUP BY d.id_departamento;
    '''
 
    cursor.execute(query_um)

  
    resultados = cursor.fetchall()

    print("CONSULTA 1 - Trazer a média dos salários (atual) dos funcionários responsáveis por projetos concluídos, agrupados por departamento.")
    for row in resultados:
        print(f"Departamento: {row[0]}, Média Salarial: {row[1]:.2f}")

    conn.close()


consulta_media_salarios_por_departamento()



def consulta_top_3_recursos_materiais():
    """
    Realiza uma consulta no banco de dados SQLite para identificar os três recursos materiais 
    mais utilizados nos projetos, listando a descrição do recurso e a quantidade total usada.

    A consulta filtra os recursos do tipo 'Material' na tabela `recursos_projeto`, soma a quantidade 
    de cada recurso e agrupa os resultados pela descrição do recurso. Os resultados são ordenados pela 
    quantidade total usada, de forma decrescente, e limitados aos três primeiros recursos mais usados.

    A função exibe os resultados no formato:
    "Recurso: [descricao_recurso], Quantidade Total Usada: [quantidade_total]".

    A conexão com o banco de dados é fechada após a execução da consulta.
    """
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

   
    query = '''
    SELECT r.descricao, SUM(r.quantidade) AS quantidade_total
    FROM recursos_projeto r
    WHERE r.tipo = 'Material'
    GROUP BY r.descricao
    ORDER BY quantidade_total DESC
    LIMIT 3;
    '''

    cursor.execute(query)

    resultados = cursor.fetchall()

    print("CONSULTA 2 - Identificar os três recursos materiais mais usados nos projetos, listando a descrição do recurso e a quantidade total usada. ")
    for row in resultados:
        print(f"Recurso: {row[0]}, Quantidade Total Usada: {row[1]:.2f}")

    conn.close()

consulta_top_3_recursos_materiais()

def consulta_custo_total_por_departamento():
    """
    Realiza uma consulta no banco de dados SQLite para calcular o custo total dos projetos 
    concluídos, agrupados por departamento.

    A consulta soma os valores das colunas `custo_estimado` e `custo_atual` da tabela 
    `projetos_desenvolvidos` para cada projeto com o status 'Concluído'. Os resultados são 
    agrupados por departamento, com base no `id_departamento` da tabela `departamentos`.

    A função exibe os resultados no formato:
    "Departamento: [nome_departamento], Custo Total: [valor_total]".

    A conexão com o banco de dados é fechada após a execução da consulta.
    """
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

 
    query = '''
    SELECT d.nome_departamento, SUM(p.custo_estimado + p.custo_atual) AS custo_total
    FROM projetos_desenvolvidos p
    JOIN departamentos d ON p.id_funcionario = d.id_gerente
    WHERE p.status = 'Concluído'
    GROUP BY d.id_departamento;
    '''

    cursor.execute(query)

 
    resultados = cursor.fetchall()

    print("CONSULTA 3 - Calcular o custo total dos projetos por departamento, considerando apenas os projetos 'Concluídos'. ")
    for row in resultados:
        print(f"Departamento: {row[0]}, Custo Total: {row[1]:.2f}")

    
    conn.close()


consulta_custo_total_por_departamento()


def consulta_projetos_em_execucao():
    """
    Realiza uma consulta no banco de dados SQLite para listar todos os projetos que estão 
    'Em Execução', com seus respectivos detalhes.

    A consulta seleciona o nome do projeto, o custo total (soma do custo estimado e custo atual), 
    a data de início, a data de conclusão e o nome do funcionário responsável. A junção entre 
    as tabelas `projetos_desenvolvidos` e `funcionarios` é feita através da coluna `id_funcionario` 
    para recuperar o nome do responsável.

    A consulta filtra os projetos com o status 'Em Execução' e exibe as informações no formato:
    "Projeto: [nome_projeto], Custo Total: [valor_total], Início: [data_inicio], 
    Conclusão: [data_conclusao], Responsável: [nome_funcionario]".

    A conexão com o banco de dados é fechada após a execução da consulta.
    """
    
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    
    query = '''
    SELECT p.nome_projeto, (p.custo_estimado + p.custo_atual) AS custo_total, p.data_inicio, p.data_conclusao, f.nome_funcionario
    FROM projetos_desenvolvidos p
    JOIN funcionarios f ON p.id_funcionario = f.id_funcionario
    WHERE p.status = 'Em Execução';
    '''

    
    cursor.execute(query)

    resultados = cursor.fetchall()

    print("CONSULTA 4 - Listar todos os projetos com seus respectivos nomes, custo, data de início, data de conclusão e o nome do funcionário responsável, que estejam 'Em Execução'.")
    for row in resultados:
        print(f"Projeto: {row[0]}, Custo Total: {row[1]:.2f}, Início: {row[2]}, Conclusão: {row[3]}, Responsável: {row[4]}")
 
    conn.close()

consulta_projetos_em_execucao()



def consulta_projeto_com_mais_dependentes():
  
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

   
    query = '''
    SELECT p.nome_projeto, COUNT(d.id_dependente) AS num_dependentes
    FROM projetos_desenvolvidos p
    JOIN funcionarios f ON p.id_funcionario = f.id_funcionario
    LEFT JOIN dependentes d ON f.id_funcionario = d.id_funcionario
    GROUP BY p.id_projeto
    ORDER BY num_dependentes DESC
    LIMIT 1;
    '''

   
    cursor.execute(query)

    resultado = cursor.fetchone()

    print("CONSULTA 5 - Identificar o projeto com o maior número de dependentes envolvidos, considerando que os Sdependentes são associados aos funcionários que estão gerenciando os projetos.")
    if resultado:
        print(f"Projeto com mais dependentes: {resultado[0]}, Número de Dependentes: {resultado[1]}")
    else:
        print("Nenhum projeto encontrado ou sem dependentes.")


    conn.close()


consulta_projeto_com_mais_dependentes()
