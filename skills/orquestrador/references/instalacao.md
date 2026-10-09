# Preparar o computador (modo `preparar`)

Para quem nunca usou o Claude Code. Parta do princípio de que a pessoa é leiga:
nada de sigla sem explicação, um passo por vez nas trilhas e o nome exato de
cada botão. Faça por ela tudo o que der para fazer pelo terminal. O que exigir
conta, login, cartão, senha ou clique numa tela do Google ou do Facebook, ela
faz, com você guiando.

Regras desta etapa:
- Nunca peça para colar senha, número de cartão ou o conteúdo da chave JSON no
  chat. Você também nunca digita senha nem cartão.
- Nunca contrate nem ative nada pago. Se uma tela pedir pagamento, explique o
  que é e deixe a pessoa decidir.
- Tudo que travar vai para o relatório da etapa 6, com a mensagem de erro
  exata, para o Luis melhorar este roteiro.

## Etapa 1. Pré-auditoria (sem perguntar nada)

Rode os testes abaixo e monte a tabela. No Windows, use os comandos da coluna
Windows no PowerShell.

| Item | Mac | Windows | Obrigatório |
|---|---|---|---|
| Sistema | `uname -s; sw_vers -productVersion` | `[Environment]::OSVersion` | — |
| Pasta de trabalho | `pwd; ls` (deve se chamar `Convertr`, com `clientes/` dentro) | `pwd; ls` | sim |
| Python 3.9 ou mais novo | `python3 --version` | `py --version` | sim |
| Ambiente dos scripts | `ls ~/.orquestrador-otimizacao/venv/bin/python` | `Test-Path $HOME\.orquestrador-otimizacao\venv\Scripts\python.exe` | sim |
| Bibliotecas | `<venv python> -c "import googleapiclient, google.analytics.data"` | idem | sim |
| Chave do Google | `ls ~/.orquestrador-otimizacao/chave-google.json` | `Test-Path $HOME\.orquestrador-otimizacao\chave-google.json` | sim |
| Conector do Meta | procure ferramentas com `ads_get_ad_accounts` na busca de ferramentas | idem | sim |
| GA4 por MCP | ferramentas `ga4` | idem | não (o `ga4.py` substitui) |
| Google Ads por MCP | ferramentas `google-ads` ou `gads_` | idem | não |
| Clarity | ferramentas `Clarity` | idem | não |
| Claude in Chrome | ferramentas `claude-in-chrome` | idem | não |

No Mac, `python3 --version` sem as ferramentas de linha de comando abre uma
janela pedindo para instalá-las: isso é esperado e vira item da etapa 2.

Não são necessários: Google Cloud instalado no computador (`gcloud`), GitHub,
Git, MCP do Google Sheets nem MCP do Google Drive. As planilhas e o GA4 são
lidos pelos scripts do plugin com a chave da conta de serviço, e o Google Cloud
é usado só pelo navegador.

Mostre a tabela com ✅, ❌ e "opcional", e diga em uma frase o que falta.

## Etapa 2. Uma autorização para instalar tudo o que dá

Liste numa única mensagem o que você vai fazer e peça um "sim":

1. Criar a pasta `Convertr/clientes/` (se a pasta aberta não for a `Convertr`,
   crie `~/Documents/Convertr/clientes/` e peça para a pessoa abrir essa pasta
   no Claude Code depois).
2. Instalar o Python, se faltar:
   - Mac: `xcode-select --install`. Abre uma janela: a pessoa clica em
     **Instalar** e espera terminar (de 5 a 15 minutos). Se o Homebrew já
     existir (`brew --version`), `brew install python` é mais rápido.
   - Windows: `winget install -e --id Python.Python.3.12`. Depois, fechar e
     abrir o Claude.
3. Criar o ambiente dos scripts e instalar as bibliotecas:
   `python3 -m venv ~/.orquestrador-otimizacao/venv` e
   `<venv python> -m pip install -r <raiz do plugin>/scripts/requirements.txt`.
