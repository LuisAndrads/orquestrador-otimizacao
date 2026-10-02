#!/usr/bin/env python3
"""
Pedidos da base do cliente: totais por período e receita por UTM. Não escreve nada.

Lê a aba de pedidos da Base de Dados (planilha alimentada pela plataforma da
loja), com o mapa de colunas e a regra de "faturado" do cliente.json. Funciona
com qualquer plataforma que grave a base (Nuvemshop, Tray, Shopify, VTEX...).

Cada pedido conta uma vez: se o mesmo id aparecer em mais de uma linha (já
aconteceu por gravação repetida em falha de rede), vale a última e o script
avisa quantas linhas repetidas encontrou.

Definições:
  captado  = soma do total de todos os pedidos criados no período
  faturado = pedidos que passam na regra "faturado" do cliente.json

Uso:
    python pedidos.py --cliente clientes/hocks/cliente.json totais 2026-09-21 2026-09-27 --por-dia
    python pedidos.py --cliente clientes/hocks/cliente.json utm 2026-09-21 2026-09-27 --nivel conjunto --fonte meta
"""

import argparse
import sys
from collections import defaultdict
from datetime import datetime, timedelta

from comum import api_planilhas, carrega_cliente, intervalo_a1, numero

NIVEIS = {
    "fonte": ("utm_source",),
    "campanha": ("utm_source", "utm_campaign"),
    "conjunto": ("utm_source", "utm_campaign", "utm_content"),
    "anuncio": ("utm_source", "utm_campaign", "utm_content", "utm_term"),
}


def le_base(cliente):
    cfg = cliente["planilhas"]["base_pedidos"]
    if not cfg.get("id"):
        sys.exit("ERRO: base de pedidos sem id no cliente.json (régua da loja: sem dado).")
    v = api_planilhas(cliente).values().get(
        spreadsheetId=cfg["id"], range=intervalo_a1(cfg["aba"]),
        valueRenderOption="UNFORMATTED_VALUE", dateTimeRenderOption="FORMATTED_STRING",
    ).execute().get("values", [])
    cab = [str(c).strip() for c in v[0]]
    col = cfg["colunas"]
    faltando = [k for k in ("id", "data", "total") if col.get(k) not in cab]
    if faltando:
        sys.exit(f"ERRO: colunas {faltando} do cliente.json não existem na aba {cfg['aba']}.")
    idx = {n: i for i, n in enumerate(cab)}

    linhas, ultima = [], {}
    for r in v[1:]:
        r = list(r) + [""] * (len(cab) - len(r))
        pid = str(r[idx[col["id"]]]).strip()
        if pid:
            ultima[pid] = len(linhas)
            linhas.append(r)
    repetidas = len(linhas) - len(ultima)
    unicos = [linhas[i] for i in sorted(ultima.values())]
    return unicos, idx, cfg, repetidas


def faturado(r, idx, regra):
    if regra.get("tipo") == "situacao":
        s = str(r[idx[regra["coluna"]]])
        return not any(x.lower() in s.lower() for x in regra.get("excluir_se_contem", []))
    pago = str(r[idx[regra["coluna_pagamento"]]]) == regra.get("valor_pago", "paid")
    cancelado = str(r[idx[regra["coluna_status"]]]) == regra.get("valor_cancelado", "cancelled")
    return pago and not cancelado


def data_do(r, idx, cfg):
    bruto = str(r[idx[cfg["colunas"]["data"]]]).strip()
    fmt = cfg.get("formato_data", "%d/%m/%Y")
    try:
        return datetime.strptime(bruto[:len(datetime(2000, 1, 1).strftime(fmt))], fmt).date()
    except ValueError:
        return None


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--cliente", required=True)
    p.add_argument("modo", choices=["totais", "utm"])
    p.add_argument("inicio")
    p.add_argument("fim")
    p.add_argument("--por-dia", action="store_true")
    p.add_argument("--nivel", choices=NIVEIS, default="campanha")
    p.add_argument("--fonte", help="filtra utm_source que contenha este texto")
    a = p.parse_args()

    cliente = carrega_cliente(a.cliente)
    linhas, idx, cfg, repetidas = le_base(cliente)
    ini = datetime.strptime(a.inicio, "%Y-%m-%d").date()
    fim = datetime.strptime(a.fim, "%Y-%m-%d").date()
    regra = cfg["faturado"]
    col = cfg["colunas"]

    print(f"Base de pedidos ({cfg['aba']}), pedidos criados de {a.inicio} a {a.fim}")
    if repetidas:
        print(f"AVISO: {repetidas} linhas com id repetido na base; cada pedido foi contado uma vez.")

    grupos = defaultdict(lambda: [0, 0.0, 0, 0.0])
    for r in linhas:
        d = data_do(r, idx, cfg)
        if not d or not (ini <= d <= fim):
            continue
        if a.modo == "totais":
            chave = (d.isoformat(),) if a.por_dia else ("TOTAL",)
        else:
            fonte = str(r[idx[col["utm_source"]]]).strip() if col.get("utm_source") in idx else ""
            if a.fonte and a.fonte.lower() not in fonte.lower():
                continue
            if not fonte:
                chave = ("(sem utm)",)
            else:
                chave = tuple((str(r[idx[col[k]]]).strip() if col.get(k) in idx else "") or "-" for k in NIVEIS[a.nivel])
        g = grupos[chave]
        total = numero(r[idx[col["total"]]])
        g[0] += 1
        g[1] += total
        if faturado(r, idx, regra):
            g[2] += 1
            g[3] += total

    titulo = "dia" if a.modo == "totais" else "\t".join(NIVEIS[a.nivel])
    print(f"{titulo}\tpedidos\tcaptado\tpedidos_faturados\tfaturado")
    ordem = sorted(grupos.items()) if a.modo == "totais" else sorted(grupos.items(), key=lambda x: -x[1][3])
    soma = [0, 0.0, 0, 0.0]
    for chave, g in ordem:
        soma = [s + x for s, x in zip(soma, g)]
        print("\t".join(chave) + f"\t{g[0]}\t{g[1]:.2f}\t{g[2]}\t{g[3]:.2f}")
    if a.modo == "totais" and a.por_dia:
        print(f"TOTAL\t{soma[0]}\t{soma[1]:.2f}\t{soma[2]}\t{soma[3]:.2f}")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        sys.exit(1)
