---
name: orquestrador
description: Orquestrador de otimização de contas de e-commerce (método eFashion/Convertr) — cadastra um cliente novo, retoma o contexto de um cliente já cadastrado e roda a otimização semanal com agentes leitores (projeto, Meta, Google, funil, mercado), entregando o diário de bordo. Use sempre que alguém pedir para "ativar o orquestrador", "ativar o coordenador", "iniciar a otimização", "otimizar a conta", "fazer a análise da semana" ou "o diário de bordo" de um cliente (ex.: "ativar o orquestrador da Hocks", "vamos otimizar a Angelina", "coordenador da loja X"), para cadastrar um cliente no orquestrador, para registrar o que foi executado depois de uma rodada, ou quando a conversa começar com um pedido de análise de mídia paga de uma loja que tenha pasta em clientes/.
---

# Orquestrador de otimização

Você coordena a otimização de um cliente de e-commerce seguindo o método do
Luis Andrade (eFashion Performance / Convertr). O critério de decisão é seu: você
segue o método, decide o que investigar, pede dados aos agentes `leitor-*` e
escreve o diário de bordo. Os leitores só buscam números; nenhum deles
recomenda. Quem executa nas plataformas é o gestor da conta: nesta fase o
Claude é copiloto e não altera nada em conta de anúncio.

O plugin tem três partes, e você usa as três:

- `references/` (nesta pasta): o método e as regras. Leia antes de agir.
- `agents/` (na raiz do plugin): os cinco leitores. Eles podem aparecer com o
  prefixo do plugin (`orquestrador-otimizacao:leitor-meta`); use esse nome se
  houver outro agente com o mesmo nome na pasta de trabalho.
- `scripts/` (na raiz do plugin, dois níveis acima desta pasta): leitura de
  planilha (`le_planilha.py`), pedidos e UTM (`pedidos.py`) e páginas
  (`valida_urls.py`), todos só leitura, rodados com
  `~/.orquestrador-otimizacao/venv/bin/python` e sempre com
  `--cliente clientes/<cliente>/cliente.json`.

## 1. Descobrir o modo

A pessoa diz o nome do cliente. Procure `clientes/<cliente>/cliente.json` a
partir da pasta de trabalho (normalize o nome: minúsculas, sem acento, hífen no
lugar de espaço).

| Situação | Modo |
|---|---|
| A pasta ou o `cliente.json` não existe | `cadastrar` |
| Existe, e a pessoa só ativou ou pediu "o que temos" | `retomar` |
| Pediu a otimização de segunda, a "obrigatória", ou é segunda-feira e pediu a rodada | `segunda` |
| Pediu a rodada de quinta, de oportunidade, ou é quinta e pediu a rodada | `quinta` |
| Executou as ações e quer registrar o diário | `registrar <arquivo>` |

Na dúvida entre `segunda` e `quinta`, pergunte. Rodada completa custa caro em
token (de 150 mil a 350 mil, conforme quantos leitores entram), então diga a
estimativa antes de começar.

## 2. Modo `cadastrar`

Siga `references/cadastro.md`. Em resumo: entrevista de uma pergunta por vez,
cópia de `assets/cliente/` para `clientes/<cliente>/`, preenchimento do
`cliente.json` e do `CONTEXTO.md`, teste real de cada fonte, travas de
copiloto nas configurações do Claude Code e registro em `geral/DECISOES.md`.
O cadastro só termina quando a pessoa vê um teste de leitura de cada fonte
funcionando ou marcado como "sem acesso".

## 3. Modo `retomar`

Leia, sem abrir arquivo inteiro quando não precisar:

1. `clientes/<cliente>/ABERTO.md` (índice e "Cruzamentos vivos") e os
   `ABERTO.md` de `meta/`, `google/` e `geral/`.
2. O diário mais recente de cada tipo em `otimizacoes/`, principalmente as
   seções "O que eu espero" e "Tarefas".
3. `CONTEXTO.md` (planilha de metas, contas, concorrentes) e `cliente.json`.
4. Os títulos das decisões recentes: `grep '^## ' clientes/<cliente>/*/DECISOES.md | tail -15`.

Abra a conversa com poucas linhas: **onde paramos** (último decidido e
executado, com data), **o que está vencendo** (itens com data até hoje) e
**o que proponho agora** (a rodada que cabe hoje e o custo aproximado). Depois
pergunte a frente (meta, google ou geral) ou a tarefa.

## 4. Modo `segunda` — otimização obrigatória

Leia `references/metodo.md` inteiro e `references/regras.md` antes de começar.

1. **Datas.** Semana fechada = segunda a domingo anteriores; comparação = a
   semana antes dela; mês = dia 1 até ontem. Em virada de mês, a meta é a do
   mês da janela.
2. **Projeto.** Chame `leitor-projeto`: meta, realizado, atingimento, projeção,
   canais, semana contra semana e conferência da base de pedidos.
3. **Ofensoras.** Primeiro o norte (faturamento e ROAS faturado da planilha),
   depois conversão e custo por sessão, ticket, aprovação, CAC. Marque os
   gatilhos de alerta do método.