4. Gravar em `Convertr/.claude/settings.json` o plugin e as permissões de
   leitura (assim a rodada não para pedindo autorização):
   ```json
   {
     "extraKnownMarketplaces": {
       "convertr": {"source": {"source": "github", "repo": "LuisAndrads/orquestrador-otimizacao"}}
     },
     "enabledPlugins": {"orquestrador-otimizacao@convertr": true},
     "permissions": {
       "allow": [
         "Bash(<home>/.orquestrador-otimizacao/venv/bin/python <raiz do plugin>/scripts/*)",
         "Write(clientes/*/otimizacoes/**)",
         "Edit(clientes/*/otimizacoes/**)"
       ]
     }
   }
   ```
   Use os caminhos absolutos expandidos. Se o arquivo já existir, acrescente
   sem apagar o que há nele.

Com o "sim", faça tudo e teste de novo os itens da etapa 1.

## Etapa 3. Questionário único

Mande todas as perguntas numa só mensagem, numeradas, com as opções. A pessoa
responde o que souber; depois pergunte só o que faltou.

1. Qual e-mail você vai usar no Google Cloud: um Gmail pessoal ou o e-mail da
   Convertr? (Recomendado: o mesmo e-mail que tem acesso às planilhas e ao GA4
   dos clientes. Se for e-mail de empresa e o Google bloquear a criação da
   chave, usamos o Gmail.)
2. Você já entrou alguma vez em console.cloud.google.com? Já tem um projeto
   lá?
3. Você já tem um arquivo de chave JSON de "conta de serviço"? Se sim, onde
   ele está?
4. Você abre o Gerenciador de Anúncios do Meta dos seus clientes com o seu
   Facebook? Em quais portfólios (Business Managers)?
5. Por qual MCC você acessa o Google Ads dos clientes (eFashion, Convertr ou
   direto na conta)?
6. Você é administrador ou editor do GA4 dos seus clientes? (É preciso para
   dar acesso de leitura à conta de serviço.)
7. Os seus clientes têm Microsoft Clarity? Você tem acesso a ele?
8. Você usa o Google Chrome? Quer a extensão do Claude no Chrome (opcional)?
9. Quais clientes você quer cadastrar primeiro, e qual a plataforma da loja de
   cada um (Convertr, Nuvemshop, Tray, Shopify, outra)?
10. Qual o seu plano do Claude (Pro, Max ou Team)? (A rodada completa de
    segunda consome bastante; no Pro ela pode bater no limite da semana.)

## Etapa 4. Trilhas, uma de cada vez

Siga só as trilhas do que falta, nesta ordem. Mande um passo, espere a pessoa
dizer "feito" (ou mandar um print), confira e mande o próximo.

### Trilha A. Google Cloud, conta de serviço e chave (obrigatória)

1. Abrir https://console.cloud.google.com e entrar com o e-mail da pergunta 1.
   Aceitar os termos e escolher o país Brasil.
2. **Faturamento.** Para o que o plugin usa (planilhas e GA4), não é preciso
   ativar faturamento nem o teste gratuito: pode fechar o aviso de "US$ 300
   grátis". Se o Google bloquear algum passo exigindo conta de faturamento, aí
   sim: o teste gratuito dá US$ 300 por 90 dias, pede cartão e pode pedir um
   pré-pagamento pequeno, que fica como crédito (caso visto em 05/10/2026). O
   uso do plugin custa centavos. Depois de cadastrar o cartão, criar um alerta
   de orçamento (Faturamento → Orçamentos e alertas → R$ 20).
3. **Projeto.** No topo da tela, clicar no seletor de projeto → **Novo
   projeto** → nome `orquestrador-<seunome>` → **Criar**. Esperar e
   selecionar o projeto no seletor.
4. **Ativar as APIs.** Abrir cada link com o projeto selecionado e clicar em
   **Ativar**:
   - https://console.cloud.google.com/apis/library/sheets.googleapis.com
   - https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com
5. **Conta de serviço.** Menu ☰ → **IAM e administrador** → **Contas de
   serviço** → **Criar conta de serviço** → nome `orquestrador` → **Criar e
   continuar** → pular as permissões → **Concluir**.
6. **Chave.** Clicar na conta criada → aba **Chaves** → **Adicionar chave** →
   **Criar nova chave** → **JSON** → **Criar**. O navegador baixa um arquivo
   `.json`.
   - Erro "a criação de chaves de conta de serviço está desativada": é uma
     política de e-mail de empresa. Refazer as etapas 1 a 6 com o Gmail
     pessoal.
