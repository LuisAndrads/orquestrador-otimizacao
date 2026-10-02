# Rotina de otimização semanal

Método de otimização de Luis Andrade (eFashion Performance / Convertr), escrito em
30/09/2026 e refinado com o uso real na conta da Ladydress. Vale para qualquer
cliente de e-commerce. O que é específico de cada cliente (onde fica a planilha
de metas, quais abas, quais contas) fica no `CONTEXTO.md` e no `cliente.json`
dele.

Esta rotina é seguida pela skill `orquestrador` deste plugin. Os agentes
`leitor-*` só buscam dados. Quem decide o que investigar e o que propor é o
orquestrador, com o critério descrito aqui. "Gestor da conta" é a pessoa do
time responsável pelo cliente, que conversa com o Claude e executa nas
plataformas.

## O norte

A otimização existe para bater a meta de faturamento do mês com o ROAS faturado
definido. Em projeto trimestral, a referência é a meta do trimestre. Os dois
números, meta de faturamento e ROAS faturado, saem da planilha de metas do
cliente e de nenhum outro lugar. Se o cliente ainda não tiver uma meta, o
primeiro trabalho é criar uma com ele, porque sem meta não há contra o que
otimizar.

## As métricas secundárias

São as métricas que explicam por que o norte está sendo batido ou não. Em ordem
de importância:

1. Taxa de conversão e custo por sessão, com o mesmo peso.
2. Ticket médio.
3. Taxa de aprovação.
4. CAC.
5. As demais que a planilha de metas trouxer, como quantidade de sessões.

Cada uma tem a sua meta na planilha. A análise compara o realizado com essa meta,
e não com uma referência de mercado.

## A ordem da análise

A análise nunca começa pela conta de anúncios, mas as contas de anúncio são
olhadas em toda rodada.

1. **Projeto.** Comparar o realizado do mês com a meta na aba de visão geral da
   planilha, levando em conta o dia do mês em que se está.
2. **Projeção.** Projetar quanto o mês vai fechar no ritmo atual e quanto falta
   para a meta.
3. **Métricas ofensoras.** Identificar quais métricas secundárias estão abaixo da
   meta, na semana e no acumulado do mês. Uma métrica pode estar bem no mês e mal
   na semana, e isso também conta.
4. **Detalhamento.** Detalhar cada métrica ofensora até achar o que está
   causando o resultado ruim. Não existe roteiro fixo para isso: a investigação
   vai para onde o dado apontar. Os caminhos abaixo são pontos de partida comuns
   e não regras:
   - Custo por sessão alto: pode ser um canal que ficou mais caro, a mídia que
     encareceu de forma geral, o tráfego orgânico que caiu e deixou o custo médio
     mais alto, ou outra causa.
   - Taxa de conversão caindo: pode ser uma etapa do funil que oscilou, um
     produto ou uma página de categoria que mudou, ou o mix de produtos.
   - Canal abaixo da própria meta: a aba de acompanhamento de canais mostra quanto
     cada canal deveria estar entregando, conforme a divisão feita na projeção.

   Quando o dado mostrar que um caminho está normal, a investigação abandona esse
   caminho e segue por outro. O rascunho registra o que foi descartado e por quê.
5. **Hipóteses e plano de ação.** Para cada causa encontrada, escrever a
   hipótese de melhoria e o plano de ação que a testa. O plano sempre traz:
   - as tarefas que precisam ser executadas, com responsável e data;
   - o resultado esperado de cada tarefa, em métrica e valor;
   - por quanto tempo o teste vai rodar antes de ser lido;
   - o que se espera concluir do teste, ou seja, qual resultado confirma a
     hipótese e qual a derruba.

**Contas de anúncio.** Meta Ads e Google Ads entram em toda rodada. A diferença
está na profundidade. Quando a métrica investigada passa por uma conta, a
leitura desce até conjunto, anúncio, termo de busca ou produto. Quando não passa,
a leitura fica na saúde geral da conta: gasto contra o ritmo, ROAS, aprendizado,
alterações recentes e alertas da plataforma.

Antes de propor mexida em qualquer campanha, olhar a estrutura inteira e não o
objeto isolado: histórico de alterações dos últimos 14 dias; janelas fechadas de
7 e 14 dias, iguais às do gerenciador e iguais para todo objeto comparado;
orçamento, aprendizado e compras por semana; público e sobreposição; estoque do
produto; efeitos cruzados entre canais e com a verba do mês.

