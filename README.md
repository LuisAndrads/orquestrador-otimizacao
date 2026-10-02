# Orquestrador de otimização

Plugin do Claude Code com o método de otimização de contas de e-commerce do
Luis Andrade (eFashion Performance / Convertr). Ele transforma o Claude num
coordenador da conta: cadastra o cliente, retoma o contexto em qualquer
conversa, roda a otimização de segunda (obrigatória, contra a meta do mês) e a
de quinta (oportunidade), usando cinco agentes leitores, e entrega o diário de
bordo para o gestor executar.

Nasceu na conta da Ladydress em setembro e outubro de 2026 e foi generalizado
para qualquer cliente.

## O que vem dentro

| Peça | O que faz |
|---|---|
| `skills/orquestrador/` | A porta de entrada. Modos: `cadastrar`, `retomar`, `segunda`, `quinta`, `registrar` |
| `skills/orquestrador/references/metodo.md` | O método: norte, métricas secundárias, ordem da análise, segunda e quinta, critérios da varredura, gatilhos, diário |
| `skills/orquestrador/references/regras.md` | Regras aprendidas no uso real: três réguas, jornada antes de pausar, estado de hoje, estrutura da Shopping, recomendação externa, token |
| `skills/orquestrador/references/cadastro.md` | Roteiro de cadastro de cliente |
| `skills/orquestrador/assets/cliente/` | Modelo da pasta do cliente (`ABERTO`, `DECISOES`, `ESTRUTURA`, `ROADMAP`, `cliente.json`) |
| `agents/` | `leitor-projeto`, `leitor-meta`, `leitor-google`, `leitor-funil`, `leitor-mercado` |
| `scripts/` | Leitura de planilha, pedidos e UTM da base, e validação de páginas. Só leitura |

## Instalar

No Claude Code:

```
/plugin marketplace add LuisAndrads/orquestrador-otimizacao
/plugin install orquestrador-otimizacao@convertr
```

(Repositório: https://github.com/LuisAndrads/orquestrador-otimizacao.
Repositório privado: peça acesso ao Luis antes.)

Requisitos:

1. **Python 3** no computador. O cadastro cria o ambiente dos scripts em
   `~/.orquestrador-otimizacao/venv`.
2. **Conta de serviço do Google** com acesso de leitor às planilhas do cliente
   (planilha de metas e base de pedidos).
3. **MCPs** de leitura ligadas no Claude Code, conforme o que cada pessoa tem:
   Meta Ads, Google Ads, GA4, Merchant Center, Clarity. Fonte sem MCP vira
   "sem acesso" e a análise segue com o resto.
4. Para a régua da loja, a **Base de Dados de pedidos** do cliente (planilha
   alimentada pela plataforma: Nuvemshop, Tray, Shopify, VTEX ou outra). O
   mapa de colunas fica no `cliente.json`.

## Usar

Em qualquer conversa, numa pasta de trabalho onde os clientes ficam em
`clientes/<cliente>/`:

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

0.1.0 — primeira versão generalizada a partir da Ladydress (outubro de 2026).