7. **Guardar a chave** (você faz): procurar em Downloads o `.json` mais novo
   com `"type": "service_account"`, mover para
   `~/.orquestrador-otimizacao/chave-google.json` e restringir a leitura
   (`chmod 600` no Mac). Nunca deixar em pasta sincronizada (iCloud, OneDrive,
   Google Drive) nem dentro de `Convertr/`. Mostre só o e-mail da conta de
   serviço, lido com
   `<venv python> -c "import json;print(json.load(open('<chave>'))['client_email'])"`.
   Nunca mostre o resto do arquivo.
8. **Dar acesso** (por cliente, durante o cadastro): o e-mail da conta de
   serviço entra como
   - **Leitor** em cada planilha (PDA 13.0 e base de pedidos): botão
     **Compartilhar** → colar o e-mail → **Leitor** → desmarcar "Notificar" →
     **Compartilhar**;
   - **Leitor** no GA4: **Administrador** → **Gerenciamento de acesso à
     propriedade** → **+** → **Adicionar usuários** → colar o e-mail → papel
     **Leitor** → **Adicionar**.
9. **Teste:** `le_planilha.py --planilha <id da PDA> "configs!A1:B5"` e
   `ga4.py --cliente <json> <ontem> <ontem> --metricas sessions`.

### Trilha B. Meta Ads (obrigatória)

1. No app do Claude: clicar no seu nome (canto inferior esquerdo) →
   **Configurações** → **Conectores** → procurar **Meta** → **Conectar**.
2. Entrar com o Facebook que acessa os portfólios dos clientes e autorizar
   todas as contas de anúncio que você gerencia.
3. Fechar e abrir o Claude.
4. **Teste:** listar as contas de anúncio e ler o gasto de ontem de uma delas.
5. No cadastro do primeiro cliente, as ferramentas de escrita do Meta são
   travadas (`cadastro.md`, seção 5).

### Trilha C. Google Ads (sem instalação)

O plugin não precisa de MCP do Google Ads. O custo por canal vem da planilha
de metas do cliente (aba de canais ou `dados_bq`). Detalhe de campanha, termo
ou produto: pela interface do Google Ads no navegador, só leitura, com a
extensão do Chrome (trilha E), e sempre pela MCC que a pessoa informou. Acesso
pela API do Google Ads exige token de desenvolvedor da MCC: só se o Luis
liberar.

### Trilha D. Microsoft Clarity (opcional)

1. Em https://clarity.microsoft.com, abrir o projeto do cliente →
   **Configurações** → **Exportação de dados** → **Gerar novo token de API**.
   Copiar o token.
2. No Claude: **Configurações** → **Conectores** → **Microsoft Clarity** →
   **Conectar** e colar o token na tela do conector (não no chat).
3. Limite: a API do Clarity só devolve os últimos dias e poucas chamadas por
   dia por projeto. Serve para sinal de página, e não para histórico.

### Trilha E. Claude no Chrome (opcional)

Instalar a extensão **Claude** na Chrome Web Store, entrar com a mesma conta
do Claude e fixar o ícone. Serve para ler a Biblioteca de Anúncios do Meta e
a interface do Google Ads quando a ferramenta não traz o dado.

### GitHub

Não é preciso: o repositório do plugin é público.

## Etapa 5. Plugin ativo

Se o plugin foi registrado agora no `settings.json`, peça para a pessoa fechar
e abrir o Claude com a pasta `Convertr` aberta. Para conferir, ela digita `/`
e procura `orquestrador`. Sem o plugin listado, os comandos manuais, um por
vez (cada um numa linha só):
```
/plugin marketplace add LuisAndrads/orquestrador-otimizacao
```
```
/plugin install orquestrador-otimizacao@convertr
```

## Etapa 6. Verificação final e relatório

1. Refaça a tabela da etapa 1, agora com o resultado dos testes.
2. Grave `~/.orquestrador-otimizacao/ambiente.json`: data, sistema, caminho do
   Python do ambiente, caminho da chave, e-mail da conta de serviço (nunca a
   chave) e o estado de cada item (`ok`, `falta`, `opcional`, `erro: <msg>`).
3. Grave `Convertr/relatorio-instalacao.md` com o que foi feito, o que travou
   (mensagem exata e o que resolveu) e o tempo de cada trilha, e peça para a
   pessoa mandar esse arquivo ao Luis. Ele usa esses relatórios para melhorar
   este roteiro.
4. Próximo passo: "ativar o orquestrador da <cliente>", que abre o cadastro.
