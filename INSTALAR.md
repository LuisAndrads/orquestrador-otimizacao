# Instalar o orquestrador de otimização

## Para a pessoa

1. Abra o app do Claude e vá na aba **Code**.
2. Embaixo, onde você escreve, clique em **Selecionar pasta** (ou "nenhuma
   pasta") → **Abrir pasta**. Crie uma pasta chamada **Convertr** em
   Documentos e abra ela.
3. Cole este link numa conversa nova e escreva "instala isso para mim":
   https://github.com/LuisAndrads/orquestrador-otimizacao
4. Siga o que o Claude pedir. Ele faz quase tudo sozinho e explica cada passo
   do que só você pode fazer (entrar em contas e clicar em telas do Google e
   do Facebook). Leva de 30 a 60 minutos na primeira vez.

## Para o Claude que recebeu este link

Você vai preparar o computador de uma pessoa leiga para usar o plugin. Faça
nesta ordem, sem pular:

1. **Pasta.** Confira se a pasta de trabalho se chama `Convertr`. Se não,
   crie `~/Documents/Convertr/clientes/` e diga à pessoa para abrir essa pasta
   no Claude Code e colar o link de novo lá.
2. **Registrar o plugin.** Grave em `Convertr/.claude/settings.json` (crie ou
   acrescente, sem apagar o que existir):
   ```json
   {
     "extraKnownMarketplaces": {
       "convertr": {"source": {"source": "github", "repo": "LuisAndrads/orquestrador-otimizacao"}}
     },
     "enabledPlugins": {"orquestrador-otimizacao@convertr": true}
   }
   ```
3. **Preparar o computador.** Baixe e siga
   `skills/orquestrador/references/instalacao.md` deste repositório
   (https://raw.githubusercontent.com/LuisAndrads/orquestrador-otimizacao/main/skills/orquestrador/references/instalacao.md):
   pré-auditoria sem perguntar nada, uma autorização para instalar o que dá,
   questionário único, trilhas passo a passo, verificação e relatório.
4. Peça para a pessoa fechar e abrir o Claude com a pasta `Convertr` aberta.
   Depois disso o plugin está ativo, e "ativar o orquestrador da <cliente>"
   começa o cadastro do primeiro cliente.

Problemas já vistos e a solução de cada um:
`skills/orquestrador/references/problemas-conhecidos.md`.
