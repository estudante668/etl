# Pipeline ETL de Vendas — Engenharia de Dados

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento-yellow)
![Architecture](https://img.shields.io/badge/Architecture-ETL-orange)

## 1. Sobre o projeto

Este projeto implementa um pipeline ETL (*Extract, Transform, Load*) para processamento e tratamento de dados de vendas utilizando Python.

O objetivo é desenvolver uma aplicação de Engenharia de Dados capaz de extrair informações de arquivos CSV, validar a qualidade dos registros, realizar transformações, calcular valores financeiros e carregar os dados tratados em arquivos estruturados.

O pipeline também registra logs de execução e gera um relatório consolidado com indicadores do processamento.

## 2. Objetivos

- Implementar um fluxo ETL utilizando Python.
- Desenvolver processos de extração de arquivos CSV.
- Aplicar regras de validação e qualidade de dados.
- Identificar registros duplicados e inconsistentes.
- Realizar conversões de tipos de dados.
- Calcular o valor total das vendas.
- Separar registros aprovados e rejeitados.
- Implementar logs para monitoramento da execução.
- Gerar relatórios de processamento.

## 3. Arquitetura do pipeline

O projeto utiliza uma arquitetura ETL dividida em três etapas principais:

```text
              FONTE DE DADOS
                    |
                    v
             data/raw/vendas.csv
                    |
                    v
              1. EXTRACT
          Extração dos registros
          e validação das colunas
                    |
                    v
              2. TRANSFORM
          Validação dos registros
          Conversão dos dados
          Identificação de duplicados
          Aplicação das regras de qualidade
          Cálculo do valor total
                    |
                    v
              3. LOAD
               /       \
              v         v
          APROVADOS   REJEITADOS
              |         |
              v         v
        data/processed  data/rejected
              |
              v
         RELATÓRIO ETL
              |
              v
          LOGS E MÉTRICAS
```

## 4. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| CSV | Leitura e gravação dos dados |
| Decimal | Precisão nos cálculos financeiros |
| Logging | Registro de eventos e erros |
| Pathlib | Gerenciamento de caminhos e diretórios |
| Datetime | Conversão e validação de datas |

**Dependências externas:** o projeto utiliza exclusivamente bibliotecas da biblioteca padrão do Python. Não exige instalação de pacotes externos.

## 5. Estrutura do projeto

```text
modulo_01/
│
├── src/
│   └── etl.py
│
├── data/
│   ├── raw/
│   │   └── vendas.csv
│   │
│   ├── processed/
│   │   └── vendas_tratadas.csv
│   │
│   └── rejected/
│       └── vendas_rejeitadas.csv
│
├── logs/
│   ├── etl.log
│   └── relatorio_etl.txt
│
├── .gitignore
└── README.md
```

### Descrição dos diretórios

- `src/`: contém o código-fonte do pipeline.
- `data/raw/`: armazena os dados originais recebidos.
- `data/processed/`: armazena os registros aprovados e transformados.
- `data/rejected/`: armazena os registros que não passaram pelas validações.
- `logs/`: armazena os registros de execução e o relatório ETL.
- `.gitignore`: define os arquivos e diretórios que não devem ser versionados.

## 6. Funcionamento do ETL

### 6.1 Extract — Extração

A função `extrair()` realiza:

- Verificação da existência do arquivo CSV.
- Leitura dos dados utilizando `csv.DictReader`.
- Identificação das colunas disponíveis.
- Verificação das colunas obrigatórias.
- Carregamento dos registros para processamento.

Colunas obrigatórias:

| Campo | Descrição |
|---|---|
| `id_venda` | Identificador da venda |
| `data` | Data da venda |
| `cliente` | Nome do cliente |
| `produto` | Produto vendido |
| `quantidade` | Quantidade comercializada |
| `preco_unitario` | Preço unitário do produto |

### 6.2 Transform — Transformação

A função `transformar()` executa as regras de qualidade e transformação.

**Validações implementadas:**

1. Identificador da venda não pode estar vazio.
2. Identificadores duplicados são rejeitados.
3. Campos obrigatórios não podem estar vazios.
4. A data deve seguir o formato ISO `YYYY-MM-DD`.
5. A quantidade deve ser um número inteiro maior que zero.
6. O preço deve ser um valor decimal finito e não negativo.

**Conversões de dados:**

- Data: `date.fromisoformat()`.
- Quantidade: `int()`.
- Preço: `Decimal()`.

**Cálculo financeiro:**

O valor total da venda é calculado por:

`valor_total = quantidade × preco_unitario`

A precisão monetária é tratada com `Decimal`, evitando os problemas de precisão binária comuns em cálculos financeiros com `float`.

**Tratamento de registros:**

- Aprovados: registros que passam por todas as validações.
- Rejeitados: registros que apresentam erros, acompanhados do número da linha de origem e do motivo da rejeição.

### 6.3 Load — Carregamento

A função `carregar()` realiza a persistência dos dados em arquivos CSV.

| Saída | Localização |
|---|---|
| Vendas aprovadas | `data/processed/vendas_tratadas.csv` |
| Vendas rejeitadas | `data/rejected/vendas_rejeitadas.csv` |

Os registros aprovados recebem uma coluna adicional:

`valor_total`

Os registros rejeitados recebem duas colunas adicionais:

- `linha_origem`
- `motivo_rejeicao`

### 6.4 Relatórios e monitoramento

O pipeline utiliza o módulo `logging` para registrar:

- Início e encerramento da execução.
- Extração dos dados.
- Quantidade de registros processados.
- Registros rejeitados e seus respectivos motivos.
- Falhas durante o processamento.

O relatório apresenta:

- Total de registros recebidos.
- Total de registros aprovados.
- Total de registros rejeitados.
- Faturamento dos registros aprovados.

## 7. Como executar o projeto

### Pré-requisitos

- Python instalado.
- Git instalado.
- Terminal PowerShell ou outro terminal compatível.

### 7.1 Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Acesse a pasta do projeto:

```bash
cd modulo_01
```

### 7.2 Preparar os diretórios

No PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path `
    data\raw, data\processed, data\rejected, logs
```

### 7.3 Preparar o arquivo de entrada

Crie o arquivo:

`data/raw/vendas.csv`

Exemplo:

```csv
id_venda,data,cliente,produto,quantidade,preco_unitario
V001,2026-11-14,Ana,Notebook,2,3500.00
V002,2026-11-14,Pedro,Mouse,3,50.00
V003,2026-11-14,Maria,Teclado,2,150.00
V004,2026-11-15,Joao,Monitor,1,1200.00
V005,2026-11-15,Carlos,Mouse,5,50.00
```

### 7.4 Executar o pipeline

Considerando que o código esteja localizado em `src/etl.py`, execute a partir da raiz do projeto:

```bash
python src/etl.py
```

O processamento será iniciado e os arquivos de saída serão gerados nos respectivos diretórios.

## 8. Resultado esperado

Para os cinco registros do exemplo, o resultado esperado é:

| Indicador | Resultado |
|---|---:|
| Registros recebidos | 5 |
| Registros aprovados | 5 |
| Registros rejeitados | 0 |
| Faturamento aprovado | R$ 8.900,00 |

O resultado depende dos dados efetivamente fornecidos ao pipeline.

## 9. Limitações da implementação atual

Esta versão representa a primeira implementação do pipeline ETL e possui algumas limitações técnicas:

- O processamento utiliza carregamento dos registros em memória (`list`).
- Não possui processamento distribuído.
- Não possui processamento de eventos em tempo real.
- Não utiliza banco de dados.
- A identificação de duplicados considera os registros da execução atual.
- Os arquivos de saída são sobrescritos em cada execução.
- Não possui orquestração automatizada de tarefas.

Para volumes de milhões de registros, será necessário evoluir a arquitetura para processamento em lotes, otimização de memória, persistência confiável e mecanismos de recuperação de falhas.

## 10. Evolução planejada

As próximas etapas de desenvolvimento incluem:

| Etapa | Tecnologia / recurso | Objetivo |
|---|---|---|
| 1 | Polars | Processamento eficiente de grandes volumes |
| 2 | Parquet / PyArrow | Armazenamento colunar |
| 3 | PostgreSQL | Persistência e integridade dos dados |
| 4 | Apache Kafka | Ingestão e processamento de eventos |
| 5 | Apache Airflow | Orquestração de pipelines |
| 6 | Docker | Padronização do ambiente |
| 7 | AWS S3 | Data Lake na nuvem |
| 8 | AWS Glue e Athena | Catálogo e consultas analíticas |
| 9 | Amazon MSK / Kinesis | Arquitetura de streaming gerenciada |

Essas tecnologias representam etapas futuras, não funcionalidades já implementadas nesta versão.

## 11. Conceitos de Engenharia de Dados aplicados

Este projeto permite desenvolver conhecimentos práticos sobre:

- Arquitetura ETL.
- Ingestão de dados.
- Qualidade e validação de dados.
- Transformação de dados.
- Tratamento de exceções.
- Tipagem e conversão de dados.
- Deduplicação.
- Persistência de dados.
- Logs e monitoramento.
- Organização de projetos Python.
- Versionamento com Git.

## 12. Licença

Projeto desenvolvido para fins educacionais e de evolução profissional em Engenharia de Dados.

---

**Projeto:** Pipeline ETL de Vendas  
**Área:** Engenharia de Dados  
**Linguagem:** Python  
**Versão:** 1.0.0 — Implementação inicial
