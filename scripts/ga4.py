#!/usr/bin/env python3
"""
Relatório do GA4 pela Data API, com a conta de serviço do cliente.json. Não escreve nada.

Serve para quem não tem MCP do GA4: basta a conta de serviço ter acesso de
leitor na propriedade (Administrador > Gerenciamento de acesso à propriedade).

Uso:
    python ga4.py --cliente clientes/hocks/cliente.json 2026-09-28 2026-10-04 \\
        --dimensoes sessionDefaultChannelGroup --metricas sessions,ecommercePurchases,purchaseRevenue
    python ga4.py --cliente ... 2026-09-28 2026-10-04 --dimensoes date --metricas sessions --limite 50
"""

import argparse
import os
import sys

from comum import carrega_cliente


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--cliente", required=True)
    p.add_argument("inicio")
    p.add_argument("fim")
    p.add_argument("--dimensoes", default="")
    p.add_argument("--metricas", required=True)
    p.add_argument("--limite", type=int, default=100)
    p.add_argument("--propriedade", help="sobrepõe contas.ga4 do cliente.json")
    a = p.parse_args()

    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (DateRange, Dimension, Metric,
                                                    OrderBy, RunReportRequest)
    from google.oauth2 import service_account

    cliente = carrega_cliente(a.cliente)
    prop = str(a.propriedade or cliente.get("contas", {}).get("ga4", "")).replace("properties/", "")
    if not prop:
        sys.exit("ERRO: sem propriedade do GA4 (contas.ga4 no cliente.json).")
    chave = cliente.get("credencial_google") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not chave or not os.path.exists(chave):
        sys.exit("ERRO: chave da conta de serviço não encontrada (credencial_google).")
    cred = service_account.Credentials.from_service_account_file(
        chave, scopes=["https://www.googleapis.com/auth/analytics.readonly"])

    dims = [d for d in a.dimensoes.split(",") if d]
    mets = [m for m in a.metricas.split(",") if m]
    req = RunReportRequest(
        property=f"properties/{prop}",
        date_ranges=[DateRange(start_date=a.inicio, end_date=a.fim)],
        dimensions=[Dimension(name=d) for d in dims],
        metrics=[Metric(name=m) for m in mets],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name=mets[0]), desc=True)],
        limit=a.limite,
    )
    r = BetaAnalyticsDataClient(credentials=cred).run_report(req)
    print(f"GA4 {prop}, {a.inicio} a {a.fim}, {r.row_count} linhas no total (mostrando até {a.limite})")
    print("\t".join(dims + mets))
    for linha in r.rows:
        print("\t".join([v.value for v in linha.dimension_values] + [v.value for v in linha.metric_values]))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        sys.exit(1)
