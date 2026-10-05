# Regras aprendidas no uso real

Cada regra abaixo veio de um erro ou de uma correção do Luis na conta da
uma conta real de moda (setembro e outubro de 2026). Elas valem para todo cliente.

## Meta é a da planilha

O faturamento, o ROAS faturado e as métricas secundárias que a otimização
persegue saem da planilha de metas do cliente (no modelo 13.0, aba Visão Geral).
Número de "equilíbrio" ou de margem escrito em outro arquivo não é a meta. Se a
planilha não tiver meta para o mês, o primeiro passo é criar uma com o gestor.

## Três réguas

O ROAS e o CPA do gerenciador são uma régua. Toda leitura que sustenta uma
decisão mostra também:

1. **GA4**, por ID de campanha (`sessionCampaignId`) e, no Meta, por ID de
   anúncio (`utm_adid`). Nunca por nome: o nome gravado na UTM do Meta vem do
   momento em que o anúncio foi criado, e a mesma campanha aparece com nomes
   diferentes.
2. **Plataforma da loja**, pelos pedidos com a UTM da campanha
   (`scripts/pedidos.py utm`). É o último toque da loja.

A diferença entre as três é normal. O que se procura é se ela faz sentido.

## Antes de propor pausar, cortar ou escalar

Pausar um anúncio, conjunto ou campanha pode derrubar compras que aparecem em
outro lugar: a pessoa entra por ele e compra por outra campanha ou outro
produto. Responda antes:

1. As três réguas concordam?
2. Onde o objeto está na jornada? Leitura barata: no GA4, compras em que a
   campanha é a primeira origem (`firstUserCampaignId`) contra compras em que é
   a origem da sessão; conversões assistidas no Google.
3. Ele alimenta outra campanha (topo alimentando remarketing)?
4. O que mais muda ao mesmo tempo (teste em andamento, controle, estoque)?

Sem as respostas, a proposta sai como "pendente de análise de jornada".
Análise profunda de caminhos só com autorização do gestor.

## Estrutura antes do detalhe (Meta)

Antes de recomendar mexida em conjunto ou anúncio: histórico de alterações dos
últimos 14 dias; janelas fechadas de 7 e 14 dias, iguais às do gerenciador e
iguais para todo objeto comparado; orçamento, aprendizado e compras por semana;
público e sobreposição; estoque do produto; efeitos cruzados. Troca de ID de
criativo não prova criativo novo (editar texto, URL ou UTM troca o ID).

## Estado de hoje se lê com dado até ontem

Janela fechada serve para medir o período, não para descrever como um anúncio
está hoje. Antes de dizer que algo está parado, sem gasto ou em aprendizado,
leia os últimos dias e o `ABERTO.md`. (Erro real: dizer que um anúncio estava
"sem gasto" com leitura que parava dois dias antes da reativação dele.)

## Google: o que olhar que o gerenciador não mostra

- **Estrutura da Shopping:** listar os grupos, o ROAS desejado de cada um e os
  nós de produto. Dois grupos com o nó "todos os outros" ativo disputam o mesmo
  catálogo, e o de meta menor ganha quase todos os leilões. (Caso real: uma
  campanha chamada "top conversores" era uma Shopping aberta, com 90% da verba
  no grupo de meta menor e 42% do custo em produtos sem conversão.)
- **Marca separada de não marca** nos termos de pesquisa: a marca infla o ROAS
  da campanha.
- **Parcela de impressão e perda por orçamento**: a API devolve
  (`metrics.search_impression_share`, `search_budget_lost_impression_share`);
  quando o MCP não traz, use a API ou, com autorização, a interface pelo
  navegador, só leitura.
- No Merchant Center cada tamanho é um item próprio; tamanho sem estoque já
  sai do leilão sozinho.

## Recomendação externa

Gerente de contas do Google ou do Meta, agência e ferramenta trazem o
resultado na régua da plataforma. Leia como insumo, filtre pelo resultado do
projeto e diga o que serve e o que não serve, com dado. Pausar uma campanha que
"tinha ROAS 5 na plataforma" pode melhorar o ROAS do projeto.

## Dados

- Base de pedidos pode ter linha repetida (gravação repetida por falha de
  rede). O `scripts/pedidos.py` conta cada pedido uma vez e avisa quando há
  repetição. Divergência acima de 3% entre a planilha e a base é divergência,
  não arredondamento.
- Conferir a hora da última atualização de qualquer planilha antes de usar.
- Página de produto esgotado pode responder HTTP 200 com texto de erro; o
  `scripts/valida_urls.py` procura o texto.

## Token

Rodada completa é cara. Prefira os scripts e chamadas diretas às MCPs antes de
disparar agentes. Leitores com escopo próprio e enxuto; quinta mais leve que
segunda; aprofundamento só depois de o orquestrador pedir e o gestor
autorizar. Termine com o que já foi coletado em vez de chamar agente de novo.

## Escrita

Frases completas, sem tom de efeito. Separe "dado:" de "hipótese:". Linguagem
que o dono da loja entende quando o texto for para ele.
