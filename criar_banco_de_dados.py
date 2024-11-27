import sqlite3


conn = sqlite3.connect('banco_de_dados.db')
cursor = conn.cursor()

script_sql = """

-- Tabela cargos
CREATE TABLE IF NOT EXISTS cargos (
    id_cargo INTEGER PRIMARY KEY,
    descricao TEXT NOT NULL,
    salario_base REAL NOT NULL,
    nivel TEXT CHECK(nivel IN ('estagiario', 'tecnico', 'analista', 'gerente', 'diretor')),
    requisitos TEXT
);


-- Tabela departamentos
CREATE TABLE IF NOT EXISTS departamentos (
    id_departamento INTEGER PRIMARY KEY,
    nome_departamento TEXT NOT NULL,
    id_gerente INTEGER,
    andar INTEGER NOT NULL,
    orcamento_anual REAL,
    FOREIGN KEY (id_gerente) REFERENCES funcionarios(id_funcionario)
);


-- Tabela funcionarios
CREATE TABLE IF NOT EXISTS funcionarios (
    id_funcionario INTEGER PRIMARY KEY,
    nome_funcionario TEXT NOT NULL,
    id_cargo INTEGER,
    id_departamento INTEGER,
    salario REAL NOT NULL,
    data_admissao DATE NOT NULL,
    FOREIGN KEY (id_cargo) REFERENCES cargos(id_cargo),
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
);


-- Tabela dependentes
CREATE TABLE IF NOT EXISTS dependentes (
    id_dependente INTEGER PRIMARY KEY,
    id_funcionario INTEGER NOT NULL,
    nome_dependente TEXT NOT NULL,
    data_nascimento DATE NOT NULL,
    parentesco TEXT NOT NULL,
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
);



-- Tabela historico_salarios
CREATE TABLE IF NOT EXISTS historico_salarios (
    id_historico INTEGER PRIMARY KEY,
    id_funcionario INTEGER NOT NULL,
    mes_ano TEXT NOT NULL,
    salario_recebido REAL NOT NULL,
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
);



-- Tabela projetos_desenvolvidos
CREATE TABLE IF NOT EXISTS projetos_desenvolvidos (
    id_projeto INTEGER PRIMARY KEY,
    nome_projeto TEXT NOT NULL,
    descricao TEXT,
    data_inicio DATE NOT NULL,
    data_conclusao DATE,
    id_funcionario INTEGER NOT NULL, -- Responsável pelo projeto
    custo_estimado REAL,
    custo_atual REAL,
    status TEXT CHECK(status IN ('Em Planejamento', 'Em Execução', 'Concluído', 'Cancelado')) NOT NULL,
    observacoes TEXT,
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
);


-- Tabela recursos_projeto
CREATE TABLE IF NOT EXISTS recursos_projeto (
    id_recurso INTEGER PRIMARY KEY,
    id_projeto INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    tipo TEXT CHECK(tipo IN ('Financeiro', 'Material', 'Humano')) NOT NULL,
    quantidade REAL,
    data_utilizacao DATE NOT NULL,
    FOREIGN KEY (id_projeto) REFERENCES projetos_desenvolvidos(id_projeto)
);


-- INSERINDO DADOS 


-- Inserindo cargos na tabela cargos
INSERT INTO cargos (descricao, salario_base, nivel, requisitos) VALUES 
('Estagiário de Desenvolvimento', 1500.00, 'estagiario', 'Cursando graduação em TI, conhecimento básico em programação'),
('Técnico de Suporte', 2500.00, 'tecnico', 'Ensino técnico em informática ou similar, experiência em suporte técnico'),
('Analista de Sistemas', 4500.00, 'analista', 'Graduação completa em TI, experiência com análise de sistemas e SQL'),
('Gerente de Projetos', 8000.00, 'gerente', 'Certificação em gestão de projetos (PMP ou similar), experiência com equipes ágeis'),
('Diretor de Tecnologia', 15000.00, 'diretor', 'Formação superior em TI, ampla experiência em liderança tecnológica e estratégia'),
('Analista de Marketing Digital', 4000.00, 'analista', 'Conhecimento em SEO, ferramentas de análise e campanhas digitais'),
('Gerente Financeiro', 9000.00, 'gerente', 'Graduação em finanças ou contabilidade, experiência em planejamento financeiro');

-- Inserindo departamentos na tabela departamentos
INSERT INTO departamentos (nome_departamento, id_gerente, andar, orcamento_anual) VALUES
('Tecnologia da Informação', 1, 3, 500000.00),
('Recursos Humanos', 2, 2, 200000.00),
('Marketing', NULL, 5, 300000.00),
('Financeiro', 3, 4, 400000.00),
('Pesquisa e Desenvolvimento', NULL, 6, 700000.00);

-- Inserindo funcionários na tabela funcionarios
INSERT INTO funcionarios (nome_funcionario, id_cargo, id_departamento, salario, data_admissao) VALUES
('Ana Souza', 1, 1, 1500.00, '2023-01-10'),
('Carlos Pereira', 2, 1, 2500.00, '2022-06-15'),
('Fernanda Lima', 3, 1, 4500.00, '2021-03-20'),
('João Silva', 4, 2, 8000.00, '2020-09-01'),
('Mariana Castro', 3, 3, 4500.00, '2022-11-05'),
('Paulo Almeida', 5, 4, 15000.00, '2018-07-12'),
('Renata Santos', 6, 5, 4000.00, '2021-12-01');

-- Inserindo dependentes na tabela dependentes
INSERT INTO dependentes (id_funcionario, nome_dependente, data_nascimento, parentesco) VALUES
(1, 'Lucas Souza', '2010-05-15', 'filho'),
(2, 'Beatriz Pereira', '2015-08-20', 'filha'),
(3, 'Clara Lima', '2012-03-10', 'filha'),
(4, 'Eduardo Silva', '2008-11-30', 'filho'),
(5, 'Sofia Castro', '2016-07-25', 'filha');


-- Inserindo dependentes na tabela dependentes
INSERT INTO dependentes (id_funcionario, nome_dependente, data_nascimento, parentesco) VALUES
(1, 'Lucas Souza', '2010-05-15', 'filho'),
(2, 'Beatriz Pereira', '2015-08-20', 'filha'),
(3, 'Clara Lima', '2012-03-10', 'filha'),
(4, 'Eduardo Silva', '2008-11-30', 'filho'),
(5, 'Sofia Castro', '2016-07-25', 'filha');

-- Inserindo registros na tabela historico_salarios
INSERT INTO historico_salarios (id_funcionario, mes_ano, salario_recebido) VALUES
(1, '2023-01', 1500.00),
(2, '2023-01', 2500.00),
(3, '2023-01', 4500.00),
(4, '2023-01', 8000.00),
(5, '2023-01', 4500.00);

-- Inserindo projetos desenvolvidos na tabela projetos_desenvolvidos
INSERT INTO projetos_desenvolvidos (nome_projeto, descricao, data_inicio, data_conclusao, id_funcionario, custo_estimado, custo_atual, status, observacoes) VALUES
('Sistema de Gestão de Estoque', 'Desenvolvimento de um sistema para controle de estoque de produtos.', '2023-01-10', '2023-06-30', 1, 20000.00, 21000.00, 'Concluído', 'Projeto entregue com 5% de aumento no custo devido a ajustes de última hora.'),
('Automação de Processos de RH', 'Automatização do fluxo de recrutamento e seleção.', '2023-02-01', '2023-05-20', 2, 15000.00, 14800.00, 'Concluído', 'O projeto foi concluído dentro do prazo e com leve redução no custo estimado.'),
('Plataforma de E-commerce', 'Desenvolvimento de plataforma online para vendas de produtos.', '2023-03-15', NULL, 3, 50000.00, 30000.00, 'Em Execução', 'A plataforma está na fase de integração de pagamentos.'),
('Sistema de Relatórios Financeiros', 'Criação de um sistema de relatórios financeiros automatizados.', '2023-04-01', NULL, 4, 25000.00, 12000.00, 'Em Execução', 'A equipe está trabalhando na integração com o banco de dados corporativo.'),
('App Mobile para Gestão de Tarefas', 'Aplicativo para gestão de tarefas diárias de equipes.', '2023-06-10', NULL, 5, 10000.00, 7000.00, 'Em Planejamento', 'O projeto está em fase de definição de funcionalidades e protótipos.');

-- Inserindo recursos para os projetos na tabela recursos_projeto
INSERT INTO recursos_projeto (id_projeto, descricao, tipo, quantidade, data_utilizacao) VALUES
(1, 'Licença de Software para Controle de Estoque', 'Financeiro', 5000.00, '2023-01-15'),
(1, 'Computadores para os desenvolvedores', 'Material', 10, '2023-01-20'),
(2, 'Consultoria externa para processo seletivo', 'Financeiro', 3000.00, '2023-02-10'),
(3, 'Equipe de desenvolvedores para plataforma', 'Humano', 5, '2023-03-20'),
(4, 'Serviço de integração de sistemas', 'Financeiro', 7000.00, '2023-04-15');


"""

cursor.executescript(script_sql)


conn.commit()
conn.close()

print("Deu bomm!!! BD criado com Sucesso! :3")