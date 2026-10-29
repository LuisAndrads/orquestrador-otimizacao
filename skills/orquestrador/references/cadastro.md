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
     aba `Acom. Canais`; hora da atualização em `configs!B5`. Em algumas PDAs
     essa célula está vazia ou nem existe (a aba `configs` tem só três
     linhas). Nesse caso, a referência de atualização é o dia mais recente da
     `dados_bq`: grave isso no `CONTEXTO.md`, sem marcar a planilha como erro.
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
   Não confie só no que a pessoa disser:
   - **Meta:** a lista de contas vem em páginas de 50. Percorra todas as
     páginas, até não haver cursor, e procure o nome da loja, a razão social e
     o nome do BM. Conta parecida que não é do cliente fica registrada com o
     motivo, para a auditoria não perguntar de novo.
   - **Google Ads:** na MCC, procure nomes parecidos. Na dúvida, confira para
     qual site levam os anúncios da conta.
   - **Merchant Center:** se a pessoa não souber o ID, ele aparece no
     `shopping_setting.merchant_id` da campanha de Shopping ou PMax.
6. **Concorrentes:** de três a cinco lojas, com site e Instagram.
7. **Fuso** (padrão: Brasília, -03:00) e **o mês ou trimestre** da meta.

## 2A. Plataforma Convertr (Convertr Commerce)