### Três réguas de resultado

O ROAS e o custo por compra que o gerenciador mostra são uma das réguas, e não a
única. Toda leitura de campanha ou anúncio que for sustentar uma decisão mostra o
resultado nas três:

1. **Gerenciador** (Meta Ads, Google Ads), com a atribuição da própria plataforma.
2. **GA4**, por ID de campanha e, no Meta, por ID de anúncio (`utm_adid`).
3. **Nuvemshop**, pelos pedidos com a UTM da campanha ou do anúncio
   (`scripts/pedidos.py utm` deste plugin, que lê a base de pedidos do cliente).

A diferença entre as três é normal, porque cada uma atribui de um jeito. O que a
análise procura é se a diferença faz sentido. Uma campanha forte no gerenciador
e fraca no GA4 e na Nuvemshop pode estar levando crédito de compra que não gerou.
Uma campanha fraca no gerenciador e forte nas outras duas pode estar abrindo
compras que fecham em outro lugar.

### Antes de propor pausar ou cortar

Pausar um anúncio, um conjunto ou uma campanha pode derrubar compras que
aparecem em outro lugar. A pessoa entra por aquele anúncio, mas compra por outra
campanha ou compra outro produto. Antes de propor pausa, corte de verba ou
exclusão, a análise precisa responder:

1. **As três réguas concordam?** Se só o gerenciador mostra resultado ruim, a
   pausa não está justificada.
2. **Onde esse objeto está na jornada de compra?** Ele aparece no início, no
   meio ou no fim da compra, e quantos pontos de contato a compra costuma ter. A
   primeira leitura é barata: no GA4, comparar as compras em que a campanha é a
   primeira origem do usuário (`firstUserCampaignId`) com as compras em que é a
   origem da sessão (`sessionCampaignId`), e olhar as conversões assistidas do
   Google Ads. Uma campanha que aparece muito como primeira origem e pouco como
   última está abrindo jornada.
3. **Ele alimenta outra campanha?** O topo alimenta o remarketing. Uma
   campanha que traz muita sessão nova pode estar sustentando a compra de outra.
4. **O que mais muda ao mesmo tempo?** Teste em andamento, campanha usada como
   controle, estoque do produto.

Se essas respostas não estiverem disponíveis, a proposta de pausa sai no diário
como **"pendente de análise de jornada"**, e não como recomendação. A análise
profunda de jornada (caminhos de conversão completos, BigQuery) só roda com
autorização do gestor da conta, porque custa mais tempo e consulta.

## Os dois dias

**Segunda-feira: otimização obrigatória.** A pergunta da segunda é o que precisa
ser resolvido para atingir a meta do mês. A análise segue a ordem acima, lê a
semana fechada de segunda a domingo contra a semana anterior e contra o
acumulado do mês, e termina com as ações para as métricas ofensoras.

**Quinta-feira: otimização de oportunidade.** A quinta acompanha o andamento das
ações da segunda e procura melhorias que não dependem de mexer em campanha
naquele dia. Muitas vezes uma campanha foi alterada na segunda e não pode ser
tocada de novo tão cedo, e o tempo da quinta vai para o resto do projeto: página
de produto, SEO, etapas do funil, processo do cliente, mercado e região. As
oportunidades encontradas não são executadas na hora: entram no roadmap do
cliente para serem encaixadas no planejamento, às vezes com uma verba de teste
separada. Um exemplo registrado: uma campanha Shopping só para os estados do Sul,
porque a conversão lá é melhor e a maior parte do orçamento está indo para São
Paulo.

## Como a quinta escolhe o que olhar

A busca de oportunidade segue três critérios fixos, para que a escolha não
dependa do que parecer interessante no dia e para que nenhuma área fique semanas
sem ser olhada.

### O que conta como oportunidade

Oportunidade é um recorte do projeto (região, produto, categoria, canal,
aparelho, dia, base de clientes, criativo) que está muito acima ou muito abaixo
da média e cujo volume faz esse desvio valer dinheiro. O impacto é sempre
calculado da mesma forma e mostrado no diário:

> impacto mensal = (média do projeto − valor do recorte) × volume do recorte × ticket médio

