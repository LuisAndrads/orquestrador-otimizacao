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
| Google Cloud no computador | `gcloud --version; bq version` | `gcloud --version; bq version` (num PowerShell aberto depois da instalação) | sim |
| Login no Google Cloud | `gcloud auth list` (uma conta com `*`) | idem | sim |
| Acesso ao projeto da Convertr | `bq ls --project_id=<projeto>` sem erro | idem | sim |

No Mac, `python3 --version` sem as ferramentas de linha de comando abre uma
janela pedindo para instalá-las: isso é esperado e vira item da etapa 2.

Não são necessários: GitHub, Git, MCP do Google Sheets nem MCP do Google
Drive. As planilhas e o GA4 são lidos pelos scripts do plugin com a chave da
conta de serviço. O Google Cloud no computador (`gcloud` e `bq`) cria essa
chave e consulta o BigQuery.

**Como o Google Cloud é organizado.** Existe um projeto do Google Cloud da
Convertr, com faturamento ativo, onde ficam todas as exportações para o
BigQuery. Quem cuida dele (o dono do projeto) segue a trilha F. Cada pessoa
que usa o plugin recebe ali uma conta de serviço só dela (`orq-<nome>`) e não
cria projeto, não paga nada e não cadastra cartão. Sem o ID do projeto,
pergunte à pessoa quem é o coordenador dela e peça o ID a ele.

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
4. Instalar o Google Cloud CLI, que traz os comandos `gcloud` e `bq`:
   - Mac com Homebrew (`brew --version` responde):
     `brew install --cask google-cloud-sdk`.
   - Mac sem Homebrew: o instalador oficial do Google,
     `curl -sSL https://sdk.cloud.google.com | bash -s -- --disable-prompts --install-dir="$HOME"`,
     e depois acrescentar ao `~/.zshrc` a linha
     `source "$HOME/google-cloud-sdk/path.zsh.inc"`. Enquanto o Claude não for
     reaberto, use o caminho completo `$HOME/google-cloud-sdk/bin/gcloud`.
   - Windows: `winget install -e --id Google.CloudSDK`. Depois, fechar e abrir
     o Claude.
   - Conferência, nos dois: `gcloud --version` e `bq version` respondem com o
     número da versão.
5. Gravar em `Convertr/.claude/settings.json` o plugin e as permissões de
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

1. Qual e-mail do Google você vai usar? (Recomendado: o mesmo que tem acesso
   às planilhas e ao GA4 dos clientes.)
2. O seu coordenador já te deu o ID do projeto da Convertr no Google Cloud e
   avisou que criou a sua conta de serviço? (Se não, mande a ele o seu nome e
   o e-mail da pergunta 1: ele segue a trilha F, item 2.)
3. Você já tem um arquivo de chave JSON de "conta de serviço"? Se sim, onde
   ele está?
4. Você abre o Gerenciador de Anúncios do Meta dos seus clientes com o seu
   Facebook? Em quais portfólios (Business Managers)?
5. No Google Ads, você é administrador da MCC, administrador da conta do
   cliente, ou tem acesso só à conta, sem ser administrador? (Quem não é
   administrador pede ao coordenador para dar o acesso do item 1 do cadastro,
   seção 3A.)
6. No GA4 dos seus clientes, qual é o seu papel: administrador, editor ou
   leitor? (Só o administrador consegue dar acesso de leitura à conta de
   serviço.)
7. Os seus clientes têm Microsoft Clarity? Você tem acesso a ele?
8. Você usa o Google Chrome? Quer a extensão do Claude no Chrome (opcional)?
9. Quais clientes você quer cadastrar primeiro, e qual a plataforma da loja de
   cada um (Convertr, Nuvemshop, Tray, Shopify, outra)?
10. Qual o seu plano do Claude (Pro, Max ou Team)? (A rodada completa de
    segunda consome bastante; no Pro ela pode bater no limite da semana.)

## Etapa 4. Trilhas, uma de cada vez

Siga só as trilhas do que falta, nesta ordem. Mande um passo, espere a pessoa
dizer "feito" (ou mandar um print), confira e mande o próximo. A trilha F é só
para o dono do projeto da Convertr; a pessoa comum não passa por ela.

### Trilha A. Google Cloud: login e chave da conta de serviço (obrigatória)

Antes, a pessoa precisa de duas coisas do coordenador (pergunta 2 do
questionário): o ID do projeto da Convertr e o aviso de que a conta de
serviço `orq-<nome>` dela já existe (trilha F, item 2). Sem isso, siga as
outras trilhas e volte aqui depois. O Google Cloud CLI já foi instalado na
etapa 2.