A régua do dia a dia vem da aba `dados_bq` da própria PDA 13.0 ("Dashboard de
Acompanhamento Diário"), que é a mesma planilha das metas. Ela traz o total
do dia, sem um pedido por linha e sem UTM. O pedido a pedido com UTM existe na
exportação do painel da loja (item 7).

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
   - A `dados_bq` não tem pedido a pedido nem UTM. Na rodada semanal, a
     régua da loja é o total do dia e a divisão por canal é a do GA4
     (`pedidos.py canais`). Pedido por canal e análise por pedido saem da
     exportação do painel (item 7), quando houver uma do período; sem ela,
     "sem exportação do painel para o período", sem estimar.
7. **Exportação do painel.** Peça ao gestor as três exportações do painel
   Convertr Commerce: pedidos, clientes e produtos com estoque. Elas são
   obrigatórias na auditoria inicial e opcionais nas rodadas.
   - O arquivo de pedidos tem uma linha por item, com status, pagamento,
     cupom, frete, estado, histórico de status e, no campo `additional`, as
     UTMs gravadas no pedido (`utm_source`, `utm_medium`, `utm_campaign`,
     `utm_content`, `utm_term`, `utm_id`). Isso dá a terceira régua do método
     (pedidos com a UTM da campanha) também nas lojas Convertr.
   - Antes de usar, confira o faturado mês a mês contra a `dados_bq` e tire os
     pedidos de teste da equipe: `pedidos.py --cliente <json> totais <ini> <fim>
     --painel <csv> --excluir-email <domínio da equipe>`, ao lado do mesmo
     comando sem `--painel`. Pedido por UTM: modo `utm` com `--painel`. Se não bater,
     registre a diferença e não use o arquivo.
   - **Dado pessoal.** Os três arquivos têm nome, CPF e endereço de consumidor
     final. Ficam numa pasta temporária fora do repositório, nunca no git nem
     na pasta do cliente. Os documentos levam só números somados.
   - A exportação vale para o período em que foi tirada. Para uma leitura
     nova, peça uma exportação nova.

## 3. Criar a pasta

Copie `assets/cliente/` para `clientes/<cliente>/` e preencha:

- `cliente.json` com o que a entrevista trouxe.
- `CONTEXTO.md`: negócio em duas linhas, contas e IDs, planilha de metas
  (onde está cada número), concorrentes, fontes e status de cada uma.
- `ABERTO.md` da raiz com o primeiro próximo passo de cada frente.

O cadastro é a exceção à regra de que só o modo `registrar` escreve em
`DECISOES.md` e `ABERTO.md`: ele cria esses arquivos e faz a primeira entrada.

## 3A. Exportações para o BigQuery (antes da auditoria inicial)

As ferramentas de GA4, Google Ads e Merchant devolvem poucas linhas por
consulta e não filtram evento. Com os dados no BigQuery, uma consulta pequena
traz caminho de conversão, primeira origem de cada compra e o funil inteiro,
gastando muito menos token que os leitores. Por isso as quatro exportações
são ligadas no cadastro, antes da auditoria inicial, e não depois.

| Exportação | Quem liga e onde | Conjunto de dados | Região |
|---|---|---|---|
| GA4 | quem é proprietário do projeto e Editor no GA4, na tela: Administrador do GA4 → Vinculações do BigQuery, exportação diária | automático: `analytics_<id da propriedade>` | São Paulo |
| Google Ads | o Claude, com `bq mk --transfer_config` e o login de um coordenador, pedindo os dias anteriores | `ads_<cliente>` | São Paulo |
| Merchant Center | o Claude, com `bq mk --transfer_config` e o login de um coordenador | `merchant_<cliente>` | **EUA** |
| Search Console | o proprietário da propriedade no Search Console, na tela: Configurações → Exportação em massa de dados | `searchconsole_<cliente>` | São Paulo |

`<cliente>` é o nome da pasta do cliente, sem hífen. O projeto é o da
Convertr (`ambiente.json`, campo `projeto_bigquery`), com faturamento ativo.
Num projeto sem faturamento as transferências e o Search Console não rodam e
as tabelas se apagam com 60 dias: não ligue exportação de cliente nele
(`instalacao.md`, trilha A, "Sem acesso ao projeto da Convertr").

1. **Acessos do cliente, uma vez por cliente.** São dois e-mails de conta de
   serviço. O da pessoa (`orq-<nome>`, no `ambiente.json`) lê planilha e GA4
   pelos scripts. O das exportações (`conta_servico_exportacoes`, no
   `ambiente.json`) é dono das transferências e não sai do projeto quando
   alguém sai do time.

   | Onde | E-mail | Papel | Quem consegue adicionar, e onde |
   |---|---|---|---|
   | Planilhas (metas e base de pedidos) | o da pessoa | Leitor | quem edita a planilha: **Compartilhar** → colar → **Leitor** → desmarcar "Notificar" → **Compartilhar** |
   | GA4 | o da pessoa | Leitor | administrador do GA4: **Administrador** → **Gerenciamento de acesso à propriedade** → **+** → **Adicionar usuários** |
   | Google Ads | o das exportações | Somente leitura | na MCC, uma vez, vale para todas as contas dela: administrador da MCC → **Administrador** → **Acesso e segurança** → **+**. Sem MCC, o administrador da conta do cliente faz o mesmo na conta. Analista com acesso só à conta, sem ser administrador, pede ao coordenador |
   | Merchant Center | o das exportações | Acesso padrão | administrador do Merchant: **Configurações** → **Pessoas e acesso** → **Adicionar pessoa** |
   | Search Console | nenhum | | a exportação não usa conta de serviço; só exige que quem liga seja proprietário da propriedade |
   | Meta | nenhum | | o conector usa o Facebook da pessoa, que precisa ver a conta de anúncio no portfólio do cliente |
   | Clarity | nenhum | | token do projeto do cliente (seção 4, "Clarity com mais de um cliente") |

   Quem não consegue adicionar não insiste: registra no `ABERTO.md` quem
   precisa fazer o quê e segue com as outras fontes.
2. **O GA4 aceita um vínculo com o BigQuery só.** Antes de ligar, abra
   Administrador → Vinculações do BigQuery. Com um vínculo feito, o botão
   **Vincular** fica desligado (visto em 29/10/2026). Se o vínculo for com o
   projeto da Convertr, só confira o conjunto. Se for com outro projeto (do
   cliente ou de outra agência), não desfaça: desvincular corta a exportação
   de quem usa. Peça ao dono daquele projeto leitura no conjunto
   (`roles/bigquery.dataViewer` no `analytics_<id>`, para o e-mail da pessoa
   e o da conta de serviço dela) e grave o projeto em `bigquery.projeto_ga4`
   do `cliente.json`. Sem a leitura, a fonte fica "GA4 no BigQuery de outro
   projeto, sem acesso". No Search Console, se a tela já mostrar uma
   exportação para outro projeto, siga o mesmo caminho.
3. **Quem cria as transferências.** A conta de serviço sozinha não cria
   transferência (falta a permissão `bigquery.transfers.update`). O Claude
   cria as de Google Ads e Merchant com o login no `gcloud` de um coordenador
   (`instalacao.md`, trilha F, item 3), apontando a conta das exportações
   como dona (`--service_account_name`). Sem `gcloud` logado, rode antes a
   trilha A. Sem o papel de coordenador, o erro é de permissão: registre no
   `ABERTO.md` e peça ao coordenador. Criar transferência muda configuração
   do projeto: mostre o comando e espere o "ok" da pessoa. GA4 e Search
   Console não têm caminho por programa e são ligados na tela, com o passo a
   passo da tabela.
4. **Merchant fica nos EUA.** São Paulo não está entre as regiões que a
   transferência do Merchant aceita, e todas as cargas falham com "Failed to
   schedule run". Crie o conjunto `merchant_<cliente>` com `--location=US`.
   Consequência: uma consulta não junta Merchant com GA4 ou Google Ads direto;
   leia cada um e cruze o resultado.
5. **Search Console:** os dois papéis da conta de exportação do Google são
   dados uma vez por projeto, na trilha F, item 1d. Depois disso, cada cliente
   só precisa ser ligado na tela.
6. **O que cada exportação traz do passado.** GA4 e Search Console começam no
   dia em que são ligados. O Google Ads aceita pedir dias anteriores, uma
   carga por dia, que entram em fila e levam horas. O Merchant pede sozinho os
   dois dias anteriores; desempenho e mais vendidos aceitam até 2 anos para
   trás, produtos e estoque até 14 dias, e preço competitivo nada. Os
   caminhos de conversão do GA4 antes da exportação saem pela tela
   (Publicidade → Caminhos de conversão → exportar). Grave no `CONTEXTO.md` a
   data de início de cada uma: antes dela, a resposta é "sem dado no
   BigQuery", e um buraco no meio (exportação que parou e voltou) também fica
   escrito com as datas. Confira também se a transferência grava no conjunto
   certo: transferência apontando para um conjunto apagado ou renomeado para
   de carregar sem aviso.
7. **Custo.** A exportação diária do GA4 e as transferências de Google Ads e
   Merchant não cobram; o armazenamento sai no faturamento do projeto da
   Convertr. A exportação contínua do GA4 (streaming) cobra por volume:
   deixe desligada, salvo pedido. Consulta tem 1 TB grátis por mês; acima de
   1 GB processado, pare e pergunte.
8. Grave os nomes dos conjuntos em `bigquery` do `cliente.json`.
9. Teste cada conjunto com uma consulta pequena (uma tabela, um dia, poucas
   colunas) e ponha o resultado na tabela "Fontes". Conjunto que ainda não
   recebeu o primeiro dia fica "ligado, aguardando o primeiro dia".
10. **Na auditoria inicial, o BigQuery vem primeiro:** consulte o que ele
    cobre e chame os leitores só para o que ele não cobre (estrutura das
    contas, criativos, histórico de alterações, concorrentes). A regra de
    parar e perguntar antes de consulta que cobre continua valendo.

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
| BigQuery | uma consulta pequena em cada conjunto da seção 3A |
| Exportação do painel (Convertr) | faturado mês a mês do arquivo contra a `dados_bq` (seção 2A, item 7) |

**Clarity com mais de um cliente.** O conector oficial guarda um token só, ou
seja, um projeto. Para cada cliente, crie uma conexão própria
(`clarity-<cliente>`) que leia o token de um arquivo fora do git, com
permissão só do dono (`chmod 600`), e abra esse arquivo para a pessoa colar o
token; nunca peça o token no chat. A conexão nova só aparece numa conversa
aberta depois de criada; no mesmo dia, teste pela API direto. Projeto criado
no cadastro só tem dado a partir daquele dia: registre a data.

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
   e `Write(clientes/<cliente>/otimizacoes/**)`. Acrescente também
   `Bash(jq *)`: resposta grande de MCP é salva em arquivo, e os leitores
   precisam filtrar e contar esse arquivo sem pedir permissão.

## 6. Registro

Entrada em `clientes/<cliente>/geral/DECISOES.md` ("Cliente cadastrado no
orquestrador"), com as fontes ativas e as pendências, e o `ABERTO.md` com a
primeira rodada sugerida (a próxima segunda-feira).
