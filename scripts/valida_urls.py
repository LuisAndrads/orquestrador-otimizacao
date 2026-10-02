#!/usr/bin/env python3
"""
Confere se as paginas de produto dos anuncios estao no ar. Nao escreve nada.

Algumas plataformas (a Nuvemshop, por exemplo) respondem HTTP 200 com um texto
de erro para produto esgotado; por isso o script procura esse texto no corpo.
O texto pode vir do cliente.json (pagina_esgotada_texto) ou de --marca.


Uso:
    python valida_urls.py URL [URL ...]
    python valida_urls.py --arquivo urls.txt --cliente clientes/hocks/cliente.json
"""

import argparse
import time
import warnings
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings("ignore")

import requests

MARCAS_DE_ERRO = ("Erro - 404", "Página não encontrada", "Pagina nao encontrada")
CABECALHO = {"User-Agent": "Mozilla/5.0 (otimizacao-semanal; verificacao de url)"}


def confere(url):
    # A loja responde 429 quando recebe muitas requisicoes seguidas: espera e
    # tenta de novo, em vez de marcar a pagina como problema.
    for espera in (0, 5, 15, 30):
        time.sleep(espera)
        try:
            r = requests.get(url, headers=CABECALHO, timeout=20, allow_redirects=True)
        except requests.RequestException as erro:
            return url, "falha", "", type(erro).__name__
        if r.status_code != 429:
            break
    marca = next((m for m in MARCAS_DE_ERRO if m in r.text), "")
    situacao = "ok" if r.status_code == 200 and not marca else "problema"
    destino = r.url if r.url.rstrip("/") != url.rstrip("/") else ""
    return url, situacao, str(r.status_code), marca or (f"redireciona para {destino}" if destino else "")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("urls", nargs="*")
    p.add_argument("--arquivo", help="um URL por linha")
    p.add_argument("--cliente", help="cliente.json (usa pagina_esgotada_texto)")
    p.add_argument("--marca", action="append", help="texto que indica pagina de erro")
    a = p.parse_args()

    global MARCAS_DE_ERRO
    if a.cliente:
        import json
        with open(a.cliente, encoding="utf-8") as f:
            MARCAS_DE_ERRO = tuple(json.load(f).get("pagina_esgotada_texto") or MARCAS_DE_ERRO)
    if a.marca:
        MARCAS_DE_ERRO = tuple(a.marca)

    urls = list(a.urls)
    if a.arquivo:
        with open(a.arquivo, encoding="utf-8") as f:
            urls += [l.strip() for l in f if l.strip()]
    urls = list(dict.fromkeys(u for u in urls if u.startswith("http")))
    if not urls:
        p.error("nenhum URL")

    print("situacao\tstatus\turl\tobservacao")
    with ThreadPoolExecutor(max_workers=3) as pool:
        for url, situacao, status, obs in pool.map(confere, urls):
            print(f"{situacao}\t{status}\t{url}\t{obs}")


if __name__ == "__main__":
    main()
