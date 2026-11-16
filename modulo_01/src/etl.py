
# ============================================================
# PROJETO: PIPELINE ETL DE VENDAS
# MÓDULO 1 - ENGENHARIA DE DADOS
# ============================================================

import csv
import logging

from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


# ------------------------------------------------------------
# 1. CONFIGURAÇÃO DOS CAMINHOS
# ------------------------------------------------------------

# Descobre automaticamente a pasta principal do projeto.
BASE_DIR = Path(__file__).resolve().parents[1]

ARQUIVO_ENTRADA = (
    BASE_DIR / "data" / "raw" / "vendas.csv"
)

ARQUIVO_APROVADOS = (
    BASE_DIR / "data" / "processed" / "vendas_tratadas.csv"
)

ARQUIVO_REJEITADOS = (
    BASE_DIR / "data" / "rejected" / "vendas_rejeitadas.csv"
)

ARQUIVO_LOG = BASE_DIR / "logs" / "etl.log"

ARQUIVO_RELATORIO = (
    BASE_DIR / "logs" / "relatorio_etl.txt"
)


# ------------------------------------------------------------
# 2. CONFIGURAÇÃO DO LOG
# ------------------------------------------------------------

logging.basicConfig(
    filename=str(ARQUIVO_LOG),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ------------------------------------------------------------
# 3. EXTRAÇÃO - EXTRACT
# ------------------------------------------------------------

def extrair():

    logging.info("Iniciando extração dos dados.")

    if not ARQUIVO_ENTRADA.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO_ENTRADA}"
        )

    with open(
        ARQUIVO_ENTRADA,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        colunas_obrigatorias = [
            "id_venda",
            "data",
            "cliente",
            "produto",
            "quantidade",
            "preco_unitario"
        ]

        colunas = leitor.fieldnames or []

        if not all(
            coluna in colunas
            for coluna in colunas_obrigatorias
        ):
            raise ValueError(
                "O arquivo possui colunas obrigatórias ausentes."
            )

        dados = list(leitor)

    logging.info(
        "Extração concluída. Registros: %s",
        len(dados)
    )

    return dados, colunas

# ------------------------------------------------------------
# 4. TRANSFORMAÇÃO - TRANSFORM
# ------------------------------------------------------------

def transformar(dados):

    logging.info("Iniciando transformação.")

    aprovados = []
    rejeitados = []

    ids_processados = set()

    for numero_linha, linha in enumerate(dados, start=2):

        try:

            # --------------------------------------------
            # IDENTIFICADOR
            # --------------------------------------------

            id_venda = (
                linha["id_venda"] or ""
            ).strip()

            if not id_venda:
                raise ValueError("ID da venda ausente.")

            if id_venda in ids_processados:
                raise ValueError("Venda duplicada.")

            # --------------------------------------------
            # CAMPOS OBRIGATÓRIOS
            # --------------------------------------------

            campos = [
                "data",
                "cliente",
                "produto",
                "quantidade",
                "preco_unitario"
            ]

            for campo in campos:

                if not (linha[campo] or "").strip():
                    raise ValueError(
                        f"Campo obrigatório vazio: {campo}"
                    )

            # --------------------------------------------
            # CONVERSÃO DOS TIPOS DE DADOS
            # --------------------------------------------

            data_venda = date.fromisoformat(
                linha["data"]
            )

            quantidade = int(
                linha["quantidade"]
            )

            preco = Decimal(
                linha["preco_unitario"]
            )

            # --------------------------------------------
            # REGRAS DE QUALIDADE
            # --------------------------------------------

            if quantidade <= 0:
                raise ValueError(
                    "Quantidade deve ser maior que zero."
                )

            if not preco.is_finite() or preco < 0:
                raise ValueError(
                    "Preço inválido."
                )

            # --------------------------------------------
            # CÁLCULO FINANCEIRO
            # --------------------------------------------

            valor_total = (
                quantidade * preco
            ).quantize(Decimal("0.01"))

            # --------------------------------------------
            # REGISTRO APROVADO
            # --------------------------------------------

            registro = dict(linha)

            registro["data"] = data_venda.isoformat()

            registro["quantidade"] = quantidade

            registro["preco_unitario"] = format(
                preco,
                ".2f"
            )

            registro["valor_total"] = format(
                valor_total,
                ".2f"
            )

            aprovados.append(registro)

            # Só registramos o ID depois da validação.
            ids_processados.add(id_venda)

        except (
            ValueError,
            InvalidOperation,
            KeyError
        ) as erro:

            registro_rejeitado = dict(linha)

            registro_rejeitado["linha_origem"] = (
                numero_linha
            )

            registro_rejeitado["motivo_rejeicao"] = (
                str(erro)
            )

            rejeitados.append(registro_rejeitado)

            logging.warning(
                "Linha %s rejeitada: %s",
                numero_linha,
                erro
            )

    logging.info(
        "Transformação concluída. Aprovados: %s. Rejeitados: %s",
        len(aprovados),
        len(rejeitados)
    )

    return aprovados, rejeitados


# ------------------------------------------------------------
# 5. CARREGAMENTO - LOAD
# ------------------------------------------------------------

def carregar(aprovados, rejeitados, colunas):

    logging.info("Iniciando carregamento.")

    # Criar diretórios, se necessário.
    ARQUIVO_APROVADOS.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    ARQUIVO_REJEITADOS.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------
    # GRAVAR REGISTROS APROVADOS
    # --------------------------------------------

    colunas_saida = colunas + ["valor_total"]

    with open(
        ARQUIVO_APROVADOS,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas_saida
        )

        escritor.writeheader()
        escritor.writerows(aprovados)

    # --------------------------------------------
    # GRAVAR REGISTROS REJEITADOS
    # --------------------------------------------

    colunas_rejeitados = (
        colunas
        + ["linha_origem", "motivo_rejeicao"]
    )

    with open(
        ARQUIVO_REJEITADOS,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas_rejeitados
        )

        escritor.writeheader()
        escritor.writerows(rejeitados)

    logging.info("Carregamento concluído.")


# ------------------------------------------------------------
# 6. GERAÇÃO DO RELATÓRIO
# ------------------------------------------------------------

def gerar_relatorio(dados, aprovados, rejeitados):

    faturamento = sum(
        (
            Decimal(registro["valor_total"])
            for registro in aprovados
        ),
        Decimal("0.00")
    )

    relatorio = [
        "===================================",
        "RELATORIO DO PIPELINE ETL",
        "===================================",
        f"Registros recebidos: {len(dados)}",
        f"Registros aprovados: {len(aprovados)}",
        f"Registros rejeitados: {len(rejeitados)}",
        f"Faturamento aprovado: R$ {faturamento:.2f}",
        "==================================="
    ]

    texto = "\n".join(relatorio)

    ARQUIVO_RELATORIO.write_text(
        texto,
        encoding="utf-8"
    )

    print(texto)

    logging.info("Relatório gerado.")


# ------------------------------------------------------------
# 7. ORQUESTRADOR PRINCIPAL
# ------------------------------------------------------------

def main():

    logging.info("========== INÍCIO DO PIPELINE ==========")

    try:

        dados, colunas = extrair()

        aprovados, rejeitados = transformar(dados)

        carregar(
            aprovados,
            rejeitados,
            colunas
        )

        gerar_relatorio(
            dados,
            aprovados,
            rejeitados
        )

        logging.info("Pipeline executado com sucesso.")

    except Exception:

        logging.exception(
            "Falha na execução do pipeline."
        )

        raise

    finally:

        logging.info("========== FIM DO PIPELINE ==========")


# ------------------------------------------------------------
# 8. PONTO DE ENTRADA DO PROGRAMA
# ------------------------------------------------------------

if __name__ == "__main__":

    main()
