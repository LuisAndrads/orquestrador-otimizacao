# Orquestrador de otimização

Plugin do Claude Code com o método de otimização de contas de e-commerce do
Luis Andrade (eFashion Performance / Convertr). Ele transforma o Claude num
coordenador da conta: cadastra o cliente, retoma o contexto em qualquer
conversa, roda a otimização de segunda (obrigatória, contra a meta do mês) e a
de quinta (oportunidade), usando cinco agentes leitores, e entrega o diário de
bordo para o gestor executar.

Nasceu numa conta real de moda em setembro e outubro de 2026 e foi generalizado
para qualquer cliente.

## O que vem dentro

| Peça | O que faz |
|---|---|
| `skills/orquestrador/` | A porta de entrada. Modos: `preparar`, `cadastrar`, `retomar`, `segunda`, `quinta`, `registrar` |
| `skills/orquestrador/references/metodo.md` | O método: norte, métricas secundárias, ordem da análise, segunda e quinta, critérios da varredura, gatilhos, diário |
| `skills/orquestrador/references/regras.md` | Regras aprendidas no uso real: três réguas, jornada antes de pausar, estado de hoje, estrutura da Shopping, recomendação externa, token |
| `skills/orquestrador/references/cadastro.md` | Roteiro de cadastro de cliente |
| `skills/orquestrador/assets/cliente/` | Modelo da pasta do cliente (`ABERTO`, `DECISOES`, `ESTRUTURA`, `ROADMAP`, `cliente.json`) |
| `agents/` | `leitor-projeto`, `leitor-meta`, `leitor-google`, `leitor-funil`, `leitor-mercado` |
| `scripts/` | Leitura de planilha, pedidos e UTM da base, e validação de páginas. Só leitura |

## Instalar

Passo a passo para quem nunca usou o Claude Code: **[INSTALAR.md](INSTALAR.md)**.
Em resumo: abra a aba Code do app do Claude com uma pasta `Convertr`, cole o
link deste repositório e peça "instala isso para mim". O Claude audita o
computador, instala o que dá e guia o resto.

Quem já usa o Claude Code pode instalar direto, um comando por vez:

```
/plugin marketplace add LuisAndrads/orquestrador-otimizacao
```
```
/plugin install orquestrador-otimizacao@convertr
```

Requisitos (o modo `preparar` confere e instala):

1. **Python 3** no computador. O cadastro cria o ambiente dos scripts em
   `~/.orquestrador-otimizacao/venv`.
2. **Conta de serviço do Google** com acesso de leitor às planilhas do cliente
   (planilha de metas e base de pedidos).
3. **Conector do Meta** no Claude (Configurações → Conectores). GA4 e
   planilhas são lidos pelos scripts com a conta de serviço, sem MCP. Google
   Ads, Merchant e Clarity são opcionais: fonte sem acesso vira "sem acesso" e
   a análise segue com o resto.
4. Para a régua da loja, a **Base de Dados de pedidos** do cliente (planilha
   alimentada pela plataforma: Nuvemshop, Tray, Shopify, VTEX ou outra; o mapa
   de colunas fica no `cliente.json`). **Plataforma Convertr:** não há base por
   pedido; os pedidos vêm da aba `dados_bq` da PDA 13.0.

## Usar

Em qualquer conversa, numa pasta de trabalho onde os clientes ficam em
`clientes/<cliente>/`:

- "Preparar o computador" — audita e instala o que falta (primeira vez).
- "Ativar o orquestrador da Hocks" — cadastra, se for a primeira vez; retoma,
  se já existir.
- "Rodar a otimização de segunda da Hocks" / "rodada de quinta da Hocks".
- "Registrar o diário de segunda da Hocks" — depois de executar as ações.

## Princípios

- **Copiloto:** o Claude propõe; o gestor executa nas plataformas. O cadastro
  trava as ferramentas de escrita das MCPs nas configurações do Claude Code.
- **Meta é a da planilha do cliente.** Sem meta, o primeiro passo é criar uma.
- **Três réguas** (gerenciador, GA4, loja) e leitura de jornada antes de
  propor pausar, cortar ou escalar.
- **Registro sempre:** toda conversa termina com entrada em `DECISOES.md` e
  `ABERTO.md` atualizado.
- **Token conta:** scripts e chamadas diretas antes de agentes; aprofundamento
  só com autorização.

## Versão

0.2.0 — instalação guiada para leigos (modo `preparar`), plataforma Convertr
(`dados_bq`), GA4 sem MCP (`ga4.py`) (outubro de 2026).
0.1.0 — primeira versão generalizada a partir de uma conta real (outubro de 2026).
