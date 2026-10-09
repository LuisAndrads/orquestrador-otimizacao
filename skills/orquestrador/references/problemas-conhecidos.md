# Problemas conhecidos na instalação

Cada linha veio de uma instalação real. Quando aparecer um problema novo,
o relatório da instalação (`relatorio-instalacao.md`) vai para o Luis, e a
solução entra aqui.

| Sintoma | Causa | Solução | Visto em |
|---|---|---|---|
| "Página não existe" ou "repositório privado" ao abrir o link | o repositório era privado | público desde 05/10/2026; não precisa de conta no GitHub | 05/10/2026 |
| `/plugin` dá erro de login ou "só funciona em uma linha" | os dois comandos colados juntos | colar um comando por vez, cada um numa linha | 05/10/2026 |
| A pessoa usa o Claude no chat, e não no Code | o plugin só roda no Claude Code | aba **Code** do app, com a pasta `Convertr` aberta | 05/10/2026 |
| Pasta errada (a pasta geral do computador) | Code aberto sem selecionar pasta | abrir a pasta `Convertr` antes de colar o link | 05/10/2026 |
| E-mail do Google Workspace bloqueado por fatura vencida | conta da empresa | usar outro e-mail (Gmail pessoal) para o Google Cloud | 05/10/2026 |
| E-mail do Claude diferente do e-mail convidado | contas diferentes em cada serviço | usar o mesmo e-mail em tudo; com repositório público, deixou de importar | 05/10/2026 |
| Google Cloud: "erro na configuração de faturamento" mesmo depois do cartão | o teste gratuito pede pré-pagamento no Brasil | o plugin não precisa de faturamento (planilhas e GA4); se exigir, confirmar o pré-pagamento, que vira crédito | 05/10/2026 |
| Chave JSON salva em pasta do OneDrive | Downloads sincronizado | guardar em `~/.orquestrador-otimizacao/chave-google.json` | 05/10/2026 |
| A pessoa não sabe onde fica o conector do Meta | — | app do Claude → seu nome → Configurações → Conectores → Meta | 05/10/2026 |
| Metas da PDA zeradas durante a instalação | outra pessoa atualizou a planilha (não foi o plugin, que só lê) | conferir o histórico de versões da planilha | 05/10/2026 |
| "Python não instalado" | Mac sem ferramentas de linha de comando | `xcode-select --install` e clicar em Instalar | 05/10/2026 |