Assim, oportunidades de áreas diferentes são comparadas na mesma unidade, reais
por mês contra a meta. Quando a métrica do recorte não for conversão (por
exemplo, CTR ou custo por sessão de um criativo), a conta usa o caminho
equivalente até receita, e o diário mostra cada passo.

Um candidato só entra no diário se passar pelos quatro filtros:

1. Há dado que mostra o desvio.
2. O impacto estimado é de pelo menos **1% da meta de faturamento do mês**.
3. Alguém consegue executar: o gestor da conta, a cliente ou o time dela.
4. A execução não depende de mexer numa campanha que está em teste ou em
   aprendizado.

### Varredura fixa e um aprofundamento

Toda quinta tem duas partes. A primeira é uma varredura fixa, igual em todas as
semanas, que lê rapidamente os sinais abaixo só para achar desvios. A segunda é
um aprofundamento em uma única área: a de maior impacto em reais na varredura.
O aprofundamento investiga a causa e monta a oportunidade completa (hipótese,
resultado esperado, esforço e verba de teste).

| Área | Onde olhar | Sinal de desvio |
|---|---|---|
| Funil | Abas de funil e perda de funil da planilha | Etapa que caiu contra a média de 4 semanas |
| Produto | Funil de produto, quadrante ABCD | Muita visita com pouca conversão, ou alta conversão com pouco tráfego |
| Mix e estoque | Estoque x vendas | Produto que vende sem estoque, estoque parado |
| Região | Funil de regiões, região x investimento | Conversão ou ROAS de um estado muito diferente da fatia de verba que ele recebe |
| Canais não pagos | Acompanhamento de canais | Orgânico, CRM ou direto abaixo da própria meta |
| Base de clientes | Análise da base, cross-sell | Recompra, combinações de produtos |
| Comportamento | Pagamento e horário, ritmo do dia | Dia, horário ou forma de pagamento fora do padrão |
| Página | Clarity, Merchant Center | Páginas com clique de frustração, produtos reprovados |
| Criativo e concorrência | Meta e Google (criativos ativos), Biblioteca de Anúncios do Meta, Central de Transparência do Google, Instagram dos concorrentes | Criativo nosso com CTR caindo ou frequência alta; formato ou tipo de conteúdo que o mercado está rodando e nós não (vídeo contra imagem, tipo de vídeo, abordagem) |

Search Console entra na varredura quando houver acesso. Até lá, o diário registra
que o dado falta.

**Criativo e concorrência** é uma área em que o processo ainda está sendo
formado. Por enquanto, a leitura compara os criativos que estão rodando nas
nossas contas com os que os concorrentes estão veiculando (formato, tipo de
vídeo, abordagem, oferta) e com o conteúdo que eles publicam no Instagram. A
oportunidade que sai daqui costuma ser produzir um tipo de conteúdo que falta,
e o investimento em produção entra como verba de teste. A lista de concorrentes
de cada cliente fica no `CONTEXTO.md` dele; se não houver, montar a lista com o
gestor da conta é o primeiro passo.

### Regra de cobertura

Uma área que ficou quatro quintas sem ser aprofundada ganha prioridade na quinta
seguinte, mesmo que não tenha o maior impacto. Cada diário de quinta registra
qual área foi aprofundada, e é esse registro que controla o rodízio.

### Ligação com a segunda

Quando a segunda apontar uma métrica ofensora, a varredura da quinta procura
primeiro as oportunidades fora de campanha que atacam essa mesma métrica, para
que as duas otimizações trabalhem para a mesma meta.

## Gatilhos de alerta

Qualquer um destes coloca o assunto no rascunho, mesmo que a investigação não
tenha passado por ele:

- ROAS faturado da semana ou do mês abaixo da meta da planilha.
- Queda na taxa de conversão do projeto ou de um canal, contra a meta ou contra
  a semana anterior.
- Variação de 15% ou mais contra a semana anterior em ROAS, CPA, compras ou custo
  por sessão de uma campanha ou canal.
- Produto anunciado sem estoque. Em toda rodada, as URLs dos produtos que estão
  nos anúncios (Meta e Google) são validadas para conferir se a página está no
  ar e se o produto ainda tem estoque. Produto que vende bem e ficou sem estoque,
  mesmo fora dos anúncios, também entra.
- Anúncio com erro, reprovação ou limitação de veiculação no Meta, no Google ou
  no Merchant Center.
