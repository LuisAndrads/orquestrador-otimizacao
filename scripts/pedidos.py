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

Plataforma Convertr (base_pedidos.tipo = "dados_bq"): não há pedido por linha
nem UTM. O script soma a aba dados_bq da PDA 13.0 (um dia por linha; linha com
channel vazio = pedidos da loja; linha com channel preenchido = mídia e GA4 do
canal). O modo `utm` não existe nessa plataforma; use `canais`.

Uso:
    python pedidos.py --cliente clientes/hocks/cliente.json totais 2026-09-21 2026-09-27 --por-dia
    python pedidos.py --cliente clientes/hocks/cliente.json utm 2026-09-21 2026-09-27 --nivel conjunto --fonte meta
    python pedidos.py --cliente clientes/hocks/cliente.json canais 2026-09-21 2026-09-27   (só Convertr)
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


# --- Plataforma Convertr: aba dados_bq da PDA 13.0 -------------------------

DADOS_BQ_PEDIDOS = {
    "captado": "total_pedidos",
    "faturado": "total_pedidos_aprovados",
    "pedidos": "qtd_pedidos",
    "aprovados": "qtd_pedidos_aprovados",
    "pedidos_primeira": "qtd_pedidos_primeira",
    "pedidos_recompra": "qtd_pedidos_recompra",
    "receita_primeira": "total_pedidos_primeira",
    "receita_recompra": "total_pedidos_recompra",
    "pecas": "qtd_pecas",
    "pecas_validas": "qtd_pecas_validos",
}


def le_dados_bq(cliente):
    """Linhas da aba dados_bq, com o cabeçalho normalizado.

    A aba fica na própria PDA 13.0 (planilhas.metas.id), a não ser que
    base_pedidos.id aponte para outra. Datas em DD/MM/AAAA, números com
    vírgula decimal; por isso a leitura é do valor formatado.
    """
    cfg = cliente["planilhas"]["base_pedidos"]
    pid = cfg.get("id") or cliente["planilhas"]["metas"].get("id")
    if not pid:
        sys.exit("ERRO: sem id da PDA 13.0 no cliente.json (planilhas.metas.id).")
    v = api_planilhas(cliente).values().get(
        spreadsheetId=pid, range=intervalo_a1(cfg.get("aba") or "dados_bq"),
    ).execute().get("values", [])
    if not v:
        sys.exit("ERRO: aba dados_bq vazia ou inexistente.")
    cab = [str(c).strip().lower() for c in v[0]]
    col = cfg.get("colunas", {})
    c_data = col.get("data") or next((c for c in ("date", "data", "dia") if c in cab), None)
    c_canal = col.get("channel") or ("channel" if "channel" in cab else None)
    if not c_data or not c_canal:
        sys.exit(f"ERRO: a aba dados_bq não tem coluna de data e de channel. Cabeçalho: {cab}")
    return cab, v[1:], c_data, c_canal


def numero_br(valor):
    """Número no formato da dados_bq: ponto é milhar e vírgula é decimal."""
    if isinstance(valor, (int, float)):
        return float(valor)
    t = str(valor).replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(t) if t else 0.0
    except ValueError:
        return 0.0


def agrega_dados_bq(cab, linhas, c_data, c_canal, ini, fim, por_dia=False, modo="totais"):
    """Soma as linhas do período. Função pura, para teste sem planilha."""
    idx = {n: i for i, n in enumerate(cab)}
    grupos = defaultdict(lambda: defaultdict(float))
    dias = set()
    for r in linhas:
        r = list(r) + [""] * (len(cab) - len(r))
        try:
            d = datetime.strptime(str(r[idx[c_data]]).strip()[:10], "%d/%m/%Y").date()
        except ValueError:
            continue
        if not (ini <= d <= fim):
            continue
        canal = str(r[idx[c_canal]]).strip()
        if modo == "totais":
            if canal:
                continue
            chave = d.isoformat() if por_dia else "TOTAL"
            for nome, coluna in DADOS_BQ_PEDIDOS.items():
                if coluna in idx:
                    grupos[chave][nome] += numero_br(r[idx[coluna]])
        else:
            if not canal:
                continue
            for nome, i in idx.items():
                if nome in (c_data, c_canal):
                    continue
                grupos[canal][nome] += numero_br(r[i])
        dias.add(d)
    return grupos, dias