1. **Login.** `gcloud auth login` abre o navegador: a pessoa entra com o
   e-mail da pergunta 1 e clica em **Permitir**. Depois,
   `gcloud config set project <projeto>`. Não há cartão nem faturamento a
   cadastrar: quem paga é o projeto da Convertr.
2. **Conferir o acesso:** `bq ls --project_id=<projeto>` lista os conjuntos
   sem erro. Erro de permissão: o coordenador não terminou a trilha F, item 2.
3. **Criar a chave** (você roda). Ela vai direto para o lugar certo, sem passar
   por Downloads:
   - Mac: `gcloud iam service-accounts keys create ~/.orquestrador-otimizacao/chave-google.json --iam-account=orq-<nome>@<projeto>.iam.gserviceaccount.com`
     e depois `chmod 600 ~/.orquestrador-otimizacao/chave-google.json`.
   - Windows (PowerShell): o mesmo comando, com o arquivo em
     `$HOME\.orquestrador-otimizacao\chave-google.json`.
   - Erro de permissão ("permission denied", "does not have permission"): o
     coordenador ainda não deu à pessoa o direito de criar a chave (trilha F,
     item 2c).
   - Erro "a criação de chaves de conta de serviço está desativada" ("key
     creation is disabled"): é uma regra da organização dona do projeto. Quem
     resolve é o dono do projeto; trocar o e-mail da pessoa não adianta.
   - A chave nunca fica em pasta sincronizada (iCloud, OneDrive, Google Drive)
     nem dentro de `Convertr/`.
4. Mostre só o e-mail da conta de serviço, lido com
   `<venv python> -c "import json;print(json.load(open('<chave>'))['client_email'])"`.
   Nunca mostre o resto do arquivo.
5. **Dar acesso por cliente** acontece no cadastro de cada cliente
   (`cadastro.md`, seção 3A, item 1): lá está em que papel cada e-mail entra
   em cada ferramenta e quem consegue adicionar.
6. **Teste** (depois do primeiro cadastro):
   `le_planilha.py --planilha <id da PDA> "configs!A1:B5"` e
   `ga4.py --cliente <json> <ontem> <ontem> --metricas sessions`.

**Sem acesso ao projeto da Convertr (provisório).** Se a pessoa precisa
começar antes de o coordenador liberar o acesso, ela pode criar um projeto só
dela. Explique o que isso dá e o que não dá antes de começar:

- Em https://console.cloud.google.com: aceitar os termos, seletor de projeto →
  **Novo projeto** → `orquestrador-<seunome>` → **Criar**. Ativar, com o
  projeto selecionado, as APIs
  https://console.cloud.google.com/apis/library/sheets.googleapis.com e
  https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com.
  Criar a conta de serviço em ☰ → **IAM e administrador** → **Contas de
  serviço** → **Criar conta de serviço**, e a chave com o comando do item 3
  (com o projeto e a conta novos).
- Sem cartão, o projeto funciona no modo gratuito do BigQuery (o Google chama
  de "sandbox"). Planilhas e GA4 pelos scripts funcionam normalmente. No
  BigQuery, porém, cada tabela se apaga sozinha 60 dias depois de criada, o
  espaço é de 10 GB para a vida inteira do projeto, e não rodam as
  transferências de Google Ads e Merchant nem a exportação do Search Console.
- Ativar o faturamento pede cartão e é decisão da pessoa (regra desta etapa).
  Quando a tela pedir, explique e deixe ela decidir.
- Nunca ligue as exportações de um cliente num projeto provisório. O GA4
  aceita um vínculo com o BigQuery só (em 29/10/2026, com um vínculo feito, o
  botão **Vincular** ficou desligado), e trocar depois perde a continuidade.

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

### Trilha F. Projeto da Convertr (só quem cuida do projeto)

Quem segue esta trilha é o dono do projeto da Convertr. A pessoa comum pula.
Todos os comandos mudam permissão ou configuração do projeto: mostre cada um e
espere o "ok" antes de rodar. `<projeto>` é o ID do projeto; `<nome>` é o nome
da pessoa em minúsculas, sem acento nem espaço; `<email>` é o e-mail do Google
dela.

1. **Uma vez por projeto.**
   a. **Faturamento ativo**, com alerta de orçamento (Faturamento →
      Orçamentos e alertas). Sem faturamento, o BigQuery fica no modo
      gratuito: tabelas se apagam com 60 dias e não há transferência de
      Google Ads e Merchant nem exportação do Search Console.
   b. **APIs:** `gcloud services enable bigquery.googleapis.com bigquerydatatransfer.googleapis.com sheets.googleapis.com analyticsdata.googleapis.com --project=<projeto>`.
   c. **Conta de serviço das exportações**, dona das transferências. Ela não
      pertence a ninguém do time, então nada para quando alguém sai:
      `gcloud iam service-accounts create orq-exportacoes --project=<projeto> --display-name="Orquestrador exportações"`,
      com os papéis `roles/bigquery.dataEditor` e `roles/bigquery.jobUser`
      (`gcloud projects add-iam-policy-binding <projeto> --member=serviceAccount:orq-exportacoes@<projeto>.iam.gserviceaccount.com --role=<papel>`,
      um comando por papel). Se o projeto já tem uma conta de serviço fazendo
      esse papel, use a que existe. Grave o e-mail dela em
      `conta_servico_exportacoes` do `ambiente.json`.
   d. **Search Console:** a conta de exportação do Google precisa de dois
      papéis no projeto:
      `gcloud projects add-iam-policy-binding <projeto> --member=serviceAccount:search-console-data-export@system.gserviceaccount.com --role=roles/bigquery.jobUser`
      e o mesmo com `--role=roles/bigquery.dataEditor`.
2. **Por pessoa nova.**
   a. Criar a conta de serviço dela:
      `gcloud iam service-accounts create orq-<nome> --project=<projeto> --display-name="Orquestrador <Nome>"`.
   b. Papéis da conta de serviço no projeto: `roles/bigquery.dataViewer` e
      `roles/bigquery.jobUser`, com
      `--member=serviceAccount:orq-<nome>@<projeto>.iam.gserviceaccount.com`.
   c. Papéis da pessoa: `roles/bigquery.user` e `roles/bigquery.dataViewer`
      no projeto, com `--member=user:<email>`, e o direito de criar a chave só
      da conta dela:
      `gcloud iam service-accounts add-iam-policy-binding orq-<nome>@<projeto>.iam.gserviceaccount.com --member=user:<email> --role=roles/iam.serviceAccountKeyAdmin --project=<projeto>`.
   d. Mandar à pessoa o ID do projeto. Ela segue a trilha A.
3. **Por coordenador**, quem cria as transferências no cadastro: além do item
   2, `roles/bigquery.admin` no projeto e o direito de usar a conta das
   exportações:
   `gcloud iam service-accounts add-iam-policy-binding <conta das exportações> --member=user:<email> --role=roles/iam.serviceAccountUser --project=<projeto>`.
   **Ligar o GA4 ao BigQuery exige ser proprietário do projeto** (regra do
   Google, além de Editor no GA4). O dono liga, ou dá o papel `roles/owner` a
   quem confiar.
4. **Quando alguém sai do time:** apagar a conta de serviço da pessoa
   (`gcloud iam service-accounts delete orq-<nome>@<projeto>.iam.gserviceaccount.com --project=<projeto>`),
   o que inutiliza a chave que ficou no computador dela, e tirar os papéis do
   e-mail dela (`gcloud projects remove-iam-policy-binding`, um por papel). Os
   dados e as transferências continuam, porque são da conta das exportações.
5. **Teste:** `bq ls --project_id=<projeto>` com o login da pessoa nova.
6. Grave o projeto em `projeto_bigquery` do `ambiente.json`.

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
   Python do ambiente, caminho da chave, e-mail da conta de serviço da pessoa
   (nunca a chave), `projeto_bigquery`, `conta_servico_exportacoes` (o
   coordenador informa; é o e-mail que entra no Google Ads e no Merchant de
   cada cliente) e o estado de cada item (`ok`, `falta`,
   `opcional`, `erro: <msg>`). É por esse arquivo que o orquestrador sabe que o
   computador está pronto e pula a instalação nas próximas conversas.
   Computador que já funciona sem ele (preparado à mão, antes deste roteiro):
   rode só a etapa 1, grave o arquivo com o que achou e siga para o cadastro,
   sem reinstalar nada.
3. Grave `Convertr/relatorio-instalacao.md` com o que foi feito, o que travou
   (mensagem exata e o que resolveu) e o tempo de cada trilha, e peça para a
   pessoa mandar esse arquivo ao Luis. Ele usa esses relatórios para melhorar
   este roteiro.
4. Próximo passo: "ativar o orquestrador da <cliente>", que abre o cadastro.
