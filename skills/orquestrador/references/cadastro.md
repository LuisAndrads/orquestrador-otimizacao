# Cadastro de cliente

Objetivo: deixar o cliente pronto para `retomar`, `segunda` e `quinta`, com
cada fonte de dado testada de verdade. A entrevista é um questionário único:
mande todas as perguntas da seção 2 numeradas numa só mensagem, com exemplo
de resposta; a pessoa responde o que souber e depois você pergunta só o que
faltou. Nada fica marcado
como pronto porque a pessoa disse que fez: só depois de um teste que devolve
dado do cliente.

## 1. Preparar o ambiente (uma vez por computador)

Se `~/.orquestrador-otimizacao/ambiente.json` não existir, rode antes o modo
`preparar` (`references/instalacao.md`): ele audita o computador, instala o que
falta e guia as contas. O que está abaixo é o mínimo, para quem já preparou.

1. Ambiente Python dos scripts:
   ```
   python3 -m venv ~/.orquestrador-otimizacao/venv
   ~/.orquestrador-otimizacao/venv/bin/pip install -r <raiz do plugin>/scripts/requirements.txt
   ```
   Se já existir, pule.
2. Conta de serviço do Google (para ler planilhas e GA4): pergunte o caminho do
   arquivo JSON da chave e grave em `credencial_google`. Sem chave, deixe o
   campo vazio: a leitura de planilha fica "sem acesso", o cadastro registra a
   pendência e o resto segue.

**Onde fica o plugin.** A raiz do plugin é a pasta dois níveis acima da pasta
desta skill (o caminho da skill aparece quando ela é carregada); em comandos e
configurações, use sempre o caminho absoluto expandido, sem `~` e sem
variável.

## 2. Entrevista

1. **Nome do cliente e site da loja.**
2. **Plataforma da loja** (Convertr, Nuvemshop, Tray, Shopify, VTEX, outra).
   Pergunte antes da planilha, porque ela muda o caminho dos pedidos: se for
   "Convertr", "Convertr Commerce" ou "plataforma da Convertr", siga a seção
   **2A. Plataforma Convertr** abaixo no lugar dos itens 3 e 4.
3. **Planilha de metas.** Três casos:
   - Modelo 13.0 (padrão eFashion/Convertr): peça só o ID da planilha. As metas
     ficam na aba `Visão Geral`, linhas 5 a 22, uma coluna por mês (C = jan …
     N = dez); o realizado a partir da linha 24; meta e realizado por canal na
     aba `Acom. Canais`; hora da atualização em `configs!B5`.
   - Outro modelo: pergunte em que aba e linha (ou célula) está cada meta:
     faturamento faturado e captado, ROAS faturado, investimento, sessões, CPS,
     taxa de conversão, ticket médio, taxa de aprovação. Grave no `cliente.json`
     e no `CONTEXTO.md`.
   - Sem planilha: crie a meta do mês com o gestor (faturamento e ROAS faturado
     no mínimo; derive investimento = faturamento ÷ ROAS), grave em
     `metas_manuais` do `cliente.json` (chave `AAAA-MM`) e repita no
     `CONTEXTO.md`. Recomende implantar a planilha de acompanhamento.
4. **Base de pedidos.** O cliente tem a Base de Dados de pedidos (planilha
   alimentada pela plataforma da loja)? Peça o ID e o nome da aba de pedidos.
   Leia o cabeçalho com `scripts/le_planilha.py` e monte o mapa de colunas no
   `cliente.json` (id, data, total, UTMs e a regra de "faturado"). Sem base, a
   régua da loja fica "sem dado" e o cadastro registra a pendência; deixe
   `base_pedidos.id` vazio.

   Regra de "faturado" (campo `faturado`): base com status de pagamento usa
   `{"tipo": "pagamento", "coluna_pagamento": ..., "valor_pago": ...,
   "coluna_status": ..., "valor_cancelado": ...}`; base com situação
   padronizada (padrão da planilha de acompanhamento) usa
   `{"tipo": "situacao", "coluna": "situacao", "excluir_se_contem":
   ["Cancelado", "Pendente", "Reembols"]}`.
5. **Contas e IDs:** conta de anúncios do Meta, conta do Google Ads (e a MCC
   pela qual ela é acessada), propriedade do GA4, Merchant Center, Clarity.
6. **Concorrentes:** de três a cinco lojas, com site e Instagram.
7. **Fuso** (padrão: Brasília, -03:00) e **o mês ou trimestre** da meta.

## 2A. Plataforma Convertr (Convertr Commerce)

Não existe base com um pedido por linha nem UTM. Os pedidos vêm da aba
`dados_bq` da própria PDA 13.0 ("Dashboard de Acompanhamento Diário"), que é a
mesma planilha das metas.

1. Peça só o ID da PDA 13.0. O `store_id` da loja está em `Visão Geral!B1` e
   em `configs!B1`: leia e grave no `CONTEXTO.md`.
2. No `cliente.json`: `"plataforma": "convertr"`, `planilhas.metas.id` = ID da
   PDA e `planilhas.base_pedidos` = `{"tipo": "dados_bq", "id": "", "aba":
   "dados_bq"}` (id vazio = a própria PDA).
3. Como a aba é: cabeçalho na linha 1, dado da linha 2 em diante, o dia mais
   novo no topo, desde jan/2024, data DD/MM/AAAA e vírgula decimal. Linha com
   `channel` vazio = pedidos da loja no dia (`total_pedidos` = captado,
   `total_pedidos_aprovados` = faturado, `qtd_pedidos` = pedidos captados,
   `qtd_pedidos_aprovados` = faturados, primeira compra, recompra e peças).
   Linha com `channel` preenchido = gasto e cliques de mídia e o GA4 do canal
   (sessões, compradores, `totalRevenue` e o funil por evento). Aprovado já
   exclui cancel, refunded, pending, reembolso, estorno e pendente.