def main_dados_bq(cliente, a):
    if a.modo == "utm":
        print("Atribuição de pedido por canal: indisponível nesta plataforma (Convertr não "
              "grava pedido por linha nem UTM). Use o modo `canais` (receita e compras do GA4 "
              "por canal) e diga isso no retorno; não estime.")
        sys.exit(2)
    ini = datetime.strptime(a.inicio, "%Y-%m-%d").date()
    fim = datetime.strptime(a.fim, "%Y-%m-%d").date()
    cab, linhas, c_data, c_canal = le_dados_bq(cliente)
    grupos, dias = agrega_dados_bq(cab, linhas, c_data, c_canal, ini, fim, a.por_dia, a.modo)
    hoje = datetime.now().date()
    print(f"PDA 13.0, aba dados_bq, de {a.inicio} a {a.fim} ({len(dias)} dias com dado)")
    if fim >= hoje:
        print("AVISO: o período inclui hoje, que está incompleto.")
    if fim >= hoje - timedelta(days=7):
        print("AVISO: aprovados dos últimos dias ainda mudam (pendente vira aprovado ou "
              "cancelado). Marque a última semana como provisória e releia na próxima rodada.")
    if a.modo == "totais":
        campos = ["captado", "faturado", "pedidos", "aprovados", "pedidos_primeira",
                  "pedidos_recompra", "receita_primeira", "receita_recompra", "pecas", "pecas_validas"]
        print("dia\t" + "\t".join(campos) + "\taprovacao_pedidos\tticket_faturado")
        soma = defaultdict(float)
        for chave in sorted(grupos):
            g = grupos[chave]
            for c in campos:
                soma[c] += g[c]
            print(chave + "\t" + "\t".join(f"{g[c]:.2f}" for c in campos) + _taxas(g))
        if a.por_dia:
            print("TOTAL\t" + "\t".join(f"{soma[c]:.2f}" for c in campos) + _taxas(soma))
    else:
        metricas = sorted({m for g in grupos.values() for m, x in g.items() if x})
        print("channel\t" + "\t".join(metricas))
        for canal in sorted(grupos, key=lambda c: -grupos[c].get("totalrevenue", 0)):
            print(canal + "\t" + "\t".join(f"{grupos[canal].get(m, 0):.2f}" for m in metricas))
        print("Lembrete: receita e compras por canal são do GA4 (totalRevenue, totalPurchasers), "
              "não da loja. Gasto do Meta sem imposto (a PDA soma o imposto, Visão Geral!E1).")


def _taxas(g):
    aprov = g["aprovados"] / g["pedidos"] if g["pedidos"] else 0
    ticket = g["faturado"] / g["aprovados"] if g["aprovados"] else 0
    return f"\t{aprov:.4f}\t{ticket:.2f}"


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--cliente", required=True)
    p.add_argument("modo", choices=["totais", "utm", "canais"])
    p.add_argument("inicio")
    p.add_argument("fim")
    p.add_argument("--por-dia", action="store_true")
    p.add_argument("--nivel", choices=NIVEIS, default="campanha")
    p.add_argument("--fonte", help="filtra utm_source que contenha este texto")
    a = p.parse_args()

    cliente = carrega_cliente(a.cliente)
    if cliente["planilhas"]["base_pedidos"].get("tipo") == "dados_bq":
        return main_dados_bq(cliente, a)
    if a.modo == "canais":
        sys.exit("ERRO: o modo `canais` é só da plataforma Convertr (base_pedidos.tipo = dados_bq).")
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
