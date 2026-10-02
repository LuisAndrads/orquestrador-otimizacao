#!/usr/bin/env python3
"""
Lê um intervalo de uma planilha Google e imprime as linhas. Não escreve nada.

A primeira coluna da saída é o número da linha na planilha, para a análise
citar a célula de onde tirou cada número.

Uso:
    python le_planilha.py --cliente clientes/hocks/cliente.json --chave metas "Visão Geral!B5:N22"
    python le_planilha.py --cliente clientes/hocks/cliente.json --chave base_pedidos --abas
    python le_planilha.py --planilha <id> "configs!A5:B5"
"""

import argparse
import sys

from comum import api_planilhas, carrega_cliente, intervalo_a1


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("intervalo", nargs="?")
    p.add_argument("--cliente", help="caminho do cliente.json")
    p.add_argument("--chave", default="metas", help="qual planilha do cliente.json (metas, base_pedidos)")
    p.add_argument("--planilha", help="id da planilha (sobrepõe --chave)")
    p.add_argument("--abas", action="store_true", help="lista as abas")
    a = p.parse_args()

    cliente = carrega_cliente(a.cliente) if a.cliente else {}
    pid = a.planilha or cliente.get("planilhas", {}).get(a.chave, {}).get("id")
    if not pid:
        p.error("informe --planilha ou um --cliente com o id da planilha")
    api = api_planilhas(cliente)

    if a.abas:
        meta = api.get(spreadsheetId=pid, fields="properties.title,sheets.properties(title,gridProperties)").execute()
        print(meta["properties"]["title"])
        for s in meta["sheets"]:
            g = s["properties"]["gridProperties"]
            print(f'{s["properties"]["title"]}\t{g.get("rowCount")} linhas\t{g.get("columnCount")} colunas')
        return
    if not a.intervalo:
        p.error("informe o intervalo ou use --abas")

    valores = api.values().get(spreadsheetId=pid, range=intervalo_a1(a.intervalo)).execute().get("values", [])
    celulas = a.intervalo.partition("!")[2]
    digitos = "".join(c for c in celulas.split(":")[0] if c.isdigit())
    inicio = int(digitos) if digitos else 1
    for i, linha in enumerate(valores, inicio):
        if any(str(c).strip() for c in linha):
            print(f"{i}\t" + "\t".join(linha))


if __name__ == "__main__":
    try:
        main()
    except Exception as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        sys.exit(1)
