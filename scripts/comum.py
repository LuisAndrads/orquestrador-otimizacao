"""Funções compartilhadas pelos scripts do orquestrador. Só leitura."""

import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")


def carrega_cliente(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def api_planilhas(cliente=None):
    """Cliente da API do Google Sheets com escopo somente leitura.

    A chave vem do cliente.json (credencial_google) ou da variável
    GOOGLE_APPLICATION_CREDENTIALS. O escopo readonly faz a API recusar
    qualquer escrita, mesmo que o script seja alterado.
    """
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    chave = (cliente or {}).get("credencial_google") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not chave or not os.path.exists(chave):
        sys.exit("ERRO: chave da conta de serviço não encontrada (credencial_google no "
                 "cliente.json ou GOOGLE_APPLICATION_CREDENTIALS).")
    cred = service_account.Credentials.from_service_account_file(
        chave, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    return build("sheets", "v4", credentials=cred, cache_discovery=False).spreadsheets()


def intervalo_a1(texto):
    """'Visão Geral!A1:B2' -> "'Visão Geral'!A1:B2" (aba com espaço precisa de aspas)."""
    aba, _, celulas = texto.partition("!")
    if not aba.startswith("'"):
        aba = "'" + aba.replace("'", "''") + "'"
    return f"{aba}!{celulas}" if celulas else aba


def numero(valor):
    if isinstance(valor, (int, float)):
        return float(valor)
    t = str(valor).replace("R$", "").strip()
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return 0.0