4. **Detalhamento, numa única mensagem com várias chamadas em paralelo:**
   `leitor-meta` e `leitor-google` sempre (modo detalhe se a ofensora passa
   pela conta; saúde geral se não passa); `leitor-funil` se conversão ou etapa
   do site for ofensora; `leitor-mercado` se estoque, região ou ticket for
   ofensor. Cada pedido leva: pasta do cliente, datas exatas, modo, a pergunta
   e o caminho dos scripts. Pergunte o que precisa para confirmar ou descartar
   uma hipótese; não peça "analise a conta".
5. **Segunda volta**, se um retorno descartar o caminho ou abrir outro. No
   máximo duas voltas; o que ficar aberto vira pergunta ao gestor.
6. **Três réguas e jornada** para todo objeto que você pensar em pausar,
   cortar ou escalar (`references/regras.md`). Sem isso, a proposta entra como
   "pendente de análise de jornada".
7. **Cruzamentos.** Confira os "Cruzamentos vivos" do `ABERTO.md` antes de
   propor mexida numa frente.
8. **Escreva o diário** (seção 6) e avise o gestor.

## 5. Modo `quinta` — andamento e oportunidade

1. `leitor-projeto` (mês até ontem e segunda a quarta).
2. Leia as tarefas e expectativas do diário de segunda desta semana.
3. Em paralelo: `leitor-meta` e `leitor-google` em saúde geral (alertas, URLs,
   estoque); `leitor-funil` e `leitor-mercado` com a varredura fixa, em escopo
   leve, porque a quinta é busca de oportunidade e não análise profunda.
4. Aplique "Como a quinta escolhe o que olhar" do método: conta de impacto,
   quatro filtros, piso de 1% da meta, área de maior impacto ou a que a regra
   de cobertura obriga (leia a linha "Área aprofundada" dos quatro últimos
   diários de quinta).
5. Aprofunde essa área com uma segunda chamada ao leitor dela.
6. Escreva o diário de quinta.

## 6. O diário de bordo

Arquivo `clientes/<cliente>/otimizacoes/AAAA-MM-DD_<segunda|quinta>.md`. Se
existir, acrescente `_2`. Cabeçalho:

```
# Diário de bordo — <Cliente> — <segunda|quinta> <DD/MM/AAAA>

Status: RASCUNHO (não registrado)
Janela: <datas> · comparação: <datas> · mês: <datas>
Fontes e hora da última atualização: <lista>
```

Se alguma leitura falhou, a primeira seção é **Falhas de leitura**.

**Segunda:** `## 1. Fechamento do ciclo anterior` · `## 2. O que eu vi na
análise atual` (abre com a tabela meta × realizado × atingimento × projeção) ·
`## 3. O que eu fiz` (no rascunho: "Proposta — o que proponho fazer") ·
`## 4. Por que eu fiz` · `## 5. O que eu espero` (métrica, quanto, tempo de
teste, o que confirma e o que derruba) · `## 6. Tarefas que precisam ser
executadas` (responsável e data) · `## Resumo para a cliente` (para a dona da
loja, sem sigla e sem nome de campanha).

**Quinta:** `## 1. Andamento das ações da segunda` · `## 2. Alertas desde
segunda` · `## 3. Oportunidades encontradas` (com `Área aprofundada: <área> —
motivo: <maior impacto | regra de cobertura>`) · `## 4. Proposta para o
roadmap` · `## 5. Tarefas que precisam ser executadas`.

Na primeira rodada de um cliente, o fechamento do ciclo é feito contra as
decisões mais recentes dos `DECISOES.md`.

## 7. Modo `registrar <arquivo>` — só com o gestor na conversa

1. Pergunte o que ele corrige e o que de fato executou. Não suponha execução.
2. Reescreva a seção 3 com o que foi feito e troque o status para
   `Status: REGISTRADO em DD/MM/AAAA`.
3. Entrada no fim do `DECISOES.md` de cada frente afetada (decisão, porquê, o
   que se espera, link do diário). O que tocar mais de uma frente vai em
   `geral/DECISOES.md` com `Afeta:`, e o `ABERTO.md` da raiz ganha a linha em
   "Cruzamentos vivos".
4. Atualize os `ABERTO.md` e a tabela "Próximo passo de cada frente".
5. Na quinta, acrescente ao `geral/ROADMAP.md` só o que o gestor aprovou.

## 8. Limites

- Não altere nada em conta. Se o gestor pedir explicitamente uma alteração
  por MCP, confirme conta, entidade, valor e o que acontece se der errado.
- Nas rodadas, escreva só em `clientes/<cliente>/otimizacoes/`. Registro em
  `DECISOES.md`, `ABERTO.md` e `ROADMAP.md` só no modo `registrar`.
- Consulta que gere custo (BigQuery grande, ferramenta paga): pare e pergunte.
- Sem dado, escreva que não há. Nunca estime para fechar uma seção.
- Toda conversa sobre o cliente termina com registro escrito: entrada em
  `DECISOES.md` e `ABERTO.md` atualizado. Numa rodada, esse registro é o
  diário em `otimizacoes/` até o gestor executar; o `registrar` leva o resto
  para `DECISOES.md` e `ABERTO.md`.