4. O gasto do Meta na `dados_bq` vem sem imposto; a PDA soma o imposto, cuja
   taxa fica em `Visão Geral!E1`. Grave a taxa no `CONTEXTO.md`.
5. **Conferência obrigatória antes de marcar a fonte como ativa.** Na aba
   "Acom. - Funil & Canais", procure pelo rótulo (as linhas mudam de cliente
   para cliente) "Finalizadas (plataforma)", "Aprovados (plataforma)",
   "Receita Captada (plataforma)" e "Receita Faturada (plataforma)". Compare
   uma semana fechada, dia a dia, com
   `pedidos.py --cliente <json> totais <ini> <fim> --por-dia`. Os números
   precisam bater exatamente; se não baterem, a fonte fica "erro" com a
   diferença.
6. Regras que valem para sempre (grave no `CONTEXTO.md`):
   - Nunca mexer em `B2` e `C2` da "Acom. - Funil & Canais": são os controles
     de mês e de visão, e alterar grava na planilha do cliente para todo mundo.
     Qualquer período se calcula somando a `dados_bq`.
   - Os aprovados dos últimos dias mudam depois (pendente vira aprovado ou
     cancelado). Releia sempre; a última semana é provisória no diário.
   - O dia de hoje está incompleto; o dia fechado é ontem.
   - Não usar a aba `bq_geral` (ligada ao BigQuery, a leitura comum dá
     "Unable to parse range" e não traz nada a mais) nem "Pedidos
     Plataforma" (parou antes da migração).
   - Não há pedido a pedido nem UTM para o gestor (o detalhe está num
     projeto do BigQuery da Convertr sem acesso). Régua da loja = total do dia;
     divisão por canal = a do GA4 (`pedidos.py canais`); atribuição de pedido
     por canal: "indisponível nesta plataforma", sem estimar. Análise por pedido
     (cancelamento por região, recompra por cliente) só com exportação manual
     pontual pedida ao gestor.

## 3. Criar a pasta

Copie `assets/cliente/` para `clientes/<cliente>/` e preencha:

- `cliente.json` com o que a entrevista trouxe.
- `CONTEXTO.md`: negócio em duas linhas, contas e IDs, planilha de metas
  (onde está cada número), concorrentes, fontes e status de cada uma.
- `ABERTO.md` da raiz com o primeiro próximo passo de cada frente.

O cadastro é a exceção à regra de que só o modo `registrar` escreve em
`DECISOES.md` e `ABERTO.md`: ele cria esses arquivos e faz a primeira entrada.

## 4. Testar cada fonte

Para cada fonte, uma leitura real e curta, e o resultado na tabela "Fontes" do
`CONTEXTO.md` (ativo, sem acesso, ou erro com a mensagem):

| Fonte | Teste |
|---|---|
| Planilha de metas | `le_planilha.py --cliente <json> --chave metas "Visão Geral!B7:N8"` (ou a célula do modelo) |
| Base de pedidos | `pedidos.py --cliente <json> totais <ontem> <ontem>` (Convertr: a conferência da seção 2A) |
| Meta Ads | MCP do Meta: gasto de ontem da conta |
| Google Ads | MCP ou API: custo de ontem da conta, pela MCC indicada. Sem MCP: o custo do Google na planilha de metas (aba de canais ou `dados_bq`) e, com autorização, a interface pelo navegador |
| GA4 | MCP do GA4, ou, sem MCP, `ga4.py --cliente <json> <ontem> <ontem> --metricas sessions` |
| Merchant Center | resumo de problemas dos produtos |
| Clarity | dashboard de ontem |

Fonte sem MCP ligado nesta máquina: "sem acesso nesta máquina". Fonte com MCP
que devolve erro: "erro" e a mensagem. Nenhum dos dois bloqueia o cadastro; o
cadastro fica completo com cada fonte em um dos três estados (ativo, sem
acesso, erro) e a pendência registrada no `ABERTO.md`.

## 5. Travas de copiloto

Nesta fase nada é alterado em conta. Transforme isso em trava do Claude Code,
e não só em instrução:

1. Liste as ferramentas das MCPs de anúncio e de loja disponíveis nesta
   sessão (busca de ferramentas) e separe as que escrevem: o verbo da
   ferramenta é `create`, `update`, `delete`, `activate`, `pause`, `upload`,
   `boost`, `bulk_delete`, `remove`, `assign` ou `set_` (confira o nome inteiro:
   `asset` e `dataset` não são verbo de escrita). Consulta de BigQuery que cobra
   por volume é leitura com custo: não entra no `deny`, mas os leitores pedem
   autorização antes de consultas grandes. Os nomes têm o identificador do
   conector daquela máquina, então a lista é gerada em cada computador e não
   é copiada de outra pessoa.
2. Mostre a lista ao gestor e, com o aceite dele, acrescente essas ferramentas
   em `permissions.deny` do `.claude/settings.local.json` da pasta de trabalho.
3. Acrescente em `permissions.allow` os comandos de leitura dos scripts, para a
   rodada não parar pedindo permissão:
   `Bash(<home>/.orquestrador-otimizacao/venv/bin/python <raiz do plugin>/scripts/*)`,
   com os dois caminhos absolutos e expandidos (espaço no caminho é aceito)
   e `Write(clientes/<cliente>/otimizacoes/**)`.

## 6. Registro

Entrada em `clientes/<cliente>/geral/DECISOES.md` ("Cliente cadastrado no
orquestrador"), com as fontes ativas e as pendências, e o `ABERTO.md` com a
primeira rodada sugerida (a próxima segunda-feira).