- Investimento fora do ritmo. A primeira referência é o investimento da meta do
  mês, proporcional ao dia. A segunda é a soma dos orçamentos diários ativos
  multiplicada pelos dias decorridos.

## O diário de bordo

Cada rodada entrega um diário de bordo em
`clientes/<cliente>/otimizacoes/AAAA-MM-DD_<segunda|quinta>.md`. O diário sai da
rodada agendada como rascunho e passa a valer depois que o gestor da conta o revisa e
registra.

### Diário de bordo de segunda-feira

Seis tópicos, nesta ordem:

1. **Fechamento do ciclo anterior.** O que a rodada anterior esperava e o que
   aconteceu, item por item, com o número. Na primeira rodada de um cliente, o
   fechamento é feito contra as decisões mais recentes do `DECISOES.md` de cada
   frente.
2. **O que eu vi na análise atual.** Meta contra realizado, projeção, métricas
   ofensoras e o que o detalhamento mostrou, incluindo os caminhos descartados.
3. **O que eu fiz.** No rascunho, esta seção traz o que se propõe fazer. Depois
   que o gestor da conta executa e registra a rodada, ela passa a dizer o que foi de fato
   feito.
4. **Por que eu fiz.** A ligação entre a ação, a métrica ofensora e a meta.
5. **O que eu espero.** Qual métrica deve mudar, quanto, em quanto tempo de
   teste e qual resultado confirma ou derruba a hipótese. É contra isso que a
   próxima rodada faz o fechamento.
6. **Tarefas que precisam ser executadas.** Cada uma com responsável e data.

O diário de segunda termina com um **resumo para a cliente**, escrito para a
dona da loja e não para um analista. O gestor da conta revisa e envia; o sistema não envia
nada.

### Diário de bordo de quinta-feira

A quinta não repete a análise da segunda. Ela acompanha o que foi decidido e
procura oportunidade. Cinco tópicos, nesta ordem:

1. **Andamento das ações da segunda.** Cada tarefa com o status (feita, em
   andamento, não feita) e a leitura parcial da métrica esperada. Um teste que
   ainda não completou o tempo combinado não recebe conclusão, só a leitura
   parcial e o aviso de quando fecha.
2. **Alertas desde segunda.** Os gatilhos que dispararam de segunda a quarta,
   incluindo a validação das URLs e do estoque dos produtos anunciados e os
   anúncios com erro ou limitação. Um alerta grave pode pedir ação antes da
   próxima segunda, e isso fica dito com clareza.
3. **Oportunidades encontradas.** Primeiro, a varredura: uma linha por área com
   o desvio encontrado ou "sem desvio", e qual área foi aprofundada e por quê
   (maior impacto ou regra de cobertura). Depois, cada oportunidade que passou
   pelos quatro filtros, com o cálculo do impacto, o dado que a sustenta, a
   hipótese, a área (página de produto, SEO, funil, processo do cliente,
   mercado, região ou campanha futura), o resultado esperado, o esforço, se
   precisa de verba de teste e quanto, e a proposta de quando encaixar no
   planejamento.
4. **Proposta para o roadmap.** Quais oportunidades entram no roadmap do
   cliente e em que ordem. Elas só entram de fato no `ROADMAP.md` depois que o
   gestor da conta aprovar no registro.
5. **Tarefas que precisam ser executadas.** Só as que não mexem em campanha
   naquele dia, salvo alerta grave, cada uma com responsável e data.

A quinta não tem resumo para a cliente.

## Regras que valem em toda rodada

- Separar "dado:" de "hipótese:" sempre que houver risco de confusão.
- Se não houver o dado, dizer que não há. Nunca estimar para preencher lacuna.
- Todo número vem com fonte, janela e hora da última atualização da fonte.
- Planilha de acompanhamento só vale depois de conferir a hora da última
  atualização dela. Divergência acima de 3% entre a planilha e a plataforma de
  pedidos vai para o rascunho como divergência.
- Qualquer consulta que gere custo (por exemplo, uma consulta grande no
  BigQuery) para e pergunta ao gestor da conta antes.
- Nesta fase o Claude não altera nada nas contas. Propõe, e o gestor da conta executa.
- A rodada agendada só escreve o rascunho. O registro em `DECISOES.md`,
  `ABERTO.md` e `ROADMAP.md` acontece no modo `registrar`, com o gestor da conta na
  conversa.
